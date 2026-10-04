"""
Compare errors made by the baseline and tuned Random Forest models.

This experiment uses the exact same 80/20 stratified split used during
hyperparameter tuning.

It does NOT modify the production model.
"""

from pathlib import Path

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "ml-service"
    / "data"
    / "raw"
    / "Crop_recommendation.csv"
)

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

RANDOM_STATE = 42


# Best configuration discovered during tuning.
TUNED_PARAMETERS = {
    "n_estimators": 200,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 1,
    "max_features": "sqrt",
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


def main():
    X, y = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print("\n" + "=" * 70)
    print("BASELINE VS TUNED RANDOM FOREST ERROR ANALYSIS")
    print("=" * 70)

    print(f"\nTraining samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")

    # ---------------------------------------------------------
    # BASELINE MODEL
    # ---------------------------------------------------------

    baseline = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    baseline.fit(X_train, y_train)

    baseline_predictions = baseline.predict(X_test)

    baseline_accuracy = accuracy_score(
        y_test,
        baseline_predictions,
    )

    # ---------------------------------------------------------
    # TUNED MODEL
    # ---------------------------------------------------------

    tuned = RandomForestClassifier(
        **TUNED_PARAMETERS
    )

    tuned.fit(X_train, y_train)

    tuned_predictions = tuned.predict(X_test)

    tuned_accuracy = accuracy_score(
        y_test,
        tuned_predictions,
    )

    print("\n" + "-" * 70)
    print("OVERALL PERFORMANCE")
    print("-" * 70)

    print(
        f"Baseline accuracy : {baseline_accuracy:.4f}"
    )

    print(
        f"Tuned accuracy    : {tuned_accuracy:.4f}"
    )

    print(
        f"Difference        : "
        f"{tuned_accuracy - baseline_accuracy:+.4f}"
    )

    # ---------------------------------------------------------
    # ERROR ANALYSIS
    # ---------------------------------------------------------

    comparison = X_test.copy()

    comparison["actual"] = y_test.values
    comparison["baseline_prediction"] = baseline_predictions
    comparison["tuned_prediction"] = tuned_predictions

    comparison["baseline_correct"] = (
        comparison["actual"]
        == comparison["baseline_prediction"]
    )

    comparison["tuned_correct"] = (
        comparison["actual"]
        == comparison["tuned_prediction"]
    )

    baseline_errors = comparison[
        ~comparison["baseline_correct"]
    ]

    tuned_errors = comparison[
        ~comparison["tuned_correct"]
    ]

    fixed_errors = comparison[
        (~comparison["baseline_correct"])
        & (comparison["tuned_correct"])
    ]

    new_errors = comparison[
        (comparison["baseline_correct"])
        & (~comparison["tuned_correct"])
    ]

    unchanged_errors = comparison[
        (~comparison["baseline_correct"])
        & (~comparison["tuned_correct"])
    ]

    print("\n" + "-" * 70)
    print("ERROR COUNTS")
    print("-" * 70)

    print(
        f"Baseline errors        : {len(baseline_errors)}"
    )

    print(
        f"Tuned errors           : {len(tuned_errors)}"
    )

    print(
        f"Errors fixed by tuning : {len(fixed_errors)}"
    )

    print(
        f"New errors introduced  : {len(new_errors)}"
    )

    print(
        f"Errors remaining       : {len(unchanged_errors)}"
    )

    # ---------------------------------------------------------
    # BASELINE ERRORS
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("BASELINE MODEL ERRORS")
    print("-" * 70)

    if len(baseline_errors) == 0:
        print("No baseline errors.")
    else:
        print(
            baseline_errors[
                FEATURE_COLUMNS
                + [
                    "actual",
                    "baseline_prediction",
                    "tuned_prediction",
                ]
            ].to_string()
        )

    # ---------------------------------------------------------
    # FIXED ERRORS
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("ERRORS FIXED BY TUNING")
    print("-" * 70)

    if len(fixed_errors) == 0:
        print("No baseline errors were fixed.")
    else:
        print(
            fixed_errors[
                FEATURE_COLUMNS
                + [
                    "actual",
                    "baseline_prediction",
                    "tuned_prediction",
                ]
            ].to_string()
        )

    # ---------------------------------------------------------
    # NEW ERRORS
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("NEW ERRORS INTRODUCED BY TUNING")
    print("-" * 70)

    if len(new_errors) == 0:
        print("No new errors were introduced.")
    else:
        print(
            new_errors[
                FEATURE_COLUMNS
                + [
                    "actual",
                    "baseline_prediction",
                    "tuned_prediction",
                ]
            ].to_string()
        )

    # ---------------------------------------------------------
    # REMAINING ERRORS
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("ERRORS REMAINING AFTER TUNING")
    print("-" * 70)

    if len(unchanged_errors) == 0:
        print("No errors remain.")
    else:
        print(
            unchanged_errors[
                FEATURE_COLUMNS
                + [
                    "actual",
                    "baseline_prediction",
                    "tuned_prediction",
                ]
            ].to_string()
        )

    # ---------------------------------------------------------
    # FINAL SUMMARY
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("ERROR ANALYSIS COMPLETE")
    print("=" * 70)

    print("\nTuned parameters:")

    for parameter, value in TUNED_PARAMETERS.items():
        print(f"  {parameter}: {value}")

    print("\nProduction model has NOT been changed.")


if __name__ == "__main__":
    main()