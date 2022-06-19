from matplotlib import pyplot as plt
from networkx import nx
import numpy as np
import random

def prices_model(n, m, k0 = 1, n0 = 1, reciprocal_threshold = 1):
    """
    Extended version of Prices model: possibility to vary n0 (the number of initial nodes.)
    """
    in_degrees = np.zeros(n, dtype=int)
    sum_in_degrees = 0
    out_degrees = np.zeros(n, dtype=int)
    
    # Initialize graph with n0 nodes
    G = nx.DiGraph()

    for i in range(n0):
        G.add_node(i)

    n_nodes = n0

    # At each time step
    while n_nodes < n:
        j = n_nodes
        # A new node j
        G.add_node(j)

        
        # Pick m nodes at random with probability proportional to their degree + k0
        k0n = k0/n_nodes
        if sum_in_degrees == 0:
            # Make a numpy array of size n_nodes with values 1/n_nodes
            p = np.ones(n_nodes) * 1/n_nodes
        else:
            p = (in_degrees[:n_nodes]/sum_in_degrees + k0n)/(1+k0)

        nodes_to_join = np.random.choice(n_nodes, min(n_nodes, m), replace=False, p=p)

        # Create directed edges (citation)
        for i in nodes_to_join:
            G.add_edge(j, i)
            in_degrees[i] += 1
            sum_in_degrees += 1
            out_degrees[j] += 1

            # Reciprocals
            rp = 1/(out_degrees[i] + 1)
            if rp > reciprocal_threshold:
                G.add_edge(i, j)
                in_degrees[j] += 1
                sum_in_degrees += 1
                out_degrees[i] += 1
            #     print("Reciprocal threshold reached at node", i, rp)
            # else:
            #     print("Reciprocal threshold not reached at node", i, rp)

        n_nodes += 1
    return G

if __name__ == '__main__':
    # prices_graph = prices_model(20, 3, 1, 1, 0.20)
    prices_graph = prices_model(7, 3, 1, 1, 0)
    nx.draw(prices_graph, with_labels=True)
    plt.show()