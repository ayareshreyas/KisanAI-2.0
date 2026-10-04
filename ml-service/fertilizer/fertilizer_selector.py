"""
KisanAI Fertilizer Selector

Selects fertilizer candidates based on the nutrients
identified as deficient.

This module does NOT calculate fertilizer dosage.
It only identifies fertilizer candidates.
"""

from .fertilizer_database import get_all_fertilizers


def get_deficient_nutrients(deficit):
    """Return nutrients with a positive deficit."""

    return {
        nutrient: amount
        for nutrient, amount in deficit.items()
        if amount > 0
    }


def select_fertilizers(deficit):
    """
    Select fertilizer candidates based on nutrient deficits.

    A fertilizer is considered a candidate when it contains
    at least one nutrient that is currently deficient.

    Returns:
        list of fertilizer candidate dictionaries
    """

    deficient_nutrients = get_deficient_nutrients(deficit)

    if not deficient_nutrients:
        return []

    fertilizers = get_all_fertilizers()
    candidates = []

    for name, composition in fertilizers.items():

        covered_nutrients = {}

        for nutrient, deficit_amount in deficient_nutrients.items():
            concentration = composition[nutrient]

            if concentration > 0:
                covered_nutrients[nutrient] = {
                    "deficit": deficit_amount,
                    "composition_percent": concentration,
                }

        if covered_nutrients:
            candidates.append({
                "name": name,
                "composition": composition,
                "covers": covered_nutrients,
            })

    return candidates


if __name__ == "__main__":
    test_deficit = {
        "N": 40,
        "P": 10,
        "K": 0,
    }

    candidates = select_fertilizers(test_deficit)

    print("=" * 60)
    print("KISANAI FERTILIZER CANDIDATES")
    print("=" * 60)

    print("\nNutrient deficit:")
    print(test_deficit)

    print("\nSuitable fertilizer candidates:")

    for fertilizer in candidates:
        print(f"\n{fertilizer['name']}")
        print(f"  Composition: {fertilizer['composition']}")
        print(f"  Covers: {fertilizer['covers']}")