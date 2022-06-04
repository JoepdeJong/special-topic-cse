from random import random
import networkx as nx

def node_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n nodes from the graph.
    """
    nodes = list(graph.nodes)
    random.shuffle(nodes)
    for i in range(n):
        graph.remove_node(nodes[i])
    return graph

def edge_removal(graph: nx.DiGraph, n: int = 1):
    """
    Remove n edges from the graph.
    """
    edges = list(graph.edges)
    random.shuffle(edges)
    for i in range(n):
        graph.remove_edge(edges[i][0], edges[i][1])
    return graph

def edge_reversal(graph: nx.DiGraph, n: int = 1):
    """
    Reverse n edges from the graph.
    """
    edges = list(graph.edges)
    random.shuffle(edges)
    for i in range(n):
        graph.add_edge(edges[i][1], edges[i][0])
        graph.remove_edge(edges[i][0], edges[i][1])

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