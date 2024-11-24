Names: Jeelin Liu, Bon Nguyen
NetID: jliu189, anguy49

EXACT INFERENCE:
python3 mybninferencer.py [xmlFileBayesianNetwork] [queryVariable] [evidenceVariable] [evidenceVariableValue]

APPROXIMATE INFERENCE (using Likelihood weighting):
python3 mybninferencer.py [samplingSize] [xmlFileBayesianNetwork] [queryVariable] [evidenceVariable] [evidenceVariableValue]

To parse the XML to return the necessary data needed for the Bayesian Network, we relied on the functions provided in the read.py file. For both Exact Inference and Approximate Inference, we followed the pseudocode in the textbook and converted into Python for our implementation. We created a Bayesian object to contain all necessary information related to the baysian network parsed from the XML and formatted it in an easier to read way. Each node created from the Bayesian Network has a domain, their parent(s), and the CPT based on their parents. We used this to implement both our algorithms.
