# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:56:03 2022

@author: Anne-Fleur
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from quantum_analyse_prices import *
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

def draw_quantum_prob(G, p):
	stat = p

	plt.figure()
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = stat, cmap = plt.cm.autumn_r, vmin = 0, vmax = 1)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G,pos)
	plt.colorbar(nodes)
	plt.axis('off')
	plt.show()

def draw_classic_quantum_probs(G, p, s):
	A = nx.adjacency_matrix(G)
	A = A.todense()
	T = transmatrix(A)
	classic = weightedev(T) ###stationary distribution of classical random walk using eigenvalues of markov chain
	quantum = p
	vmax = max(max(np.abs(classic)), max(quantum))

	fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (18,9))
	plt.sca(ax1)
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = classic, cmap = plt.cm.autumn_r, vmin = 0, vmax = vmax)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G, pos)
	plt.colorbar(nodes)
	plt.axis('off')

	plt.sca(ax2)
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = quantum, cmap = plt.cm.autumn_r, vmin = 0, vmax = vmax)
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G,pos)
	plt.colorbar(nodes)
	plt.axis('off')

# 	plt.savefig("probability_results/"+str(s)+".svg", format = 'svg', dpi=300)
	plt.show()



if __name__ == '__main__':
	plt.figure()
	i = 0
	for f in graph_data_list(0)[:25]:
		i += 1
		### build graph
		G = nx.DiGraph()
		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))

		f2 = str(f[:-3] + 'npy')
		p = np.load('results_650_steps_it0/'+f2)
# 		draw_classic_quantum_probs(G, p, f[:-4])
		plt.plot(np.arange(len(G.nodes())), p, label = str(i))
		plt.legend()
		plt.show()

