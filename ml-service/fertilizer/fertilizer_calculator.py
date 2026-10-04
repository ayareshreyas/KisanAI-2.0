"""
KisanAI Fertilizer Calculator

This module calculates the theoretical quantity of fertilizer
needed to supply a given nutrient deficit.

Important:
- This is a mathematical nutrient-content calculation.
- It is NOT a field application prescription.
- Actual fertilizer recommendations require agronomic validation,
  soil-test interpretation, crop stage, local conditions, and
  appropriate extension guidance.
"""


def calculate_quantity_for_nutrient(
    nutrient_deficit,
    fertilizer_percentage
):
    """
    Calculate the fertilizer quantity needed to supply
    a given nutrient deficit.

    Formula:
        quantity = nutrient_deficit / (fertilizer_percentage / 100)

    Example:
        40 kg N deficit
        Urea contains 46% N

        40 / 0.46 = 86.96 kg Urea
    """

    if nutrient_deficit < 0:
        raise ValueError("Nutrient deficit cannot be negative.")

    if fertilizer_percentage <= 0:
        raise ValueError(
            "Fertilizer nutrient percentage must be greater than 0."
        )

    quantity = nutrient_deficit / (fertilizer_percentage / 100)

    return round(quantity, 2)


if __name__ == "__main__":
    print("=" * 60)
    print("KISANAI FERTILIZER QUANTITY CALCULATOR")
    print("=" * 60)

    nutrient_deficit = 40
    fertilizer_percentage = 46

    quantity = calculate_quantity_for_nutrient(
        nutrient_deficit,
        fertilizer_percentage
    )

    print(f"\nNutrient deficit: {nutrient_deficit} kg")
    print(f"Fertilizer nutrient content: {fertilizer_percentage}%")
    print(f"Required fertilizer quantity: {quantity} kg")