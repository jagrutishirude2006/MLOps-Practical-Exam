import pandas as pd
from sklearn.datasets import load_wine
wine = load_wine(as_frame=True)
df = wine.frame
df.to_csv("data/raw/wine_v1.csv", index=False)
print(f"Saved {len(df)} rows to data/raw/wine_v1.csv")
print(df.head())