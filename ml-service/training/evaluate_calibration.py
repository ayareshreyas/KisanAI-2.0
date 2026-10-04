import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    log_loss,
    brier_score_loss,
)
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "raw" / "Crop_recommendation.csv"

BASE_MODEL_PATH = (
    BASE_DIR
    / "models"
    / "crop_recommendation_random_forest.joblib"
)

CALIBRATED_MODEL_PATH = (
    BASE_DIR
    / "models"
    / "crop_recommendation_calibrated.joblib"
)

OUTPUT_PATH = (
    BASE_DIR
    / "models"
    / "crop_model_calibration_evaluation.json"
)


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

RANDOM_STATE = 42
TEST_SIZE = 0.20

NUMBER_OF_BINS = 10


def calculate_multiclass_brier_score(
    y_true,
    probabilities,
    classes,
):
    """
    Calculate the multiclass Brier score.
    """

    class_to_index = {
        class_name: index
        for index, class_name in enumerate(classes)
    }

    total = 0.0

    for actual_label, probability_row in zip(
        y_true,
        probabilities,
    ):
        actual_index = class_to_index[actual_label]

        for index, probability in enumerate(probability_row):
            actual_value = (
                1.0
                if index == actual_index
                else 0.0
            )

            total += (
                probability - actual_value
            ) ** 2

    return total / len(y_true)


def calculate_confidence_calibration(
    y_true,
    predictions,
    probabilities,
    number_of_bins=10,
):
    """
    Evaluate calibration of the maximum predicted class probability.

    This matches the confidence value KisanAI currently displays:

        confidence = maximum class probability
    """

    correct = (
        predictions == y_true
    )

    confidence = probabilities.max(axis=1)

    bin_edges = [
        index / number_of_bins
        for index in range(number_of_bins + 1)
    ]

    bins = []

    total_samples = len(y_true)

    expected_calibration_error = 0.0
    maximum_calibration_error = 0.0

    for index in range(number_of_bins):
        lower = bin_edges[index]
        upper = bin_edges[index + 1]

        if index == number_of_bins - 1:
            mask = (
                (confidence >= lower)
                & (confidence <= upper)
            )
        else:
            mask = (
                (confidence >= lower)
                & (confidence < upper)
            )

        sample_count = int(mask.sum())

        if sample_count == 0:
            continue

        bin_confidence = float(
            confidence[mask].mean()
        )

        bin_accuracy = float(
            correct[mask].mean()
        )

        calibration_error = abs(
            bin_confidence - bin_accuracy
        )

        bin_weight = (
            sample_count / total_samples
        )

        expected_calibration_error += (
            bin_weight * calibration_error
        )

        maximum_calibration_error = max(
            maximum_calibration_error,
            calibration_error,
        )

        bins.append(
            {
                "range": (
                    f"{lower:.1f}-{upper:.1f}"
                ),
                "samples": sample_count,
                "mean_confidence": round(
                    bin_confidence,
                    6,
                ),
                "accuracy": round(
                    bin_accuracy,
                    6,
                ),
                "absolute_error": round(
                    calibration_error,
                    6,
                ),
            }
        )

    return {
        "expected_calibration_error": (
            float(expected_calibration_error)
        ),
        "maximum_calibration_error": (
            float(maximum_calibration_error)
        ),
        "mean_confidence": float(
            confidence.mean()
        ),
        "overall_accuracy": float(
            correct.mean()
        ),
        "bins": bins,
    }


def evaluate_model(
    name,
    model,
    X_test,
    y_test,
):
    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)

    classes = model.classes_

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    log_loss_value = log_loss(
        y_test,
        probabilities,
        labels=classes,
    )

    brier_score = calculate_multiclass_brier_score(
        y_test,
        probabilities,
        classes,
    )

    calibration = calculate_confidence_calibration(
        y_test.to_numpy(),
        predictions,
        probabilities,
        NUMBER_OF_BINS,
    )

    return {
        "name": name,
        "accuracy": float(accuracy),
        "log_loss": float(log_loss_value),
        "brier_score": float(brier_score),
        "confidence_calibration": calibration,
    }


def print_results(result):
    print()
    print("=" * 60)
    print(result["name"])
    print("=" * 60)

    print(
        f"Accuracy: "
        f"{result['accuracy']:.4f}"
    )

    print(
        f"Log loss: "
        f"{result['log_loss']:.4f}"
    )

    print(
        f"Brier score: "
        f"{result['brier_score']:.4f}"
    )

    calibration = (
        result["confidence_calibration"]
    )

    print(
        f"Mean confidence: "
        f"{calibration['mean_confidence']:.4f}"
    )

    print(
        f"Actual accuracy: "
        f"{calibration['overall_accuracy']:.4f}"
    )

    print(
        f"Expected Calibration Error: "
        f"{calibration['expected_calibration_error']:.4f}"
    )

    print(
        f"Maximum Calibration Error: "
        f"{calibration['maximum_calibration_error']:.4f}"
    )

    print()
    print("Confidence bins:")

    print(
        f"{'Range':<12}"
        f"{'Samples':>10}"
        f"{'Confidence':>15}"
        f"{'Accuracy':>12}"
        f"{'Error':>12}"
    )

    for bin_data in calibration["bins"]:
        print(
            f"{bin_data['range']:<12}"
            f"{bin_data['samples']:>10}"
            f"{bin_data['mean_confidence']:>15.4f}"
            f"{bin_data['accuracy']:>12.4f}"
            f"{bin_data['absolute_error']:>12.4f}"
        )


def main():
    print("Loading dataset...")

    dataset = pd.read_csv(DATA_PATH)

    X = dataset[FEATURES]
    y = dataset[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(
        f"Training samples: {len(X_train)}"
    )

    print(
        f"Test samples: {len(X_test)}"
    )

    print()
    print("Loading models...")

    base_model = joblib.load(
        BASE_MODEL_PATH
    )

    calibrated_model = joblib.load(
        CALIBRATED_MODEL_PATH
    )

    print(
        "Base model loaded:"
        f" {BASE_MODEL_PATH.name}"
    )

    print(
        "Calibrated model loaded:"
        f" {CALIBRATED_MODEL_PATH.name}"
    )

    base_result = evaluate_model(
        "Base Random Forest",
        base_model,
        X_test,
        y_test,
    )

    calibrated_result = evaluate_model(
        "Calibrated Random Forest",
        calibrated_model,
        X_test,
        y_test,
    )

    print_results(base_result)
    print_results(calibrated_result)

    ece_difference = (
        calibrated_result[
            "confidence_calibration"
        ]["expected_calibration_error"]
        -
        base_result[
            "confidence_calibration"
        ]["expected_calibration_error"]
    )

    print()
    print("=" * 60)
    print("Calibration comparison")
    print("=" * 60)

    print(
        f"ECE difference "
        f"(calibrated - base): "
        f"{ece_difference:+.4f}"
    )

    if ece_difference < 0:
        print(
            "The calibrated model has lower "
            "confidence calibration error."
        )
    elif ece_difference > 0:
        print(
            "The calibrated model has higher "
            "confidence calibration error."
        )
    else:
        print(
            "Both models have the same "
            "confidence calibration error."
        )

    output = {
        "dataset": {
            "total_samples": int(len(dataset)),
            "training_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "number_of_classes": int(
                y.nunique()
            ),
        },
        "evaluation": {
            "number_of_bins": NUMBER_OF_BINS,
            "base_random_forest": base_result,
            "calibrated_random_forest": calibrated_result,
        },
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

    print()
    print(
        "Evaluation saved:"
    )
    print(OUTPUT_PATH)

    print()
    print(
        "Calibration evaluation "
        "completed successfully."
    )


if __name__ == "__main__":
    main()