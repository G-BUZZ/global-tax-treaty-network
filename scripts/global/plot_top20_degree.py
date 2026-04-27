from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CENTRALITY_PATH = Path("data/processed/global/centrality_global.csv")
OUT_PATH = Path("visuals/global/top20_degree_bar.png")

df = pd.read_csv(CENTRALITY_PATH).head(20).copy()

plt.figure(figsize=(14, 8))
plt.barh(df["country_name"][::-1], df["degree"][::-1])
plt.xlabel("Degree")
plt.ylabel("Country")
plt.title("Top 20 Countries by Degree in the Global Tax Treaty Network")
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
print(f"Saved bar chart to: {OUT_PATH}")
