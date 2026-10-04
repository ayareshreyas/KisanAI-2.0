from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from joblib import load
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from sklearn.preprocessing import label_binarize


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
print("CROP RECOMMENDATION — CONFIDENCE CALIBRATION")
print("=" * 70)


# --------------------------------------------------
# 3. Generate probabilities
# --------------------------------------------------

probabilities = model.predict_proba(X_test)

class_names = model.classes_

y_pred = model.predict(X_test)

top_indices = probabilities.argmax(axis=1)

top_confidence = probabilities[
    range(len(probabilities)),
    top_indices
]

correct = (
    y_pred == y_test.to_numpy()
)


# --------------------------------------------------
# 4. Confidence vs actual correctness
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

labels = [
    "<50%",
    "50–60%",
    "60–70%",
    "70–80%",
    "80–90%",
    "90–100%"
]


calibration_df = pd.DataFrame({
    "Confidence": top_confidence,
    "Correct": correct
})

calibration_df["Confidence Range"] = pd.cut(
    calibration_df["Confidence"],
    bins=confidence_bins,
    labels=labels,
    right=False
)


print("\n" + "=" * 70)
print("CONFIDENCE VS OBSERVED ACCURACY")
print("=" * 70)

for label in labels:

    group = calibration_df[
        calibration_df["Confidence Range"] == label
    ]

    if len(group) == 0:
        continue

    average_confidence = group["Confidence"].mean()
    observed_accuracy = group["Correct"].mean()

    print(
        f"\n{label}"
        f"\n  Samples             : {len(group)}"
        f"\n  Average confidence : {average_confidence * 100:.2f}%"
        f"\n  Observed accuracy  : {observed_accuracy * 100:.2f}%"
    )


# --------------------------------------------------
# 5. Multiclass Brier score
# --------------------------------------------------

y_test_encoded = label_binarize(
    y_test,
    classes=class_names
)

brier_score = (
    (
        probabilities - y_test_encoded
    ) ** 2
).sum(axis=1).mean()


print("\n" + "=" * 70)
print("BRIER SCORE")
print("=" * 70)

print(
    f"\nMulticlass Brier score: "
    f"{brier_score:.6f}"
)


# --------------------------------------------------
# 6. Calibration curve for top prediction
# --------------------------------------------------

fraction_of_positives, mean_predicted_value = calibration_curve(
    correct.astype(int),
    top_confidence,
    n_bins=10,
    strategy="uniform"
)


# --------------------------------------------------
# 7. Save calibration plot
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.plot(
    mean_predicted_value,
    fraction_of_positives,
    marker="o",
    label="Random Forest"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Perfect calibration"
)

plt.xlabel("Mean predicted confidence")
plt.ylabel("Observed accuracy")
plt.title("Crop Recommendation Model Calibration")
plt.legend()
plt.grid(True)
plt.tight_layout()


output_path = (
    DATA_DIR /
    "crop_model_calibration_curve.png"
)

plt.savefig(
    output_path,
    dpi=200,
    bbox_inches="tight"
)

plt.show()


# --------------------------------------------------
# 8. Save calibration data
# --------------------------------------------------

calibration_output = (
    DATA_DIR /
    "crop_model_calibration_data.csv"
)

calibration_curve_df = pd.DataFrame({
    "Mean Predicted Confidence": mean_predicted_value,
    "Observed Accuracy": fraction_of_positives
})

calibration_curve_df.to_csv(
    calibration_output,
    index=False
)


print("\n" + "=" * 70)
print("CALIBRATION ANALYSIS COMPLETED")
print("=" * 70)

print(f"\nCalibration plot saved to:")
print(output_path)

print(f"\nCalibration data saved to:")
print(calibration_output)