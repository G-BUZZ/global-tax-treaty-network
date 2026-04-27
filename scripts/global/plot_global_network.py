from pathlib import Path
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

NODES_PATH = Path("data/processed/global/nodes_global.csv")
EDGES_PATH = Path("data/processed/global/edges_global_undirected.csv")
OUT_PATH = Path("visuals/global/global_network_full.png")

nodes = pd.read_csv(NODES_PATH)
edges = pd.read_csv(EDGES_PATH)

G = nx.Graph()

for _, row in nodes.iterrows():
    G.add_node(row["iso3"], country_name=row["country_name"])

for _, row in edges.iterrows():
    G.add_edge(row["iso3_a"], row["iso3_b"])

degree_dict = dict(G.degree())
node_sizes = [20 + degree_dict[n] * 8 for n in G.nodes()]

plt.figure(figsize=(18, 14))
pos = nx.spring_layout(G, seed=42, k=0.22, iterations=100)

nx.draw_networkx_edges(G, pos, width=0.25, alpha=0.15)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.75)

plt.title("Global Tax Treaty Network (OECD-derived, undirected)", fontsize=18)
plt.axis("off")
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
print(f"Saved full network graph to: {OUT_PATH}")
