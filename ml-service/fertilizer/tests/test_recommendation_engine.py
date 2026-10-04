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
"""

import unittest

from fertilizer.recommendation_engine import (
    generate_fertilizer_recommendation,
)


class TestRecommendationEngine(unittest.TestCase):

    def test_rice_recommendation_without_budget(self):
        """Test a normal fertilizer recommendation."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=80,
            soil_p=50,
            soil_k=70,
        )

        self.assertEqual(
            result["crop"],
            "Rice",
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 40.0,
                "P": 10.0,
                "K": 0.0,
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
        """Test fertilizer recommendation with a farmer budget."""

        budget = 4000

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=60,
            soil_p=30,
            soil_k=20,
            budget=budget,
        )

        self.assertEqual(
            result["crop"],
            "Rice",
        )

        self.assertEqual(
            result["nutrient_deficit"],
            {
                "N": 60.0,
                "P": 30.0,
                "K": 40.0,
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
            soil_n=50,
            soil_p=20,
            soil_k=20,
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
            soil_n=60,
            soil_p=30,
            soil_k=20,
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
        """Test a case where soil already meets crop requirements."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=120,
            soil_p=60,
            soil_k=60,
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
        """Test a budget-aware request when no fertilizer is needed."""

        result = generate_fertilizer_recommendation(
            crop="Rice",
            soil_n=120,
            soil_p=60,
            soil_k=60,
            budget=4000,
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


if __name__ == "__main__":
    unittest.main()