"""
KisanAI Fertilizer Optimizer

This module finds a mathematically cost-efficient combination
of fertilizers that can satisfy the calculated N, P and K
nutrient deficits.

Optimization method:
    Linear Programming using scipy.optimize.linprog

Important:
- This is mathematical decision-support logic.
- It is NOT a field-application prescription.
- Fertilizer quantities require agronomic validation before
  being used in real farming.
- Prices come from the prototype fertilizer database and
  are not guaranteed current market prices.
"""

from scipy.optimize import linprog

from .fertilizer_database import get_all_fertilizers


def optimize_fertilizers(deficit):
    """
    Find a fertilizer combination that satisfies the nutrient
    deficits at minimum estimated cost.

    Parameters:
        deficit:
            Dictionary containing required additional N, P and K.

            Example:
                {
                    "N": 40,
                    "P": 10,
                    "K": 0
                }

    Returns:
        Dictionary containing:
            - success
            - selected_fertilizers
            - nutrients_required
            - nutrients_supplied
            - nutrient_surplus
            - total_cost
    """

    nutrients = ("N", "P", "K")

    # Keep only positive nutrient deficits.
    required = {
        nutrient: max(0.0, float(deficit.get(nutrient, 0)))
        for nutrient in nutrients
    }

    # If there is no nutrient deficit, no fertilizer is required.
    if all(amount == 0 for amount in required.values()):
        return {
            "success": True,
            "selected_fertilizers": [],
            "nutrients_required": required,
            "nutrients_supplied": {
                nutrient: 0.0
                for nutrient in nutrients
            },
            "nutrient_surplus": {
                nutrient: 0.0
                for nutrient in nutrients
            },
            "total_cost": 0.0,
            "message": "No fertilizer is required based on the calculated nutrient deficits.",
        }

    fertilizers = get_all_fertilizers()
    fertilizer_names = list(fertilizers.keys())

    # Objective function:
    # Minimize total estimated fertilizer cost.
    costs = [
        fertilizers[name]["price_per_kg"]
        for name in fertilizer_names
    ]

    # linprog solves:
    #
    #     A_ub * x <= b_ub
    #
    # We need:
    #
    #     nutrient supplied >= nutrient required
    #
    # So we multiply both sides by -1:
    #
    #    -nutrient supplied <= -nutrient required

    constraint_matrix = []
    constraint_values = []

    for nutrient in nutrients:

        row = []

        for name in fertilizer_names:
            percentage = fertilizers[name][nutrient]

            # Example:
            # Urea contains 46% N.
            # 1 kg Urea supplies 0.46 kg N.
            nutrient_fraction = percentage / 100

            row.append(-nutrient_fraction)

        constraint_matrix.append(row)
        constraint_values.append(-required[nutrient])

    # Every fertilizer quantity must be >= 0.
    bounds = [
        (0, None)
        for _ in fertilizer_names
    ]

    result = linprog(
        c=costs,
        A_ub=constraint_matrix,
        b_ub=constraint_values,
        bounds=bounds,
        method="highs",
    )

    if not result.success:
        return {
            "success": False,
            "selected_fertilizers": [],
            "nutrients_required": required,
            "nutrients_supplied": {},
            "nutrient_surplus": {},
            "total_cost": None,
            "message": result.message,
        }

    selected_fertilizers = []

    nutrients_supplied = {
        nutrient: 0.0
        for nutrient in nutrients
    }

    total_cost = 0.0

    # Process the optimized quantities.
    for index, quantity in enumerate(result.x):

        # Ignore extremely tiny floating-point values.
        if quantity < 0.01:
            continue

        fertilizer_name = fertilizer_names[index]
        fertilizer = fertilizers[fertilizer_name]

        quantity = float(quantity)

        supplied = {}

        for nutrient in nutrients:
            nutrient_amount = (
                quantity * fertilizer[nutrient] / 100
            )

            supplied[nutrient] = round(
                nutrient_amount,
                2
            )

            nutrients_supplied[nutrient] += nutrient_amount

        cost = quantity * fertilizer["price_per_kg"]

        total_cost += cost

        selected_fertilizers.append({
            "fertilizer": fertilizer_name,
            "quantity_kg": round(quantity, 2),
            "price_per_kg": fertilizer["price_per_kg"],
            "estimated_cost": round(cost, 2),
            "composition": {
                "N": fertilizer["N"],
                "P": fertilizer["P"],
                "K": fertilizer["K"],
            },
            "nutrients_supplied": supplied,
        })

    # Calculate how much each nutrient is supplied above
    # the required amount.
    nutrient_surplus = {
        nutrient: round(
            max(
                0.0,
                nutrients_supplied[nutrient] - required[nutrient]
            ),
            2,
        )
        for nutrient in nutrients
    }

    nutrients_supplied = {
        nutrient: round(amount, 2)
        for nutrient, amount in nutrients_supplied.items()
    }

    return {
        "success": True,
        "selected_fertilizers": selected_fertilizers,
        "nutrients_required": required,
        "nutrients_supplied": nutrients_supplied,
        "nutrient_surplus": nutrient_surplus,
        "total_cost": round(total_cost, 2),
        "message": (
            "Fertilizer combination optimized mathematically "
            "to satisfy the calculated nutrient deficits."
        ),
    }


if __name__ == "__main__":

    print("=" * 60)
    print("KISANAI FERTILIZER OPTIMIZER")
    print("=" * 60)

    test_deficit = {
        "N": 40,
        "P": 10,
        "K": 0,
    }

    result = optimize_fertilizers(test_deficit)

    print("\nNutrient requirement:")
    print(result["nutrients_required"])

    print("\nSelected fertilizers:")

    for fertilizer in result["selected_fertilizers"]:

        print(
            f"\n{fertilizer['fertilizer']}"
        )

        print(
            f"  Quantity: "
            f"{fertilizer['quantity_kg']} kg"
        )

        print(
            f"  Cost: "
            f"₹{fertilizer['estimated_cost']}"
        )

        print(
            f"  Nutrients supplied: "
            f"{fertilizer['nutrients_supplied']}"
        )

    print("\nTotal nutrients supplied:")
    print(result["nutrients_supplied"])

    print("\nNutrient surplus:")
    print(result["nutrient_surplus"])

    print(
        f"\nTotal estimated cost: "
        f"₹{result['total_cost']}"
    )

    print("\nStatus:")
    print(result["message"])