from matplotlib import pyplot as plt
from networkx import nx
import numpy as np
import random

def prices_model(n, m, k0 = 1):
    """
    Prices model. Implementation according to wikipedia, but it doesn't work. xd
    """
    in_degrees = np.zeros(n, dtype=int)
    # in_degrees = np.zeros(n, dtype=int)
    # out_degrees = np.zeros(n, dtype=int)
    
    # Initialize graph with 1 node
    G = nx.DiGraph()
    G.add_node(1)

    n_nodes = 1

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
            p = (degrees + k0s)/(sum(degrees) + 1)


            # Find node i by looping over the probabilities.
            randp = random.random()
            tot = 0
            i = -1
            while tot < randp:
                i += 1
                tot += p[i]

            # Create directed edges (citation)
            G.add_edge(n_nodes, i)
            in_degrees[i] += 1
            joined += [i]

            print('Add edge', k+1, 'of', m, 'to node', i+1)

            # Break when n_nodes is less than m.
            if len(joined) == n_nodes:
                break

        n_nodes += 1

    return G

if __name__ == '__main__':
    prices_graph = prices_model2(20, 1, 1)
    nx.draw(prices_graph, with_labels=True)
    plt.show()
