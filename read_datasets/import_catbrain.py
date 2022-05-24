# -*- coding: utf-8 -*-
"""
Created on Mon May  9 17:43:26 2022

@author: Anne-Fleur
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

def import_draw_catbrain(draw=False):

	os.chdir(os.pardir)
	os.chdir('datasets')

	fileName = 'mixed.species_brain_1.graphml'

	### read graphml file
	G = nx.read_graphml(fileName)

	os.chdir(os.pardir)			
	os.chdir('read-datasets')

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