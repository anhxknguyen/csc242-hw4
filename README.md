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

To parse the XML to return the necessary data needed for the Bayesian Network, we relied on the functions provided in the read.py file.
We created a Bayesian object to contain all necessary information related to the baysian network parsed from the XML and formatted it in an easier to read way.
Each node created from the Bayesian Network has a domain, their parent(s), and the CPT based on their parents. We used this to implement both our algorithms.

### Inference by Enumeration

For our Inference by Enumeration algorithm, we traverse a topologically sorted list of all the nodes (nodes with no parents first).
After taking the first node in the list, we first check if it exists in the evidence, if so, we return the probability of that nodes value given its CPT, multiplied by the value returned by our enumeration algorithm for the rest of the list.
If it doesn't exist in the evidence, then we calculate the total probability as a SUM of all the possible enumerated values in the variable's domain, which then recurses through the rest of the list.
Basically, we followed the pseudocode in the textbook but implemented a topological sort to avoid issues where the parents of variables aren't instantiated when going through the CPT.

### Likelihood Weighted Sampling

For our Inference by Approximation algorithm, we used the Likelihood Weighting sampling method to generate samples for our data.
We generate cases from the top down, and when presented with a node already determined by the evidence, we take that node with the evidence value, and then multiply the weight by the chance of that value.

