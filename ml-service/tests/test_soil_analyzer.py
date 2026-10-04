from pathlib import Path
import sys


# --------------------------------------------------
# Allow importing from the project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


from soil.soil_analyzer import (
    classify_nitrogen,
    classify_phosphorus,
    classify_potassium,
    classify_ph,
)


# --------------------------------------------------
# Simple test helper
# --------------------------------------------------

def check(test_name, actual, expected):

    if actual != expected:

        print(f"FAIL: {test_name}")
        print(f"Expected: {expected}")
        print(f"Got     : {actual}")

        raise AssertionError(test_name)

    print(f"PASS: {test_name}")


# --------------------------------------------------
# Nitrogen tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("NITROGEN THRESHOLD TESTS")
print("=" * 60)

check(
    "N = 279 → Low",
    classify_nitrogen(279),
    "Low",
)

check(
    "N = 280 → Medium",
    classify_nitrogen(280),
    "Medium",
)

check(
    "N = 281 → Medium",
    classify_nitrogen(281),
    "Medium",
)

check(
    "N = 560 → Medium",
    classify_nitrogen(560),
    "Medium",
)

check(
    "N = 561 → High",
    classify_nitrogen(561),
    "High",
)


# --------------------------------------------------
# Phosphorus tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("PHOSPHORUS THRESHOLD TESTS")
print("=" * 60)

check(
    "P = 9 → Low",
    classify_phosphorus(9),
    "Low",
)

check(
    "P = 10 → Medium",
    classify_phosphorus(10),
    "Medium",
)

check(
    "P = 11 → Medium",
    classify_phosphorus(11),
    "Medium",
)

check(
    "P = 25 → Medium",
    classify_phosphorus(25),
    "Medium",
)

check(
    "P = 26 → High",
    classify_phosphorus(26),
    "High",
)

check(
    "P = 50 → High",
    classify_phosphorus(50),
    "High",
)

check(
    "P = 51 → Very High",
    classify_phosphorus(51),
    "Very High",
)


# --------------------------------------------------
# Potassium tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("POTASSIUM THRESHOLD TESTS")
print("=" * 60)

check(
    "K = 119 → Low",
    classify_potassium(119),
    "Low",
)

check(
    "K = 120 → Medium",
    classify_potassium(120),
    "Medium",
)

check(
    "K = 121 → Medium",
    classify_potassium(121),
    "Medium",
)

check(
    "K = 280 → Medium",
    classify_potassium(280),
    "Medium",
)

check(
    "K = 281 → High",
    classify_potassium(281),
    "High",
)

check(
    "K = 600 → High",
    classify_potassium(600),
    "High",
)

check(
    "K = 601 → Very High",
    classify_potassium(601),
    "Very High",
)


# --------------------------------------------------
# pH tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("pH THRESHOLD TESTS")
print("=" * 60)

check(
    "pH = 5.49 → Strongly Acidic",
    classify_ph(5.49),
    "Strongly Acidic",
)

check(
    "pH = 5.5 → Moderately Acidic",
    classify_ph(5.5),
    "Moderately Acidic",
)

check(
    "pH = 6.49 → Moderately Acidic",
    classify_ph(6.49),
    "Moderately Acidic",
)

check(
    "pH = 6.5 → Neutral",
    classify_ph(6.5),
    "Neutral",
)

check(
    "pH = 7.5 → Neutral",
    classify_ph(7.5),
    "Neutral",
)

check(
    "pH = 7.51 → Moderately Alkaline",
    classify_ph(7.51),
    "Moderately Alkaline",
)

check(
    "pH = 8.5 → Moderately Alkaline",
    classify_ph(8.5),
    "Moderately Alkaline",
)

check(
    "pH = 8.51 → Strongly Alkaline",
    classify_ph(8.51),
    "Strongly Alkaline",
)


# --------------------------------------------------
# Negative-value tests
# --------------------------------------------------

print("\n" + "=" * 60)
print("INVALID VALUE TESTS")
print("=" * 60)


def expect_error(test_name, function, value):

    try:

        function(value)

    except ValueError:

        print(f"PASS: {test_name}")
        return

    raise AssertionError(
        f"{test_name} should have raised ValueError"
    )


expect_error(
    "Negative nitrogen rejected",
    classify_nitrogen,
    -1,
)

expect_error(
    "Negative phosphorus rejected",
    classify_phosphorus,
    -1,
)

expect_error(
    "Negative potassium rejected",
    classify_potassium,
    -1,
)

expect_error(
    "pH below 0 rejected",
    classify_ph,
    -1,
)

expect_error(
    "pH above 14 rejected",
    classify_ph,
    15,
)


# --------------------------------------------------
# Final result
# --------------------------------------------------

print("\n" + "=" * 60)
print("ALL SOIL ANALYZER TESTS PASSED")
print("=" * 60)