from matplotlib import pyplot as plt
from networkx import nx
import numpy as np
import random

def prices_model(n, m, k0 = 1, n0 = 1, reciprocal_prob = 1):
    """
    Extended version of Prices model: possibility to vary n0 (the number of initial nodes.)
    """
    in_degrees = np.zeros(n, dtype=int)
    out_degrees = np.zeros(n, dtype=int)
    
    # Initialize graph with n0 nodes
    G = nx.DiGraph()

    for i in range(n0):
        G.add_node(i)

    n_nodes = n0

    # At each time step
    while n_nodes < n:
        # A new node j
        G.add_node(n_nodes)

        joined = []
        degrees = in_degrees.copy()

        # Creates m directed edges to m (distinct) already present nodes.
        for k in range(m):

            # Divide the factor k0 over the nodes that are the current node has not joined.
            k0s = np.zeros(n)
            k0s[:n_nodes] = k0/(n_nodes - len(joined))
            k0s[joined] = 0
            degrees[joined] = 0
            
            # Choose a node i with probability proportional to its in-degree and the factor k0.
            p = (degrees + k0s)/(sum(degrees) + k0)

            i = np.random.choice(range(n), p=p)

            # Create directed edges (citation)
            G.add_edge(n_nodes, i)
            in_degrees[i] += 1
            out_degrees[n_nodes] += 1
            joined += [i]

            # print('Add edge', k+1, 'of', m, 'to node', i+1)

            # Break when n_nodes is less than m.
            if len(joined) == n_nodes:
                break

        n_nodes += 1

    # Reciprocals
    if reciprocal_prob < 1:
        # Generate a reciprocal edge i -> j with probability proportional to 1/out_degree(j)

        for i in range(n):
            if out_degrees[i] > 0:
                p = 1/out_degrees[i]
            else:
                p = 0
            # Get all incoming edges from node i
            incoming = G.in_edges(i)

            if p >= reciprocal_prob:
                # For each edge, generate a reciprocal edge with probability p
                for j in incoming:
                    G.add_edge(j[1], j[0])
    return G

if __name__ == '__main__':
    prices_graph = prices_model(10, 2, 1, 1, .5)
    nx.draw(prices_graph, with_labels=True)
    plt.show()
