"""
KisanAI Crop Nutrient Requirements

Stores the crop-specific NPK requirement values used
by the fertilizer recommendation engine.

Important:
- These are requirement values used by the prototype
  recommendation engine.
- They are expressed as kg per acre.
- They must not be confused with fertilizer NPK
  composition percentages or the crop ML dataset
  feature values.
"""

CROP_REQUIREMENTS = {
    "Rice": {
        "N": 120,
        "P": 60,
        "K": 60,
    },
    "Wheat": {
        "N": 100,
        "P": 50,
        "K": 50,
    },
    "Maize": {
        "N": 150,
        "P": 60,
        "K": 60,
    },
    "Sugarcane": {
        "N": 200,
        "P": 80,
        "K": 100,
    },
    "Cotton": {
        "N": 80,
        "P": 40,
        "K": 40,
    },
    "Soybean": {
        "N": 60,
        "P": 40,
        "K": 40,
    },
    "Potato": {
        "N": 100,
        "P": 60,
        "K": 80,
    },
    "Tomato": {
        "N": 80,
        "P": 50,
        "K": 60,
    },
    "Onion": {
        "N": 60,
        "P": 40,
        "K": 40,
    },
    "Chilli": {
        "N": 70,
        "P": 50,
        "K": 50,
    },
    "Brinjal": {
        "N": 60,
        "P": 40,
        "K": 40,
    },
    "Okra": {
        "N": 50,
        "P": 30,
        "K": 30,
    },
    "Cabbage": {
        "N": 80,
        "P": 50,
        "K": 60,
    },
    "Cauliflower": {
        "N": 80,
        "P": 50,
        "K": 60,
    },
    "Spinach": {
        "N": 40,
        "P": 20,
        "K": 20,
    },
}


def get_crop_requirements(crop):
    """
    Return NPK requirements for a crop.

    Returns:
        dict | None
    """
    return CROP_REQUIREMENTS.get(crop)


def get_supported_crops():
    """Return all crops supported by this engine."""
    return list(CROP_REQUIREMENTS.keys())


if __name__ == "__main__":
    print("=" * 60)
    print("KISANAI CROP NUTRIENT REQUIREMENTS")
    print("=" * 60)

    for crop, requirements in CROP_REQUIREMENTS.items():
        print(
            f"{crop:15} "
            f"N:{requirements['N']:>4} "
            f"P:{requirements['P']:>4} "
            f"K:{requirements['K']:>4} kg/acre"
        )