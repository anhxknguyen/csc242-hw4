import read
import xml.dom.minidom
import sys
import os

def exact_inference():
    pass

def approximate_inference():
    pass

def main():
    try:
        firstArg = sys.argv[1]
        remainingArgs = sys.argv[2:]
        try:
            samples = int(firstArg)
            if samples < 0:
                print("The number of samples must be greater than 0.")
                return
            xmlFile = remainingArgs[0]
            if not os.path.isfile(xmlFile) or not xmlFile.endswith('.xml'):
                print("The file must be an XML file.")
                return
            queryVariable = remainingArgs[1]
            evidenceVariablesMap = {}
            for i in range(2, len(remainingArgs), 2):
                evidenceVariablesMap[remainingArgs[i]] = remainingArgs[i+1]
            doc = xml.dom.minidom.parse(xmlFile)
            (vars,domains) = read.vars_and_domains(doc)
            (tables,parents) = read.tables_and_parents(doc)
            #Handle Approximate Inference
            print('Approximate Inference')
            
            # print('Query Variable is:', queryVariable)
            # print('Evidence Variables are:', evidenceVariablesMap)
            # print('Variables are:', vars)
            # print('Domains are:', domains)
            # print('Parents are:', parents)
            # print('Tables are:', tables)
        except ValueError:
            xmlFile = firstArg
            if not os.path.isfile(xmlFile) or not xmlFile.endswith('.xml'):
                print("The file must be an XML file.")
                return
            queryVariable = remainingArgs[0]
            evidenceVariablesMap = {}
            for i in range(1, len(remainingArgs), 2):
                evidenceVariablesMap[remainingArgs[i]] = remainingArgs[i+1]
            doc = xml.dom.minidom.parse(xmlFile)
            (vars,domains) = read.vars_and_domains(doc)
            (tables,parents) = read.tables_and_parents(doc)
            #Handle Exact Inference
            print("Exact Inference")
            # print('Query Variable is:', queryVariable)
            # print('Evidence Variables are:', evidenceVariablesMap)
            # print('Variables are:', vars)
            # print('Domains are:', domains)
            # print('Parents are:', parents)
            # print('Tables are:', tables)
    except IndexError:
        print("Invalid number of arguments. Make sure you have a value assigned for each evidence variable.") 
        return

if __name__ == "__main__":
    main()