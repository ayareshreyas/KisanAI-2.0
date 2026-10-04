from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from joblib import load


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "models" / "crop_recommendation_random_forest.joblib"


# --------------------------------------------------
# 2. Load test data
# --------------------------------------------------

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").squeeze("columns")


# --------------------------------------------------
# 3. Load trained model
# --------------------------------------------------

model = load(MODEL_PATH)


print("=" * 70)
print("CROP RECOMMENDATION — ERROR & GENERALIZATION ANALYSIS")
print("=" * 70)

print(f"\nTest samples: {len(X_test)}")
print(f"Test features: {X_test.shape[1]}")


# --------------------------------------------------
# 4. Generate predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 5. Overall test performance
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 70)
print("HELD-OUT TEST PERFORMANCE")
print("=" * 70)

print(f"\nTest Accuracy: {accuracy:.4f}")
print(f"Test Accuracy: {accuracy * 100:.2f}%")


# --------------------------------------------------
# 6. Identify incorrect predictions
# --------------------------------------------------

comparison = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})

errors = comparison[
    comparison["Actual"] != comparison["Predicted"]
].copy()


print("\n" + "=" * 70)
print("ERROR ANALYSIS")
print("=" * 70)

print(f"\nIncorrect predictions: {len(errors)}")
print(f"Correct predictions:   {len(comparison) - len(errors)}")

if len(errors) > 0:

    print("\nIncorrect prediction pairs:")

    error_pairs = (
        errors
        .groupby(["Actual", "Predicted"])
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    print(error_pairs.to_string(index=False))

else:
    print("\nNo incorrect predictions found.")


# --------------------------------------------------
# 7. Classification report
# --------------------------------------------------

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

print(
    classification_report(
        y_test,
        y_pred,
        digits=4
    )
)


# --------------------------------------------------
# 8. Confusion matrix
# --------------------------------------------------

labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print("\nCrop labels:")
print(labels)

print("\nMatrix:")
print(cm)


# --------------------------------------------------
# 9. Save confusion matrix visualization
# --------------------------------------------------

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

fig, ax = plt.subplots(figsize=(14, 14))

display.plot(
    ax=ax,
    xticks_rotation=90,
    values_format="d"
)

plt.title("Crop Recommendation — Held-Out Test Confusion Matrix")
plt.tight_layout()

output_path = DATA_DIR / "crop_error_analysis_confusion_matrix.png"

plt.savefig(
    output_path,
    dpi=200,
    bbox_inches="tight"
)

plt.show()

print(f"\nConfusion matrix saved to:")
print(output_path)


# --------------------------------------------------
# 10. Save incorrect predictions
# --------------------------------------------------

errors_path = DATA_DIR / "crop_prediction_errors.csv"

errors.to_csv(
    errors_path,
    index=False
)

print(f"\nPrediction errors saved to:")
print(errors_path)


print("\n" + "=" * 70)
print("ERROR ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)