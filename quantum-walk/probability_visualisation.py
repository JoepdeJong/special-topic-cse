# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 12:56:03 2022

@author: Anne-Fleur
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from quantum_analyse_prices2 import *
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

	plt.figure(figsize = (18,9))
	pos = nx.spring_layout(G, seed = 2)
	nodes = nx.draw_networkx_nodes(G, pos, node_color = stat, cmap = plt.cm.autumn_r, vmin = 0, vmax = max(abs(stat)))
	nx.draw_networkx_edges(G, pos)
	nx.draw_networkx_labels(G, pos)
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

# 	fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (18,9))
# 	plt.sca(ax1)
# 	pos = nx.spring_layout(G, seed = 2)
# 	nodes = nx.draw_networkx_nodes(G, pos, node_color = classic, cmap = plt.cm.autumn_r, vmin = 0, vmax = vmax)
# 	nx.draw_networkx_edges(G, pos)
# 	nx.draw_networkx_labels(G, pos)
# 	plt.colorbar(nodes)
# 	plt.axis('off')

# 	plt.sca(ax2)
# 	pos = nx.spring_layout(G, seed = 2)
# 	nodes = nx.draw_networkx_nodes(G, pos, node_color = quantum, cmap = plt.cm.autumn_r, vmin = 0, vmax = vmax)
# 	nx.draw_networkx_edges(G, pos)
# 	nx.draw_networkx_labels(G,pos)
# 	plt.colorbar(nodes)
# 	plt.axis('off')

 	# plt.savefig("probability_results/"+str(s)+".svg", format = 'svg', dpi=300)
# 	plt.show()

	return classic



if __name__ == '__main__':
	a = np.loadtxt('../dataset/prices_model_seed1313_m3_k01_initial_nodes1.csv', delimiter = ',', skiprows = 1, usecols = (4,5))
	a = np.round(a[0::10,1], 2)

	i = 0
	for f in graph_data_list(1):
		### build graph
		G = nx.DiGraph()
		G.add_edges_from(np.loadtxt('../dataset/'+str(f)))
		G = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)

		f2 = str(f[:-3] + 'npy')

		### code that creates probability difference in graphs
		p = np.load('new_results_650_steps_it1/'+f2)
		c = draw_classic_quantum_probs(G, p, f[:-4])

		draw_quantum_prob(G, np.abs(p.flatten()-c))
		plt.savefig("probability_results_graphs/"+str(f[:-4])+".png", format = 'png', dpi=300)
		plt.close()


		### code that creates probability plots

		p = np.load('new_results_650_steps_it1/'+f2)
		print(p[:3])
		c = draw_classic_quantum_probs(G, p, f[:-4])
		plt.figure()
		plt.plot(np.arange(len(G.nodes())), p, label = 'quantum')
		plt.plot(np.arange(len(G.nodes())), c, label = 'classic')
# 		plt.title('p = '+str(a[i]))
		plt.legend()
		plt.savefig("probability_results_plots/"+str(f[:-4])+".png", format = 'png', dpi=300)
		plt.close()

		i += 1


