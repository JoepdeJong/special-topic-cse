import networkx as nx

def leader_nodes(G):
	'''
	Calculates the leader nodes of a directed graph
	Arg: 
	A directed graph G
	Return: 
	a list with the leader nodes
	'''
	SCC = nx.strongly_connected_components(G) # generator of set of nodes within the same SCC

	leaders = []
	for component in SCC:
	    if len(component)==1 and G.out_degree()[list(component)[0]]==0:
	        leaders.append(list(component)[0])

	return leaders


