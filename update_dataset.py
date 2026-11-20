import pandas as pd

df = pd.read_csv("data/wine.csv")

# Add a new column to demonstrate dataset versioning
df["dataset_version"] = "version_2"

df.to_csv("data/wine.csv", index=False)

print("Dataset updated to Version 2!")
print(df.head())