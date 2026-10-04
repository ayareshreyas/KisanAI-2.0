"""
KisanAI Fertilizer Database

This module stores fertilizer composition data used by the
KisanAI fertilizer recommendation engine.

N, P and K values represent the percentage composition
listed for each fertilizer product.

Important:
- These values describe fertilizer composition.
- They are NOT soil nutrient levels.
- They should not be confused with the N/P/K values used
  by the crop recommendation ML dataset.
"""

FERTILIZERS = {
    "Urea": {
        "N": 46,
        "P": 0,
        "K": 0,
        "price_per_kg": 25,
    },
    "DAP": {
        "N": 18,
        "P": 46,
        "K": 0,
        "price_per_kg": 35,
    },
    "MOP": {
        "N": 0,
        "P": 0,
        "K": 60,
        "price_per_kg": 20,
    },
    "SSP": {
        "N": 0,
        "P": 16,
        "K": 0,
        "price_per_kg": 15,
    },
    "NPK 19-19-19": {
        "N": 19,
        "P": 19,
        "K": 19,
        "price_per_kg": 40,
    },
    "NPK 20-20-20": {
        "N": 20,
        "P": 20,
        "K": 20,
        "price_per_kg": 42,
    },
    "NPK 12-32-16": {
        "N": 12,
        "P": 32,
        "K": 16,
        "price_per_kg": 38,
    },
    "NPK 10-26-26": {
        "N": 10,
        "P": 26,
        "K": 26,
        "price_per_kg": 36,
    },
    "Compost": {
        "N": 2,
        "P": 1,
        "K": 2,
        "price_per_kg": 5,
    },
    "Vermicompost": {
        "N": 3,
        "P": 2,
        "K": 3,
        "price_per_kg": 8,
    },
    "Farm Yard Manure": {
        "N": 0.5,
        "P": 0.2,
        "K": 0.5,
        "price_per_kg": 3,
    },
    "Bone Meal": {
        "N": 4,
        "P": 20,
        "K": 0,
        "price_per_kg": 25,
    },
    "Rock Phosphate": {
        "N": 0,
        "P": 25,
        "K": 0,
        "price_per_kg": 18,
    },
    "Potash": {
        "N": 0,
        "P": 0,
        "K": 50,
        "price_per_kg": 22,
    },
}


def get_fertilizer(name):
    """Return fertilizer information by name."""
    return FERTILIZERS.get(name)


def get_all_fertilizers():
    """Return the complete fertilizer database."""
    return FERTILIZERS


if __name__ == "__main__":
    print("=" * 60)
    print("KISANAI FERTILIZER DATABASE")
    print("=" * 60)

    for name, details in FERTILIZERS.items():
        print(
            f"{name:20} "
            f"N:{details['N']:>5} "
            f"P:{details['P']:>5} "
            f"K:{details['K']:>5} "
            f"₹{details['price_per_kg']}/kg"
        )