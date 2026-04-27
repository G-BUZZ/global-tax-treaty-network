from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw/oecd")

files = list(RAW_DIR.glob("*.csv")) + list(RAW_DIR.glob("*.xlsx")) + list(RAW_DIR.glob("*.xls"))

if not files:
    raise SystemExit("No CSV/XLS/XLSX file found in data/raw/oecd")

path = files[0]
print(f"[INFO] Found file: {path}")

if path.suffix.lower() == ".csv":
    df = pd.read_csv(path)
    print("[INFO] File type: CSV")
    print("[INFO] Columns:")
    for c in df.columns:
        print("-", c)
    print("\n[INFO] First 10 rows:")
    print(df.head(10).to_string(index=False))
else:
    print("[INFO] File type: Excel")
    xls = pd.ExcelFile(path)
    print("[INFO] Sheets:")
    for s in xls.sheet_names:
        print("-", s)
    first_sheet = xls.sheet_names[0]
    print(f"\n[INFO] Reading first sheet: {first_sheet}")
    df = pd.read_excel(path, sheet_name=first_sheet)
    print("[INFO] Columns:")
    for c in df.columns:
        print("-", c)
    print("\n[INFO] First 10 rows:")
    print(df.head(10).to_string(index=False))
