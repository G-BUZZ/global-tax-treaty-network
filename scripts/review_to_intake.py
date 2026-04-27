from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REVIEW_PATH = PROJECT_ROOT / "docs" / "review_pairs.csv"
INTAKE_EDGES = PROJECT_ROOT / "data" / "intake" / "new_edges.csv"

review_df = pd.read_csv(REVIEW_PATH).fillna("")
intake_df = pd.read_csv(INTAKE_EDGES).fillna("")

approved = review_df[review_df["treaty_verified"].astype(str).str.strip().str.lower() == "yes"].copy()

if approved.empty:
    print("No approved pairs found in review_pairs.csv")
    raise SystemExit(0)

new_rows = []
for _, row in approved.iterrows():
    new_rows.append({
        "source_country": row["country_a"],
        "target_country": row["country_b"],
        "source_iso3": row["iso3_a"],
        "target_iso3": row["iso3_b"],
        "treaty_in_force": "yes",
        "signature_date": "",
        "entry_into_force_date": "",
        "data_source": row["data_source"],
        "mli_relevant": "unknown",
        "notes": row["notes"],
    })

new_df = pd.DataFrame(new_rows)

# avoid duplicates already present in intake
combined = pd.concat([intake_df, new_df], ignore_index=True)

def edge_key(row):
    return tuple(sorted([str(row["source_iso3"]).strip(), str(row["target_iso3"]).strip()]))

combined["_edge_key"] = combined.apply(edge_key, axis=1)
combined = combined.drop_duplicates(subset=["_edge_key"], keep="first").drop(columns=["_edge_key"])

combined.to_csv(INTAKE_EDGES, index=False)

print(f"Approved pairs added to intake: {len(new_df)}")
print(f"Updated intake file: {INTAKE_EDGES}")
