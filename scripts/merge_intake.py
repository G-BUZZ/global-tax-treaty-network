from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_NODES = PROJECT_ROOT / "data" / "processed" / "nodes.csv"
PROCESSED_EDGES = PROJECT_ROOT / "data" / "processed" / "edges.csv"

INTAKE_NODES = PROJECT_ROOT / "data" / "intake" / "new_nodes.csv"
INTAKE_EDGES = PROJECT_ROOT / "data" / "intake" / "new_edges.csv"

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

def read_csv_checked(path: Path, expected_cols: list[str], label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    df = pd.read_csv(path)
    actual_cols = list(df.columns)
    if actual_cols != expected_cols:
        raise ValueError(
            f"{label} columns mismatch.\nExpected: {expected_cols}\nActual:   {actual_cols}"
        )
    return df

def normalize_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
    return df

def edge_key(row) -> tuple[str, str]:
    return tuple(sorted([row["source_iso3"], row["target_iso3"]]))

def main() -> None:
    processed_nodes = read_csv_checked(PROCESSED_NODES, EXPECTED_NODES, "processed nodes")
    processed_edges = read_csv_checked(PROCESSED_EDGES, EXPECTED_EDGES, "processed edges")
    intake_nodes = read_csv_checked(INTAKE_NODES, EXPECTED_NODES, "intake nodes")
    intake_edges = read_csv_checked(INTAKE_EDGES, EXPECTED_EDGES, "intake edges")

    processed_nodes = normalize_text(processed_nodes, EXPECTED_NODES)
    processed_edges = normalize_text(processed_edges, EXPECTED_EDGES)
    intake_nodes = normalize_text(intake_nodes, EXPECTED_NODES)
    intake_edges = normalize_text(intake_edges, EXPECTED_EDGES)

    print(f"[INFO] Processed nodes before merge: {len(processed_nodes)}")
    print(f"[INFO] Processed edges before merge: {len(processed_edges)}")
    print(f"[INFO] Intake nodes: {len(intake_nodes)}")
    print(f"[INFO] Intake edges: {len(intake_edges)}")

    # Merge nodes by unique ISO3
    existing_iso = set(processed_nodes["iso3"])
    new_node_rows = intake_nodes[~intake_nodes["iso3"].isin(existing_iso)].copy()

    merged_nodes = pd.concat([processed_nodes, new_node_rows], ignore_index=True)
    merged_nodes = merged_nodes.drop_duplicates(subset=["iso3"], keep="first")

    # Validate edge references against merged nodes
    merged_iso = set(merged_nodes["iso3"])
    invalid_sources = intake_edges.loc[~intake_edges["source_iso3"].isin(merged_iso), "source_iso3"].unique().tolist()
    invalid_targets = intake_edges.loc[~intake_edges["target_iso3"].isin(merged_iso), "target_iso3"].unique().tolist()

    if invalid_sources:
        raise ValueError(f"Intake edges contain unknown source ISO codes: {invalid_sources}")
    if invalid_targets:
        raise ValueError(f"Intake edges contain unknown target ISO codes: {invalid_targets}")

    if (intake_edges["source_iso3"] == intake_edges["target_iso3"]).any():
        raise ValueError("Intake edges contain self-loops.")

    processed_edge_keys = set(processed_edges.apply(edge_key, axis=1).tolist())
    intake_edges["_edge_key"] = intake_edges.apply(edge_key, axis=1)

    new_edge_rows = intake_edges[~intake_edges["_edge_key"].isin(processed_edge_keys)].copy()
    new_edge_rows = new_edge_rows.drop(columns=["_edge_key"])

    merged_edges = pd.concat([processed_edges, new_edge_rows], ignore_index=True)

    # Save merged files
    merged_nodes.to_csv(PROCESSED_NODES, index=False)
    merged_edges.to_csv(PROCESSED_EDGES, index=False)

    print(f"[OK] Added nodes: {len(new_node_rows)}")
    print(f"[OK] Added edges: {len(new_edge_rows)}")
    print(f"[INFO] Processed nodes after merge: {len(merged_nodes)}")
    print(f"[INFO] Processed edges after merge: {len(merged_edges)}")

    # Reset intake files to headers only
    pd.DataFrame(columns=EXPECTED_NODES).to_csv(INTAKE_NODES, index=False)
    pd.DataFrame(columns=EXPECTED_EDGES).to_csv(INTAKE_EDGES, index=False)
    print("[OK] Intake files reset to empty headers.")

if __name__ == "__main__":
    main()
