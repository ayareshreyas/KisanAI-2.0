from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"


# --------------------------------------------------
# 2. Load processed training data
# --------------------------------------------------

X_train_path = DATA_DIR / "X_train.csv"
y_train_path = DATA_DIR / "y_train.csv"

X_train = pd.read_csv(X_train_path)
y_train = pd.read_csv(y_train_path).squeeze("columns")


print("=" * 60)
print("CROSS-VALIDATION — CROP RECOMMENDATION MODEL")
print("=" * 60)

print(f"\nTraining features shape: {X_train.shape}")
print(f"Training labels shape:   {y_train.shape}")

print(f"\nNumber of crop classes: {y_train.nunique()}")


# --------------------------------------------------
# 3. Define Random Forest model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# 4. Define Stratified K-Fold cross-validation
# --------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# --------------------------------------------------
# 5. Run cross-validation
# --------------------------------------------------

scoring = {
    "accuracy": "accuracy",
    "precision": "precision_weighted",
    "recall": "recall_weighted",
    "f1": "f1_weighted"
}

results = cross_validate(
    model,
    X_train,
    y_train,
    cv=cv,
    scoring=scoring,
    n_jobs=-1
)


# --------------------------------------------------
# 6. Display results for each fold
# --------------------------------------------------

print("\n" + "=" * 60)
print("RESULTS BY FOLD")
print("=" * 60)

for fold in range(5):
    print(f"\nFold {fold + 1}")
    print(f"  Accuracy : {results['test_accuracy'][fold]:.4f}")
    print(f"  Precision: {results['test_precision'][fold]:.4f}")
    print(f"  Recall   : {results['test_recall'][fold]:.4f}")
    print(f"  F1 Score : {results['test_f1'][fold]:.4f}")


# --------------------------------------------------
# 7. Calculate average and standard deviation
# --------------------------------------------------

print("\n" + "=" * 60)
print("CROSS-VALIDATION SUMMARY")
print("=" * 60)

for metric in ["accuracy", "precision", "recall", "f1"]:
    scores = results[f"test_{metric}"]

    mean_score = scores.mean()
    std_score = scores.std()

    print(
        f"{metric.capitalize():<10}: "
        f"{mean_score:.4f} ± {std_score:.4f}"
    )


# --------------------------------------------------
# 8. Interpretation
# --------------------------------------------------

print("\n" + "=" * 60)
print("INTERPRETATION")
print("=" * 60)

accuracy_scores = results["test_accuracy"]

print(
    f"\nAverage validation accuracy: "
    f"{accuracy_scores.mean() * 100:.2f}%"
)

print(
    f"Validation accuracy variation: "
    f"± {accuracy_scores.std() * 100:.2f}%"
)

print("\nCross-validation completed successfully.")