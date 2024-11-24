import read
import xml.dom.minidom
import sys

def main():
    doc = xml.dom.minidom.parse(sys.argv[1])
    (vars,domains) = read.vars_and_domains(doc)
    (tables,parents) = read.tables_and_parents(doc)
    print('Variables are:', vars)
    print('Domains are:', domains)

if __name__ == "__main__":
    main()