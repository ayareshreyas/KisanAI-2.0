"""
Random Forest hyperparameter tuning experiment for KisanAI crop recommendation.

Important:
- This script does NOT replace the production model.
- It uses cross-validation to investigate whether a different
  Random Forest configuration improves the current baseline.
- Final production-model selection happens separately after reviewing
  the results.
"""

from pathlib import Path
import json
import time

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "ml-service"
    / "data"
    / "raw"
    / "Crop_recommendation.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "ml-service"
    / "data"
    / "processed"
)

RESULTS_CSV = OUTPUT_DIR / "random_forest_tuning_results.csv"
RESULTS_JSON = OUTPUT_DIR / "random_forest_tuning_summary.json"


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


def load_dataset():
    """Load and validate the crop recommendation dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    missing_columns = [
        column
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if df[FEATURE_COLUMNS + [TARGET_COLUMN]].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return X, y


def build_parameter_grid():
    """
    Controlled parameter grid.

    The goal is to test meaningful Random Forest changes without
    creating an unnecessarily huge experiment.
    """

    return {
        "n_estimators": [200, 300, 500],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "max_features": ["sqrt", "log2"],
    }


def run_grid_search(X_train, y_train):
    """Run stratified cross-validation over the parameter grid."""

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    baseline = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    parameter_grid = build_parameter_grid()

    total_combinations = 1

    for values in parameter_grid.values():
        total_combinations *= len(values)

    total_fits = total_combinations * cv.get_n_splits()

    print("\n" + "=" * 70)
    print("RANDOM FOREST HYPERPARAMETER TUNING")
    print("=" * 70)

    print(f"\nParameter combinations : {total_combinations}")
    print(f"CV folds              : {cv.get_n_splits()}")
    print(f"Total model fits      : {total_fits}")

    print("\nParameter grid:")

    for parameter, values in parameter_grid.items():
        print(f"  {parameter}: {values}")

    print("\nScoring metric: accuracy")
    print("Search strategy: GridSearchCV")
    print("Parallel jobs: all available CPU cores")

    start_time = time.time()

    search = GridSearchCV(
        estimator=baseline,
        param_grid=parameter_grid,
        scoring="accuracy",
        cv=cv,
        n_jobs=-1,
        verbose=1,
        return_train_score=True,
    )

    search.fit(X_train, y_train)

    elapsed = time.time() - start_time

    print(f"\nTuning completed in {elapsed:.2f} seconds.")

    return search, elapsed


def evaluate_model(model, X_test, y_test):
    """Evaluate a fitted model on the untouched hold-out test set."""

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "precision_weighted": precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        ),
        "recall_weighted": recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        ),
        "f1_weighted": f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        ),
        "log_loss": log_loss(
            y_test,
            probabilities,
            labels=model.classes_,
        ),
    }


def evaluate_baseline(X_train, X_test, y_train, y_test):
    """Train and evaluate the current production-style baseline."""

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    return model, evaluate_model(model, X_test, y_test)


def save_results(search, baseline_metrics, tuned_metrics, elapsed):
    """Save detailed CV results and experiment summary."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = pd.DataFrame(search.cv_results_)

    results = results.sort_values(
        by="rank_test_score"
    )

    results.to_csv(
        RESULTS_CSV,
        index=False,
    )

    summary = {
        "experiment": "Random Forest hyperparameter tuning",
        "random_state": RANDOM_STATE,
        "dataset": {
            "path": str(DATA_PATH),
            "samples": int(search.n_splits_ if False else 0),
        },
        "cross_validation": {
            "folds": 5,
            "scoring": "accuracy",
            "search_strategy": "GridSearchCV",
        },
        "baseline": {
            "parameters": {
                "n_estimators": 300,
                "random_state": RANDOM_STATE,
                "n_jobs": -1,
            },
            "holdout_metrics": baseline_metrics,
        },
        "best_cv_result": {
            "cv_accuracy_mean": float(search.best_score_),
            "best_parameters": search.best_params_,
        },
        "tuned_holdout_metrics": tuned_metrics,
        "tuning_time_seconds": elapsed,
        "production_model_replaced": False,
    }

    with open(RESULTS_JSON, "w", encoding="utf-8") as file:
        json.dump(
            summary,
            file,
            indent=4,
        )

    return results


def main():
    X, y = load_dataset()

    print(f"\nDataset samples : {len(X)}")
    print(f"Features        : {len(FEATURE_COLUMNS)}")
    print(f"Crop classes    : {y.nunique()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples : {len(X_test)}")

    print("\n" + "-" * 70)
    print("STEP 1 — CURRENT RANDOM FOREST BASELINE")
    print("-" * 70)

    baseline_model, baseline_metrics = evaluate_baseline(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    print(
        f"Accuracy : {baseline_metrics['accuracy']:.4f}"
    )
    print(
        f"Precision: {baseline_metrics['precision_weighted']:.4f}"
    )
    print(
        f"Recall   : {baseline_metrics['recall_weighted']:.4f}"
    )
    print(
        f"F1 Score : {baseline_metrics['f1_weighted']:.4f}"
    )
    print(
        f"Log Loss : {baseline_metrics['log_loss']:.4f}"
    )

    print("\n" + "-" * 70)
    print("STEP 2 — HYPERPARAMETER SEARCH")
    print("-" * 70)

    search, elapsed = run_grid_search(
        X_train,
        y_train,
    )

    print("\n" + "-" * 70)
    print("BEST CROSS-VALIDATION RESULT")
    print("-" * 70)

    print(
        f"CV Accuracy: {search.best_score_:.4f}"
    )

    print("\nBest parameters:")

    for parameter, value in search.best_params_.items():
        print(f"  {parameter}: {value}")

    print("\n" + "-" * 70)
    print("STEP 3 — TUNED MODEL ON UNTOUCHED TEST SET")
    print("-" * 70)

    tuned_model = search.best_estimator_

    tuned_metrics = evaluate_model(
        tuned_model,
        X_test,
        y_test,
    )

    print(
        f"Accuracy : {tuned_metrics['accuracy']:.4f}"
    )
    print(
        f"Precision: {tuned_metrics['precision_weighted']:.4f}"
    )
    print(
        f"Recall   : {tuned_metrics['recall_weighted']:.4f}"
    )
    print(
        f"F1 Score : {tuned_metrics['f1_weighted']:.4f}"
    )
    print(
        f"Log Loss : {tuned_metrics['log_loss']:.4f}"
    )

    print("\n" + "-" * 70)
    print("STEP 4 — BASELINE VS TUNED")
    print("-" * 70)

    accuracy_difference = (
        tuned_metrics["accuracy"]
        - baseline_metrics["accuracy"]
    )

    f1_difference = (
        tuned_metrics["f1_weighted"]
        - baseline_metrics["f1_weighted"]
    )

    log_loss_difference = (
        tuned_metrics["log_loss"]
        - baseline_metrics["log_loss"]
    )

    print(
        f"Accuracy difference : {accuracy_difference:+.4f}"
    )
    print(
        f"F1 difference       : {f1_difference:+.4f}"
    )
    print(
        f"Log Loss difference  : {log_loss_difference:+.4f}"
    )

    results = save_results(
        search,
        baseline_metrics,
        tuned_metrics,
        elapsed,
    )

    print("\n" + "-" * 70)
    print("TOP 10 CONFIGURATIONS")
    print("-" * 70)

    display_columns = [
        "rank_test_score",
        "mean_test_score",
        "std_test_score",
        "mean_train_score",
        "param_n_estimators",
        "param_max_depth",
        "param_min_samples_split",
        "param_min_samples_leaf",
        "param_max_features",
    ]

    print(
        results[display_columns]
        .head(10)
        .to_string(index=False)
    )

    print("\n" + "=" * 70)
    print("TUNING EXPERIMENT COMPLETE")
    print("=" * 70)

    print("\nResults saved to:")
    print(RESULTS_CSV)

    print(RESULTS_JSON)

    print(
        "\nIMPORTANT: The production model has NOT been replaced."
    )


if __name__ == "__main__":
    main()