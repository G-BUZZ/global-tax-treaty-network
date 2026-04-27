from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NODES_PATH = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
EDGES_PATH = PROJECT_ROOT / "data" / "processed" / "edges.csv"

EXPECTED_NODES = [
    "country_name",
    "iso3",
    "region",
    "oecd_member",
    "source_notes",
]

EXPECTED_EDGES = [
    "source_country",
    "target_country",
    "source_iso3",
    "target_iso3",
    "treaty_in_force",
    "signature_date",
    "entry_into_force_date",
    "data_source",
    "mli_relevant",
    "notes",
]

def check_file(path: Path, expected_cols: list[str], name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{name} not found: {path}")

    df = pd.read_csv(path)

    actual = list(df.columns)
    if actual != expected_cols:
        raise ValueError(
            f"{name} columns mismatch.\nExpected: {expected_cols}\nActual:   {actual}"
        )

    print(f"[OK] {name} columns are valid.")
    print(f"[INFO] {name} rows: {len(df)}")
    return df

def main() -> None:
    nodes = check_file(NODES_PATH, EXPECTED_NODES, "nodes.csv")
    edges = check_file(EDGES_PATH, EXPECTED_EDGES, "edges.csv")

    if len(nodes) == 0:
        print("[WARN] nodes.csv has no data rows yet.")
    else:
        print("[OK] nodes.csv contains at least one node.")

    if nodes["iso3"].duplicated().any():
        dupes = nodes.loc[nodes["iso3"].duplicated(), "iso3"].tolist()
        print(f"[WARN] Duplicate ISO3 codes found in nodes.csv: {dupes}")
    else:
        print("[OK] No duplicate ISO3 codes in nodes.csv.")

    node_iso_set = set(nodes["iso3"].dropna().astype(str).str.strip())

    if len(edges) == 0:
        print("[INFO] edges.csv is empty.")
        print("\nValidation complete.")
        return

    # strip whitespace
    for col in ["source_iso3", "target_iso3", "source_country", "target_country"]:
        edges[col] = edges[col].astype(str).str.strip()

    # unknown ISO references
    missing_source = sorted(set(edges.loc[~edges["source_iso3"].isin(node_iso_set), "source_iso3"]))
    missing_target = sorted(set(edges.loc[~edges["target_iso3"].isin(node_iso_set), "target_iso3"]))

    if missing_source:
        print(f"[WARN] Source ISO codes missing from nodes.csv: {missing_source}")
    else:
        print("[OK] All source ISO codes exist in nodes.csv.")

    if missing_target:
        print(f"[WARN] Target ISO codes missing from nodes.csv: {missing_target}")
    else:
        print("[OK] All target ISO codes exist in nodes.csv.")

    # self loops
    self_loops = edges[edges["source_iso3"] == edges["target_iso3"]]
    if not self_loops.empty:
        print(f"[WARN] Self-loop edges found: {len(self_loops)}")
    else:
        print("[OK] No self-loop edges found.")

    # reverse duplicate detection
    pair_key = edges.apply(
        lambda row: tuple(sorted([row["source_iso3"], row["target_iso3"]])),
        axis=1
    )
    dup_mask = pair_key.duplicated()
    if dup_mask.any():
        print("[WARN] Duplicate undirected edges found:")
        print(edges.loc[dup_mask, ["source_country", "target_country", "source_iso3", "target_iso3"]])
    else:
        print("[OK] No duplicate undirected edges found.")

    print("\nValidation complete.")

if __name__ == "__main__":
    main()
