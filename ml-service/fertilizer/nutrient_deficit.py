"""
KisanAI Nutrient Deficit Calculator

Calculates the difference between a crop's nutrient
requirements and the available soil-test nutrients.

Important:
- Soil nutrient values are expected in kg/acre for
  this prototype calculation.
- These values must come from a compatible soil-test
  interpretation layer.
- A deficit of zero means no additional nutrient is
  requested by this calculation.
"""

from .crop_requirements import get_crop_requirements


def calculate_nutrient_deficit(
    crop,
    nitrogen,
    phosphorus,
    potassium,
):
    """
    Calculate N, P and K deficits for a selected crop.

    Returns:
        dict containing:
            required
            available
            deficit
    """

    requirements = get_crop_requirements(crop)

    if requirements is None:
        raise ValueError(
            f"Unsupported crop: {crop}"
        )

    nitrogen = float(nitrogen)
    phosphorus = float(phosphorus)
    potassium = float(potassium)

    if nitrogen < 0 or phosphorus < 0 or potassium < 0:
        raise ValueError(
            "Soil nutrient values cannot be negative."
        )

    deficit = {
        "N": max(
            0,
            requirements["N"] - nitrogen,
        ),
        "P": max(
            0,
            requirements["P"] - phosphorus,
        ),
        "K": max(
            0,
            requirements["K"] - potassium,
        ),
    }

    return {
        "required": {
            "N": requirements["N"],
            "P": requirements["P"],
            "K": requirements["K"],
        },
        "available": {
            "N": nitrogen,
            "P": phosphorus,
            "K": potassium,
        },
        "deficit": deficit,
    }


if __name__ == "__main__":
    result = calculate_nutrient_deficit(
        crop="Rice",
        nitrogen=80,
        phosphorus=50,
        potassium=70,
    )

    print("=" * 60)
    print("KISANAI NUTRIENT DEFICIT ANALYSIS")
    print("=" * 60)

    print("\nCrop: Rice")

    print("\nRequired:")
    print(result["required"])

    print("\nAvailable:")
    print(result["available"])

    print("\nDeficit:")
    print(result["deficit"])