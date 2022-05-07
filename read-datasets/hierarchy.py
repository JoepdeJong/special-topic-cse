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

def hierarchy(G):

	all_paths_length = dict(nx.all_pairs_shortest_path_length(G))

	leaders = leader_nodes(G)

	non_leaders = set(G.nodes()).difference(set(leaders))

	hierarchy = {}

	for node in non_leaders:
		connected_leaders = {key:value for key,value in all_paths_length[node].items() if key in leaders}
		min_dist = min(connected_leaders.values())
		dic[node] = {key:value for key,value in connected_leaders.items() if value == min_dist}

	return hierarchy



