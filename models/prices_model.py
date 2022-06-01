from matplotlib import pyplot as plt
from networkx import nx
import numpy as np
import random

def prices_model(n, m, k0 = 1, n0 = 1, reciprocal_threshold = 1):
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

            # Reciprocals
            if reciprocal_threshold < 1:
                if out_degrees[i] > 0:
                    p = 1/(out_degrees[i])
                else:
                    p = 1

                if p >= reciprocal_threshold:
                    G.add_edge(i, n_nodes)
                    in_degrees[n_nodes] += 1
                    out_degrees[i] += 1

            # Break when n_nodes is less than m.
            if len(joined) == n_nodes:
                break

        n_nodes += 1
    return G

if __name__ == '__main__':
    prices_graph = prices_model(50, 3, 1, 1, 0.3)
    nx.draw(prices_graph, with_labels=True)
    plt.show()