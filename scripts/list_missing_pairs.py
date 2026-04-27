from pathlib import Path
from itertools import combinations
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"
OUTPUT_PATH = PROJECT_ROOT / "docs" / "review_pairs.csv"

nodes = pd.read_csv(NODES_PATH)
edges = pd.read_csv(EDGES_PATH)

# Build existing undirected edge set
existing_edges = set()
for _, row in edges.iterrows():
    key = tuple(sorted([str(row["source_iso3"]).strip(), str(row["target_iso3"]).strip()]))
    existing_edges.add(key)

# Use current nodes except Italy to build a manageable first review queue
candidate_nodes = nodes[nodes["iso3"] != "ITA"].copy()

pairs = []
for a, b in combinations(candidate_nodes.to_dict("records"), 2):
    key = tuple(sorted([a["iso3"], b["iso3"]]))
    if key in existing_edges:
        continue
    pairs.append({
        "country_a": a["country_name"],
        "iso3_a": a["iso3"],
        "country_b": b["country_name"],
        "iso3_b": b["iso3"],
        "treaty_verified": "",
        "data_source": "",
        "notes": ""
    })

review_df = pd.DataFrame(pairs)
review_df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved review queue to: {OUTPUT_PATH}")
print(f"Pairs to review: {len(review_df)}")
