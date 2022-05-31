# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:49:18 2022

@author: Anne-Fleur
"""

import numpy as np
from scipy.linalg import dft
import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.path.append('../read-datasets')
from import_rhesusbrain import *

def flatten(t):
    return [item for sublist in t for item in sublist]

def permutations(G):
	### first add self loops to all vertices
# 	for i in range(len(G.nodes())):
# 		G.add_edge(i, i)
# 	### find all cycles
# 	cycles = nx.simple_cycles(G)
	
	### find permutations
	perms = []
	for i in nx.simple_cycles(G):
		perm = [i]
		for j in nx.simple_cycles(G):
			if len(list(set(j) & set(flatten(perm)))) == 0:
					perm = perm + [j]
		perms = perms + [perm]

	### some permutations are double so we remove these
	for i in range(len(perms)):
		perms[i].sort()
	
	final_perms = []
	[final_perms.append(x) for x in perms if x not in final_perms]
	return final_perms

def quantum_walk_perms(G, steps):
	pass

if __name__ == '__main__':
	G = import_draw_rhesusbrain(False)
# 	G = nx.DiGraph()
# 	G.add_nodes_from([0, 1, 2])
# 	G.add_edges_from([(0,1), (1,0), (0,2), (2,0), (2,1)])
	P = permutations(G)

### find permutations = disjoint cycles and added with self loops	

### Wrong! Needs a graph coloring
# def quantum_walk_dreg(G):
# 	n = len(G.nodes())
# 	d = max([G.out_degree(i) for i in G.nodes()])
# 	A = nx.adjacency_matrix(G)
# 	A = A.todense()
# 	C = dft(d)			#NOG EVEN GOED KIJKEN OF DIT DE JUISTE COIN IS
# 	S = np.zeros((d*n, d*n))
# 	i = 0
# 	for k in G.nodes():
# 		j = 0
# 		neighbor = 0
# 		for l in G.nodes():
# 			if A[i,j] == 1: ### check that ordering of the nodes is the same as in the adjacency matrix
# 				S[j+(n*neighbor), i+(n*neighbor)] = 1
# 				neighbor += 1
# 			j += 1
# 		n_selfloops = d-neighbor
# 		for l in range(n_selfloops):
# 			S[(neighbor + l) * n + i, (neighbor + l) * n + i] = 1
# 		i += 1
# 	
# 	U = S @ np.kron(C, np.eye(n))