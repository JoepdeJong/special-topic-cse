# -*- coding: utf-8 -*-
"""
Created on Fri May 20 16:12:36 2022

@author: Anne-Fleur
"""

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import sys
sys.path.append('../read-datasets')
from import_literature1976 import *


def reversible(G):
	A = nx.adjacency_matrix(G)
	A = A.todense()
	n = len(A)
	for i in range(n): #for every node, check if all other nodes are reachable through the directed graph
		A_it = A
		A_it[[0, i]] = A_it [[i, 0]] #change i'th row and first row of adjacency matrix
		dist_matrix = dijkstra(csgraph=A, directed=True, indices=0)
		if np.where(dist_matrix == np.inf)[0].size > 0:
			return False
	return True

if __name__ == '__main__':
	G = import_draw_literature(draw=False)
	print("Is G reversible? " + str(reversible(G)))