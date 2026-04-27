from pathlib import Path
import math
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"
OUTPUT_PATH = PROJECT_ROOT / "visuals" / "italy_seed_network_showcase.png"

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

# Manual radial layout: Italy in center, others on a circle
pos = {}
center_node = "ITA"
other_nodes = sorted([n for n in G.nodes() if n != center_node])

pos[center_node] = (0.0, 0.0)

radius = 1.8
for i, node in enumerate(other_nodes):
    angle = 2 * math.pi * i / len(other_nodes)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    pos[node] = (x, y)

node_sizes = []
node_colors = []

for node in G.nodes():
    if node == "ITA":
        node_sizes.append(5200)
        node_colors.append("#d62828")
    else:
        node_sizes.append(2200)
        node_colors.append("#3a86ff")

plt.figure(figsize=(12, 10), facecolor="white")

nx.draw_networkx_edges(
    G,
    pos,
    width=2.2,
    alpha=0.55,
    edge_color="#444444"
)

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=node_sizes,
    node_color=node_colors,
    alpha=0.92,
    linewidths=1.5,
    edgecolors="white"
)

nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=11,
    font_weight="medium"
)

plt.title("Italy Treaty Network — Seed Snapshot", fontsize=22, pad=22)
plt.text(
    0.5, -0.06,
    "Current stage: ego-network centered on Italy; suitable as methodological checkpoint, not final full network.",
    ha="center",
    va="center",
    fontsize=10,
    transform=plt.gca().transAxes
)

plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Saved showcase graph to: {OUTPUT_PATH}")
