"""
KisanAI Fertilizer Recommendation Engine

This module provides the main entry point for fertilizer
recommendations.

Workflow:

    Crop
      ↓
    Soil N/P/K
      ↓
    Nutrient Deficit
      ↓
    ┌───────────────────────────────┐
    │ Budget provided?              │
    │                               │
    │ YES → Budget-aware optimizer  │
    │ NO  → Cost optimizer          │
    └───────────────────────────────┘
      ↓
    Fertilizer Recommendation

Important:
- Fertilizer quantities are mathematical optimization results.
- They are NOT field-application prescriptions.
- Real agricultural recommendations require validation using
  appropriate agronomic guidance, soil-test interpretation,
  crop stage, local conditions and fertilizer practices.
- Prices are prototype values and are not guaranteed current
  market prices.
"""

from .nutrient_deficit import calculate_nutrient_deficit
from .fertilizer_optimizer import optimize_fertilizers
from .budget_optimizer import optimize_with_budget


def generate_fertilizer_recommendation(
    crop,
    soil_n,
    soil_p,
    soil_k,
    budget=None,
):
    """
    Generate a fertilizer recommendation.

    Parameters:
        crop:
            Crop name.

        soil_n:
            Soil nitrogen value.

        soil_p:
            Soil phosphorus value.

        soil_k:
            Soil potassium value.

        budget:
            Optional maximum fertilizer budget in rupees.

            If None:
                Standard cost optimizer is used.

            If provided:
                Budget-aware optimizer is used.

    Returns:
        Dictionary containing:

        - crop
        - soil
        - crop_requirements
        - nutrient_deficit
        - fertilizer_optimization
        - optimization_mode
    """

    # ---------------------------------------------------------
    # STEP 1
    # Convert soil values to numeric values.
    # ---------------------------------------------------------

    soil_values = {
        "N": float(soil_n),
        "P": float(soil_p),
        "K": float(soil_k),
    }

    # ---------------------------------------------------------
    # STEP 2
    # Calculate crop requirements and nutrient deficits.
    # ---------------------------------------------------------

    nutrient_analysis = calculate_nutrient_deficit(
        crop,
        soil_values["N"],
        soil_values["P"],
        soil_values["K"],
    )

    # ---------------------------------------------------------
    # STEP 3
    # Extract nutrient deficit.
    # ---------------------------------------------------------

    deficit = nutrient_analysis["deficit"]

    # ---------------------------------------------------------
    # STEP 4
    # Select optimization strategy.
    # ---------------------------------------------------------

    if budget is not None:

        budget = float(budget)

        optimization = optimize_with_budget(
            deficit=deficit,
            budget=budget,
        )

        optimization_mode = "budget_aware"

    else:

        optimization = optimize_fertilizers(
            deficit=deficit
        )

        optimization_mode = "cost_minimization"

    # ---------------------------------------------------------
    # STEP 5
    # Return complete recommendation.
    # ---------------------------------------------------------

    return {
        "crop": crop,

        "soil": soil_values,

        "crop_requirements": (
            nutrient_analysis["required"]
        ),

        "nutrient_deficit": deficit,

        "fertilizer_optimization": optimization,

        "optimization_mode": optimization_mode,
    }


if __name__ == "__main__":

    print("=" * 70)
    print("KISANAI FERTILIZER RECOMMENDATION ENGINE")
    print("=" * 70)

    # ---------------------------------------------------------
    # Example 1:
    # No farmer budget.
    # ---------------------------------------------------------

    print("\n\nEXAMPLE 1 — NO BUDGET")
    print("-" * 70)

    result = generate_fertilizer_recommendation(
        crop="Rice",
        soil_n=80,
        soil_p=50,
        soil_k=70,
    )

    print("\nCrop:")
    print(result["crop"])

    print("\nNutrient deficit:")
    print(result["nutrient_deficit"])

    print("\nOptimization mode:")
    print(result["optimization_mode"])

    print("\nFertilizer recommendation:")

    for fertilizer in result[
        "fertilizer_optimization"
    ]["selected_fertilizers"]:

        print(
            f"  {fertilizer['fertilizer']}: "
            f"{fertilizer['quantity_kg']} kg "
            f"→ ₹{fertilizer['estimated_cost']}"
        )

    print(
        "\nTotal estimated cost: "
        f"₹{result['fertilizer_optimization']['total_cost']}"
    )

    # ---------------------------------------------------------
    # Example 2:
    # Farmer provides a ₹4,000 budget.
    # ---------------------------------------------------------

    print("\n\nEXAMPLE 2 — ₹4,000 BUDGET")
    print("-" * 70)

    result = generate_fertilizer_recommendation(
        crop="Rice",
        soil_n=60,
        soil_p=30,
        soil_k=20,
        budget=4000,
    )

    print("\nCrop:")
    print(result["crop"])

    print("\nNutrient deficit:")
    print(result["nutrient_deficit"])

    print("\nOptimization mode:")
    print(result["optimization_mode"])

    optimization = result[
        "fertilizer_optimization"
    ]

    print("\nFertilizer recommendation:")

    for fertilizer in optimization[
        "selected_fertilizers"
    ]:

        print(
            f"  {fertilizer['fertilizer']}: "
            f"{fertilizer['quantity_kg']} kg "
            f"→ ₹{fertilizer['estimated_cost']}"
        )

    print("\nNutrients supplied:")
    print(
        optimization["nutrients_supplied"]
    )

    if "coverage_percentage" in optimization:

        print("\nNutrient coverage:")

        for nutrient, percentage in optimization[
            "coverage_percentage"
        ].items():

            print(
                f"  {nutrient}: "
                f"{percentage}%"
            )

    print(
        "\nTotal estimated cost: "
        f"₹{optimization['total_cost']}"
    )

    if "remaining_budget" in optimization:

        print(
            "Remaining budget: "
            f"₹{optimization['remaining_budget']}"
        )

    if "remaining_deficit" in optimization:

        print("\nRemaining nutrient deficit:")
        print(
            optimization["remaining_deficit"]
        )

    print("\nStatus:")
    print(
        optimization["message"]
    )