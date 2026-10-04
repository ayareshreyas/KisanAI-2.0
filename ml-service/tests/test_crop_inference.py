from pathlib import Path
import sys

import pandas as pd


# --------------------------------------------------
# 1. Allow importing from the ML service
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


from inference.predict_crop import predict_crop
from inference.input_reliability import assess_input_reliability


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Crop_recommendation.csv"
)

data = pd.read_csv(DATASET_PATH)


# --------------------------------------------------
# 3. Test configuration
# --------------------------------------------------

SAMPLE_COUNT = 10
RANDOM_STATE = 42

EXPECTED_FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]


# --------------------------------------------------
# 4. Helpers
# --------------------------------------------------

def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def assert_condition(condition, message):
    if not condition:
        raise AssertionError(message)


# --------------------------------------------------
# 5. Dataset integrity checks
# --------------------------------------------------

print_section("DATASET INTEGRITY VALIDATION")

assert_condition(
    list(data.columns[:7]) == EXPECTED_FEATURES,
    "Dataset feature columns do not match the expected model features.",
)

assert_condition(
    "label" in data.columns,
    "Dataset is missing the label column.",
)

assert_condition(
    len(data) == 2200,
    f"Expected 2200 dataset rows, found {len(data)}.",
)

assert_condition(
    data["label"].nunique() == 22,
    f"Expected 22 crop classes, found {data['label'].nunique()}.",
)

print("PASS: Dataset feature columns are correct.")
print("PASS: Dataset contains the label column.")
print("PASS: Dataset contains 2200 rows.")
print("PASS: Dataset contains 22 crop classes.")


# --------------------------------------------------
# 6. Production inference validation
# --------------------------------------------------

samples = data.sample(
    n=SAMPLE_COUNT,
    random_state=RANDOM_STATE,
)

print_section("CROP INFERENCE VALIDATION")

correct_predictions = 0


for index, row in samples.iterrows():

    result = predict_crop(
        nitrogen=row["N"],
        phosphorus=row["P"],
        potassium=row["K"],
        temperature=row["temperature"],
        humidity=row["humidity"],
        ph=row["ph"],
        rainfall=row["rainfall"],
    )

    predicted_crop = result["crop"]
    confidence = result["confidence"]
    confidence_type = result.get("confidence_type")

    actual_crop = row["label"]

    # Basic response validation
    assert_condition(
        isinstance(predicted_crop, str),
        f"Row {index}: prediction must be a string.",
    )

    assert_condition(
        0.0 <= confidence <= 1.0,
        f"Row {index}: confidence must be between 0 and 1.",
    )

    assert_condition(
        confidence_type == "random_forest_class_probability",
        (
            f"Row {index}: unexpected confidence type: "
            f"{confidence_type}"
        ),
    )

    # Input reliability validation
    reliability = result.get("input_reliability")

    assert_condition(
        isinstance(reliability, dict),
        f"Row {index}: input_reliability must be a dictionary.",
    )

    assert_condition(
        reliability.get("status") == "within_training_range",
        (
            f"Row {index}: expected dataset sample to be "
            "within training range."
        ),
    )

    is_correct = (
        predicted_crop == actual_crop
    )

    if is_correct:
        correct_predictions += 1

    status = "PASS" if is_correct else "FAIL"

    print("\n" + "-" * 70)

    print(f"Dataset row       : {index}")
    print(f"Actual crop       : {actual_crop}")
    print(f"Predicted crop    : {predicted_crop}")
    print(
        f"Model confidence : "
        f"{confidence * 100:.2f}%"
    )
    print(f"Confidence type   : {confidence_type}")
    print(
        f"Reliability      : "
        f"{reliability.get('status')}"
    )
    print(f"Result            : {status}")


# --------------------------------------------------
# 7. Input reliability boundary test
# --------------------------------------------------

print_section("INPUT RELIABILITY VALIDATION")

normal_input = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 25,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200,
}

normal_reliability = assess_input_reliability(
    normal_input
)

assert_condition(
    normal_reliability["status"] == "within_training_range",
    "Normal test input should be within training range.",
)

print("PASS: Normal farm input is within training range.")


out_of_range_input = {
    "N": 150,
    "P": 42,
    "K": 43,
    "temperature": 25,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200,
}

out_of_range_reliability = assess_input_reliability(
    out_of_range_input
)

assert_condition(
    out_of_range_reliability["status"] == "outside_training_range",
    "N=150 should be detected as outside the training range.",
)

assert_condition(
    len(out_of_range_reliability["warnings"]) > 0,
    "Out-of-range input should produce at least one warning.",
)

print(
    "PASS: Out-of-range nitrogen input is correctly detected."
)


# --------------------------------------------------
# 8. Final validation result
# --------------------------------------------------

total_samples = len(samples)

accuracy = (
    correct_predictions / total_samples
)


print_section("VALIDATION SUMMARY")

print(f"\nSamples tested      : {total_samples}")
print(f"Correct predictions : {correct_predictions}")
print(
    f"Inference accuracy : "
    f"{accuracy * 100:.2f}%"
)

print("\nAdditional checks:")
print("PASS: Dataset integrity")
print("PASS: Prediction response structure")
print("PASS: Confidence range")
print("PASS: Confidence type")
print("PASS: Input reliability for normal input")
print("PASS: Out-of-range input detection")


if correct_predictions == total_samples:

    print(
        "\nSUCCESS: "
        "All crop inference and reliability tests passed."
    )

else:

    print(
        "\nWARNING: "
        "Some sampled dataset rows were predicted incorrectly."
    )