from pathlib import Path

import networkx as nx
import pandas as pd

NODES_PATH = Path("data/processed/global/nodes_global.csv")
EDGES_PATH = Path("data/processed/global/edges_global_undirected.csv")
OUT_PATH = Path("data/processed/global/centrality_global.csv")

nodes = pd.read_csv(NODES_PATH)
edges = pd.read_csv(EDGES_PATH)

G = nx.Graph()

for _, row in nodes.iterrows():
    G.add_node(row["iso3"], country_name=row["country_name"])

for _, row in edges.iterrows():
    G.add_edge(
        row["iso3_a"],
        row["iso3_b"],
        directions_present=row["directions_present"],
        measure_count=row["measure_count"],
    )

print("=== GLOBAL NETWORK SUMMARY ===")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

degree_dict = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, normalized=True)
closeness = nx.closeness_centrality(G)

rows = []

for node in G.nodes():
    rows.append(
        {
            "iso3": node,
            "country_name": G.nodes[node].get("country_name", node),
            "degree": degree_dict[node],
            "degree_centrality": degree_centrality[node],
            "betweenness_centrality": betweenness[node],
            "closeness_centrality": closeness[node],
        }
    )

df = pd.DataFrame(rows).sort_values(
    by=["degree", "betweenness_centrality", "closeness_centrality"],
    ascending=False,
)

df.to_csv(OUT_PATH, index=False)

print(f"Saved centrality file to: {OUT_PATH}")
print("\n=== TOP 20 NODES ===")
print(df.head(20).to_string(index=False))
