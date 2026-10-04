"""
KisanAI Crop Model Explainability

This module explains individual crop predictions made by
the KisanAI Random Forest crop recommendation model.

Explainability method:
    SHAP (SHapley Additive exPlanations)

The explanation describes how the model's input features
contributed to the selected prediction.

Important:
- SHAP explains the behavior of the trained model.
- It does NOT prove that a crop will succeed in the real world.
- Feature contribution is model-specific.
- It should not be interpreted as an agronomic prescription.
"""

from pathlib import Path

import joblib
import pandas as pd
import shap


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "crop_recommendation_random_forest.joblib"
)


# ------------------------------------------------------------
# Model feature order
# ------------------------------------------------------------

FEATURE_NAMES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]


# ------------------------------------------------------------
# Load model
# ------------------------------------------------------------

model = joblib.load(MODEL_PATH)


# ------------------------------------------------------------
# Create SHAP explainer
# ------------------------------------------------------------

explainer = shap.TreeExplainer(model)


def explain_crop_prediction(
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall,
):
    """
    Explain a single crop prediction.

    Returns:
        Dictionary containing:

        - prediction
        - model_confidence
        - feature_contributions
    """

    input_data = pd.DataFrame(
        [[
            float(N),
            float(P),
            float(K),
            float(temperature),
            float(humidity),
            float(ph),
            float(rainfall),
        ]],
        columns=FEATURE_NAMES,
    )

    # --------------------------------------------------------
    # Model prediction
    # --------------------------------------------------------

    prediction = model.predict(
        input_data
    )[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    predicted_class_index = (
        list(model.classes_).index(prediction)
    )

    confidence = float(
        probabilities[predicted_class_index]
    )

    # --------------------------------------------------------
    # SHAP values
    # --------------------------------------------------------

    shap_values = explainer.shap_values(
        input_data
    )

    # SHAP's output structure can differ between versions.
    #
    # For multiclass Random Forest models, recent SHAP
    # versions can return:
    #
    #     (samples, features, classes)
    #
    # Older versions can return:
    #
    #     list[classes][samples][features]
    #
    # Handle both formats.

    if isinstance(shap_values, list):

        class_values = shap_values[
            predicted_class_index
        ]

        contribution_values = class_values[0]

    else:

        shap_array = shap_values

        if shap_array.ndim == 3:

            # Shape:
            # samples × features × classes

            contribution_values = shap_array[
                0,
                :,
                predicted_class_index,
            ]

        elif shap_array.ndim == 2:

            contribution_values = shap_array[
                0
            ]

        else:

            raise ValueError(
                "Unexpected SHAP output shape: "
                f"{shap_array.shape}"
            )

    # --------------------------------------------------------
    # Build contribution output
    # --------------------------------------------------------

    contributions = []

    for feature, value, contribution in zip(
        FEATURE_NAMES,
        input_data.iloc[0].tolist(),
        contribution_values,
    ):

        contributions.append({
            "feature": feature,
            "value": float(value),
            "contribution": round(
                float(contribution),
                6,
            ),
        })

    # --------------------------------------------------------
    # Sort by absolute influence.
    # --------------------------------------------------------

    contributions.sort(
        key=lambda item: abs(
            item["contribution"]
        ),
        reverse=True,
    )

    return {
        "prediction": prediction,
        "model_confidence": round(
            confidence,
            6,
        ),
        "feature_contributions": contributions,
    }


# ------------------------------------------------------------
# Test
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("KISANAI CROP MODEL EXPLAINABILITY")
    print("=" * 70)

    result = explain_crop_prediction(
        N=90,
        P=42,
        K=43,
        temperature=25,
        humidity=80,
        ph=6.5,
        rainfall=200,
    )

    print("\nPrediction:")
    print(result["prediction"])

    print("\nModel confidence:")
    print(
        f"{result['model_confidence'] * 100:.2f}%"
    )

    print("\nFeature contributions:")

    for item in result[
        "feature_contributions"
    ]:

        direction = (
            "supports"
            if item["contribution"] > 0
            else "opposes"
        )

        print(
            f"  {item['feature']:12} "
            f"value={item['value']:8.2f} "
            f"contribution={item['contribution']: .6f} "
            f"({direction})"
        )