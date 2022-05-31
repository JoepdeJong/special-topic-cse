# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:51:03 2022

@author: Anne-Fleur
"""


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

def import_draw_highschool(draw=False):

	os.chdir(os.pardir)
	os.chdir('datasets')
	
	fileName = 'net_moreno_highschool.dat'
	
	a = np.loadtxt(fileName)
	a = a.astype(np.int32) #a is now an array with each row a link between two nodes in the network

	os.chdir(os.pardir)			
	os.chdir('read-datasets')

	### add 70 nodes to a directed graph
	G = nx.DiGraph()
	G.add_nodes_from(np.arange(1,70))


	### add edges to the directed graph
	edges = tuple([tuple(e) for e in a]) #arcs as tuples

	G.add_edges_from(edges)

	### compute adjacency matrix of G
	A = nx.adjacency_matrix(G)
	A = A.todense()

	if not draw:
		return G

	### draw the graph with node labels
	plt.close('all')
	plt.figure()
	nx.draw(G, with_labels= True)
	plt.show()

	return G
