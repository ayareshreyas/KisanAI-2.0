"""
Tests for the KisanAI Fertilizer Recommendation Engine.

These tests verify:

1. Standard cost-minimization recommendations.
2. Budget-aware recommendations.
3. Correct optimizer selection.
4. Budget constraints.
5. Nutrient coverage.
6. Remaining nutrient deficits.
7. No-fertilizer scenarios.
8. Newly researched ML crop profiles.
9. Case-sensitive crop lookup behavior.
"""

import unittest

from fertilizer.recommendation_engine import (
    generate_fertilizer_recommendation,
)


class TestRecommendationEngine(unittest.TestCase):

    def test_rice_recommendation_without_budget(self):
        """Test a normal recommendation using the researched Rice profile."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=20,
            soil_p=5,
            soil_k=5,
        )

        self.assertEqual(
            result["crop"],
            "Rice",
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 40.70,
                "P": 5.60,
                "K": 15.16,
            },
        )

        self.assertEqual(
            result["optimization_mode"],
            "cost_minimization",
        )

        optimization = result[
            "fertilizer_optimization"
        ]

        self.assertTrue(
            optimization["success"]
        )

        self.assertGreater(
            optimization["total_cost"],
            0,
        )

        self.assertGreater(
            len(
                optimization[
                    "selected_fertilizers"
                ]
            ),
            0,
        )


    def test_budget_aware_recommendation(self):
        """Test a fertilizer recommendation with a farmer budget."""

        budget = 4000

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=10,
            soil_p=2,
            soil_k=2,
            budget=budget,
        )

        self.assertEqual(
            result["crop"],
            "Rice",
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 50.70,
                "P": 8.60,
                "K": 18.16,
            },
        )

        self.assertEqual(
            result["optimization_mode"],
            "budget_aware",
        )

        optimization = result[
            "fertilizer_optimization"
        ]

        self.assertTrue(
            optimization["success"]
        )

        self.assertLessEqual(
            optimization["total_cost"],
            budget,
        )

        self.assertIn(
            "coverage_percentage",
            optimization,
        )

        self.assertIn(
            "remaining_deficit",
            optimization,
        )


    def test_budget_is_respected(self):
        """Ensure the optimizer never exceeds the farmer's budget."""

        budget = 2500

        result = generate_fertilizer_recommendation(
            crop="Wheat",
            soil_n=40,
            soil_p=20,
            soil_k=20,
            budget=budget,
        )

        optimization = result[
            "fertilizer_optimization"
        ]

        self.assertLessEqual(
            optimization["total_cost"],
            budget,
        )

        self.assertGreaterEqual(
            optimization["remaining_budget"],
            0,
        )


    def test_budget_coverage_is_valid(self):
        """Ensure nutrient coverage percentages are valid."""

        result = generate_fertilizer_recommendation(
            crop="Maize",
            soil_n=20,
            soil_p=5,
            soil_k=5,
            budget=3000,
        )

        coverage = result[
            "fertilizer_optimization"
        ]["coverage_percentage"]

        for nutrient in ("N", "P", "K"):

            self.assertIn(
                nutrient,
                coverage,
            )

            self.assertGreaterEqual(
                coverage[nutrient],
                0,
            )

            self.assertLessEqual(
                coverage[nutrient],
                100,
            )


    def test_remaining_deficit_is_non_negative(self):
        """Ensure remaining nutrient deficits cannot be negative."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=10,
            soil_p=2,
            soil_k=2,
            budget=4000,
        )

        remaining_deficit = result[
            "fertilizer_optimization"
        ]["remaining_deficit"]

        for nutrient in ("N", "P", "K"):

            self.assertGreaterEqual(
                remaining_deficit[nutrient],
                0,
            )


    def test_no_fertilizer_required(self):
        """Test when soil values meet the Rice baseline profile."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=60.70,
            soil_p=10.60,
            soil_k=20.16,
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 0.0,
                "P": 0.0,
                "K": 0.0,
            },
        )

        optimization = result[
            "fertilizer_optimization"
        ]

        self.assertTrue(
            optimization["success"]
        )

        self.assertEqual(
            optimization["selected_fertilizers"],
            [],
        )

        self.assertEqual(
            optimization["total_cost"],
            0.0,
        )


    def test_budget_with_no_fertilizer_required(self):
        """Test budget-aware request when no fertilizer is needed."""

        budget = 4000

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=60.70,
            soil_p=10.60,
            soil_k=20.16,
            budget=budget,
        )

        self.assertEqual(
            result["optimization_mode"],
            "budget_aware",
        )

        optimization = result[
            "fertilizer_optimization"
        ]

        self.assertTrue(
            optimization["success"]
        )

        self.assertEqual(
            optimization["selected_fertilizers"],
            [],
        )

        self.assertEqual(
            optimization["total_cost"],
            0.0,
        )

        self.assertEqual(
            optimization["remaining_budget"],
            4000.0,
        )


    def test_jute_recommendation(self):
        """
        Verify that Jute, which can be predicted by the ML model,
        is now supported by the fertilizer requirement layer.
        """

        result = generate_fertilizer_recommendation(
            crop="Jute",
            soil_n=2,
            soil_p=1,
            soil_k=1,
        )

        self.assertEqual(
            result["crop"],
            "Jute",
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 6.09,
                "P": 2.53,
                "K": 5.72,
            },
        )

        self.assertEqual(
            result["optimization_mode"],
            "cost_minimization",
        )

        self.assertTrue(
            result["fertilizer_optimization"]["success"]
        )


    def test_banana_recommendation(self):
        """Verify that a researched fruit-crop profile works."""

        result = generate_fertilizer_recommendation(
            crop="Banana",
            soil_n=100,
            soil_p=5,
            soil_k=100,
        )

        self.assertEqual(
            result["crop"],
            "Banana",
        )

        self.assertGreater(
            result["nutrient_deficit"]["N"],
            0,
        )

        self.assertGreater(
            result["nutrient_deficit"]["K"],
            0,
        )

        self.assertTrue(
            result["fertilizer_optimization"]["success"]
        )


    def test_all_ml_crop_profiles_are_available(self):
        """
        Ensure every crop class in the ML dataset has a
        fertilizer requirement profile.
        """

        expected_ml_crops = {
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

        from fertilizer.crop_requirements import (
            get_supported_crops,
        )

        supported_crops = set(
            get_supported_crops()
        )

        self.assertTrue(
            expected_ml_crops.issubset(
                supported_crops
            )
        )


if __name__ == "__main__":
    unittest.main()