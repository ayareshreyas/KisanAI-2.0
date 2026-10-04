"""
Tests for the KisanAI crop nutrient requirement database.

These tests verify:

1. All current ML crop classes have profiles.
2. Every profile contains N, P and K.
3. Values are numeric and non-negative.
4. Important researched profiles contain expected values.
5. Unknown crops are handled safely.
6. The supported crop list contains no duplicates.
"""

import unittest

from fertilizer.crop_requirements import (
    CROP_REQUIREMENTS,
    get_crop_requirements,
    get_supported_crops,
)


ML_CROPS = {
    "Apple",
    "Banana",
    "Blackgram",
    "Chickpea",
    "Coconut",
    "Coffee",
    "Cotton",
    "Grapes",
    "Jute",
    "Kidneybeans",
    "Lentil",
    "Maize",
    "Mango",
    "Mothbeans",
    "Mungbean",
    "Muskmelon",
    "Orange",
    "Papaya",
    "Pigeonpeas",
    "Pomegranate",
    "Rice",
    "Watermelon",
}


class TestCropRequirements(unittest.TestCase):

    def test_all_ml_crops_are_supported(self):
        """Every ML crop class should have a fertilizer profile."""

        supported = set(get_supported_crops())

        missing = ML_CROPS - supported

        self.assertFalse(
            missing,
            f"Missing fertilizer profiles: {sorted(missing)}",
        )

    def test_every_profile_has_required_nutrients(self):
        """Every crop profile must contain N, P and K."""

        for crop, requirements in CROP_REQUIREMENTS.items():

            self.assertEqual(
                set(requirements.keys()),
                {"N", "P", "K"},
                f"{crop} does not contain exactly N, P and K.",
            )

    def test_every_profile_has_numeric_non_negative_values(self):
        """N, P and K values must be valid non-negative numbers."""

        for crop, requirements in CROP_REQUIREMENTS.items():

            for nutrient in ("N", "P", "K"):

                value = requirements[nutrient]

                self.assertIsInstance(
                    value,
                    (int, float),
                    f"{crop} {nutrient} must be numeric.",
                )

                self.assertGreaterEqual(
                    value,
                    0,
                    f"{crop} {nutrient} cannot be negative.",
                )

    def test_rice_profile(self):
        """Verify the researched Rice baseline."""

        rice = get_crop_requirements("Rice")

        self.assertEqual(
            rice,
            {
                "N": 60.70,
                "P": 10.60,
                "K": 20.16,
            },
        )

    def test_maize_profile(self):
        """Verify the researched Maize baseline."""

        maize = get_crop_requirements("Maize")

        self.assertEqual(
            maize,
            {
                "N": 60.70,
                "P": 13.25,
                "K": 25.19,
            },
        )

    def test_cotton_profile(self):
        """Verify the TNAU acre-based Cotton baseline."""

        cotton = get_crop_requirements("Cotton")

        self.assertEqual(
            cotton,
            {
                "N": 24.00,
                "P": 5.24,
                "K": 9.96,
            },
        )

    def test_jute_profile(self):
        """Verify the researched Jute baseline."""

        jute = get_crop_requirements("Jute")

        self.assertEqual(
            jute,
            {
                "N": 8.09,
                "P": 3.53,
                "K": 6.72,
            },
        )

    def test_unknown_crop_returns_none(self):
        """Unknown crops should not silently receive a profile."""

        self.assertIsNone(
            get_crop_requirements("UnknownCrop")
        )

    def test_supported_crop_list_contains_no_duplicates(self):
        """The supported crop list should contain unique names."""

        supported = get_supported_crops()

        self.assertEqual(
            len(supported),
            len(set(supported)),
        )


if __name__ == "__main__":
    unittest.main()
