import pandas as pd
import numpy as np
df = pd.read_csv("data/raw/wine_v1.csv")
feature_cols = [c for c in df.columns if c != "target"]
rng = np.random.default_rng(42)
sample = df.sample(n=20, random_state=42).copy().reset_index(drop=True)
feature_scale = df[feature_cols].std().to_numpy()
noise = rng.normal(
loc=0.0,
scale=0.01 * feature_scale,
size=(20, len(feature_cols))
)
sample.loc[:, feature_cols] = (
sample[feature_cols].to_numpy() + noise
)
augmented = pd.concat([df, sample], ignore_index=True)
augmented.to_csv("data/raw/wine_v1.csv", index=False)
print(f"Dataset now has {len(augmented)} rows")