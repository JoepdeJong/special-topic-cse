import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os

def import_draw_roads(draw=False):

	#plt.close('all')

	os.chdir(os.pardir)
	os.chdir('datasets')

	fileName = 'SiouxFalls_net.csv'

	a = np.loadtxt(fileName, delimiter = ',', skiprows = 1)
	a = a[:, 1:3].astype(np.int32) #a is now an array with each row a link between two nodes in the network

	os.chdir(os.pardir)
	os.chdir('read-datasets')


	### add 24 nodes to a directed graph
	G = nx.DiGraph()
	G.add_nodes_from(np.arange(1,24))


	### add edges to the directed graph
	edges = tuple([tuple(e) for e in a]) #forward edges as tuples
	backedges = tuple([tuple(e) for e in np.flip(a, axis=1)]) #backward edges as tuples

	G.add_edges_from(edges)
	G.add_edges_from(backedges)

	if not draw:
		return G

	### draw the graph with node labels
	plt.figure()
	nx.draw(G, with_labels= True)
	plt.show()

	return G, A
