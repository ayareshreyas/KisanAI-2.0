"""
KisanAI Soil Intelligence

Analyzes laboratory soil-test values using nutrient
classification thresholds referenced from the
Government of India's Soil Health Card educational
soil-testing material.

Important:
- N, P and K are expected in kg/ha.
- pH is expected on the standard 0–14 scale.
- These thresholds are for soil-test interpretation.
- They must NOT be applied directly to the crop ML
  dataset without confirming unit compatibility.
"""


# --------------------------------------------------
# Nutrient classification thresholds
# --------------------------------------------------

NITROGEN_THRESHOLDS = {
    "low_max": 280,
    "medium_max": 560,
}


PHOSPHORUS_THRESHOLDS = {
    "low_max": 10,
    "medium_max": 25,
    "high_max": 50,
}


POTASSIUM_THRESHOLDS = {
    "low_max": 120,
    "medium_max": 280,
    "high_max": 600,
}


# --------------------------------------------------
# Nutrient classifiers
# --------------------------------------------------

def classify_nitrogen(value):
    """
    Classify nitrogen concentration in kg/ha.
    """

    if value < 0:
        raise ValueError("Nitrogen cannot be negative.")

    if value < NITROGEN_THRESHOLDS["low_max"]:
        return "Low"

    if value <= NITROGEN_THRESHOLDS["medium_max"]:
        return "Medium"

    return "High"


def classify_phosphorus(value):
    """
    Classify phosphorus concentration in kg/ha.
    """

    if value < 0:
        raise ValueError("Phosphorus cannot be negative.")

    if value < PHOSPHORUS_THRESHOLDS["low_max"]:
        return "Low"

    if value <= PHOSPHORUS_THRESHOLDS["medium_max"]:
        return "Medium"

    if value <= PHOSPHORUS_THRESHOLDS["high_max"]:
        return "High"

    return "Very High"


def classify_potassium(value):
    """
    Classify potassium concentration in kg/ha.
    """

    if value < 0:
        raise ValueError("Potassium cannot be negative.")

    if value < POTASSIUM_THRESHOLDS["low_max"]:
        return "Low"

    if value <= POTASSIUM_THRESHOLDS["medium_max"]:
        return "Medium"

    if value <= POTASSIUM_THRESHOLDS["high_max"]:
        return "High"

    return "Very High"


# --------------------------------------------------
# pH classifier
# --------------------------------------------------

def classify_ph(value):
    """
    Classify soil pH.

    This is a broad interpretation layer.
    Exact crop suitability will be handled separately
    by the crop recommendation system.
    """

    if not 0 <= value <= 14:
        raise ValueError("pH must be between 0 and 14.")

    if value < 5.5:
        return "Strongly Acidic"

    if value < 6.5:
        return "Moderately Acidic"

    if value <= 7.5:
        return "Neutral"

    if value <= 8.5:
        return "Moderately Alkaline"

    return "Strongly Alkaline"


# --------------------------------------------------
# Overall soil summary
# --------------------------------------------------

def analyze_soil(
    nitrogen,
    phosphorus,
    potassium,
    ph,
):
    """
    Analyze the main soil-test parameters.
    """

    nitrogen = float(nitrogen)
    phosphorus = float(phosphorus)
    potassium = float(potassium)
    ph = float(ph)

    analysis = {
        "nitrogen": {
            "value": nitrogen,
            "unit": "kg/ha",
            "status": classify_nitrogen(nitrogen),
        },
        "phosphorus": {
            "value": phosphorus,
            "unit": "kg/ha",
            "status": classify_phosphorus(phosphorus),
        },
        "potassium": {
            "value": potassium,
            "unit": "kg/ha",
            "status": classify_potassium(potassium),
        },
        "ph": {
            "value": ph,
            "unit": "pH",
            "status": classify_ph(ph),
        },
    }

    return analysis


# --------------------------------------------------
# Local test
# --------------------------------------------------

if __name__ == "__main__":

    result = analyze_soil(
        nitrogen=250,
        phosphorus=18,
        potassium=150,
        ph=6.8,
    )

    print("=" * 60)
    print("KISANAI SOIL ANALYSIS")
    print("=" * 60)

    for nutrient, details in result.items():

        print(
            f"\n{nutrient.title()}"
        )

        print(
            f"  Value  : {details['value']}"
        )

        print(
            f"  Unit   : {details['unit']}"
        )

        print(
            f"  Status : {details['status']}"
        )