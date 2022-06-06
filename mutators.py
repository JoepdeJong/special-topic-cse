import networkx as nx
import numpy as np

def node_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n nodes from the graph.
    """
    # Get number of nodes in graph
    n_nodes = len(graph.nodes)

    # Pick n random indices
    indices = np.random.choice(range(n_nodes), min(n, n_nodes))
    graph.remove_nodes_from(indices)

    return graph

def edge_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n edges from the graph.
    """
    # Convert list of edges to array
    edges = np.array(graph.edges)
    n_edges = len(edges)

    # Pick n random indices
    indices = np.random.choice(range(n_edges), min(n, n_edges))
    graph.remove_edges_from(edges[indices])
    return graph

def edge_reversal(graph: nx.DiGraph, n: int = 1):
    """
    Reverse n edges from the graph.
    """
    edges = list(graph.edges)
    n_edges = len(edges)
    indices = np.random.choice(range(n_edges), min(n, n_edges))
    for index in indices:
        if (edges[index][1], edges[index][0]) not in edges:
            graph.add_edge(edges[index][1], edges[index][0])
            graph.remove_edge(edges[index][0], edges[index][1])
            edges.append((edges[index][1], edges[index][0]))

    # TODO: what do we do if the reciprocal edge already exists?
    
    return graph

def edge_addition(graph: nx.DiGraph, n: int = 1):
    """
    Add n edges to the graph between two random nodes which are not connected.
    """
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    max_edges = len(nodes) * (len(nodes) - 1) / 2

    k = 0
    while k < n:
        # Return if the graph is fully connected
        if len(edges) == max_edges:
            break

        # Pick 2 random nodes
        [i,j] = np.random.choice(len(nodes), 2)

        if i != j and (i, j) not in edges:
            graph.add_edge(i, j)
            edges.append((i, j))
            k += 1
    
    return graph