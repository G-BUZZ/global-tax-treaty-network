from pathlib import Path

import numpy as np
import pandas as pd

RAW_DIR = Path("data/raw/oecd")
OUT_DIR = Path("data/processed/global")
OUT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*.csv")) + list(RAW_DIR.glob("*.xlsx")) + list(RAW_DIR.glob("*.xls"))

if not files:
    raise SystemExit("No OECD raw file found in data/raw/oecd")

path = files[0]
print(f"[INFO] Using raw file: {path}")

if path.suffix.lower() == ".csv":
    df = pd.read_csv(path, low_memory=False)
else:
    df = pd.read_excel(path)

required = {
    "REF_AREA": "ref_iso3",
    "Reference area": "ref_name",
    "COUNTERPART_AREA": "cp_iso3",
    "Counterpart area": "cp_name",
    "TIME_PERIOD": "time_period",
    "MEASURE": "measure",
    "LEGAL_BASIS": "legal_basis",
    "TREATY_DATE": "treaty_date",
    "OBS_VALUE": "obs_value",
}

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing expected columns: {missing}")

df = df[list(required.keys())].rename(columns=required)

for col in ["ref_iso3", "ref_name", "cp_iso3", "cp_name", "measure", "legal_basis"]:
    df[col] = df[col].astype(str).str.strip()

df["time_period_num"] = pd.to_numeric(df["time_period"], errors="coerce")
df["treaty_date_num"] = pd.to_numeric(df["treaty_date"], errors="coerce")

df = df[df["legal_basis"] == "TRE"].copy()

latest_year = int(df["time_period_num"].dropna().max())
df = df[df["time_period_num"] == latest_year].copy()

df = df[
    df["ref_iso3"].ne("")
    & df["cp_iso3"].ne("")
    & df["ref_name"].ne("")
    & df["cp_name"].ne("")
].copy()

print(f"[INFO] Latest year used: {latest_year}")
print(f"[INFO] Rows after filter: {len(df)}")

nodes_left = df[["ref_iso3", "ref_name"]].rename(
    columns={"ref_iso3": "iso3", "ref_name": "country_name"}
)

nodes_right = df[["cp_iso3", "cp_name"]].rename(
    columns={"cp_iso3": "iso3", "cp_name": "country_name"}
)

nodes = (
    pd.concat([nodes_left, nodes_right], ignore_index=True)
    .drop_duplicates()
    .sort_values(["country_name", "iso3"])
)

nodes.to_csv(OUT_DIR / "nodes_global.csv", index=False)
print(f"[OK] Saved nodes_global.csv with {len(nodes)} nodes")

directed = (
    df.groupby(["ref_iso3", "ref_name", "cp_iso3", "cp_name"], as_index=False)
    .agg(
        latest_year=("time_period_num", "max"),
        measures_present=("measure", lambda s: "|".join(sorted(set(s.dropna())))),
        measure_count=("measure", lambda s: s.dropna().nunique()),
        obs_row_count=("obs_value", "size"),
        non_null_obs_count=("obs_value", lambda s: s.notna().sum()),
        treaty_year_min=("treaty_date_num", "min"),
        treaty_year_max=("treaty_date_num", "max"),
    )
    .rename(
        columns={
            "ref_iso3": "source_iso3",
            "ref_name": "source_country",
            "cp_iso3": "target_iso3",
            "cp_name": "target_country",
        }
    )
    .sort_values(["source_country", "target_country"])
)

directed.to_csv(OUT_DIR / "edges_global_directed.csv", index=False)
print(f"[OK] Saved edges_global_directed.csv with {len(directed)} directed edges")

tmp = df.copy()

tmp["country_a"] = np.where(tmp["ref_iso3"] <= tmp["cp_iso3"], tmp["ref_name"], tmp["cp_name"])
tmp["iso3_a"] = np.where(tmp["ref_iso3"] <= tmp["cp_iso3"], tmp["ref_iso3"], tmp["cp_iso3"])
tmp["country_b"] = np.where(tmp["ref_iso3"] <= tmp["cp_iso3"], tmp["cp_name"], tmp["ref_name"])
tmp["iso3_b"] = np.where(tmp["ref_iso3"] <= tmp["cp_iso3"], tmp["cp_iso3"], tmp["ref_iso3"])
tmp["direction_key"] = tmp["ref_iso3"] + "->" + tmp["cp_iso3"]

undirected = (
    tmp.groupby(["iso3_a", "country_a", "iso3_b", "country_b"], as_index=False)
    .agg(
        latest_year=("time_period_num", "max"),
        directions_present=("direction_key", "nunique"),
        measures_present=("measure", lambda s: "|".join(sorted(set(s.dropna())))),
        measure_count=("measure", lambda s: s.dropna().nunique()),
        obs_row_count=("obs_value", "size"),
        non_null_obs_count=("obs_value", lambda s: s.notna().sum()),
        treaty_year_min=("treaty_date_num", "min"),
        treaty_year_max=("treaty_date_num", "max"),
    )
    .sort_values(["country_a", "country_b"])
)

undirected.to_csv(OUT_DIR / "edges_global_undirected.csv", index=False)
print(f"[OK] Saved edges_global_undirected.csv with {len(undirected)} undirected edges")

print("\n[DONE] Global network datasets created.")
