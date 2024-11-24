import read
import xml.dom.minidom
import sys
import os
from itertools import product
import pprint

class Bayesian:
    def __init__(self, xmlFile):
        self.nodes = {}
        self.var_list = []

        doc = xml.dom.minidom.parse(xmlFile)
        (vars,domains) = read.vars_and_domains(doc)
        (tables,parents) = read.tables_and_parents(doc)

        # print('VARS: ', vars)
        # print('DOMAINS: ', domains)
        # print("TABLES:", tables)
        # print("PARENTS:", parents)

        self.var_list = vars

        for var in self.var_list:
            p = parents[var] # parents of variable
            d = domains[var] # domain of variable
            cpt = {}

            if not parents[var]:
                for i, value in enumerate(d):
                    cpt[value] = tables[var][i]
            else:
                parent_combos = self.parent_combinations(p, domains)
                for i, combo in enumerate(parent_combos):
                    cpt[combo] = {}
                    index =  len(d) * i 
                    for j, value in enumerate(d):
                        cpt[combo][value] = tables[var][index + j]

            self.add_node(var, d, p, cpt)

    def parent_combinations(self, parents, domains):
        parent_domains = [domains[parent] for parent in parents]
        return list(product(*parent_domains))
    
    def add_node(self, name, domain, parents, cpt):
        self.nodes[name] = {
            "domain": domain,
            "parents": parents,
            "cpt" : cpt
        }

    def print_nodes(self):
        pp = pprint.PrettyPrinter(indent=4)
        for node, data in self.nodes.items():
            print(f"Node: {node}")
            print(f"  Domain: {data['domain']}")
            print(f"  Parents: {data['parents']}")
            print(f"  CPT: ")
            pp.pprint(data['cpt'])  # Use pprint to display the CPT
            print()

    def get_probability(self, var, value, evidence):
        node = self.nodes[var]
        parents = node['parents']
        cpt = node['cpt']

        if not parents:
            return cpt[value]
        
        parent_vals = tuple(evidence[parent] for parent in parents)
        return cpt[parent_vals][value]

# query : query variable
# evidence : evidence map
# bn : bayesian net
def exactInference(query, evidence: dict, bn: Bayesian):
    print("Exact Inference")

    vars = bn.var_list
    query_dist = {}
    for value in bn.nodes[query]['domain']:
        extended_evidence = evidence.copy()
        extended_evidence[query] = value
        query_dist[value] = enumerate_all(vars, extended_evidence, bn)

    total = sum(query_dist.values())
    for value in query_dist:
        query_dist[value] /= total

    print(query_dist)

def enumerate_all(vars: list, evidence: dict, bn: Bayesian):
    if not vars:
        return 1.0
    
    var = vars[0]
    rest = vars[1:]

    if var in evidence:
        prob = bn.get_probability(var, evidence[var], evidence)
        return prob * enumerate_all(rest, evidence, bn)
    else:
        total = 0
        for value in bn.nodes[var]['domain']:
            extended_evidence = evidence.copy()
            extended_evidence[var] = value
            prob = bn.get_probability(var, value, extended_evidence)
            total += prob * enumerate_all(rest, extended_evidence, bn)
        return total


def approximateInference(queryVariable, evidence, bn: Bayesian, samples: int):
    print('Approximate Inference')
    print('NUM SAMPLES:', samples)
    pass

def main():
    try:
        firstArg = sys.argv[1]
        remainingArgs = sys.argv[2:]
        try:
            #Get number of samples. If not a number, try Exact Inference. If sample is less than 0, print error message.
            samples = int(firstArg)
            if samples < 0:
                print("The number of samples must be greater than 0.")
                return
            
            #Get XML file. If not XML file, print error message.
            xmlFile = remainingArgs[0]
            if not os.path.isfile(xmlFile) or not xmlFile.endswith('.xml'):
                print("The file must be an XML file.")
                return   
            
            queryVariable = remainingArgs[1]
            evidenceVariablesMap = {}

            #Mapping evidence variables to their values. If out of index, print error message.
            for i in range(2, len(remainingArgs), 2):
                evidenceVariablesMap[remainingArgs[i]] = remainingArgs[i+1]

            #Parse XML File and get variables/domains and tables/parents
            bn = Bayesian(xmlFile)
            #Handle Approximate Inference
            print('Approximate Inference')
            print('NUM SAMPLES:', samples)



        except ValueError:
            #Get XML file. If not XML file, print error message.
            xmlFile = firstArg
            if not os.path.isfile(xmlFile) or not xmlFile.endswith('.xml'):
                print("The file must be an XML file.")
                return
            
            queryVariable = remainingArgs[0]
            evidenceVariablesMap = {}

            #Mapping evidence variables to their values. If out of index, print error message.
            for i in range(1, len(remainingArgs), 2):
                evidenceVariablesMap[remainingArgs[i]] = remainingArgs[i+1]

            #Parse XML File and get variables/domains and tables/parents
            # doc = xml.dom.minidom.parse(xmlFile)
            # (vars,domains) = read.vars_and_domains(doc)
            # (tables,parents) = read.tables_and_parents(doc)
            bn = Bayesian(xmlFile)
            bn.print_nodes()

            #Handle Exact Inference
            exactInference(queryVariable, evidenceVariablesMap, bn)

    except IndexError:
        print("Invalid number of arguments. Make sure you have a value assigned for each evidence variable.") 
        return

if __name__ == "__main__":
    main()