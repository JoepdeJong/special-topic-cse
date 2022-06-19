from multiprocessing import Pool
import multiprocessing
import time
from joblib import Parallel, delayed
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from mutators import *
from read_datasets.entropy import *
from read_datasets.hierarchy import *

np.random.seed(1313)
filename = 'dataset/prices_model_seed1313_m3_k01_initial_nodes1.csv'

data = pd.read_csv(filename)
number_of_mutations = 20

n_nodes = data['n'].unique()
n_iterations = data['iteration'].max()
reciprocal_threshold = data['reciprocal_threshold'].unique()

mutators = [node_removal, edge_removal, edge_reversal, edge_addition]
mutation_steps = [1, 5, 10]

# Assume m, k0 and initial_nodes are the same for all n
k0 = 1
m = 3
initial_nodes = 1

n_fields = len(['df', 'entropy', 'normalized_entropy', 'spectral_scaling', 'spectral_gap', 'root_is_leader'])

num_cores = multiprocessing.cpu_count()

def perturb(mutator, graph):
    k = 0
    output = []
    for s in range(len(mutation_steps)):
        step = mutation_steps[s]
        mutator(graph, step - k)
        k = step

        A = nx.adjacency_matrix(graph).todense()

        # Calculate the measures
        df = Henrici(A)
        h = entropy2(A).real
        h_norm = h/entropy2((A+A.T)/2).real
        spectral_scaling, spectral_gap = spectralScalingMeasure(A)

        # The only leader node in the prices model can be the root node
        root_is_leader = is_leader_node(graph, 0)

        # Save the measures=
        output.append([step, df, h, h_norm, spectral_scaling, spectral_gap, root_is_leader])

    return output

for n in n_nodes:
    output = pd.DataFrame(columns=['n', 'iteration', 'reciprocal_threshold', 'mutation', 'mutation_number', 'step', 'df', 'entropy', 'normalized_entropy', 'spectral_scaling', 'spectral_gap', 'root_is_leader'])
    for r in reciprocal_threshold:
        start_time = time.time()
        data_n_p = data[(data['n'] == n) & (data['reciprocal_threshold'] == r)]

        for index, row in data_n_p.iterrows():
            k = row['iteration']

            # Import graph from file
            graph = nx.read_edgelist('dataset/'+row['filename']+'.txt', data=False, create_using=nx.DiGraph())

            # Perturb graph
            for mutator in mutators:
                results = Parallel(n_jobs=num_cores)(delayed(perturb)(mutator, graph) for i in range(number_of_mutations))
                for i in range(number_of_mutations):
                    result = results[i]
                    for s in range(len(mutation_steps)):
                        output.loc[len(output)] = [n, k, r, mutator.__name__, i] + result[s]

        duration = time.time() - start_time
        print('Finished n =', n, 'reciprocal_threshold =', r, 'in', duration, 'seconds')
    output.to_csv('output/mutations_m' + str(m) + '_k0' + str(k0) + '_initial_nodes' + str(initial_nodes)+'_n'+str(n)+'.csv', index=False)
