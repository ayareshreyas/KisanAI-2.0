"""
KisanAI Fertilizer Optimizer Scenario Tests

This program prints the actual fertilizer combinations selected
by the optimizer for different nutrient-deficit scenarios.

Purpose:
- Inspect optimizer behavior.
- Verify nutrient coverage.
- Observe fertilizer quantities.
- Compare estimated costs.
- Identify unusual optimization results before integration.

Important:
These are mathematical optimization results, not real-world
fertilizer application prescriptions.
"""

from fertilizer.fertilizer_optimizer import optimize_fertilizers


def print_scenario(name, deficit):
    """Run and display one fertilizer optimization scenario."""

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("\nNutrient deficit:")
    print(deficit)

    result = optimize_fertilizers(deficit)

    if not result["success"]:
        print("\nOptimization failed:")
        print(result["message"])
        return

    print("\nSelected fertilizers:")

    if not result["selected_fertilizers"]:
        print("  No fertilizer required.")
    else:
        for fertilizer in result["selected_fertilizers"]:

            print(f"\n  {fertilizer['fertilizer']}")

            print(
                f"    Quantity: "
                f"{fertilizer['quantity_kg']} kg"
            )

            print(
                f"    Price: "
                f"₹{fertilizer['price_per_kg']}/kg"
            )

            print(
                f"    Estimated cost: "
                f"₹{fertilizer['estimated_cost']}"
            )

            print(
                f"    Composition: "
                f"{fertilizer['composition']}"
            )

            print(
                f"    Nutrients supplied: "
                f"{fertilizer['nutrients_supplied']}"
            )

    print("\nTotal nutrients required:")
    print(result["nutrients_required"])

    print("\nTotal nutrients supplied:")
    print(result["nutrients_supplied"])

    print("\nNutrient surplus:")
    print(result["nutrient_surplus"])

    print(
        f"\nTotal estimated cost: "
        f"₹{result['total_cost']}"
    )


def main():
    """Run all optimizer scenarios."""

    print("=" * 70)
    print("KISANAI FERTILIZER OPTIMIZER - SCENARIO ANALYSIS")
    print("=" * 70)

    # Scenario 1:
    # Only nitrogen is deficient.
    print_scenario(
        "SCENARIO 1 — Nitrogen Only",
        {
            "N": 40,
            "P": 0,
            "K": 0,
        },
    )

    # Scenario 2:
    # Only phosphorus is deficient.
    print_scenario(
        "SCENARIO 2 — Phosphorus Only",
        {
            "N": 0,
            "P": 30,
            "K": 0,
        },
    )

    # Scenario 3:
    # Only potassium is deficient.
    print_scenario(
        "SCENARIO 3 — Potassium Only",
        {
            "N": 0,
            "P": 0,
            "K": 30,
        },
    )

    # Scenario 4:
    # Nitrogen and phosphorus are deficient.
    print_scenario(
        "SCENARIO 4 — Nitrogen + Phosphorus",
        {
            "N": 40,
            "P": 10,
            "K": 0,
        },
    )

    # Scenario 5:
    # All three major nutrients are deficient.
    print_scenario(
        "SCENARIO 5 — Nitrogen + Phosphorus + Potassium",
        {
            "N": 60,
            "P": 30,
            "K": 40,
        },
    )

    # Scenario 6:
    # No nutrient deficit.
    print_scenario(
        "SCENARIO 6 — No Nutrient Deficit",
        {
            "N": 0,
            "P": 0,
            "K": 0,
        },
    )

    # Scenario 7:
    # Larger nutrient requirements.
    print_scenario(
        "SCENARIO 7 — Large Nutrient Deficit",
        {
            "N": 120,
            "P": 60,
            "K": 80,
        },
    )

    print("\n" + "=" * 70)
    print("SCENARIO ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()