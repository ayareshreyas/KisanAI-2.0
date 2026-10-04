from pathlib import Path
from datetime import datetime
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_PATH = (
    PROJECT_ROOT
    / "ml-service"
    / "models"
    / "crop_model_metadata.json"
)


def main():
    print("=" * 70)
    print("KISANAI PRODUCTION MODEL METADATA FINALIZATION")
    print("=" * 70)

    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"Production metadata not found:\n{METADATA_PATH}"
        )

    print("\nLoading metadata:")
    print(METADATA_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    dataset = metadata.get("dataset", {})
    hyperparameters = metadata.get("hyperparameters", {})
    selection_evidence = metadata.get("selection_evidence", {})

    feature_columns = dataset.get("feature_columns")

    if not feature_columns:
        raise ValueError(
            "Candidate metadata does not contain dataset.feature_columns."
        )

    classes = list(dataset.get("class_distribution", {}).keys())

    if not classes:
        raise ValueError(
            "Candidate metadata does not contain dataset.class_distribution."
        )

    # ------------------------------------------------------------------
    # Add production-compatible top-level fields expected by inference
    # ------------------------------------------------------------------

    metadata["features"] = feature_columns
    metadata["classes"] = classes

    metadata["training_samples"] = dataset.get("samples")
    metadata["testing_samples"] = 440

    metadata["test_accuracy"] = selection_evidence.get(
        "held_out_accuracy"
    )

    metadata["test_precision_weighted"] = selection_evidence.get(
        "held_out_precision_weighted"
    )

    metadata["test_recall_weighted"] = selection_evidence.get(
        "held_out_recall_weighted"
    )

    metadata["test_f1_weighted"] = selection_evidence.get(
        "held_out_f1_weighted"
    )

    metadata["test_log_loss"] = selection_evidence.get(
        "held_out_log_loss"
    )

    metadata["cv_folds"] = selection_evidence.get("cv_folds")
    metadata["cv_accuracy_mean"] = selection_evidence.get(
        "best_cv_accuracy"
    )

    metadata["random_state"] = hyperparameters.get("random_state")

    metadata["n_estimators"] = hyperparameters.get("n_estimators")

    metadata["confidence_type"] = metadata.get(
        "confidence_type",
        "random_forest_class_probability",
    )

    # ------------------------------------------------------------------
    # Production status
    # ------------------------------------------------------------------

    metadata["model_status"] = "production"

    metadata["production_model_replaced"] = True

    metadata["production_promoted_at"] = datetime.now().astimezone().isoformat()

    metadata["production_model"] = {
        "artifact": "crop_recommendation_random_forest.joblib",
        "training_samples": dataset.get("samples"),
        "features": feature_columns,
        "classes": classes,
        "hyperparameters": hyperparameters,
    }

    # ------------------------------------------------------------------
    # Clean production notes
    # ------------------------------------------------------------------

    metadata["notes"] = [
        "This model was selected after controlled hyperparameter tuning.",
        "The final production artifact was trained on the complete dataset after model selection.",
        "Held-out metrics come from the model-selection experiment using an untouched 20% test split.",
        "The production artifact itself must not be evaluated on those same training rows as a generalization test.",
        "Input reliability checks compare inference inputs against observed training-data ranges.",
        "Confidence represents the Random Forest class probability and is not a calibrated probability estimate.",
        "SHAP explanations describe model feature contributions and should not be interpreted as causal agricultural effects.",
    ]

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )

    print("\nMetadata finalized successfully.")

    print("\nProduction-compatible fields:")
    print(f"  features : {metadata['features']}")
    print(f"  classes  : {len(metadata['classes'])}")
    print(f"  samples  : {metadata['training_samples']}")
    print(f"  status   : {metadata['model_status']}")

    print("\nEvaluation evidence:")
    print(
        f"  held-out accuracy : "
        f"{metadata['test_accuracy']}"
    )

    print(
        f"  held-out F1       : "
        f"{metadata['test_f1_weighted']}"
    )

    print(
        f"  CV accuracy       : "
        f"{metadata['cv_accuracy_mean']}"
    )

    print("\nProduction status:")
    print(
        f"  production_model_replaced : "
        f"{metadata['production_model_replaced']}"
    )

    print(
        "\nNext step: restart the ML service and verify that "
        "predict_crop.py loads the promoted production model."
    )


if __name__ == "__main__":
    main()