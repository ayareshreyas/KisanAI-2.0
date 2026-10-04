"""
KisanAI Agricultural Decision Engine

Coordinates the validated agricultural intelligence modules:

    Farmer Inputs
         ↓
    Input Reliability Assessment
         ↓
    Crop ML Prediction
         ↓
    SHAP Explanation
         ↓
    Soil Health Analysis
         ↓
    Fertilizer Planning Availability

Important:
- This module coordinates existing components.
- It does NOT invent a soil-test-to-fertilizer conversion.
- Soil health N/P/K values are interpreted in kg/ha.
- The current fertilizer engine expects compatible nutrient
  values expressed on its kg/acre calculation basis.
- Therefore fertilizer optimization is only performed when
  compatible fertilizer inputs are explicitly supplied.
- Input reliability checks compare crop-model inputs against
  ranges observed in the training dataset.
"""

from inference.predict_crop import predict_crop
from explainability.crop_explainer import explain_crop_prediction
from soil.soil_analyzer import analyze_soil
from fertilizer.crop_requirements import get_crop_requirements


# ------------------------------------------------------------
# Crop name normalization
# ------------------------------------------------------------

def normalize_crop_name(crop):
    """
    Normalize a crop name for lookup purposes.

    The crop ML model returns lowercase class labels such as
    'rice', while the fertilizer knowledge base currently
    stores names such as 'Rice'.
    """

    if not isinstance(crop, str):
        return None

    normalized = crop.strip().lower()

    for supported_crop in (
        get_supported_fertilizer_crops()
    ):
        if supported_crop.lower() == normalized:
            return supported_crop

    return None


def get_supported_fertilizer_crops():
    """
    Return crops currently supported by the fertilizer
    knowledge base.
    """

    from fertilizer.crop_requirements import (
        get_supported_crops,
    )

    return get_supported_crops()


# ------------------------------------------------------------
# Main agricultural decision function
# ------------------------------------------------------------

def generate_agricultural_decision(
    nitrogen,
    phosphorus,
    potassium,
    temperature,
    humidity,
    ph,
    rainfall,
    fertilizer_inputs=None,
    fertilizer_budget=None,
):
    """
    Generate a combined agricultural decision-support result.

    Parameters
    ----------
    nitrogen, phosphorus, potassium:
        Soil-test nutrient values in kg/ha.

    temperature, humidity, ph, rainfall:
        Environmental and soil features used by the crop ML model.

    fertilizer_inputs:
        Optional compatible fertilizer-engine inputs.

        Expected format:

            {
                "N": <value>,
                "P": <value>,
                "K": <value>
            }

        These values must already be compatible with the
        fertilizer engine's kg/acre calculation basis.

        They are intentionally NOT derived automatically from
        the soil analyzer's kg/ha values.

    fertilizer_budget:
        Optional fertilizer budget in rupees.

    Returns
    -------
    dict
        Combined crop, soil and fertilizer decision-support data.
    """

    # --------------------------------------------------------
    # Normalize numeric inputs
    # --------------------------------------------------------

    nitrogen = float(nitrogen)
    phosphorus = float(phosphorus)
    potassium = float(potassium)
    temperature = float(temperature)
    humidity = float(humidity)
    ph = float(ph)
    rainfall = float(rainfall)

    # --------------------------------------------------------
    # STEP 1 — Crop prediction + input reliability
    # --------------------------------------------------------

    crop_result = predict_crop(
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
    )

    predicted_crop = crop_result["crop"]

    input_reliability = crop_result[
        "input_reliability"
    ]

    # --------------------------------------------------------
    # STEP 2 — SHAP explanation
    # --------------------------------------------------------

    explanation = explain_crop_prediction(
        N=nitrogen,
        P=phosphorus,
        K=potassium,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
    )

    # --------------------------------------------------------
    # STEP 3 — Soil health analysis
    # --------------------------------------------------------

    soil_analysis = analyze_soil(
        nitrogen=nitrogen,
        phosphorus=phosphorus,
        potassium=potassium,
        ph=ph,
    )

    # --------------------------------------------------------
    # STEP 4 — Determine fertilizer support
    # --------------------------------------------------------

    fertilizer_crop = normalize_crop_name(
        predicted_crop
    )

    fertilizer_result = {
        "available": False,
        "crop": predicted_crop,
        "supported_crop": fertilizer_crop,
        "reason": (
            "The current fertilizer knowledge base does not "
            "contain a compatible requirement profile for "
            "the predicted crop."
        ),
    }

    # --------------------------------------------------------
    # STEP 5 — Optional fertilizer optimization
    # --------------------------------------------------------

    if fertilizer_crop is not None:

        fertilizer_result = {
            "available": False,
            "crop": predicted_crop,
            "supported_crop": fertilizer_crop,
            "reason": (
                "The predicted crop is supported by the "
                "fertilizer knowledge base, but fertilizer "
                "optimization requires nutrient inputs that "
                "are explicitly compatible with the "
                "fertilizer engine's kg/acre calculation basis."
            ),
        }

        if fertilizer_inputs is not None:

            required_fields = ("N", "P", "K")

            missing_fields = [
                field
                for field in required_fields
                if field not in fertilizer_inputs
            ]

            if not missing_fields:

                compatible_n = float(
                    fertilizer_inputs["N"]
                )
                compatible_p = float(
                    fertilizer_inputs["P"]
                )
                compatible_k = float(
                    fertilizer_inputs["K"]
                )

                if (
                    compatible_n >= 0
                    and compatible_p >= 0
                    and compatible_k >= 0
                ):

                    from fertilizer.recommendation_engine import (
                        generate_fertilizer_recommendation,
                    )

                    recommendation = (
                        generate_fertilizer_recommendation(
                            crop=fertilizer_crop,
                            soil_n=compatible_n,
                            soil_p=compatible_p,
                            soil_k=compatible_k,
                            budget=fertilizer_budget,
                        )
                    )

                    fertilizer_result = {
                        "available": True,
                        "crop": predicted_crop,
                        "supported_crop": fertilizer_crop,
                        "input_basis": "kg/acre",
                        "recommendation": recommendation,
                    }

    # --------------------------------------------------------
    # STEP 6 — Return unified result
    # --------------------------------------------------------

    return {
        "crop_recommendation": {
            "crop": predicted_crop,
            "confidence": crop_result["confidence"],
        },

        "input_reliability": input_reliability,

        "crop_explanation": explanation,

        "soil_health": soil_analysis,

        "fertilizer_planning": fertilizer_result,
    }