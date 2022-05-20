from networkx import nx
import numpy as np
import random

def prices_graph(n, m, k0 = 1):
    """
    Prices model. Implementation according to wikipedia, but it doesn't work. xd
    """
    in_degrees = np.zeros(n, dtype=int)
    out_degrees = np.zeros(n, dtype=int)
    
    # Initialize graph with 1 node
    G = nx.DiGraph()
    G.add_node(1)

    n_nodes = 1

    while n_nodes < n:
        # Add a new node
        G.add_node(n_nodes)

        # Add citations
        for i in range(n_nodes):
            # Create m directed edges to m (distinct) already present nodes where the likelihood of joining to a node i is proportional to its in-degree.
            probability = (in_degrees[i] + k0)*p_k(m, k0, in_degrees[i])/(m+k0)
            print(probability)
            if random.random() < probability:
                # Create directed edges (citation)
                G.add_edge(n_nodes, i)
                out_degrees[n_nodes] += 1
                in_degrees[i] += 1

        n_nodes += 1


    return G

def p_k(m, k0, k):
    # return (1+1/m)*np.random.beta(k+1, 2+1/m)
    return (m+k0)/(m*(k0 + 1) + k0)*(np.random.beta(k+k0, 2+k0/m))/(np.random.beta(k0, 2+k0/m))
