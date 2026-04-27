from pathlib import Path
import pandas as pd
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "centrality_ranking.csv"

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

degree_dict = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, normalized=True)
closeness = nx.closeness_centrality(G)

rows = []
for node in G.nodes():
    rows.append({
        "iso3": node,
        "country_name": G.nodes[node].get("country_name", node),
        "degree": degree_dict[node],
        "degree_centrality": degree_centrality[node],
        "betweenness_centrality": betweenness[node],
        "closeness_centrality": closeness[node],
    })

df = pd.DataFrame(rows).sort_values(
    by=["degree", "betweenness_centrality", "closeness_centrality"],
    ascending=False
)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved ranking to: {OUTPUT_PATH}")
