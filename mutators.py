from random import random
import networkx as nx

def node_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n nodes from the graph.
    """
    nodes = list(graph.nodes)

    # Pick n random indices
    indices = random.sample(range(len(nodes)), n)
    for index in indices:
        graph.remove_node(nodes[index])
    return graph

def edge_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n edges from the graph.
    """
    edges = list(graph.edges)

    # Pick n random indices
    indices = random.sample(range(len(edges)), n)
    for index in indices:
        graph.remove_edge(edges[index][0], edges[index][1])
    return graph

def edge_reversal(graph: nx.DiGraph, n: int = 1):
    """
    Reverse n edges from the graph.
    """
    edges = list(graph.edges)
    indices = random.sample(range(len(edges)), n)
    for index in indices:
        graph.add_edge(edges[index][1], edges[index][0])
        graph.remove_edge(edges[index][0], edges[index][1])

    # TODO: what do we do if the reciprocal edge already exists?
    
    return graph

def edge_addition(graph: nx.DiGraph, n: int = 1):
    """
    Add n edges to the graph between two random nodes which are not connected.
    """
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    k = 0
    while k < n:
        # Pick 2 random nodes
        i = random.randint(0, len(nodes)-1)
        j = random.randint(0, len(nodes)-1)

        if i != j and (i, j) not in edges:
            graph.add_edge(i, j)
            k += 1
    
    return graph