"""
KisanAI Input Reliability

Checks whether crop-recommendation inputs fall within the
feature ranges observed in the dataset used to train the
crop recommendation model.

This is NOT a guarantee that an input is agriculturally valid.
It only indicates whether the value is inside or outside the
model's observed training distribution.
"""


TRAINING_FEATURE_RANGES = {
    "N": {
        "label": "Nitrogen (N)",
        "minimum": 0.0,
        "maximum": 140.0,
        "unit": "kg/ha",
    },
    "P": {
        "label": "Phosphorus (P)",
        "minimum": 5.0,
        "maximum": 145.0,
        "unit": "kg/ha",
    },
    "K": {
        "label": "Potassium (K)",
        "minimum": 5.0,
        "maximum": 205.0,
        "unit": "kg/ha",
    },
    "temperature": {
        "label": "Temperature",
        "minimum": 8.8,
        "maximum": 43.7,
        "unit": "°C",
    },
    "humidity": {
        "label": "Humidity",
        "minimum": 14.3,
        "maximum": 100.0,
        "unit": "%",
    },
    "ph": {
        "label": "Soil pH",
        "minimum": 3.5,
        "maximum": 9.9,
        "unit": "pH",
    },
    "rainfall": {
        "label": "Rainfall",
        "minimum": 20.2,
        "maximum": 298.6,
        "unit": "mm",
    },
}


def assess_input_reliability(values):
    """
    Compare supplied crop-model inputs with the ranges
    observed in the training dataset.

    Returns a structured reliability assessment.

    Important:
    Being inside the observed range does not mean the input
    is guaranteed to be representative of real-world farming
    conditions.
    """

    warnings = []
    checked_features = []

    for feature, metadata in TRAINING_FEATURE_RANGES.items():
        if feature not in values:
            continue

        value = float(values[feature])

        minimum = metadata["minimum"]
        maximum = metadata["maximum"]

        checked_features.append({
            "feature": feature,
            "label": metadata["label"],
            "value": value,
            "training_minimum": minimum,
            "training_maximum": maximum,
            "unit": metadata["unit"],
            "within_training_range": (
                minimum <= value <= maximum
            ),
        })

        if value < minimum:
            warnings.append({
                "feature": feature,
                "label": metadata["label"],
                "value": value,
                "training_minimum": minimum,
                "training_maximum": maximum,
                "unit": metadata["unit"],
                "direction": "below",
                "message": (
                    f"{metadata['label']} is below the "
                    f"minimum value observed during training "
                    f"({minimum} {metadata['unit']})."
                ),
            })

        elif value > maximum:
            warnings.append({
                "feature": feature,
                "label": metadata["label"],
                "value": value,
                "training_minimum": minimum,
                "training_maximum": maximum,
                "unit": metadata["unit"],
                "direction": "above",
                "message": (
                    f"{metadata['label']} is above the "
                    f"maximum value observed during training "
                    f"({maximum} {metadata['unit']})."
                ),
            })

    if warnings:
        status = "outside_training_range"
    else:
        status = "within_training_range"

    return {
        "status": status,
        "warnings": warnings,
        "checked_features": checked_features,
        "message": (
            "All supplied crop-model inputs are within the "
            "observed training ranges."
            if not warnings
            else (
                "One or more crop-model inputs are outside "
                "the ranges observed during training. "
                "The model can still produce a prediction, "
                "but it should be interpreted cautiously."
            )
        ),
    }