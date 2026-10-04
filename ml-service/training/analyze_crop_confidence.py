from pathlib import Path

import pandas as pd
from joblib import load


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "models" / "crop_recommendation_random_forest.joblib"


# --------------------------------------------------
# 2. Load test data and trained model
# --------------------------------------------------

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze("columns")

model = load(MODEL_PATH)


print("=" * 70)
print("CROP RECOMMENDATION — PREDICTION CONFIDENCE ANALYSIS")
print("=" * 70)

print(f"\nTest samples: {len(X_test)}")


# --------------------------------------------------
# 3. Generate predictions and probabilities
# --------------------------------------------------

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

class_names = model.classes_


# --------------------------------------------------
# 4. Build confidence table
# --------------------------------------------------

top_prediction_index = probabilities.argmax(axis=1)

top_confidence = probabilities[
    range(len(probabilities)),
    top_prediction_index
]

top_prediction = class_names[top_prediction_index]


confidence_df = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": top_prediction,
    "Confidence": top_confidence
})


confidence_df["Correct"] = (
    confidence_df["Actual"] == confidence_df["Predicted"]
)


# --------------------------------------------------
# 5. Overall confidence statistics
# --------------------------------------------------

print("\n" + "=" * 70)
print("OVERALL CONFIDENCE")
print("=" * 70)

print(
    f"\nAverage confidence: "
    f"{confidence_df['Confidence'].mean() * 100:.2f}%"
)

print(
    f"Minimum confidence: "
    f"{confidence_df['Confidence'].min() * 100:.2f}%"
)

print(
    f"Maximum confidence: "
    f"{confidence_df['Confidence'].max() * 100:.2f}%"
)


# --------------------------------------------------
# 6. Confidence distribution
# --------------------------------------------------

confidence_bins = [
    0.0,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
    1.01
]

confidence_labels = [
    "<50%",
    "50–60%",
    "60–70%",
    "70–80%",
    "80–90%",
    "90–100%"
]

confidence_df["Confidence Range"] = pd.cut(
    confidence_df["Confidence"],
    bins=confidence_bins,
    labels=confidence_labels,
    right=False
)

distribution = (
    confidence_df["Confidence Range"]
    .value_counts()
    .sort_index()
)

print("\n" + "=" * 70)
print("CONFIDENCE DISTRIBUTION")
print("=" * 70)

for confidence_range, count in distribution.items():
    print(f"{confidence_range:<10}: {count}")


# --------------------------------------------------
# 7. Correct vs incorrect confidence
# --------------------------------------------------

correct_predictions = confidence_df[
    confidence_df["Correct"]
]

incorrect_predictions = confidence_df[
    ~confidence_df["Correct"]
]


print("\n" + "=" * 70)
print("CORRECT vs INCORRECT PREDICTIONS")
print("=" * 70)

print(
    f"\nCorrect predictions:   {len(correct_predictions)}"
)

print(
    f"Average confidence:    "
    f"{correct_predictions['Confidence'].mean() * 100:.2f}%"
)

if len(incorrect_predictions) > 0:

    print(
        f"\nIncorrect predictions: {len(incorrect_predictions)}"
    )

    print(
        f"Average confidence:    "
        f"{incorrect_predictions['Confidence'].mean() * 100:.2f}%"
    )


# --------------------------------------------------
# 8. Show every incorrect prediction
# --------------------------------------------------

print("\n" + "=" * 70)
print("INCORRECT PREDICTIONS AND CONFIDENCE")
print("=" * 70)

if len(incorrect_predictions) > 0:

    print(
        incorrect_predictions[
            ["Actual", "Predicted", "Confidence"]
        ].to_string(
            index=False,
            formatters={
                "Confidence": "{:.4f}".format
            }
        )
    )

else:
    print("\nNo incorrect predictions found.")


# --------------------------------------------------
# 9. Show lowest-confidence predictions
# --------------------------------------------------

print("\n" + "=" * 70)
print("10 LOWEST-CONFIDENCE PREDICTIONS")
print("=" * 70)

lowest_confidence = (
    confidence_df
    .sort_values("Confidence")
    .head(10)
)

print(
    lowest_confidence[
        ["Actual", "Predicted", "Confidence", "Correct"]
    ].to_string(
        index=False,
        formatters={
            "Confidence": "{:.4f}".format
        }
    )
)


# --------------------------------------------------
# 10. Save complete confidence analysis
# --------------------------------------------------

output_path = DATA_DIR / "crop_prediction_confidence.csv"

confidence_df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 70)
print("CONFIDENCE ANALYSIS COMPLETED")
print("=" * 70)

print(f"\nDetailed confidence results saved to:")
print(output_path)