# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:56:03 2022

@author: Anne-Fleur
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
sys.path.append('../read_datasets')
from entropy import *

def draw_classical_prob(G):
	A = nx.adjacency_matrix(G)
	A = A.todense()
	T = transmatrix(A)
	stat = weightedev(T) ###stationary distribution of classical random walk using eigenvalues of markov chain

	plt.figure()
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = stat, cmap = plt.cm.autumn_r, vmin = 0, vmax = 1)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G, pos)
	plt.colorbar(nodes)
	plt.axis('off')
	plt.show()

def draw_quantum_prob(G):
	stat = np.zeros(len(G.nodes()))

	plt.figure()
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = stat, cmap = plt.cm.coolwarm, vmin = 0, vmax = 1)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G,pos)
	plt.colorbar(nodes)
	plt.axis('off')
	plt.show()

# if __name__ == '__main__':
# 	draw_classical_prob(G)