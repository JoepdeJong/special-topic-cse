# -*- coding: utf-8 -*-
"""
Created on Mon May  2 18:33:06 2022

@author: Anne-Fleur
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

plt.close('all')

fileName = 'literature_1976.txt'

a = np.loadtxt(fileName, skiprows = 37)
a = a[:, :2].astype(np.int32) #a is now an array with each row a link between two nodes in the network


### add 24 nodes to a directed graph
G = nx.DiGraph()
G.add_nodes_from(np.arange(1,35))


### add edges to the directed graph
edges = tuple([tuple(e) for e in a]) #arcs as tuples

G.add_edges_from(edges)

### compute adjacency matrix of G
A = nx.adjacency_matrix(G)
A = A.todense()

### draw the graph with node labels
plt.figure()
nx.draw(G, with_labels= True)
plt.show()