import json
from pathlib import Path

import joblib
import pandas as pd

from inference.input_reliability import assess_input_reliability


MODEL_DIR = Path(__file__).resolve().parent.parent / "models"

MODEL_PATH = MODEL_DIR / "crop_recommendation_random_forest.joblib"
METADATA_PATH = MODEL_DIR / "crop_model_metadata.json"


model = joblib.load(MODEL_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as file:
    metadata = json.load(file)


FEATURES = metadata["features"]


def predict_crop(
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float,
):
    input_values = {
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall,
    }

    reliability = assess_input_reliability(input_values)

    input_data = pd.DataFrame(
        [[
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall,
        ]],
        columns=FEATURES,
    )

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    predicted_index = probabilities.argmax()
    confidence = float(probabilities[predicted_index])

    return {
        "crop": str(prediction),
        "confidence": confidence,
        "confidence_type": "random_forest_class_probability",
        "input_reliability": reliability,
    }