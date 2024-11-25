# CSC242 Assignment 04 - Bayesian Network Inferencer

Names: Jeelin Liu, Bon Nguyen
NetID: jliu189, anguy49

## How to run the script

On UNIX-like Systems (Linux/MacOS):
NOT NECESSARY ON WINDOWS
1. Make sure the script has executable permissions:
```
$ chmod +x sat
```
2. Run the script directly

Linux/MacOS:
```
$ ./mybninferencer filename {approx,exact,converge} query [-h] [-v] [-s SAMPLES] [-e [EVIDENCE ...]]
```
Windows:
```
> python3 mybninferencer filename {approx,exact,converge} query [-h] [-v] [-s SAMPLES] [-e [EVIDENCE ...]]
```

For more information on how to run the script, please execute the script with the -h flag

## Discussion 

To parse the XML to return the necessary data needed for the Bayesian Network, we relied on the functions provided in the read.py file. For both Exact Inference and Approximate Inference, we followed the pseudocode in the textbook and converted into Python for our implementation. We created a Bayesian object to contain all necessary information related to the baysian network parsed from the XML and formatted it in an easier to read way. Each node created from the Bayesian Network has a domain, their parent(s), and the CPT based on their parents. We used this to implement both our algorithms.
