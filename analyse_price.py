import numpy as np
import networkx as nx

from read_datasets.entropy import *
from read_datasets.hierarchy import *



from models.prices_model import prices_model

n = 20 # Number of nodes
m = range(1, 5) # Number of edges
k0 = [0.1, 0.5, 1, 5, 10] # Initial factor
initial_nodes = 1
reciprocal_prob = 0.5

tol = 1e-10 # Entropy tolerance

# Set random seed
np.random.seed(0)


data = np.zeros(20*5)

for i in m:
    for k in k0:
        graph = prices_model(n, i, k, initial_nodes, reciprocal_prob)

        A = nx.adjacency_matrix(graph)
        A = A.todense()
        df = Henrici(A)
        h1 = entropy(tol, A)
        h2 = entropy2(A)

        ln = leader_nodes(graph)

        print(n, i, k, df, h1, h2, ln)