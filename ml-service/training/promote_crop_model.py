from pathlib import Path
from datetime import datetime
import json
import shutil


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "ml-service" / "models"

CANDIDATE_MODEL = (
    MODELS_DIR
    / "crop_recommendation_random_forest_tuned_candidate.joblib"
)

PRODUCTION_MODEL = (
    MODELS_DIR
    / "crop_recommendation_random_forest.joblib"
)

CANDIDATE_METADATA = (
    MODELS_DIR
    / "crop_model_tuned_candidate_metadata.json"
)

PRODUCTION_METADATA = (
    MODELS_DIR
    / "crop_model_metadata.json"
)


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_file(file_path):
    if not file_path.exists():
        return None

    backup_path = file_path.with_name(
        f"{file_path.stem}_backup_{timestamp()}{file_path.suffix}"
    )

    shutil.copy2(file_path, backup_path)

    return backup_path


def main():
    print("=" * 70)
    print("KISANAI CROP MODEL — CONTROLLED PROMOTION")
    print("=" * 70)

    print("\nModels directory:")
    print(MODELS_DIR)

    # ------------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------------

    if not MODELS_DIR.exists():
        raise FileNotFoundError(
            f"Models directory does not exist: {MODELS_DIR}"
        )

    if not CANDIDATE_MODEL.exists():
        raise FileNotFoundError(
            f"Candidate model does not exist:\n{CANDIDATE_MODEL}"
        )

    print("\nCandidate model found:")
    print(CANDIDATE_MODEL)

    if PRODUCTION_MODEL.exists():
        print("\nCurrent production model found:")
        print(PRODUCTION_MODEL)
    else:
        print("\nNo existing production model found.")

    # ------------------------------------------------------------------
    # Read candidate metadata if available
    # ------------------------------------------------------------------

    candidate_metadata = None

    if CANDIDATE_METADATA.exists():
        with open(CANDIDATE_METADATA, "r", encoding="utf-8") as file:
            candidate_metadata = json.load(file)

        print("\nCandidate metadata found.")

        print(
            f"  Samples       : "
            f"{candidate_metadata.get('samples', 'unknown')}"
        )

        print(
            f"  Features      : "
            f"{candidate_metadata.get('features', 'unknown')}"
        )

        print(
            f"  Classes       : "
            f"{candidate_metadata.get('classes', 'unknown')}"
        )

    else:
        print("\nCandidate metadata file not found.")
        print("The model itself will still be promoted.")

    # ------------------------------------------------------------------
    # Back up current production artifacts
    # ------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Creating backups")
    print("-" * 70)

    model_backup = backup_file(PRODUCTION_MODEL)

    if model_backup:
        print(f"Production model backup:")
        print(model_backup)
    else:
        print("No production model backup required.")

    metadata_backup = backup_file(PRODUCTION_METADATA)

    if metadata_backup:
        print("\nProduction metadata backup:")
        print(metadata_backup)
    else:
        print("\nNo production metadata backup required.")

    # ------------------------------------------------------------------
    # Promote model
    # ------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Promoting candidate model")
    print("-" * 70)

    shutil.copy2(
        CANDIDATE_MODEL,
        PRODUCTION_MODEL,
    )

    print("\nCandidate model promoted to:")
    print(PRODUCTION_MODEL)

    # ------------------------------------------------------------------
    # Promote metadata
    # ------------------------------------------------------------------

    if CANDIDATE_METADATA.exists():
        shutil.copy2(
            CANDIDATE_METADATA,
            PRODUCTION_METADATA,
        )

        print("\nCandidate metadata promoted to:")
        print(PRODUCTION_METADATA)

    # ------------------------------------------------------------------
    # Verify files
    # ------------------------------------------------------------------

    print("\n" + "-" * 70)
    print("Promotion verification")
    print("-" * 70)

    if not PRODUCTION_MODEL.exists():
        raise RuntimeError(
            "Promotion failed: production model does not exist."
        )

    production_model_size = PRODUCTION_MODEL.stat().st_size
    candidate_model_size = CANDIDATE_MODEL.stat().st_size

    print(f"\nCandidate model size  : {candidate_model_size:,} bytes")
    print(f"Production model size : {production_model_size:,} bytes")

    if production_model_size != candidate_model_size:
        raise RuntimeError(
            "Promotion verification failed: "
            "candidate and production model sizes differ."
        )

    print("\nModel file size check: PASSED")

    if CANDIDATE_METADATA.exists():
        if not PRODUCTION_METADATA.exists():
            raise RuntimeError(
                "Promotion failed: production metadata does not exist."
            )

        candidate_metadata_size = CANDIDATE_METADATA.stat().st_size
        production_metadata_size = PRODUCTION_METADATA.stat().st_size

        print(
            f"Candidate metadata size  : "
            f"{candidate_metadata_size:,} bytes"
        )

        print(
            f"Production metadata size : "
            f"{production_metadata_size:,} bytes"
        )

        if candidate_metadata_size != production_metadata_size:
            raise RuntimeError(
                "Promotion verification failed: "
                "candidate and production metadata sizes differ."
            )

        print("Metadata file size check: PASSED")

    # ------------------------------------------------------------------
    # Final summary
    # ------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("PROMOTION COMPLETE")
    print("=" * 70)

    print("\nProduction model:")
    print(PRODUCTION_MODEL)

    if model_backup:
        print("\nPrevious production model backed up to:")
        print(model_backup)

    if metadata_backup:
        print("\nPrevious production metadata backed up to:")
        print(metadata_backup)

    print(
        "\nThe tuned candidate is now the production crop recommendation model."
    )

    print(
        "\nNext step: verify that the live ML inference service loads "
        "and uses this production artifact correctly."
    )


if __name__ == "__main__":
    main()