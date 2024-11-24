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
            doc = xml.dom.minidom.parse(xmlFile)
            (vars,domains) = read.vars_and_domains(doc)
            (tables,parents) = read.tables_and_parents(doc)

            #Handle Approximate Inference
            print('Approximate Inference')        
            print('Query Variable is:', queryVariable)
            print('Evidence Variables are:', evidenceVariablesMap)
            print('Number of Samples:', samples)

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
            doc = xml.dom.minidom.parse(xmlFile)
            (vars,domains) = read.vars_and_domains(doc)
            (tables,parents) = read.tables_and_parents(doc)

            #Handle Exact Inference
            print("Exact Inference")
            print('Query Variable is:', queryVariable)
            print('Evidence Variables are:', evidenceVariablesMap)

    except IndexError:
        print("Invalid number of arguments. Make sure you have a value assigned for each evidence variable.") 
        return

if __name__ == "__main__":
    main()