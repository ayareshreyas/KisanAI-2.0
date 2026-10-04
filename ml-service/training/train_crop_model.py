import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    log_loss,
    brier_score_loss,
)
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Crop_recommendation.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "crop_recommendation_calibrated.joblib"
METADATA_PATH = MODEL_DIR / "crop_model_calibration_metadata.json"


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


def calculate_multiclass_brier_score(y_true, probabilities, classes):
    """
    Calculate the multiclass Brier score.

    For each sample, the squared difference is calculated between:
    - the actual one-hot encoded class
    - the predicted probability for each class
    """

    class_to_index = {
        class_name: index
        for index, class_name in enumerate(classes)
    }

    total = 0.0

    for actual_label, probability_row in zip(y_true, probabilities):
        actual_index = class_to_index[actual_label]

        for index, probability in enumerate(probability_row):
            actual_value = 1.0 if index == actual_index else 0.0
            total += (probability - actual_value) ** 2

    return total / len(y_true)


def main():
    print("Loading crop recommendation dataset...")

    dataset = pd.read_csv(DATA_PATH)

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in dataset.columns
    ]

    if TARGET not in dataset.columns:
        raise ValueError(
            f"Target column '{TARGET}' was not found in the dataset."
        )

    if missing_features:
        raise ValueError(
            f"Missing feature columns: {missing_features}"
        )

    X = dataset[FEATURES]
    y = dataset[TARGET]

    print(f"Dataset shape: {dataset.shape}")
    print(f"Number of classes: {y.nunique()}")
    print(f"Classes: {sorted(y.unique())}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print()
    print("Train/test split:")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # ------------------------------------------------------------------
    # Base Random Forest
    # ------------------------------------------------------------------

    print()
    print("Training Random Forest...")

    random_forest = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )

    random_forest.fit(X_train, y_train)

    base_predictions = random_forest.predict(X_test)
    base_probabilities = random_forest.predict_proba(X_test)

    base_accuracy = accuracy_score(
        y_test,
        base_predictions,
    )

    base_log_loss = log_loss(
        y_test,
        base_probabilities,
        labels=random_forest.classes_,
    )

    base_brier_score = calculate_multiclass_brier_score(
        y_test,
        base_probabilities,
        random_forest.classes_,
    )

    print()
    print("Base Random Forest:")
    print(f"Accuracy: {base_accuracy:.4f}")
    print(f"Log loss: {base_log_loss:.4f}")
    print(f"Brier score: {base_brier_score:.4f}")

    # ------------------------------------------------------------------
    # Probability calibration
    # ------------------------------------------------------------------

    print()
    print("Calibrating Random Forest probabilities...")

    calibrated_model = CalibratedClassifierCV(
        estimator=random_forest,
        method="sigmoid",
        cv=5,
        n_jobs=-1,
    )

    calibrated_model.fit(
        X_train,
        y_train,
    )

    calibrated_predictions = calibrated_model.predict(X_test)
    calibrated_probabilities = calibrated_model.predict_proba(X_test)

    calibrated_accuracy = accuracy_score(
        y_test,
        calibrated_predictions,
    )

    calibrated_log_loss = log_loss(
        y_test,
        calibrated_probabilities,
        labels=calibrated_model.classes_,
    )

    calibrated_brier_score = calculate_multiclass_brier_score(
        y_test,
        calibrated_probabilities,
        calibrated_model.classes_,
    )

    print()
    print("Calibrated Random Forest:")
    print(f"Accuracy: {calibrated_accuracy:.4f}")
    print(f"Log loss: {calibrated_log_loss:.4f}")
    print(f"Brier score: {calibrated_brier_score:.4f}")

    # ------------------------------------------------------------------
    # Classification report
    # ------------------------------------------------------------------

    report = classification_report(
        y_test,
        calibrated_predictions,
        output_dict=True,
    )

    # ------------------------------------------------------------------
    # Save calibrated model
    # ------------------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        calibrated_model,
        MODEL_PATH,
    )

    # ------------------------------------------------------------------
    # Save metadata
    # ------------------------------------------------------------------

    metadata = {
        "model_type": "RandomForestClassifier",
        "calibration": {
            "enabled": True,
            "method": "sigmoid",
            "cross_validation_folds": 5,
        },
        "features": FEATURES,
        "target": TARGET,
        "dataset": {
            "total_samples": int(len(dataset)),
            "training_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "number_of_classes": int(y.nunique()),
        },
        "random_state": 42,
        "metrics": {
            "base_random_forest": {
                "accuracy": float(base_accuracy),
                "log_loss": float(base_log_loss),
                "brier_score": float(base_brier_score),
            },
            "calibrated_random_forest": {
                "accuracy": float(calibrated_accuracy),
                "log_loss": float(calibrated_log_loss),
                "brier_score": float(calibrated_brier_score),
            },
        },
        "classification_report": report,
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )

    print()
    print("Model saved:")
    print(MODEL_PATH)

    print()
    print("Metadata saved:")
    print(METADATA_PATH)

    print()
    print("Calibration training completed successfully.")


if __name__ == "__main__":
    main()