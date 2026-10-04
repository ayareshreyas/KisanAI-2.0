import json
import time
from pathlib import Path

import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    log_loss,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "raw" / "Crop_recommendation.csv"
OUTPUT_PATH = BASE_DIR / "models" / "crop_model_comparison.json"


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]

TARGET = "label"

TEST_SIZE = 0.20
RANDOM_STATE = 42


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

def load_dataset():
    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    print(f"Dataset shape: {df.shape}")
    print(f"Number of classes: {y.nunique()}")

    return X, y


# ---------------------------------------------------------
# Create models
# ---------------------------------------------------------

def create_models():
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=2000,
            random_state=RANDOM_STATE,
        ),

        "Decision Tree": DecisionTreeClassifier(
            random_state=RANDOM_STATE,
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),

        "Gradient Boosting": GradientBoostingClassifier(
            random_state=RANDOM_STATE,
        ),
    }


# ---------------------------------------------------------
# Calculate metrics
# ---------------------------------------------------------

def calculate_metrics(y_true, predictions, probabilities):
    accuracy = accuracy_score(
        y_true,
        predictions,
    )

    macro_precision, macro_recall, macro_f1, _ = (
        precision_recall_fscore_support(
            y_true,
            predictions,
            average="macro",
            zero_division=0,
        )
    )

    weighted_precision, weighted_recall, weighted_f1, _ = (
        precision_recall_fscore_support(
            y_true,
            predictions,
            average="weighted",
            zero_division=0,
        )
    )

    loss = log_loss(
        y_true,
        probabilities,
    )

    return {
        "accuracy": accuracy,
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_precision": weighted_precision,
        "weighted_recall": weighted_recall,
        "weighted_f1": weighted_f1,
        "log_loss": loss,
    }


# ---------------------------------------------------------
# Evaluate one model
# ---------------------------------------------------------

def evaluate_model(
    name,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
):
    print("\n" + "=" * 60)
    print(f"MODEL: {name}")
    print("=" * 60)

    # -----------------------------------------------------
    # Training
    # -----------------------------------------------------

    train_start = time.perf_counter()

    model.fit(
        X_train,
        y_train,
    )

    training_time = time.perf_counter() - train_start

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction_start = time.perf_counter()

    predictions = model.predict(
        X_test,
    )

    prediction_time = time.perf_counter() - prediction_start

    # -----------------------------------------------------
    # Probabilities
    # -----------------------------------------------------

    probabilities = model.predict_proba(
        X_test,
    )

    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    metrics = calculate_metrics(
        y_test,
        predictions,
        probabilities,
    )

    print(f"Accuracy:           {metrics['accuracy']:.4f}")
    print(f"Macro Precision:    {metrics['macro_precision']:.4f}")
    print(f"Macro Recall:       {metrics['macro_recall']:.4f}")
    print(f"Macro F1:           {metrics['macro_f1']:.4f}")
    print(f"Weighted Precision: {metrics['weighted_precision']:.4f}")
    print(f"Weighted Recall:    {metrics['weighted_recall']:.4f}")
    print(f"Weighted F1:        {metrics['weighted_f1']:.4f}")
    print(f"Log Loss:           {metrics['log_loss']:.4f}")
    print(f"Training Time:      {training_time:.4f} seconds")
    print(f"Prediction Time:    {prediction_time:.4f} seconds")

    return {
        "model": name,
        "metrics": metrics,
        "timing": {
            "training_seconds": training_time,
            "prediction_seconds": prediction_time,
        },
    }


# ---------------------------------------------------------
# Print comparison
# ---------------------------------------------------------

def print_comparison(results):
    print("\n")
    print("=" * 90)
    print("MODEL COMPARISON")
    print("=" * 90)

    header = (
        f"{'Model':<22}"
        f"{'Accuracy':>12}"
        f"{'Macro F1':>12}"
        f"{'Weighted F1':>14}"
        f"{'Log Loss':>12}"
    )

    print(header)
    print("-" * 90)

    for result in results:
        metrics = result["metrics"]

        print(
            f"{result['model']:<22}"
            f"{metrics['accuracy']:>12.4f}"
            f"{metrics['macro_f1']:>12.4f}"
            f"{metrics['weighted_f1']:>14.4f}"
            f"{metrics['log_loss']:>12.4f}"
        )


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

def save_results(
    results,
    train_size,
    test_size,
):
    output = {
        "experiment": {
            "name": "Crop Recommendation Model Comparison",
            "dataset": DATA_PATH.name,
            "features": FEATURES,
            "target": TARGET,
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "training_samples": train_size,
            "test_samples": test_size,
        },
        "models": results,
        "notes": [
            "All models were evaluated using the same stratified train/test split.",
            "The experiment is intended as a baseline model comparison.",
            "Results are based on the benchmark dataset and should not be interpreted as real-world field accuracy.",
        ],
    }

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
        )

    print("\n" + "=" * 60)
    print("COMPARISON REPORT SAVED")
    print("=" * 60)

    print(f"File: {OUTPUT_PATH}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    X, y = load_dataset()

    print("\nCreating stratified train/test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples:     {len(X_test)}")

    models = create_models()

    results = []

    for name, model in models.items():
        result = evaluate_model(
            name,
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        results.append(result)

    print_comparison(
        results,
    )

    save_results(
        results,
        len(X_train),
        len(X_test),
    )

    print("\nModel comparison complete.")


if __name__ == "__main__":
    main()