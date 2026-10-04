"""
KisanAI Budget-Aware Fertilizer Optimizer Tests

These tests verify that the budget-aware optimizer:

1. Respects the farmer's maximum budget.
2. Balances N, P and K coverage.
3. Handles limited budgets.
4. Handles zero budget.
5. Handles no nutrient deficit.
6. Handles individual nutrient deficits.
7. Rejects invalid budgets.
8. Calculates nutrient coverage correctly.

These tests validate mathematical/software behavior only.
They do not validate real-world agricultural application rates.
"""

from fertilizer.budget_optimizer import (
    optimize_with_budget,
)


def test_budget_is_not_exceeded():
    """The optimizer must never exceed the specified budget."""

    budget = 4000

    result = optimize_with_budget(
        deficit={
            "N": 60,
            "P": 30,
            "K": 40,
        },
        budget=budget,
    )

    assert result["success"] is True
    assert result["total_cost"] <= budget

    print("✓ Budget limit test passed")


def test_balanced_nutrient_coverage():
    """
    Verify that N, P and K receive balanced coverage
    when all three nutrients are deficient.
    """

    result = optimize_with_budget(
        deficit={
            "N": 60,
            "P": 30,
            "K": 40,
        },
        budget=4000,
    )

    coverage = result["coverage_percentage"]

    # All three nutrients should receive meaningful coverage.
    assert coverage["N"] > 0
    assert coverage["P"] > 0
    assert coverage["K"] > 0

    # Coverage should be approximately balanced.
    max_coverage = max(coverage.values())
    min_coverage = min(coverage.values())

    assert max_coverage - min_coverage < 1.0

    print("✓ Balanced nutrient coverage test passed")


def test_limited_budget():
    """
    A limited budget should produce a partial recommendation
    without exceeding the available budget.
    """

    budget = 1000

    result = optimize_with_budget(
        deficit={
            "N": 60,
            "P": 30,
            "K": 40,
        },
        budget=budget,
    )

    assert result["success"] is True

    assert result["total_cost"] <= budget

    assert result["remaining_budget"] >= 0

    # At least some nutrient coverage should be achieved.
    supplied = result["nutrients_supplied"]

    total_supplied = (
        supplied["N"]
        + supplied["P"]
        + supplied["K"]
    )

    assert total_supplied > 0

    print("✓ Limited-budget test passed")


def test_zero_budget():
    """
    With a zero budget, the optimizer cannot purchase
    fertilizer.
    """

    result = optimize_with_budget(
        deficit={
            "N": 60,
            "P": 30,
            "K": 40,
        },
        budget=0,
    )

    assert result["success"] is True

    assert result["total_cost"] == 0.0

    assert result["remaining_budget"] == 0.0

    assert result["selected_fertilizers"] == []

    assert result["nutrients_supplied"] == {
        "N": 0.0,
        "P": 0.0,
        "K": 0.0,
    }

    print("✓ Zero-budget test passed")


def test_no_nutrient_deficit():
    """
    If no nutrients are deficient, fertilizer should not
    be recommended even when a budget is available.
    """

    result = optimize_with_budget(
        deficit={
            "N": 0,
            "P": 0,
            "K": 0,
        },
        budget=4000,
    )

    assert result["success"] is True

    assert result["selected_fertilizers"] == []

    assert result["total_cost"] == 0.0

    assert result["remaining_budget"] == 4000.0

    assert result["coverage_percentage"] == {
        "N": 100.0,
        "P": 100.0,
        "K": 100.0,
    }

    print("✓ No-deficit test passed")


def test_n_only_deficit():
    """Test optimization when only nitrogen is deficient."""

    result = optimize_with_budget(
        deficit={
            "N": 40,
            "P": 0,
            "K": 0,
        },
        budget=2000,
    )

    assert result["success"] is True

    assert result["nutrients_supplied"]["N"] > 0

    assert result["coverage_percentage"]["N"] > 0

    assert result["total_cost"] <= 2000

    print("✓ N-only deficit test passed")


def test_p_only_deficit():
    """Test optimization when only phosphorus is deficient."""

    result = optimize_with_budget(
        deficit={
            "N": 0,
            "P": 30,
            "K": 0,
        },
        budget=2000,
    )

    assert result["success"] is True

    assert result["nutrients_supplied"]["P"] > 0

    assert result["coverage_percentage"]["P"] > 0

    assert result["total_cost"] <= 2000

    print("✓ P-only deficit test passed")


def test_k_only_deficit():
    """Test optimization when only potassium is deficient."""

    result = optimize_with_budget(
        deficit={
            "N": 0,
            "P": 0,
            "K": 30,
        },
        budget=2000,
    )

    assert result["success"] is True

    assert result["nutrients_supplied"]["K"] > 0

    assert result["coverage_percentage"]["K"] > 0

    assert result["total_cost"] <= 2000

    print("✓ K-only deficit test passed")


def test_negative_budget_rejected():
    """Negative budgets must raise a ValueError."""

    try:

        optimize_with_budget(
            deficit={
                "N": 40,
                "P": 20,
                "K": 20,
            },
            budget=-100,
        )

        assert False, (
            "Negative budget should raise ValueError."
        )

    except ValueError:

        pass

    print("✓ Negative-budget validation test passed")


def test_coverage_calculation():
    """Verify nutrient coverage percentages."""

    result = optimize_with_budget(
        deficit={
            "N": 60,
            "P": 30,
            "K": 40,
        },
        budget=4000,
    )

    required = result["nutrients_required"]
    supplied = result["nutrients_supplied"]
    coverage = result["coverage_percentage"]

    for nutrient in ("N", "P", "K"):

        expected = (
            supplied[nutrient]
            / required[nutrient]
        ) * 100

        expected = min(
            100.0,
            expected
        )

        assert abs(
            coverage[nutrient] - expected
        ) < 0.1

    print("✓ Coverage-calculation test passed")


def run_all_tests():
    """Run the complete budget optimizer test suite."""

    print("=" * 70)
    print("KISANAI BUDGET OPTIMIZER TESTS")
    print("=" * 70)

    test_budget_is_not_exceeded()
    test_balanced_nutrient_coverage()
    test_limited_budget()
    test_zero_budget()
    test_no_nutrient_deficit()
    test_n_only_deficit()
    test_p_only_deficit()
    test_k_only_deficit()
    test_negative_budget_rejected()
    test_coverage_calculation()

    print("\n" + "=" * 70)
    print("ALL BUDGET OPTIMIZER TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()