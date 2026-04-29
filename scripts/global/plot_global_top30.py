from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

NODES_PATH = Path("data/processed/global/nodes_global.csv")
EDGES_PATH = Path("data/processed/global/edges_global_undirected.csv")
CENTRALITY_PATH = Path("data/processed/global/centrality_global.csv")
OUT_PATH = Path("visuals/global/global_top30_hubs.png")

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

nodes = pd.read_csv(NODES_PATH)
edges = pd.read_csv(EDGES_PATH)
centrality = pd.read_csv(CENTRALITY_PATH)

top_n = 30
top_nodes = set(centrality.head(top_n)["iso3"])

node_lookup = dict(zip(nodes["iso3"], nodes["country_name"]))

G = nx.Graph()

for iso in top_nodes:
    G.add_node(iso, country_name=node_lookup.get(iso, iso))

for _, row in edges.iterrows():
    a = row["iso3_a"]
    b = row["iso3_b"]

    if a in top_nodes and b in top_nodes:
        G.add_edge(a, b)

degree_dict = dict(G.degree())
labels = {n: G.nodes[n]["country_name"] for n in G.nodes()}
node_sizes = [500 + degree_dict[n] * 90 for n in G.nodes()]

plt.figure(figsize=(16, 12))

pos = nx.spring_layout(G, seed=42, k=0.55, iterations=200)

nx.draw_networkx_edges(G, pos, width=0.8, alpha=0.28)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.9)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)

plt.title("Top 30 Hubs in the Global Tax Treaty Network", fontsize=18)
plt.axis("off")
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")

print(f"Saved top-30 hub graph to: {OUT_PATH}")
