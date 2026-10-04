import os

from flask import Flask, request, jsonify

from inference.predict_crop import predict_crop
from soil.soil_analyzer import analyze_soil
from fertilizer.recommendation_engine import (
    generate_fertilizer_recommendation,
)
from decision.agricultural_decision_engine import (
    generate_agricultural_decision,
)


app = Flask(__name__)


CROP_FEATURES = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]


def validate_crop_input(data):
    missing = [
        feature
        for feature in CROP_FEATURES
        if feature not in data
    ]

    if missing:
        return {
            "valid": False,
            "error": (
                "Missing required crop-model fields: "
                + ", ".join(missing)
            ),
        }

    numeric_data = {}

    try:
        for feature in CROP_FEATURES:
            numeric_data[feature] = float(
                data[feature]
            )

    except (TypeError, ValueError):
        return {
            "valid": False,
            "error": (
                "All crop-model input values must be numeric."
            ),
        }

    return {
        "valid": True,
        "data": numeric_data,
    }


@app.get("/health")
def health():
    return jsonify({
        "success": True,
        "service": "KisanAI ML Service",
        "status": "healthy",
    })


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a JSON object.",
        }), 400

    validation = validate_crop_input(data)

    if not validation["valid"]:
        return jsonify({
            "success": False,
            "error": validation["error"],
        }), 400

    crop_input = validation["data"]

    try:
        prediction = predict_crop(
            nitrogen=crop_input["N"],
            phosphorus=crop_input["P"],
            potassium=crop_input["K"],
            temperature=crop_input["temperature"],
            humidity=crop_input["humidity"],
            ph=crop_input["ph"],
            rainfall=crop_input["rainfall"],
        )

        return jsonify({
            "success": True,
            "prediction": {
                "crop": prediction["crop"],
                "confidence": prediction["confidence"],
            },
            "input_reliability": (
                prediction["input_reliability"]
            ),
        })

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 400

    except Exception:
        app.logger.exception(
            "Crop prediction error"
        )

        return jsonify({
            "success": False,
            "error": "Unable to generate crop prediction.",
        }), 500


@app.post("/soil/analyze")
def soil_analysis():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a JSON object.",
        }), 400

    required_fields = (
        "N",
        "P",
        "K",
        "ph",
    )

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "success": False,
            "error": (
                "Missing required soil fields: "
                + ", ".join(missing)
            ),
        }), 400

    try:
        result = analyze_soil(
            nitrogen=float(data["N"]),
            phosphorus=float(data["P"]),
            potassium=float(data["K"]),
            ph=float(data["ph"]),
        )

        return jsonify({
            "success": True,
            "soil_health": result,
        })

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 400

    except Exception:
        app.logger.exception(
            "Soil analysis error"
        )

        return jsonify({
            "success": False,
            "error": "Unable to analyze soil.",
        }), 500


@app.post("/fertilizer/recommend")
def fertilizer_recommendation():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a JSON object.",
        }), 400

    required_fields = (
        "crop",
        "N",
        "P",
        "K",
    )

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "success": False,
            "error": (
                "Missing required fertilizer fields: "
                + ", ".join(missing)
            ),
        }), 400

    try:
        crop = str(data["crop"]).strip()

        if not crop:
            return jsonify({
                "success": False,
                "error": "Crop must not be empty.",
            }), 400

        soil_n = float(data["N"])
        soil_p = float(data["P"])
        soil_k = float(data["K"])

        if (
            soil_n < 0
            or soil_p < 0
            or soil_k < 0
        ):
            return jsonify({
                "success": False,
                "error": (
                    "Fertilizer nutrient values cannot "
                    "be negative."
                ),
            }), 400

        budget = data.get("budget")

        if budget is not None:
            budget = float(budget)

            if budget < 0:
                return jsonify({
                    "success": False,
                    "error": (
                        "Fertilizer budget cannot be negative."
                    ),
                }), 400

        result = generate_fertilizer_recommendation(
            crop=crop,
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k,
            budget=budget,
        )

        return jsonify({
            "success": True,
            "fertilizer_plan": result,
        })

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 400

    except Exception:
        app.logger.exception(
            "Fertilizer recommendation error"
        )

        return jsonify({
            "success": False,
            "error": (
                "Unable to generate fertilizer recommendation."
            ),
        }), 500


@app.post("/agricultural-decision")
def agricultural_decision():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "error": "Request body must be a JSON object.",
        }), 400

    validation = validate_crop_input(data)

    if not validation["valid"]:
        return jsonify({
            "success": False,
            "error": validation["error"],
        }), 400

    crop_input = validation["data"]

    fertilizer_inputs = data.get(
        "fertilizer_inputs"
    )

    fertilizer_budget = data.get(
        "fertilizer_budget"
    )

    if fertilizer_inputs is not None:
        if not isinstance(
            fertilizer_inputs,
            dict,
        ):
            return jsonify({
                "success": False,
                "error": (
                    "fertilizer_inputs must be "
                    "a JSON object."
                ),
            }), 400

    if fertilizer_budget is not None:
        try:
            fertilizer_budget = float(
                fertilizer_budget
            )
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": (
                    "fertilizer_budget must be numeric."
                ),
            }), 400

        if fertilizer_budget < 0:
            return jsonify({
                "success": False,
                "error": (
                    "fertilizer_budget cannot be negative."
                ),
            }), 400

    try:
        decision = generate_agricultural_decision(
            nitrogen=crop_input["N"],
            phosphorus=crop_input["P"],
            potassium=crop_input["K"],
            temperature=crop_input["temperature"],
            humidity=crop_input["humidity"],
            ph=crop_input["ph"],
            rainfall=crop_input["rainfall"],
            fertilizer_inputs=fertilizer_inputs,
            fertilizer_budget=fertilizer_budget,
        )

        return jsonify({
            "success": True,
            "decision": decision,
        })

    except (TypeError, ValueError) as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 400

    except Exception:
        app.logger.exception(
            "Agricultural decision error"
        )

        return jsonify({
            "success": False,
            "error": (
                "Unable to generate agricultural decision."
            ),
        }), 500


if __name__ == "__main__":
    port = int(
        os.environ.get("PORT", 5001)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )