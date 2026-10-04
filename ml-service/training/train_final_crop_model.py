"""
Train the final KisanAI crop recommendation Random Forest model.

The hyperparameters were selected through the documented
Random Forest tuning experiment.

Important:
- This script trains on the complete dataset.
- It does NOT overwrite the existing production model.
- The new model is saved as a separate artifact first.
- Final replacement happens only after final validation.
"""

from pathlib import Path
import json
import shutil
from datetime import datetime

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "ml-service"
    / "data"
    / "raw"
    / "Crop_recommendation.csv"
)

MODEL_DIR = (
    PROJECT_ROOT
    / "ml-service"
    / "models"
)

PRODUCTION_MODEL_PATH = (
    MODEL_DIR
    / "crop_recommendation_random_forest.joblib"
)

CANDIDATE_MODEL_PATH = (
    MODEL_DIR
    / "crop_recommendation_random_forest_tuned_candidate.joblib"
)

CANDIDATE_METADATA_PATH = (
    MODEL_DIR
    / "crop_model_tuned_candidate_metadata.json"
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


# Hyperparameters selected from the tuning experiment.
FINAL_PARAMETERS = {
    "n_estimators": 200,
    "max_depth": None,
    "min_samples_split": 5,
    "min_samples_leaf": 1,
    "max_features": "sqrt",
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
}


def load_dataset():
    """Load and validate the complete training dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at:\n{DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Dataset contains missing values."
        )

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    return df, X, y


def train_model(X, y):
    """Train the tuned Random Forest on the complete dataset."""

    model = RandomForestClassifier(
        **FINAL_PARAMETERS
    )

    model.fit(X, y)

    return model


def create_metadata(df, X, y):
    """Create reproducibility metadata for the candidate model."""

    class_distribution = (
        y.value_counts()
        .sort_index()
        .to_dict()
    )

    feature_ranges = {}

    for feature in FEATURE_COLUMNS:
        feature_ranges[feature] = {
            "minimum": float(X[feature].min()),
            "maximum": float(X[feature].max()),
        }

    return {
        "model_name": "KisanAI Crop Recommendation Random Forest",
        "model_type": "RandomForestClassifier",
        "model_status": "tuned_candidate",
        "training_timestamp": datetime.now().isoformat(),

        "dataset": {
            "path": str(DATA_PATH),
            "samples": int(len(df)),
            "features": int(len(FEATURE_COLUMNS)),
            "classes": int(y.nunique()),
            "target_column": TARGET_COLUMN,
            "feature_columns": FEATURE_COLUMNS,
            "class_distribution": {
                str(key): int(value)
                for key, value in class_distribution.items()
            },
        },

        "feature_ranges": feature_ranges,

        "hyperparameters": {
            "n_estimators": 200,
            "max_depth": None,
            "min_samples_split": 5,
            "min_samples_leaf": 1,
            "max_features": "sqrt",
            "random_state": RANDOM_STATE,
            "n_jobs": -1,
        },

        "selection_evidence": {
            "selection_method": "GridSearchCV",
            "cv_folds": 5,
            "best_cv_accuracy": 0.996023,
            "held_out_accuracy": 0.9955,
            "held_out_precision_weighted": 0.9957,
            "held_out_recall_weighted": 0.9955,
            "held_out_f1_weighted": 0.9955,
            "held_out_log_loss": 0.0572,
            "baseline_held_out_accuracy": 0.9932,
            "baseline_held_out_f1_weighted": 0.9932,
            "baseline_held_out_log_loss": 0.0527,
            "error_analysis": {
                "baseline_errors": 3,
                "tuned_errors": 2,
                "errors_fixed": 1,
                "new_errors_introduced": 0,
            },
        },

        "confidence_type": (
            "random_forest_class_probability"
        ),

        "production_model_replaced": False,

        "notes": [
            (
                "This candidate was selected after controlled "
                "hyperparameter tuning."
            ),
            (
                "The candidate model was trained on the complete "
                "dataset after model selection."
            ),
            (
                "The reported held-out metrics come from the "
                "model-selection experiment and not from this "
                "full-dataset training run."
            ),
            (
                "The candidate has not yet replaced the existing "
                "production model."
            ),
        ],
    }


def main():
    print("\n" + "=" * 70)
    print("KISANAI FINAL CROP MODEL TRAINING")
    print("=" * 70)

    print("\nLoading dataset...")

    df, X, y = load_dataset()

    print(f"\nDataset samples : {len(df)}")
    print(f"Features        : {len(FEATURE_COLUMNS)}")
    print(f"Crop classes    : {y.nunique()}")

    print("\nClass distribution:")

    for crop, count in y.value_counts().sort_index().items():
        print(f"  {crop:<20} {count}")

    print("\n" + "-" * 70)
    print("FINAL MODEL PARAMETERS")
    print("-" * 70)

    for parameter, value in FINAL_PARAMETERS.items():
        print(f"{parameter:<20}: {value}")

    print("\n" + "-" * 70)
    print("TRAINING")
    print("-" * 70)

    model = train_model(X, y)

    print("\nTraining completed.")

    print("\n" + "-" * 70)
    print("MODEL INFORMATION")
    print("-" * 70)

    print(
        f"Number of trees : "
        f"{len(model.estimators_)}"
    )

    print(
        f"Number of classes: "
        f"{len(model.classes_)}"
    )

    print(
        f"Features         : "
        f"{len(model.feature_names_in_)}"
    )

    print("\nModel classes:")

    print(
        ", ".join(model.classes_)
    )

    # ---------------------------------------------------------
    # SAVE CANDIDATE MODEL
    # ---------------------------------------------------------

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        CANDIDATE_MODEL_PATH,
    )

    metadata = create_metadata(
        df,
        X,
        y,
    )

    with open(
        CANDIDATE_METADATA_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metadata,
            file,
            indent=4,
        )

    print("\n" + "-" * 70)
    print("CANDIDATE MODEL SAVED")
    print("-" * 70)

    print(
        f"\nCandidate model:\n"
        f"{CANDIDATE_MODEL_PATH}"
    )

    print(
        f"\nCandidate metadata:\n"
        f"{CANDIDATE_METADATA_PATH}"
    )

    print("\n" + "-" * 70)
    print("CURRENT PRODUCTION MODEL")
    print("-" * 70)

    if PRODUCTION_MODEL_PATH.exists():
        print(
            f"\nExisting production model remains:\n"
            f"{PRODUCTION_MODEL_PATH}"
        )
    else:
        print(
            "\nNo existing production model was found."
        )

    print("\n" + "=" * 70)
    print("FINAL TRAINING COMPLETE")
    print("=" * 70)

    print(
        "\nIMPORTANT:"
        "\nThe production model has NOT been replaced."
        "\nThe candidate must pass final validation first."
    )


if __name__ == "__main__":
    main()