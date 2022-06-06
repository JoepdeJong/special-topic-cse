import numpy as np
import networkx as nx
import pandas as pd

from read_datasets.entropy import *
from read_datasets.hierarchy import *

import matplotlib.pyplot as plt


from models.prices_model import prices_model

folder = './dataset/'
seed = 1313
n_nodes = [20, 50, 100] # Number of nodes
n_iterations = 10 # Number of iterations (samples per configuration)
m = 3 # Number of edges
k0 = 1 # Initial factor
initial_nodes = 1
reciprocal_threshold = np.linspace(0, 1, 25) # 1 => DAG, 0 => Symmetric

# Set random seed
if seed is not None:
    np.random.seed(seed)

# Make new pandas dataframe
data = pd.DataFrame(columns=['n', 'm', 'k0', 'initial_nodes', 'iteration', 'reciprocal_threshold', 'df', 'entropy', 'normalized_entropy', 'root_is_leader', 'filename'])

for n in n_nodes:
    for i in range(len(reciprocal_threshold)):    
        p = reciprocal_threshold[i]
        for k in range(n_iterations):
            graph = prices_model(n, m, k0, initial_nodes, p)

            A = nx.adjacency_matrix(graph)
            A = A.todense()
            df = Henrici(A)

            h = entropy2(A).real
            h_norm = h/entropy2((A+A.T)/2).real

            # The only leader node in the prices model can be the root node
            root_is_leader = is_leader_node(graph, 0)

            filename = 'prices_model_n' + str(n) + '_m' + str(m) + '_k0' + str(k0) + '_initial_nodes' + str(initial_nodes) + '_p' + str(round(p, 2)) + '_iteration' + str(k)
            new_row = [n, m, k0, initial_nodes, k, p, df, h, h_norm, root_is_leader, filename]
            data.loc[len(data)] = new_row

            # Store graph into file
            nx.write_edgelist(graph, folder + filename + '.txt', data=False)

            # Save an image of the graph
            # nx.draw(graph, with_labels=True)
            # plt.savefig(folder + filename + '.png')

        # Distance number to leader node

# Write the dataset into a csv file
seed_string = ''
if seed is not None:
    seed_string = '_seed' + str(seed)
data.to_csv(folder + 'prices_model'+seed_string+'_m' + str(m) + '_k0' + str(k0) + '_initial_nodes' + str(initial_nodes)+'.csv', index=False)