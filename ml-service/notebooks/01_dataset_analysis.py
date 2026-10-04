from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
# 1. Project Paths
# --------------------------------------------------

# This file is inside:
# KisanAI-2.0/ml-service/notebooks/

# parents[0] = notebooks
# parents[1] = ml-service
ML_SERVICE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = ML_SERVICE_DIR / "data" / "raw" / "Crop_recommendation.csv"
OUTPUT_DIR = ML_SERVICE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Load Dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)


print("=" * 60)
print("KISANAI 2.0 - DATASET ANALYSIS")
print("=" * 60)


# --------------------------------------------------
# 3. Basic Information
# --------------------------------------------------

print("\n1. DATASET SHAPE")
print("-" * 40)
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


print("\n2. COLUMN NAMES")
print("-" * 40)
print(df.columns.tolist())


print("\n3. DATA TYPES")
print("-" * 40)
print(df.dtypes)


# --------------------------------------------------
# 4. Missing Values
# --------------------------------------------------

print("\n4. MISSING VALUES")
print("-" * 40)
print(df.isnull().sum())


# --------------------------------------------------
# 5. Duplicate Rows
# --------------------------------------------------

print("\n5. DUPLICATE ROWS")
print("-" * 40)

duplicate_count = df.duplicated().sum()

print(f"Duplicate rows: {duplicate_count}")


# --------------------------------------------------
# 6. Statistical Summary
# --------------------------------------------------

print("\n6. STATISTICAL SUMMARY")
print("-" * 40)
print(df.describe().round(2))


# --------------------------------------------------
# 7. Crop Classes
# --------------------------------------------------

print("\n7. CROP CLASSES")
print("-" * 40)

crop_counts = df["label"].value_counts()

print(f"Number of crop classes: {df['label'].nunique()}")
print()

print(crop_counts)


# --------------------------------------------------
# 8. Feature Ranges
# --------------------------------------------------

print("\n8. FEATURE RANGES")
print("-" * 40)

numeric_features = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]

for feature in numeric_features:
    print(
        f"{feature:12} "
        f"Min: {df[feature].min():8.2f} | "
        f"Max: {df[feature].max():8.2f} | "
        f"Mean: {df[feature].mean():8.2f}"
    )


# --------------------------------------------------
# 9. Correlation Analysis
# --------------------------------------------------

print("\n9. CORRELATION MATRIX")
print("-" * 40)

correlation_matrix = df[numeric_features].corr()

print(correlation_matrix.round(2))


# --------------------------------------------------
# 10. Save Correlation Heatmap
# --------------------------------------------------

plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="YlGn",
    linewidths=0.5,
)

plt.title("KisanAI - Feature Correlation Matrix")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "feature_correlation.png",
    dpi=300,
)

plt.show()


# --------------------------------------------------
# 11. Feature Distributions
# --------------------------------------------------

df[numeric_features].hist(
    figsize=(14, 10),
    bins=30,
)

plt.suptitle(
    "KisanAI - Feature Distributions",
    fontsize=16,
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "feature_distributions.png",
    dpi=300,
)

plt.show()


# --------------------------------------------------
# 12. Crop Distribution
# --------------------------------------------------

plt.figure(figsize=(12, 7))

crop_counts.sort_values().plot(
    kind="barh"
)

plt.title("KisanAI - Crop Class Distribution")

plt.xlabel("Number of Samples")

plt.ylabel("Crop")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "crop_distribution.png",
    dpi=300,
)

plt.show()


# --------------------------------------------------
# 13. Final Dataset Check
# --------------------------------------------------

print("\n10. FINAL DATASET CHECK")
print("-" * 40)

if df.isnull().sum().sum() == 0:
    print("✓ No missing values")

if duplicate_count == 0:
    print("✓ No duplicate rows")

if df["label"].nunique() == 22:
    print("✓ 22 crop classes detected")

if all(
    pd.api.types.is_numeric_dtype(df[feature])
    for feature in numeric_features
):
    print("✓ Numerical features have valid numeric types")

print("\nDataset analysis completed successfully.")

print("\nGenerated files:")
print("✓ data/processed/feature_correlation.png")
print("✓ data/processed/feature_distributions.png")
print("✓ data/processed/crop_distribution.png")