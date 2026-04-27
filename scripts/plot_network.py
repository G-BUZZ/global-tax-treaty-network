from pathlib import Path
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"
OUTPUT_PATH = PROJECT_ROOT / "visuals" / "italy_seed_network.png"

nodes = pd.read_csv(NODES_PATH)
edges = pd.read_csv(EDGES_PATH)

G = nx.Graph()

for _, row in nodes.iterrows():
    G.add_node(
        row["iso3"],
        country_name=row["country_name"],
        region=row["region"],
        oecd_member=row["oecd_member"],
    )

for _, row in edges.iterrows():
    G.add_edge(row["source_iso3"], row["target_iso3"])

labels = {node: G.nodes[node]["country_name"] for node in G.nodes()}

node_sizes = [900 + G.degree(node) * 500 for node in G.nodes()]

node_colors = []
for node in G.nodes():
    if node == "ITA":
        node_colors.append("tab:red")
    else:
        node_colors.append("tab:blue")

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)

nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

plt.title("Italy Seed Treaty Network")
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
print(f"Saved graph to: {OUTPUT_PATH}")
