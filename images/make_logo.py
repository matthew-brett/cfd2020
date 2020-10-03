from os.path import dirname, join as pjoin

import matplotlib.pyplot as plt
import networkx as nx

root = dirname(__file__)

# Number of nodes as input to graph generator
n = 30
# Colormaps for nodes, edges
n_cm = getattr(plt.cm, 'tab20b')
e_cm = getattr(plt.cm, 'bone')
# See for random number generator
seed = 692

G_orig = nx.erdos_renyi_graph(n, 0.1, seed=seed)
# Get largest connected component
G = next(G_orig.subgraph(c).copy() for c in nx.connected_components(G_orig))
n_nodes = len(G.nodes)
n_edges = len(G.edges)
pos = nx.spring_layout(G, seed=seed)
plt.close()
nx.draw(G, pos,
        node_color=range(n_nodes),
        edge_color=range(n_edges)[::-1],
        node_size=1200,
        width=10,
        cmap=n_cm,
        edge_cmap=e_cm,
        with_labels=False)

plt.savefig(pjoin(root, 'dsfe_logo.png'), dpi=150)
