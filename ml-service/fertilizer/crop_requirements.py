"""
KisanAI Crop Nutrient Requirements

Stores baseline crop nutrient requirement profiles used by
the prototype fertilizer recommendation engine.

IMPORTANT AGRONOMIC NOTE
------------------------
These values are research-backed baseline nutrient profiles
for mathematical decision-support and software testing.

They are NOT universal fertilizer prescriptions.

Actual fertilizer recommendations depend on factors such as:
- soil-test results
- crop variety/cultivar
- expected yield
- irrigation/rainfall
- crop age and growth stage
- soil type
- regional agricultural recommendations
- organic manure and biofertilizer contributions

The authoritative references used for the researched profiles
include ICAR and TNAU Agritech agricultural guidance.

UNIT CONVENTION
---------------
The fertilizer engine expects:

    N -> elemental nitrogen, kg/acre
    P -> elemental phosphorus, kg/acre
    K -> elemental potassium, kg/acre

Many agricultural recommendations are published as:

    N : P2O5 : K2O, kg/hectare

where necessary, those values were converted using:

    P = P2O5 × 0.4364
    K = K2O × 0.8301
    1 hectare = 2.47105 acres

The resulting values are intentionally stored in the
elemental kg/acre format expected by this prototype engine.

The profiles should therefore be treated as baseline
decision-support inputs rather than field-application rates.
"""


# ------------------------------------------------------------------
# Crop nutrient requirement profiles
# ------------------------------------------------------------------
#
# IMPORTANT:
# Values below are:
#
#     elemental N, P and K in kg/acre
#
# They represent baseline nutrient requirement profiles used
# by this prototype.
#
# ------------------------------------------------------------------

CROP_REQUIREMENTS = {

    # ==============================================================
    # ML MODEL CROPS
    # ==============================================================

    # ICAR rice recommendation:
    # 150 kg N + 60 kg P2O5 + 60 kg K2O / ha
    #
    # Converted to elemental kg/acre:
    # N  = 60.70
    # P  = 10.60
    # K  = 20.16
    "Rice": {
        "N": 60.70,
        "P": 10.60,
        "K": 20.16,
    },

    # TNAU/ICAR maize reference:
    # approximately 150 kg N + 75 kg P2O5 + 75 kg K2O / ha
    "Maize": {
        "N": 60.70,
        "P": 13.25,
        "K": 25.19,
    },

    # TNAU cotton recommendation:
    # 24 kg N : 12 kg P2O5 : 12 kg K2O / acre
    "Cotton": {
        "N": 24.00,
        "P": 5.24,
        "K": 9.96,
    },

    # TNAU jute:
    # 20 kg N + 20 kg P2O5 + 20 kg K2O / ha
    "Jute": {
        "N": 8.09,
        "P": 3.53,
        "K": 6.72,
    },

    # TNAU chickpea:
    # 15–20 kg N + 40 kg P2O5 / ha.
    #
    # Prototype uses the upper N value.
    # Potassium is not specified in this reference profile.
    "Chickpea": {
        "N": 8.09,
        "P": 7.06,
        "K": 0.00,
    },

    # TNAU irrigated blackgram:
    # 25 kg N + 50 kg P2O5 + 25 kg K2O / ha
    "Blackgram": {
        "N": 10.12,
        "P": 8.83,
        "K": 8.40,
    },

    # Greengram / mungbean uses the same representative
    # TNAU pulse baseline in this prototype.
    "Mungbean": {
        "N": 10.12,
        "P": 8.83,
        "K": 8.40,
    },

    # Redgram / pigeonpea:
    # 25 kg N + 50 kg P2O5 + 25 kg K2O / ha
    "Pigeonpeas": {
        "N": 10.12,
        "P": 8.83,
        "K": 8.40,
    },

    # ICAR moth bean advisory:
    # 15–20 kg N + 35–40 kg P2O5 / ha.
    #
    # Prototype uses midpoint values:
    # 17.5 kg N + 37.5 kg P2O5 / ha
    #
    # K is left at zero because the cited advisory does not
    # specify a basal K requirement.
    "Mothbeans": {
        "N": 7.08,
        "P": 6.62,
        "K": 0.00,
    },

    # Representative pulse baseline used for crops where a
    # crop-specific profile is not available in the project's
    # reference material:
    #
    # 20 kg N + 40 kg P2O5 + 20 kg K2O / ha
    #
    # This is explicitly a prototype baseline.
    "Lentil": {
        "N": 8.09,
        "P": 7.06,
        "K": 6.72,
    },

    "Kidneybeans": {
        "N": 8.09,
        "P": 7.06,
        "K": 6.72,
    },

    # --------------------------------------------------------------
    # Fruit / plantation crops
    # --------------------------------------------------------------

    # TNAU banana fertigation reference:
    # 200 g N + 30 g P2O5 + 300 g K2O / plant.
    #
    # Converted using approximately 1.8 m x 1.8 m spacing
    # for the prototype area normalization.
    "Banana": {
        "N": 249.77,
        "P": 16.35,
        "K": 311.00,
    },

    # TNAU apple:
    # 500 g N + 1 kg P + 1 kg K per bearing tree.
    #
    # Converted using approximately 4 m x 4 m spacing.
    # P and K are already expressed as elemental nutrients
    # in the source.
    "Apple": {
        "N": 126.46,
        "P": 253.00,
        "K": 253.00,
    },

    # TNAU mango high-density planting:
    # 1.0 : 0.5 : 1.0 kg N:P:K / bearing tree / year.
    #
    # Converted using approximately 6 m x 6 m spacing.
    "Mango": {
        "N": 112.10,
        "P": 56.05,
        "K": 112.10,
    },

    # TNAU sweet/mandarin orange reference:
    # approximately 0.6 : 0.2 : 0.4 kg N:P:K per mature tree/year.
    #
    # Converted using approximately 6 m x 6 m spacing.
    "Orange": {
        "N": 67.26,
        "P": 9.78,
        "K": 37.22,
    },

    # ICAR papaya recommendation:
    # 250 g N + 250 g P2O5 + 500 g K2O / plant / year.
    #
    # Converted using approximately 1.8 m x 1.8 m spacing.
    "Papaya": {
        "N": 312.22,
        "P": 136.25,
        "K": 518.34,
    },

    # TNAU pomegranate:
    # 600 g N + 500 g P + 1200 g K per plant/year
    # for plants 6 years onwards.
    #
    # Converted using approximately 3 m x 3 m spacing.
    "Pomegranate": {
        "N": 269.76,
        "P": 224.80,
        "K": 539.53,
    },

    # TNAU coconut:
    # approximately 560 g N + 320 g P2O5 + 1200 g K2O
    # per bearing palm/year.
    #
    # Converted using approximately 175 palms/ha.
    "Coconut": {
        "N": 39.66,
        "P": 9.89,
        "K": 70.55,
    },

    # TNAU bearing coffee:
    # 140 kg N + 90 kg P2O5 + 120 kg K2O / ha
    # for bearing Arabica coffee below 1 t/ha.
    "Coffee": {
        "N": 56.66,
        "P": 15.89,
        "K": 40.31,
    },

    # TNAU table-grape fertigation reference:
    # approximately 266.6 kg N + 355.2 kg P + 266.6 kg K / ha.
    #
    # The source's fertigation table reports these as nutrient
    # quantities; they are converted to the prototype acre basis.
    "Grapes": {
        "N": 107.89,
        "P": 143.74,
        "K": 107.89,
    },

    # TNAU watermelon:
    # 200:100:100 kg/ha N:P2O5:K2O.
    "Watermelon": {
        "N": 80.94,
        "P": 17.66,
        "K": 33.59,
    },

    # TNAU states the same 200:100:100 kg/ha NPK fertigation
    # recommendation for watermelon/muskmelon.
    "Muskmelon": {
        "N": 80.94,
        "P": 17.66,
        "K": 33.59,
    },


    # ==============================================================
    # LEGACY PROTOTYPE PROFILES
    # ==============================================================
    #
    # These crops were already supported by the original
    # fertilizer engine and are retained for backward compatibility.
    #
    # They are NOT ML model classes in the current
    # Crop_recommendation.csv dataset.
    #
    # They remain available because existing fertilizer-engine
    # tests and standalone functionality use them.
    # ==============================================================

    "Wheat": {
        "N": 100,
        "P": 50,
        "K": 50,
    },

    "Sugarcane": {
        "N": 200,
        "P": 80,
        "K": 100,
    },

    "Soybean": {
        "N": 60,
        "P": 40,
        "K": 40,
    },

    "Potato": {
        "N": 100,
        "P": 60,
        "K": 80,
    },

    "Tomato": {
        "N": 80,
        "P": 50,
        "K": 60,
    },

    "Onion": {
        "N": 60,
        "P": 40,
        "K": 40,
    },

    "Chilli": {
        "N": 70,
        "P": 50,
        "K": 50,
    },

    "Brinjal": {
        "N": 60,
        "P": 40,
        "K": 40,
    },

    "Okra": {
        "N": 50,
        "P": 30,
        "K": 30,
    },

    "Cabbage": {
        "N": 80,
        "P": 50,
        "K": 60,
    },

    "Cauliflower": {
        "N": 80,
        "P": 50,
        "K": 60,
    },

    "Spinach": {
        "N": 40,
        "P": 20,
        "K": 20,
    },
}


def get_crop_requirements(crop):
    """
    Return NPK requirements for a crop.

    Parameters:
        crop:
            Crop name using the canonical name stored in
            CROP_REQUIREMENTS.

    Returns:
        dict | None
    """

    return CROP_REQUIREMENTS.get(crop)


def get_supported_crops():
    """Return all crops supported by the fertilizer engine."""

    return list(CROP_REQUIREMENTS.keys())


if __name__ == "__main__":

    print("=" * 70)
    print("KISANAI CROP NUTRIENT REQUIREMENTS")
    print("=" * 70)

    print(
        "\nNOTE: Values are prototype baseline nutrient profiles "
        "in elemental kg/acre."
    )

    print(
        "They are not universal field fertilizer prescriptions.\n"
    )

    for crop, requirements in CROP_REQUIREMENTS.items():

        print(
            f"{crop:15} "
            f"N:{requirements['N']:>7.2f} "
            f"P:{requirements['P']:>7.2f} "
            f"K:{requirements['K']:>7.2f} "
            f"kg/acre"
        )