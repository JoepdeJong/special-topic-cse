# -*- coding: utf-8 -*-
"""
Created on Mon May 23 15:49:18 2022

@author: Anne-Fleur
"""

import numpy as np
from scipy.linalg import dft
import networkx as nx
import matplotlib.pyplot as plt
from reversibility import *
import sys
sys.path.append('../read_datasets')

def flatten(t):
    return [item for sublist in t for item in sublist]

def depth(t):
	if isinstance(t, list):
		return 1 + max(depth(i) for i in t)
	else:
		return 0

def permutations(G):
	### first add self loops to all vertices
	for i in range(len(G.nodes())):
		G.add_edge(i, i)
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

def quantum_walk_operator(G):
	P = permutations(G)
	n = len(G.nodes())
	d = len(P)
	C = dft(d)/np.sqrt(d)
	S = np.zeros((d*n, d*n))
	for i in range(d):
		Pi = np.zeros((n,n))
		for j in range(len(P[i])):
			for k in range(len(P[i][j])):
				Pi = Pi + np.eye(n)[[P[i][j][k]]].T @ np.eye(n)[[P[i][j][k-1]]]
		S += np.kron(np.eye(d)[[i]].T @ np.eye(d)[[i]], Pi)
	W = S @ np.kron(C, np.eye(n))
	return W

def quantum_walk(G, steps):
	W = quantum_walk_operator(G)
	n = len(G.nodes())
	d = int(len(W)/n)
	p0 = np.kron(np.ones(d)/np.sqrt(d), np.ones(n)/np.sqrt(n))
	p = p0
	for i in range(steps):
		p = W @ p
	return p

def quantum_walk_prob(p, n, plot = False):
	prob = np.zeros(n)
	for i in range(n):
		prob[i] = np.sum(np.square(np.abs(p[i::n])))
	if not plot:
		return prob

	### draw the graph with node labels
	plt.figure()
	plt.plot(np.arange(1,n+1,1), prob)
	plt.show()


def quantum_stationary_distr(G, tol, plot = False):
	n = len(G.nodes)
	W = quantum_walk_operator(G)
	d = int(len(W)/n)
	p0 = np.kron(np.eye(d)[0]/np.sqrt(d), np.ones(n)/np.sqrt(n))
	p_old = p0
	p_new = W @ p0
	prob_old = quantum_walk_prob(p_old, n, False)
	stat_distr = prob_old
	prob_new = quantum_walk_prob(p_new, n, False)
	steps = 1
	while np.sum(np.abs(prob_old-prob_new)) > n*tol:
		stat_distr = stat_distr + prob_new
		steps += 1
		p_old = p_new
		prob_old = prob_new
		p_new = W @ p_old
		prob_new = quantum_walk_prob(p_new, n, False)

	if not plot:
		return stat_distr/steps

	### draw the graph with node labels
	plt.figure()
	plt.plot(np.arange(1,n+1,1), stat_distr/steps)
	plt.show()

# if __name__ == '__main__':
# 	G = nx.DiGraph()
# 	G.add_nodes_from([0, 1, 2])
# 	G.add_edges_from([(0,1), (1,0), (0,2), (2,0), (2,1)])
# 	G = nx.DiGraph()
# 	f = 'prices_model_n20_m3_k01_initial_nodes1_p0.0_iteration1.txt'
# 	G.add_edges_from(np.loadtxt('../dataset/'+str(f)))
# 	P = permutations(G)
# 	W = quantum_walk_operator(G)
# 	### check unitarity
# 	U = W @ W.conj().T
# 	steps = 10
# 	distr = quantum_walk(G, steps)


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