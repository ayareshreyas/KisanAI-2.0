"""
KisanAI Budget-Aware Fertilizer Optimizer

This module finds a fertilizer combination that works within
a farmer's specified maximum budget.

Optimization strategy:
    Maximize the minimum percentage of N, P and K requirements
    that can be satisfied within the available budget.

Example:

    Required:
        N = 60 kg
        P = 30 kg
        K = 40 kg

    Budget:
        ₹4000

The optimizer tries to balance the nutrient coverage instead
of spending the entire budget on only one nutrient.

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


def optimize_with_budget(deficit, budget):
    """
    Find a balanced fertilizer combination within the budget.

    Parameters:
        deficit:
            Dictionary containing required additional N, P and K.

            Example:
                {
                    "N": 60,
                    "P": 30,
                    "K": 40
                }

        budget:
            Maximum amount of money available in rupees.

    Returns:
        Dictionary containing:
            - success
            - budget
            - total_cost
            - remaining_budget
            - nutrients_required
            - nutrients_supplied
            - remaining_deficit
            - coverage_percentage
            - selected_fertilizers
    """

    # ---------------------------------------------------------
    # STEP 1
    # Validate the budget.
    # ---------------------------------------------------------

    if budget < 0:
        raise ValueError("Budget cannot be negative.")

    # ---------------------------------------------------------
    # STEP 2
    # Normalize nutrient deficits.
    # ---------------------------------------------------------

    nutrients = ("N", "P", "K")

    required = {
        nutrient: max(
            0.0,
            float(deficit.get(nutrient, 0))
        )
        for nutrient in nutrients
    }

    # ---------------------------------------------------------
    # STEP 3
    # No nutrient deficit means no fertilizer is required.
    # ---------------------------------------------------------

    if all(amount == 0 for amount in required.values()):

        return {
            "success": True,
            "budget": float(budget),
            "total_cost": 0.0,
            "remaining_budget": float(budget),

            "nutrients_required": required,

            "nutrients_supplied": {
                nutrient: 0.0
                for nutrient in nutrients
            },

            "remaining_deficit": {
                nutrient: 0.0
                for nutrient in nutrients
            },

            "coverage_percentage": {
                nutrient: 100.0
                for nutrient in nutrients
            },

            "selected_fertilizers": [],

            "message": (
                "No fertilizer is required based on "
                "the calculated nutrient deficits."
            ),
        }

    # ---------------------------------------------------------
    # STEP 4
    # Load fertilizer database.
    # ---------------------------------------------------------

    fertilizers = get_all_fertilizers()

    fertilizer_names = list(
        fertilizers.keys()
    )

    # ---------------------------------------------------------
    # STEP 5
    #
    # Introduce an additional optimization variable:
    #
    #     t = minimum nutrient coverage fraction
    #
    # We maximize t.
    #
    # For every deficient nutrient:
    #
    #     supplied nutrient >= t × required nutrient
    #
    # Therefore the optimizer tries to make the N, P and K
    # coverage as balanced as possible.
    # ---------------------------------------------------------

    # Variables:
    #
    # x1, x2, x3, ... = fertilizer quantities
    #
    # t = minimum coverage fraction
    #
    # Example:
    #
    # t = 0.64
    #
    # means the optimizer is trying to satisfy at least
    # 64% of every required nutrient.

    objective = (
        [0.0] * len(fertilizer_names)
        + [-1.0]
    )

    # ---------------------------------------------------------
    # STEP 6
    # Build linear constraints.
    # ---------------------------------------------------------

    constraint_matrix = []
    constraint_values = []

    # ---------------------------------------------------------
    # Budget constraint:
    #
    # sum(quantity × price) <= budget
    # ---------------------------------------------------------

    budget_row = [
        fertilizers[name]["price_per_kg"]
        for name in fertilizer_names
    ]

    budget_row.append(0.0)

    constraint_matrix.append(
        budget_row
    )

    constraint_values.append(
        float(budget)
    )

    # ---------------------------------------------------------
    # Nutrient coverage constraints.
    #
    # We need:
    #
    # supplied >= t × required
    #
    # Rearranged:
    #
    # t × required - supplied <= 0
    # ---------------------------------------------------------

    for nutrient in nutrients:

        row = []

        for name in fertilizer_names:

            nutrient_fraction = (
                fertilizers[name][nutrient]
                / 100
            )

            row.append(
                -nutrient_fraction
            )

        # Coefficient of t.
        row.append(
            required[nutrient]
        )

        constraint_matrix.append(row)

        constraint_values.append(0.0)

    # ---------------------------------------------------------
    # STEP 7
    #
    # Fertilizer quantities must be >= 0.
    #
    # Coverage fraction t is restricted to 0–1.
    #
    # t = 1 means 100% of every nutrient requirement.
    # ---------------------------------------------------------

    bounds = [
        (0, None)
        for _ in fertilizer_names
    ]

    bounds.append(
        (0, 1)
    )

    # ---------------------------------------------------------
    # STEP 8
    # Solve optimization problem.
    # ---------------------------------------------------------

    result = linprog(
        c=objective,
        A_ub=constraint_matrix,
        b_ub=constraint_values,
        bounds=bounds,
        method="highs",
    )

    if not result.success:

        return {
            "success": False,
            "budget": float(budget),
            "total_cost": None,
            "remaining_budget": None,
            "nutrients_required": required,
            "nutrients_supplied": {},
            "remaining_deficit": required,
            "coverage_percentage": {},
            "selected_fertilizers": [],
            "message": result.message,
        }

    # ---------------------------------------------------------
    # STEP 9
    # Calculate actual fertilizer quantities.
    # ---------------------------------------------------------

    selected_fertilizers = []

    nutrients_supplied = {
        nutrient: 0.0
        for nutrient in nutrients
    }

    total_cost = 0.0

    for index, quantity in enumerate(
        result.x[:-1]
    ):

        # Ignore tiny floating-point values.
        if quantity < 0.01:
            continue

        fertilizer_name = (
            fertilizer_names[index]
        )

        fertilizer = (
            fertilizers[fertilizer_name]
        )

        quantity = float(quantity)

        supplied = {}

        for nutrient in nutrients:

            nutrient_amount = (
                quantity
                * fertilizer[nutrient]
                / 100
            )

            supplied[nutrient] = round(
                nutrient_amount,
                2
            )

            nutrients_supplied[nutrient] += (
                nutrient_amount
            )

        cost = (
            quantity
            * fertilizer["price_per_kg"]
        )

        total_cost += cost

        selected_fertilizers.append({
            "fertilizer": fertilizer_name,

            "quantity_kg": round(
                quantity,
                2
            ),

            "price_per_kg": (
                fertilizer["price_per_kg"]
            ),

            "estimated_cost": round(
                cost,
                2
            ),

            "composition": {
                "N": fertilizer["N"],
                "P": fertilizer["P"],
                "K": fertilizer["K"],
            },

            "nutrients_supplied": supplied,
        })

    # ---------------------------------------------------------
    # STEP 10
    # Round supplied nutrients.
    # ---------------------------------------------------------

    nutrients_supplied = {
        nutrient: round(
            amount,
            2
        )
        for nutrient, amount
        in nutrients_supplied.items()
    }

    # ---------------------------------------------------------
    # STEP 11
    # Calculate remaining nutrient deficit.
    # ---------------------------------------------------------

    remaining_deficit = {
        nutrient: round(
            max(
                0.0,
                required[nutrient]
                - nutrients_supplied[nutrient]
            ),
            2,
        )
        for nutrient in nutrients
    }

    # ---------------------------------------------------------
    # STEP 12
    # Calculate nutrient coverage percentages.
    # ---------------------------------------------------------

    coverage_percentage = {}

    for nutrient in nutrients:

        if required[nutrient] == 0:

            coverage_percentage[nutrient] = 100.0

        else:

            coverage = (
                nutrients_supplied[nutrient]
                / required[nutrient]
            ) * 100

            # Do not report more than 100% as requirement
            # coverage.
            coverage = min(
                100.0,
                coverage
            )

            coverage_percentage[nutrient] = round(
                coverage,
                2
            )

    # ---------------------------------------------------------
    # STEP 13
    # Calculate total and remaining budget.
    # ---------------------------------------------------------

    total_cost = round(
        total_cost,
        2
    )

    remaining_budget = round(
        max(
            0.0,
            budget - total_cost
        ),
        2,
    )

    # ---------------------------------------------------------
    # STEP 14
    # Determine recommendation status.
    # ---------------------------------------------------------

    all_requirements_satisfied = all(
        amount == 0
        for amount in remaining_deficit.values()
    )

    if all_requirements_satisfied:

        message = (
            "The nutrient requirements were satisfied "
            "within the specified budget."
        )

    else:

        message = (
            "The fertilizer combination was balanced "
            "within the specified budget, but some "
            "nutrient requirements remain unmet."
        )

    # ---------------------------------------------------------
    # STEP 15
    # Return final result.
    # ---------------------------------------------------------

    return {
        "success": True,

        "budget": float(budget),

        "total_cost": total_cost,

        "remaining_budget": (
            remaining_budget
        ),

        "nutrients_required": required,

        "nutrients_supplied": (
            nutrients_supplied
        ),

        "remaining_deficit": (
            remaining_deficit
        ),

        "coverage_percentage": (
            coverage_percentage
        ),

        "selected_fertilizers": (
            selected_fertilizers
        ),

        "message": message,
    }


if __name__ == "__main__":

    print("=" * 70)
    print("KISANAI BUDGET-AWARE FERTILIZER OPTIMIZER")
    print("=" * 70)

    test_deficit = {
        "N": 60,
        "P": 30,
        "K": 40,
    }

    budget = 4000

    result = optimize_with_budget(
        deficit=test_deficit,
        budget=budget,
    )

    print("\nNutrient requirements:")
    print(
        result["nutrients_required"]
    )

    print(
        f"\nMaximum budget: "
        f"₹{result['budget']}"
    )

    print("\nSelected fertilizers:")

    for fertilizer in result[
        "selected_fertilizers"
    ]:

        print(
            f"\n  {fertilizer['fertilizer']}"
        )

        print(
            f"    Quantity: "
            f"{fertilizer['quantity_kg']} kg"
        )

        print(
            f"    Cost: "
            f"₹{fertilizer['estimated_cost']}"
        )

        print(
            f"    Nutrients supplied: "
            f"{fertilizer['nutrients_supplied']}"
        )

    print("\nNutrients supplied:")

    print(
        result["nutrients_supplied"]
    )

    print("\nNutrient coverage:")

    for nutrient, percentage in result[
        "coverage_percentage"
    ].items():

        print(
            f"  {nutrient}: "
            f"{percentage}%"
        )

    print("\nRemaining nutrient deficit:")

    print(
        result["remaining_deficit"]
    )

    print(
        f"\nTotal estimated cost: "
        f"₹{result['total_cost']}"
    )

    print(
        f"Remaining budget: "
        f"₹{result['remaining_budget']}"
    )

    print("\nStatus:")

    print(
        result["message"]
    )