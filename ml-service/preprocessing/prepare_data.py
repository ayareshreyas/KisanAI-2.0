from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# ============================================================
# KISANAI 2.0 - DATA PREPARATION
# ============================================================


# ------------------------------------------------------------
# 1. Project Paths
# ------------------------------------------------------------

ML_SERVICE_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    ML_SERVICE_DIR
    / "data"
    / "raw"
    / "Crop_recommendation.csv"
)

PROCESSED_DIR = (
    ML_SERVICE_DIR
    / "data"
    / "processed"
)

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ------------------------------------------------------------
# 2. Configuration
# ------------------------------------------------------------

FEATURE_COLUMNS = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]

TARGET_COLUMN = "label"

TEST_SIZE = 0.20

RANDOM_STATE = 42


# ------------------------------------------------------------
# 3. Load Raw Dataset
# ------------------------------------------------------------

print("=" * 60)
print("KISANAI 2.0 - DATA PREPARATION")
print("=" * 60)

print("\nLoading raw dataset...")

df = pd.read_csv(RAW_DATA_PATH)

print(f"Dataset loaded successfully.")
print(f"Total samples: {len(df)}")


# ------------------------------------------------------------
# 4. Validate Required Columns
# ------------------------------------------------------------

print("\nValidating dataset structure...")

required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("✓ All required columns are present.")


# ------------------------------------------------------------
# 5. Validate Missing Values
# ------------------------------------------------------------

print("\nChecking missing values...")

missing_values = df[required_columns].isnull().sum()

if missing_values.sum() > 0:
    print(missing_values[missing_values > 0])

    raise ValueError(
        "Dataset contains missing values."
    )

print("✓ No missing values detected.")


# ------------------------------------------------------------
# 6. Validate Duplicate Rows
# ------------------------------------------------------------

print("\nChecking duplicate rows...")

duplicate_count = df.duplicated().sum()

if duplicate_count > 0:
    raise ValueError(
        f"Dataset contains {duplicate_count} duplicate rows."
    )

print("✓ No duplicate rows detected.")


# ------------------------------------------------------------
# 7. Separate Features and Target
# ------------------------------------------------------------

print("\nSeparating features and target...")

X = df[FEATURE_COLUMNS]

y = df[TARGET_COLUMN]

print(f"Features: {FEATURE_COLUMNS}")
print(f"Target: {TARGET_COLUMN}")

print(f"Feature matrix shape: {X.shape}")
print(f"Target shape: {y.shape}")


# ------------------------------------------------------------
# 8. Train/Test Split
# ------------------------------------------------------------

print("\nCreating train/test split...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)


# ------------------------------------------------------------
# 9. Split Summary
# ------------------------------------------------------------

print("\nSPLIT SUMMARY")
print("-" * 40)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

print(
    f"Training percentage: "
    f"{len(X_train) / len(df) * 100:.1f}%"
)

print(
    f"Testing percentage : "
    f"{len(X_test) / len(df) * 100:.1f}%"
)


# ------------------------------------------------------------
# 10. Verify Class Distribution
# ------------------------------------------------------------

print("\nVERIFYING CLASS DISTRIBUTION")
print("-" * 40)

train_distribution = y_train.value_counts().sort_index()

test_distribution = y_test.value_counts().sort_index()

distribution_check = pd.DataFrame(
    {
        "train": train_distribution,
        "test": test_distribution,
    }
)

print(distribution_check)


# ------------------------------------------------------------
# 11. Save Processed Data
# ------------------------------------------------------------

print("\nSaving processed datasets...")

X_train.to_csv(
    PROCESSED_DIR / "X_train.csv",
    index=False,
)

X_test.to_csv(
    PROCESSED_DIR / "X_test.csv",
    index=False,
)

y_train.to_csv(
    PROCESSED_DIR / "y_train.csv",
    index=False,
)

y_test.to_csv(
    PROCESSED_DIR / "y_test.csv",
    index=False,
)


# ------------------------------------------------------------
# 12. Final Verification
# ------------------------------------------------------------

print("\nFINAL VERIFICATION")
print("-" * 40)

saved_files = [
    "X_train.csv",
    "X_test.csv",
    "y_train.csv",
    "y_test.csv",
]

for filename in saved_files:
    filepath = PROCESSED_DIR / filename

    if filepath.exists():
        print(f"✓ {filename}")
    else:
        raise FileNotFoundError(
            f"Expected file was not created: {filename}"
        )


print("\n" + "=" * 60)
print("DATA PREPARATION COMPLETED SUCCESSFULLY")
print("=" * 60)