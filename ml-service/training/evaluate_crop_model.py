import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "raw" / "Crop_recommendation.csv"
MODEL_PATH = BASE_DIR / "models" / "crop_recommendation_random_forest.joblib"
OUTPUT_PATH = BASE_DIR / "models" / "crop_model_detailed_evaluation.json"


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


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

def load_dataset():
    print("Loading dataset...")

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset shape: {df.shape}")
    print(f"Number of classes: {df[TARGET].nunique()}")

    return df


# ---------------------------------------------------------
# Load model
# ---------------------------------------------------------

def load_model():
    print("\nLoading trained Random Forest model...")

    model = joblib.load(MODEL_PATH)

    print(f"Model loaded from: {MODEL_PATH}")

    return model


# ---------------------------------------------------------
# Evaluate model
# ---------------------------------------------------------

def evaluate_model(model, df):
    X = df[FEATURES]
    y = df[TARGET]

    print("\nGenerating predictions...")

    predictions = model.predict(X)

    # -----------------------------------------------------
    # Overall metrics
    # -----------------------------------------------------

    accuracy = accuracy_score(y, predictions)

    macro_precision, macro_recall, macro_f1, _ = (
        precision_recall_fscore_support(
            y,
            predictions,
            average="macro",
            zero_division=0,
        )
    )

    weighted_precision, weighted_recall, weighted_f1, _ = (
        precision_recall_fscore_support(
            y,
            predictions,
            average="weighted",
            zero_division=0,
        )
    )

    print("\n" + "=" * 60)
    print("OVERALL MODEL PERFORMANCE")
    print("=" * 60)

    print(f"Accuracy:           {accuracy:.4f}")
    print(f"Macro Precision:    {macro_precision:.4f}")
    print(f"Macro Recall:       {macro_recall:.4f}")
    print(f"Macro F1:           {macro_f1:.4f}")
    print(f"Weighted Precision: {weighted_precision:.4f}")
    print(f"Weighted Recall:    {weighted_recall:.4f}")
    print(f"Weighted F1:        {weighted_f1:.4f}")

    # -----------------------------------------------------
    # Per-class metrics
    # -----------------------------------------------------

    report = classification_report(
        y,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    class_names = sorted(y.unique())

    per_class_metrics = {}

    print("\n" + "=" * 60)
    print("PER-CROP PERFORMANCE")
    print("=" * 60)

    print(
        f"{'Crop':<20}"
        f"{'Precision':>12}"
        f"{'Recall':>12}"
        f"{'F1':>12}"
        f"{'Support':>10}"
    )

    print("-" * 66)

    for crop in class_names:
        metrics = report[crop]

        per_class_metrics[crop] = {
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1_score": metrics["f1-score"],
            "support": int(metrics["support"]),
        }

        print(
            f"{crop:<20}"
            f"{metrics['precision']:>12.4f}"
            f"{metrics['recall']:>12.4f}"
            f"{metrics['f1-score']:>12.4f}"
            f"{int(metrics['support']):>10}"
        )

    # -----------------------------------------------------
    # Confusion matrix
    # -----------------------------------------------------

    matrix = confusion_matrix(
        y,
        predictions,
        labels=class_names,
    )

    confusion_matrix_data = {
        "labels": class_names,
        "matrix": matrix.tolist(),
    }

    # -----------------------------------------------------
    # Misclassified samples
    # -----------------------------------------------------

    misclassified_indices = y.index[y != predictions]

    misclassified_samples = []

    for index in misclassified_indices:
        row = df.loc[index]

        misclassified_samples.append(
            {
                "index": int(index),
                "actual": str(y.loc[index]),
                "predicted": str(predictions[list(df.index).index(index)]),
                "features": {
                    feature: float(row[feature])
                    for feature in FEATURES
                },
            }
        )

    print("\n" + "=" * 60)
    print("MISCLASSIFIED SAMPLES")
    print("=" * 60)

    if not misclassified_samples:
        print("No misclassified samples found.")

    else:
        print(
            f"Total misclassified samples: "
            f"{len(misclassified_samples)}"
        )

        for sample in misclassified_samples:
            print(
                f"\nIndex: {sample['index']}"
                f"\nActual: {sample['actual']}"
                f"\nPredicted: {sample['predicted']}"
                f"\nFeatures: {sample['features']}"
            )

    # -----------------------------------------------------
    # Error summary by actual/predicted pair
    # -----------------------------------------------------

    error_summary = {}

    for sample in misclassified_samples:
        actual = sample["actual"]
        predicted = sample["predicted"]

        key = f"{actual} -> {predicted}"

        error_summary[key] = error_summary.get(key, 0) + 1

    print("\n" + "=" * 60)
    print("ERROR SUMMARY")
    print("=" * 60)

    if not error_summary:
        print("No classification errors.")

    else:
        for error, count in sorted(
            error_summary.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            print(f"{error}: {count}")

    # -----------------------------------------------------
    # Final evaluation object
    # -----------------------------------------------------

    evaluation = {
        "model": {
            "type": "Random Forest Classifier",
            "model_file": MODEL_PATH.name,
        },
        "dataset": {
            "file": DATA_PATH.name,
            "samples": int(len(df)),
            "features": FEATURES,
            "classes": class_names,
            "number_of_classes": len(class_names),
        },
        "overall_metrics": {
            "accuracy": accuracy,
            "macro_precision": macro_precision,
            "macro_recall": macro_recall,
            "macro_f1": macro_f1,
            "weighted_precision": weighted_precision,
            "weighted_recall": weighted_recall,
            "weighted_f1": weighted_f1,
        },
        "per_class_metrics": per_class_metrics,
        "confusion_matrix": confusion_matrix_data,
        "misclassified_samples": misclassified_samples,
        "error_summary": error_summary,
        "notes": [
            "Evaluation is performed on the full benchmark dataset.",
            "These metrics should not be interpreted as real-world field accuracy.",
            "The dataset distribution may not represent all agricultural regions or growing conditions.",
        ],
    }

    return evaluation


# ---------------------------------------------------------
# Save evaluation
# ---------------------------------------------------------

def save_evaluation(evaluation):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            evaluation,
            file,
            indent=2,
        )

    print("\n" + "=" * 60)
    print("EVALUATION REPORT SAVED")
    print("=" * 60)

    print(f"File: {OUTPUT_PATH}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    df = load_dataset()

    model = load_model()

    evaluation = evaluate_model(
        model,
        df,
    )

    save_evaluation(evaluation)

    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()