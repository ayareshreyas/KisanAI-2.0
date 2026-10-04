from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "ml-service" / "data" / "raw" / "Crop_recommendation.csv"

CANDIDATE_MODEL_PATH = (
    PROJECT_ROOT
    / "ml-service"
    / "models"
    / "crop_recommendation_random_forest_tuned_candidate.joblib"
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

TUNED_PARAMS = {
    "n_estimators": 200,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 1,
    "max_features": "sqrt",
}


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    return df, X, y


def validate_configuration_reproducibility(X, y):
    """
    Reproduce the valid 80/20 model-selection experiment.

    IMPORTANT:
    This trains the tuned configuration only on the 1,760-row training split
    and evaluates it on the untouched 440-row test split.

    This is the correct place to measure generalization performance.
    """

    print("\n" + "=" * 70)
    print("A. CONFIGURATION REPRODUCIBILITY VALIDATION")
    print("=" * 70)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        stratify=y,
        random_state=RANDOM_STATE,
    )

    print(f"Training samples : {len(X_train)}")
    print(f"Test samples     : {len(X_test)}")

    model = RandomForestClassifier(
        **TUNED_PARAMS,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    print("\nTraining tuned configuration...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )
    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )
    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )
    test_log_loss = log_loss(
        y_test,
        probabilities,
        labels=model.classes_,
    )

    print("\nHeld-out test results:")
    print(f"Accuracy  : {accuracy:.4f}")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"Log Loss  : {test_log_loss:.4f}")

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    error_mask = predictions != y_test.to_numpy()

    error_count = int(error_mask.sum())

    print(f"Misclassified samples : {error_count}")

    if error_count > 0:
        error_indices = X_test.index[error_mask]

        print("\nMisclassified examples:")

        for index in error_indices:
            actual = y.loc[index]
            predicted = predictions[list(X_test.index).index(index)]

            print(
                f"  Dataset index {index}: "
                f"{actual} -> {predicted}"
            )

    # This is the expected result from the earlier valid tuning experiment.
    expected_accuracy = 0.9955
    expected_f1 = 0.9955
    expected_error_count = 2

    accuracy_matches = np.isclose(
        accuracy,
        expected_accuracy,
        atol=0.001,
    )

    f1_matches = np.isclose(
        f1,
        expected_f1,
        atol=0.001,
    )

    errors_match = error_count == expected_error_count

    print("\nReproducibility checks:")
    print(f"Accuracy approximately 0.9955 : {accuracy_matches}")
    print(f"F1 approximately 0.9955       : {f1_matches}")
    print(f"Exactly 2 test errors          : {errors_match}")

    configuration_validation_passed = (
        accuracy_matches
        and f1_matches
        and errors_match
    )

    print(
        "\nConfiguration validation:",
        "PASSED" if configuration_validation_passed else "FAILED",
    )

    return configuration_validation_passed


def validate_candidate_artifact(X):
    """
    Validate the candidate model trained on all 2,200 samples.

    This section intentionally does NOT calculate generalization accuracy.

    The candidate has already seen the complete dataset, so evaluating it on
    rows from that dataset would be data leakage.

    Instead, we verify that the saved artifact:
      - loads successfully
      - has the expected feature count
      - has the expected crop classes
      - contains the tuned hyperparameters
      - produces valid predictions
      - produces valid probability distributions
    """

    print("\n" + "=" * 70)
    print("B. FULL-DATA CANDIDATE ARTIFACT SANITY VALIDATION")
    print("=" * 70)

    print(f"Loading candidate model:\n{CANDIDATE_MODEL_PATH}")

    if not CANDIDATE_MODEL_PATH.exists():
        print("\nCandidate model file does not exist.")
        return False

    model = joblib.load(CANDIDATE_MODEL_PATH)

    print("\nCandidate model loaded successfully.")

    # ------------------------------------------------------------------
    # Basic model structure
    # ------------------------------------------------------------------

    feature_count = model.n_features_in_
    classes = model.classes_
    estimator_count = model.n_estimators

    print("\nModel structure:")
    print(f"Feature count : {feature_count}")
    print(f"Class count   : {len(classes)}")
    print(f"Trees         : {estimator_count}")

    feature_count_valid = feature_count == len(FEATURES)
    class_count_valid = len(classes) == 22
    tree_count_valid = estimator_count == 200

    # ------------------------------------------------------------------
    # Hyperparameter checks
    # ------------------------------------------------------------------

    print("\nHyperparameters:")

    print(f"max_depth         : {model.max_depth}")
    print(f"min_samples_split : {model.min_samples_split}")
    print(f"min_samples_leaf  : {model.min_samples_leaf}")
    print(f"max_features      : {model.max_features}")

    hyperparameters_valid = (
        model.n_estimators == TUNED_PARAMS["n_estimators"]
        and model.max_depth == TUNED_PARAMS["max_depth"]
        and model.min_samples_split == TUNED_PARAMS["min_samples_split"]
        and model.min_samples_leaf == TUNED_PARAMS["min_samples_leaf"]
        and model.max_features == TUNED_PARAMS["max_features"]
    )

    # ------------------------------------------------------------------
    # Class validation
    # ------------------------------------------------------------------

    expected_classes = sorted(
        pd.read_csv(DATA_PATH)[TARGET].unique()
    )

    actual_classes = sorted(classes.tolist())

    classes_valid = actual_classes == expected_classes

    print("\nClass validation:")
    print(f"Expected classes : {len(expected_classes)}")
    print(f"Model classes    : {len(actual_classes)}")
    print(f"Classes match    : {classes_valid}")

    # ------------------------------------------------------------------
    # Prediction sanity check
    # ------------------------------------------------------------------

    sample_input = X.iloc[[0, 100, 500, 1000, 1500, 2000]]

    predictions = model.predict(sample_input)
    probabilities = model.predict_proba(sample_input)

    print("\nPrediction sanity check:")
    print(f"Prediction shape    : {predictions.shape}")
    print(f"Probability shape   : {probabilities.shape}")

    prediction_shape_valid = predictions.shape == (len(sample_input),)

    probability_shape_valid = probabilities.shape == (
        len(sample_input),
        len(classes),
    )

    probabilities_sum = probabilities.sum(axis=1)

    probabilities_valid = (
        np.all(probabilities >= 0)
        and np.all(probabilities <= 1)
        and np.allclose(probabilities_sum, 1.0)
    )

    print(f"Probability values valid : {probabilities_valid}")

    # ------------------------------------------------------------------
    # Final artifact result
    # ------------------------------------------------------------------

    artifact_validation_passed = all(
        [
            feature_count_valid,
            class_count_valid,
            tree_count_valid,
            hyperparameters_valid,
            classes_valid,
            prediction_shape_valid,
            probability_shape_valid,
            probabilities_valid,
        ]
    )

    print("\nArtifact validation checks:")
    print(f"Feature count valid      : {feature_count_valid}")
    print(f"Class count valid        : {class_count_valid}")
    print(f"Tree count valid         : {tree_count_valid}")
    print(f"Hyperparameters valid    : {hyperparameters_valid}")
    print(f"Classes valid            : {classes_valid}")
    print(f"Prediction shape valid   : {prediction_shape_valid}")
    print(f"Probability shape valid  : {probability_shape_valid}")
    print(f"Probabilities valid      : {probabilities_valid}")

    print(
        "\nCandidate artifact validation:",
        "PASSED" if artifact_validation_passed else "FAILED",
    )

    return artifact_validation_passed


def main():
    print("=" * 70)
    print("KISANAI FINAL CROP MODEL VALIDATION")
    print("=" * 70)

    print("\nDataset:")
    print(DATA_PATH)

    print("\nCandidate model:")
    print(CANDIDATE_MODEL_PATH)

    df, X, y = load_dataset()

    print(f"\nDataset samples : {len(df)}")
    print(f"Features        : {len(FEATURES)}")
    print(f"Crop classes    : {y.nunique()}")

    configuration_passed = validate_configuration_reproducibility(X, y)

    artifact_passed = validate_candidate_artifact(X)

    print("\n" + "=" * 70)
    print("FINAL VALIDATION SUMMARY")
    print("=" * 70)

    print(
        f"Configuration reproducibility : "
        f"{'PASSED' if configuration_passed else 'FAILED'}"
    )

    print(
        f"Candidate artifact sanity     : "
        f"{'PASSED' if artifact_passed else 'FAILED'}"
    )

    overall_passed = configuration_passed and artifact_passed

    print(
        f"\nOVERALL RESULT                : "
        f"{'PASSED' if overall_passed else 'FAILED'}"
    )

    if overall_passed:
        print(
            "\nThe tuned configuration reproduces the valid held-out "
            "evaluation, and the full-data candidate artifact passes "
            "structural and prediction sanity checks."
        )
        print(
            "\nThe candidate model is ready for the next step: "
            "controlled promotion to production."
        )
    else:
        print(
            "\nDo not promote the candidate model yet."
        )


if __name__ == "__main__":
    main()