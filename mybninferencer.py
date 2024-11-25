#!/usr/bin/env python3

import read
import xml.dom.minidom
import os
from itertools import product
import random
import pprint
import argparse

def main():
    parser = argparse.ArgumentParser(description='Bayesian Network Inferencer')
    parser.add_argument("filename", type=str, help="Input filename containing the model.")
    parser.add_argument(
        "inference_type", 
        type=str, 
        choices=["approx", "exact", "converge"], 
        help="Type of inference to perform (approx, exact, converge)."
    )
    parser.add_argument("query", type=str, help="Query Variable")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print Bayesian network")
    parser.add_argument("-s", "--samples", type=int, help="Number of samples (required if inference_type is 'approx')")
    parser.add_argument(
        "-e", 
        "--evidence",
        nargs="*",
        help="Evidence variables in the format of '[var] [value]', e.g. 'J true M true'"
    )

    args = parser.parse_args()

    if args.inference_type == "approx" and args.samples is None:
        parser.error("--samples is required when inference_type is 'approx'.")
    
    if not os.path.isfile(args.filename) or not args.filename.endswith('.xml'):
        print("The file must be an XML file.")
        return   
    
    if args.inference_type == "approx":
        print(f"Number of Samples: {args.samples}")
        if args.samples < 0:
            print("The number of samples must be greater than 0.")
            return
    
    evidence_dict = {}
    if args.evidence:
        evidence_dict = {k: v for k, v in zip(args.evidence[::2], args.evidence[1::2])}
    
    bn = Bayesian(args.filename)

    if args.verbose:
        print(f"Filename: {args.filename}")
        print(f"Inference Type: {args.inference_type}")
        if args.inference_type == "approx":
            print(f"Number of Samples: {args.samples}")
            
        print(f"Query Variable: {args.query}")
        print(f"Verbosity: {args.verbose}")
        if args.evidence:
            print(f"Evidence: {evidence_dict}")
        else:
            print("Evidence: None")
        bn.print_nodes()

    if args.inference_type == "approx":
        approximateInference(args.query, evidence_dict, bn, args.samples)

    if args.inference_type == "exact":
        exactInference(args.query, evidence_dict, bn)

    if args.inference_type == "converge":
        exact = exactInference(args.query, evidence_dict, bn)
        exactTrueProb = exact['true']
        exactFalseProb = exact['false']
        sample = 1
        while True:
            approx = approximateInference(args.query, evidence_dict, bn, sample)
            approxTrueProb = approx['true']
            approxFalseProb = approx['false']
            error = abs(approxTrueProb - exactTrueProb)
            if error < 0.01:
                break
            sample += 1
        print("Number of samples needed for approximate to reach 1% error: ", sample)
        print("Exact Probability of True: ", exactTrueProb)
        print("Exact Probability of False: ", exactFalseProb)
        print("Approximate Probability of True: ", approxTrueProb)
        print("Approximate Probability of True: ", approxFalseProb)

class Bayesian:
    def __init__(self, xmlFile):
        self.nodes = {}
        self.var_list = []

        doc = xml.dom.minidom.parse(xmlFile)
        (vars,domains) = read.vars_and_domains(doc)
        (tables,parents) = read.tables_and_parents(doc)

        # print(f"VARS: ", vars)
        # print(f"DOMAINS: ", domains)
        # print(f"RAW TABLES: ", tables)
        # print(f"RAW VARS: ", vars)

        self.var_list = vars

        for var in self.var_list:
            p = parents[var] if parents[var] else []
            # parents of variable, if none, empty tuple
            d = domains[var] 
            # domain of variable
            cpt = {}

            parent_domains = [domains[parent] for parent in p]
            parent_combos = list(product(*parent_domains))
            for i, combo in enumerate(parent_combos):
                cpt[combo] = {}
                index = len(d) * i 
                for j, value in enumerate(d):
                    cpt[combo][value] = tables[var][index + j]

            self.add_node(var, d, p, cpt)

        self.var_list = topological_sort(self.nodes)
        
        # print("Parsed Bayesian: ")
        # self.print_nodes()
    
    def add_node(self, name, domain, parents, cpt):
        self.nodes[name] = {
            "domain": domain,
            "parents": parents,
            "cpt" : cpt
        }

    def print_nodes(self):
        pp = pprint.PrettyPrinter(indent=8)
        for node, data in self.nodes.items():
            print(f"Node: {node}")
            print(f"\tDomain: {data['domain']}")
            print(f"\tParents: {data['parents']}")
            print(f"\tCPT: ")
            pp.pprint(data['cpt'])  # Use pprint to display the CPT
            print()

    # P (A | parents(A))
    def get_probability(self, var, value, evidence):
        node = self.nodes[var]
        parents = node['parents']
        cpt = node['cpt']
        
        # print(evidence)
        parent_vals = tuple(evidence[parent] for parent in parents)
        # print(parent_vals)
        return cpt[parent_vals][value]

# query : query variable
# evidence : evidence map
# bn : bayesian net
def exactInference(query: str, evidence: dict, bn: Bayesian):
    print("Exact Inference")

    vars = bn.var_list
    query_dist = {}

    for value in bn.nodes[query]['domain']:
        extended_evidence = evidence.copy()
        extended_evidence[query] = value
        query_dist[value] = enumerate_all(vars, extended_evidence, bn)

    return normalize(query, query_dist)

def enumerate_all(vars: list, evidence: dict, bn: Bayesian):
    if not vars:
        return 1.0
    
    var = vars[0]
    rest = vars[1:]

    # print(var)
    # print(evidence)
    if var in evidence:
        prob = bn.get_probability(var, evidence[var], evidence)
        return prob * enumerate_all(rest, evidence, bn)
    else:
        total = 0
        for value in bn.nodes[var]['domain']:
            extended_evidence = evidence.copy()
            extended_evidence[var] = value
            # print(f"extended evidence: {extended_evidence}");
            prob = bn.get_probability(var, value, extended_evidence)
            total += prob * enumerate_all(rest, extended_evidence, bn)
        return total

def approximateInference(query: str, evidence: dict, bn: Bayesian, num_samples: int):
    print('Approximate Inference')
    print('NUM SAMPLES:', num_samples)

    query_dist = {}
    for value in bn.nodes[query]['domain']:
        query_dist[value] = 0.0

    for _ in range(num_samples):
        sample, weight = likelihoodWeighting(evidence, bn)
        query_dist[sample[query]] += weight 
    
    return normalize(query, query_dist)

def likelihoodWeighting(evidence: dict, bn: Bayesian):
    sample = {}
    weight = 1.0

    for var in bn.var_list:
        # print(f"Variable: {var}");
        if var in evidence:
            sample[var] = evidence[var]
            prob = bn.get_probability(var, sample[var], sample)
            weight *= prob
        else:
            true_prob = bn.get_probability(var, 'true', sample)
            sample[var] = 'true' if (random.random() < true_prob) else 'false'

    return sample, weight

def normalize(query:str , query_dist: dict):
    print(f"Found probability of query variable: {query}")
    total = sum(query_dist.values())

    for value in query_dist:
        if total == 0:
            query_dist[value] = 0
        else:
            query_dist[value] /= total

    for key, value in query_dist.items():
        print(f"\t{key}: {value}")

    return query_dist

# chatgpt implementation
def topological_sort(nodes):
    # Step 1: Build a dependency graph and in-degree count
    in_degree = {node: 0 for node in nodes}
    adjacency_list = {node: [] for node in nodes}

    for node, details in nodes.items():
        for parent in details["parents"]:
            adjacency_list[parent].append(node)
            in_degree[node] += 1

    # Step 2: Perform topological sorting using Kahn's Algorithm
    queue = [node for node, degree in in_degree.items() if degree == 0]
    sorted_order = []

    while queue:
        current = queue.pop(0)
        sorted_order.append(current)

        for child in adjacency_list[current]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return sorted_order

if __name__ == "__main__":
    main()