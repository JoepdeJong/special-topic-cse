import networkx as nx
from prices_model import prices_graph, p_k

""" 
    Undirected graph
"""
# barabasi_albert_graph = nx.barabasi_albert_graph(24, 3)

# nx.draw(barabasi_albert_graph, with_labels=True)

import matplotlib.pyplot as plt
# plt.show()


# prices_graph2 = prices_graph(13, 0.1, 1)

# nx.draw(prices_graph2, with_labels=True)
# plt.show()

total = 0
for i in range(10):
    total += p_k(100,1,i)
print(total)