from pathlib import Path
import pandas as pd
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"

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
    G.add_edge(
        row["source_iso3"],
        row["target_iso3"],
        treaty_in_force=row["treaty_in_force"],
        data_source=row["data_source"],
    )

print("=== NETWORK SUMMARY ===")
print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

degree_dict = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, normalized=True)
closeness = nx.closeness_centrality(G)

summary_rows = []
for node in G.nodes():
    summary_rows.append({
        "iso3": node,
        "country_name": G.nodes[node].get("country_name", node),
        "degree": degree_dict[node],
        "degree_centrality": round(degree_centrality[node], 6),
        "betweenness_centrality": round(betweenness[node], 6),
        "closeness_centrality": round(closeness[node], 6),
    })

summary_df = pd.DataFrame(summary_rows).sort_values(
    by=["degree", "betweenness_centrality", "closeness_centrality"],
    ascending=False
)

print("\n=== CENTRALITY RANKING ===")
print(summary_df.to_string(index=False))
