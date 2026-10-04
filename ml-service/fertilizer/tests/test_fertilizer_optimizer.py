"""
KisanAI Fertilizer Optimizer Tests

Tests the fertilizer optimization layer against several
different nutrient-deficit scenarios.

These tests verify mathematical behavior only.
They do not validate real-world agricultural application rates.
"""

from fertilizer.fertilizer_optimizer import optimize_fertilizers


def check_result(result, expected_deficit):
    """Validate the basic structure and nutrient coverage."""

    assert result["success"] is True

    for nutrient in ("N", "P", "K"):
        required = expected_deficit[nutrient]
        supplied = result["nutrients_supplied"][nutrient]

        # The optimizer must supply at least the required amount.
        assert supplied >= required - 0.01, (
            f"{nutrient} requirement not satisfied: "
            f"required={required}, supplied={supplied}"
        )

    assert result["total_cost"] >= 0


def test_nitrogen_only():
    """Test a deficit containing only nitrogen."""

    deficit = {
        "N": 40,
        "P": 0,
        "K": 0,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("\n✓ Nitrogen-only test passed")


def test_phosphorus_only():
    """Test a deficit containing only phosphorus."""

    deficit = {
        "N": 0,
        "P": 30,
        "K": 0,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("✓ Phosphorus-only test passed")


def test_potassium_only():
    """Test a deficit containing only potassium."""

    deficit = {
        "N": 0,
        "P": 0,
        "K": 30,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("✓ Potassium-only test passed")


def test_nitrogen_and_phosphorus():
    """Test simultaneous N and P deficits."""

    deficit = {
        "N": 40,
        "P": 10,
        "K": 0,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("✓ Nitrogen + phosphorus test passed")


def test_all_nutrients():
    """Test simultaneous N, P and K deficits."""

    deficit = {
        "N": 60,
        "P": 30,
        "K": 40,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("✓ N + P + K test passed")


def test_no_deficit():
    """Test the case where no fertilizer is required."""

    deficit = {
        "N": 0,
        "P": 0,
        "K": 0,
    }

    result = optimize_fertilizers(deficit)

    assert result["success"] is True
    assert result["selected_fertilizers"] == []
    assert result["total_cost"] == 0.0

    print("✓ No-deficit test passed")


def test_larger_deficit():
    """Test a larger nutrient requirement."""

    deficit = {
        "N": 120,
        "P": 60,
        "K": 80,
    }

    result = optimize_fertilizers(deficit)

    check_result(result, deficit)

    print("✓ Larger-deficit test passed")


def run_all_tests():
    """Run all optimizer tests."""

    print("=" * 60)
    print("KISANAI FERTILIZER OPTIMIZER TESTS")
    print("=" * 60)

    test_nitrogen_only()
    test_phosphorus_only()
    test_potassium_only()
    test_nitrogen_and_phosphorus()
    test_all_nutrients()
    test_no_deficit()
    test_larger_deficit()

    print("\n" + "=" * 60)
    print("ALL FERTILIZER OPTIMIZER TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()