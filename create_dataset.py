from sklearn.datasets import load_wine
import pandas as pd

# Load Wine dataset
wine = load_wine()

# Create DataFrame
df = pd.DataFrame(wine.data, columns=wine.feature_names)

# Add target column
df["target"] = wine.target

# Save dataset
df.to_csv("data/wine.csv", index=False)

print("Wine dataset saved successfully!")
print(df.head())
print("Dataset shape:", df.shape)