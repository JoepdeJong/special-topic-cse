import numpy as np
import networkx as nx

from read_datasets.entropy import *
from read_datasets.hierarchy import *

import matplotlib.pyplot as plt


from models.prices_model import prices_model

n = 20 # Number of nodes
n_iterations = 5 # Number of iterations
m = 3 # Number of edges
k0 = 1 # Initial factor
initial_nodes = 1
reciprocal_threshold = np.linspace(0, 1, 100)

# Make a logaritmic scale of probabilities closer to 0
# reciprocal_threshold = np.logspace(-2, 0, num=100)

tol = 1e-10 # Entropy tolerance

# Set random seed
# np.random.seed(0)


data = np.zeros((len(reciprocal_threshold), 5))


for i in range(len(reciprocal_threshold)):    
    p = reciprocal_threshold[i]
    avg_df = 0
    avg_h1 = 0
    avg_h2 = 0
    avg_h3 = 0
    for k in range(n_iterations):
        graph = prices_model(n, m, k0, initial_nodes, p)

        A = nx.adjacency_matrix(graph)
        A = A.todense()
        # df = Henrici(A)
        # h1 = entropy(tol, A)
        h2 = entropy2(A).real

        h3 = h2/entropy2((A+A.T)/2).real

        spectral_scaling, spectral_gap = spectralScalingMeasure(A)
        print(spectral_scaling, spectral_gap)

        # avg_df += df
        # avg_h1 += h1
        avg_h2 += h2
        avg_h3 += h3

        # Distance number to leader node
    avg_df /= n_iterations
    # avg_h1 /= n_iterations
    avg_h2 /= n_iterations

    avg_h3 /= n_iterations
    
    # print(p, avg_h2)
    data[i,:] = [p, avg_df, avg_h1, avg_h2, avg_h3]

# Plot the Henrici against the reciprocal probability

print(data[:, 4])

plt.figure()
x = data[:,0]
y = data[:,1]
plt.plot(x, y, 'o')
plt.xlabel('Reciprocal probability')
plt.ylabel('Henrici')

plt.figure()
# Plot the entropy against the reciprocal probability
x = data[:,0]
y = data[:,3]
plt.plot(x, y, 'o')
plt.xlabel('Reciprocal probability')
plt.ylabel('Entropy')


plt.figure()
# Plot the entropy against the reciprocal probability
x = data[:,0]
y = data[:,3]
plt.plot(x, y, 'o')
# Plot the y-axis on a log scale
plt.xscale('log')
plt.xlabel('Reciprocal probability')
plt.ylabel('Entropy')


plt.figure()
# Plot the entropy against the reciprocal probability
x = data[:,0]
y = data[:,4]
plt.plot(x, y, 'o')
# Plot the y-axis on a log scale
plt.xscale('log')
plt.xlabel('Reciprocal probability')
plt.ylabel('Entropy')


plt.show()


# TODO: make henrici thing