import networkx as nx

from read_datasets.entropy import *
# Make a Directed Acyclic Graph (DAG)

graphDag = nx.DiGraph()
n = 20

k = 0
while k < n:
    graphDag.add_node(k)
    if k > 0:
        graphDag.add_edge(k-1, k)
    k += 1
graphDag.add_edge(0, 3)
graphDag.add_edge(3, k-1)

# Make a fully connected graph
graphCon = nx.complete_graph(20)

graphCon2 = graphCon.copy()
# Remove half of the edges
for i in range(int(len(graphCon2.edges)/2)):
    to_remove = np.random.choice(len(graphCon2.edges))
    graphCon2.remove_edge(list(graphCon2.edges)[to_remove][0], list(graphCon2.edges)[to_remove][1])

# Print the spectral gap:
# print('DAG:', spectralScalingMeasure(nx.adjacency_matrix(graphDag).todense()))

spectral_scaling1, spectral_gap1 = spectralScalingMeasure(nx.adjacency_matrix(graphCon).todense())
spectral_scaling2, spectral_gap2 = spectralScalingMeasure(nx.adjacency_matrix(graphCon2).todense())
# print('CON:', spectralScalingMeasure(nx.adjacency_matrix(graphCon).todense()))
# print('CON2:', spectralScalingMeasure(nx.adjacency_matrix(graphCon2).todense()))

assert(spectral_scaling1 > spectral_scaling2)
assert(spectral_gap1 > spectral_gap2)