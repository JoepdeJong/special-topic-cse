#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 23:46:01 2022

@author: ksyunetz
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

def import_draw_stonytxt(draw=False):

	os.chdir(os.pardir)
	os.chdir('datasets')
	
	fileName = 'Stonytxt.dat'
	
	a = np.loadtxt(fileName)
	a = a.astype(np.int32) #a is now an array with each row a link between two nodes in the network

	os.chdir(os.pardir)			
	os.chdir('read_datasets')

	### add 70 nodes to a directed graph
	G = nx.DiGraph()
	G.add_nodes_from(np.arange(1,115))


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