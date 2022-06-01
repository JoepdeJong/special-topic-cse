import networkx as nx
from prices_model import prices_model
import matplotlib.pyplot as plt

prices_graph = prices_model(13, 2, 1)

nx.draw(prices_graph, with_labels=True)
plt.show()