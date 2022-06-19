import time
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from mutators import *
from read_datasets.entropy import *
from read_datasets.hierarchy import *

filename = 'dataset/prices_model_seed1313_m3_k01_initial_nodes1.csv'

data = pd.read_csv(filename)
number_of_mutations = 20

n_nodes = data['n'].unique()
n_nodes = [50]
n_iterations = data['iteration'].max()
reciprocal_threshold = data['reciprocal_threshold'].unique()

mutators = [node_removal, edge_removal, edge_reversal, edge_addition]
mutation_steps = [1, 5, 10]

# Assume m, k0 and initial_nodes are the same for all n
k0 = 1
m = 3
initial_nodes = 1


output = pd.DataFrame(columns=['n', 'iteration', 'mutation', 'mutation_number', 'step', 'reciprocal_threshold', 'df', 'entropy', 'normalized_entropy', 'spectral_scaling', 'spectral_gap', 'root_is_leader'])
n_fields = len(['df', 'entropy', 'normalized_entropy', 'spectral_scaling', 'spectral_gap', 'root_is_leader'])

for n in n_nodes:
    for r in reciprocal_threshold:
        start_time = time.time()
        data_n_p = data[(data['n'] == n) & (data['reciprocal_threshold'] == r)]

        for index, row in data_n_p.iterrows():
            k = row['iteration']

            # Import graph from file
            graph = nx.read_edgelist('dataset/'+row['filename']+'.txt', data=False, create_using=nx.DiGraph())

            # Perturb graph
            for mutator in mutators:
                for i in range(number_of_mutations):
                    # Copy the graph
                    graph_copy = graph.copy()

                    k = 0
                    for s in range(len(mutation_steps)):
                        step = mutation_steps[s]
                        graph_copy = mutator(graph_copy, step - k)
                        k += step

                        A = nx.adjacency_matrix(graph_copy).todense()

                        # Calculate the measures
                        df = Henrici(A)
                        h = entropy2(A).real
                        h_norm = h/entropy2((A+A.T)/2).real
                        spectral_scaling, spectral_gap = spectralScalingMeasure(A)

                        # The only leader node in the prices model can be the root node
                        root_is_leader = is_leader_node(graph_copy, 0)

                        # Save the measures
                        output.loc[len(output)] = [n, k, mutator.__name__, r, i, s, df, h, h_norm, spectral_scaling, spectral_gap, root_is_leader]
                    del graph_copy

        duration = time.time() - start_time
        print('Finished n =', n, 'reciprocal_threshold =', r, 'in', duration, 'seconds')

output.to_csv('mutations_m' + str(m) + '_k0' + str(k0) + '_initial_nodes' + str(initial_nodes)+'.csv', index=False)