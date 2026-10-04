from pathlib import Path

import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"


# --------------------------------------------------
# 2. Load training data
# --------------------------------------------------

X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze("columns")


print("=" * 70)
print("CROP RECOMMENDATION — MODEL COMPARISON")
print("=" * 70)

print(f"\nTraining samples : {len(X_train)}")
print(f"Features         : {X_train.shape[1]}")
print(f"Crop classes     : {y_train.nunique()}")


# --------------------------------------------------
# 3. Define models
# --------------------------------------------------

models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                random_state=42
            )
        )
    ]),

    "Hist Gradient Boosting": HistGradientBoostingClassifier(
        max_iter=300,
        random_state=42
    )
}


# --------------------------------------------------
# 4. Cross-validation setup
# --------------------------------------------------

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


scoring = {
    "accuracy": "accuracy",
    "precision": "precision_weighted",
    "recall": "recall_weighted",
    "f1": "f1_weighted"
}


# --------------------------------------------------
# 5. Compare models
# --------------------------------------------------

results = []


for name, model in models.items():

    print("\n" + "-" * 70)
    print(f"Testing: {name}")
    print("-" * 70)

    scores = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=-1
    )

    accuracy_mean = scores["test_accuracy"].mean()
    accuracy_std = scores["test_accuracy"].std()

    precision_mean = scores["test_precision"].mean()
    recall_mean = scores["test_recall"].mean()
    f1_mean = scores["test_f1"].mean()

    results.append({
        "Model": name,
        "Accuracy Mean": accuracy_mean,
        "Accuracy Std": accuracy_std,
        "Precision Mean": precision_mean,
        "Recall Mean": recall_mean,
        "F1 Mean": f1_mean
    })

    print(f"Accuracy : {accuracy_mean:.4f} ± {accuracy_std:.4f}")
    print(f"Precision: {precision_mean:.4f}")
    print(f"Recall   : {recall_mean:.4f}")
    print(f"F1 Score : {f1_mean:.4f}")


# --------------------------------------------------
# 6. Create comparison table
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="F1 Mean",
    ascending=False
)


# --------------------------------------------------
# 7. Display final comparison
# --------------------------------------------------

print("\n" + "=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        formatters={
            "Accuracy Mean": "{:.4f}".format,
            "Accuracy Std": "{:.4f}".format,
            "Precision Mean": "{:.4f}".format,
            "Recall Mean": "{:.4f}".format,
            "F1 Mean": "{:.4f}".format,
        }
    )
)


# --------------------------------------------------
# 8. Save comparison results
# --------------------------------------------------

output_path = DATA_DIR / "crop_model_comparison.csv"

results_df.to_csv(
    output_path,
    index=False
)

print(f"\nComparison results saved to:")
print(output_path)

print("\nModel comparison completed successfully.")