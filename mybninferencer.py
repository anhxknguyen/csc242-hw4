import read
import xml.dom.minidom
import sys
import os
from itertools import product
import pprint

class Bayesian:
    def __init__(self, xmlFile):
        self.nodes = {}

        doc = xml.dom.minidom.parse(xmlFile)
        (vars,domains) = read.vars_and_domains(doc)
        (tables,parents) = read.tables_and_parents(doc)

        print('VARS: ', vars)
        print('DOMAINS: ', domains)
        print("TABLES:", tables)
        print("PARENTS:", parents)

        for var in vars:
            my_parents = parents[var]
            my_cpt = {}

            if not my_parents:
                for i, value in enumerate(domains[var]):
                    my_cpt[value] = tables[var][i]
            else:
                parent_combos = self.parent_combinations(my_parents, domains)
                for i, combo in enumerate(parent_combos):
                    my_cpt[combo] = {}
                    index =  len(domains[var]) * i 
                    for j, value in enumerate(domains[var]):
                        my_cpt[combo][value] = tables[var][index + j]

            self.add_node(var, my_parents, my_cpt)

    def parent_combinations(self, parents, domains):
        parent_domains = [domains[parent] for parent in parents]
        return list(product(*parent_domains))
    
    def add_node(self, name, parents, cpt):
        self.nodes[name] = {
            "parents": parents,
            "cpt" : cpt
        }

    def print_nodes(self):
        pp = pprint.PrettyPrinter(indent=4)
        for node, data in self.nodes.items():
            print(f"Node: {node}")
            print(f"  Parents: {data['parents']}")
            print(f"  CPT: ")
            pp.pprint(data['cpt'])  # Use pprint to display the CPT
            print()

def exactInference(queryVariable, evidence, bn: Bayesian):
    print("Exact Inference")
    pass


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
            exactInference(queryVariable, evidenceVariablesMap, bn);

    except IndexError:
        print("Invalid number of arguments. Make sure you have a value assigned for each evidence variable.") 
        return

if __name__ == "__main__":
    main()