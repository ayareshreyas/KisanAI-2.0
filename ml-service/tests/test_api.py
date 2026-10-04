from pathlib import Path
import sys


# --------------------------------------------------
# 1. Allow importing the ML service
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT),
)


from api import app


# --------------------------------------------------
# 2. Test client
# --------------------------------------------------

client = app.test_client()


# --------------------------------------------------
# 3. Helpers
# --------------------------------------------------

def assert_condition(condition, message):
    if not condition:
        raise AssertionError(message)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# --------------------------------------------------
# 4. Health endpoint
# --------------------------------------------------

print_section("HEALTH ENDPOINT")

response = client.get("/health")

assert_condition(
    response.status_code == 200,
    f"Expected 200, got {response.status_code}.",
)

body = response.get_json()

assert_condition(
    body["success"] is True,
    "Health endpoint should return success=True.",
)

assert_condition(
    body["status"] == "healthy",
    "ML service health status should be healthy.",
)

print("PASS: /health")


# --------------------------------------------------
# 5. Crop prediction endpoint
# --------------------------------------------------

print_section("CROP PREDICTION ENDPOINT")

crop_input = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 25,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200,
}

response = client.post(
    "/predict",
    json=crop_input,
)

assert_condition(
    response.status_code == 200,
    f"Expected 200, got {response.status_code}.",
)

body = response.get_json()

assert_condition(
    body["success"] is True,
    "Crop prediction should return success=True.",
)

assert_condition(
    "prediction" in body,
    "Crop prediction response must contain prediction.",
)

prediction = body["prediction"]

assert_condition(
    isinstance(prediction["crop"], str),
    "Predicted crop must be a string.",
)

assert_condition(
    0.0 <= prediction["confidence"] <= 1.0,
    "Prediction confidence must be between 0 and 1.",
)

assert_condition(
    "input_reliability" in body,
    "Crop prediction response must contain input_reliability.",
)

reliability = body["input_reliability"]

assert_condition(
    reliability["status"] == "within_training_range",
    "Normal crop input should be within training range.",
)

print(
    f"PASS: /predict → {prediction['crop']} "
    f"({prediction['confidence'] * 100:.2f}%)"
)


# --------------------------------------------------
# 6. Crop prediction validation
# --------------------------------------------------

print_section("CROP INPUT VALIDATION")

response = client.post(
    "/predict",
    json={
        "N": 90,
        "P": 42,
    },
)

assert_condition(
    response.status_code == 400,
    "Missing crop fields should return HTTP 400.",
)

body = response.get_json()

assert_condition(
    body["success"] is False,
    "Invalid crop input should return success=False.",
)

assert_condition(
    "error" in body,
    "Invalid crop input should contain an error message.",
)

print("PASS: Missing crop fields rejected.")


response = client.post(
    "/predict",
    json={
        "N": "not-a-number",
        "P": 42,
        "K": 43,
        "temperature": 25,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200,
    },
)

assert_condition(
    response.status_code == 400,
    "Non-numeric crop input should return HTTP 400.",
)

print("PASS: Non-numeric crop input rejected.")


# --------------------------------------------------
# 7. Soil analysis endpoint
# --------------------------------------------------

print_section("SOIL ANALYSIS ENDPOINT")

response = client.post(
    "/soil/analyze",
    json={
        "N": 250,
        "P": 18,
        "K": 150,
        "ph": 6.8,
    },
)

assert_condition(
    response.status_code == 200,
    f"Expected 200, got {response.status_code}.",
)

body = response.get_json()

assert_condition(
    body["success"] is True,
    "Soil analysis should return success=True.",
)

assert_condition(
    "soil_health" in body,
    "Soil analysis response must contain soil_health.",
)

soil_health = body["soil_health"]

for nutrient in [
    "nitrogen",
    "phosphorus",
    "potassium",
    "ph",
]:

    assert_condition(
        nutrient in soil_health,
        f"Soil health response missing {nutrient}.",
    )

print("PASS: /soil/analyze")


# --------------------------------------------------
# 8. Fertilizer recommendation endpoint
# --------------------------------------------------

print_section("FERTILIZER RECOMMENDATION ENDPOINT")

response = client.post(
    "/fertilizer/recommend",
    json={
        "crop": "Rice",
        "N": 60,
        "P": 30,
        "K": 20,
    },
)

assert_condition(
    response.status_code == 200,
    f"Expected 200, got {response.status_code}.",
)

body = response.get_json()

assert_condition(
    body["success"] is True,
    "Fertilizer recommendation should return success=True.",
)

assert_condition(
    "fertilizer_plan" in body,
    "Response must contain fertilizer_plan.",
)

fertilizer_plan = body["fertilizer_plan"]

assert_condition(
    isinstance(fertilizer_plan, dict),
    "fertilizer_plan must be a dictionary.",
)

print("PASS: /fertilizer/recommend")


# --------------------------------------------------
# 9. Fertilizer input validation
# --------------------------------------------------

response = client.post(
    "/fertilizer/recommend",
    json={
        "crop": "Rice",
        "N": -1,
        "P": 30,
        "K": 20,
    },
)

assert_condition(
    response.status_code == 400,
    "Negative fertilizer nutrients should return HTTP 400.",
)

print("PASS: Negative fertilizer nutrient values rejected.")


# --------------------------------------------------
# 10. Unified agricultural decision endpoint
# --------------------------------------------------

print_section("UNIFIED AGRICULTURAL DECISION ENDPOINT")

response = client.post(
    "/agricultural-decision",
    json={
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 25,
        "humidity": 80,
        "ph": 6.5,
        "rainfall": 200,
    },
)

assert_condition(
    response.status_code == 200,
    f"Expected 200, got {response.status_code}.",
)

body = response.get_json()

assert_condition(
    body["success"] is True,
    "Agricultural decision should return success=True.",
)

assert_condition(
    "decision" in body,
    "Response must contain decision.",
)

decision = body["decision"]


# --------------------------------------------------
# 11. Unified decision structure
# --------------------------------------------------

required_sections = [
    "crop_recommendation",
    "crop_explanation",
    "soil_health",
    "fertilizer_planning",
    "input_reliability",
]

for section in required_sections:

    assert_condition(
        section in decision,
        f"Decision is missing '{section}'.",
    )

print(
    "PASS: Unified decision contains all required sections."
)


# --------------------------------------------------
# 12. Crop recommendation structure
# --------------------------------------------------

crop_recommendation = decision[
    "crop_recommendation"
]

assert_condition(
    isinstance(
        crop_recommendation["crop"],
        str,
    ),
    "Decision crop must be a string.",
)

assert_condition(
    0.0 <= crop_recommendation["confidence"] <= 1.0,
    "Decision confidence must be between 0 and 1.",
)

print(
    "PASS: Crop recommendation structure."
)


# --------------------------------------------------
# 13. SHAP explanation structure
# --------------------------------------------------

crop_explanation = decision[
    "crop_explanation"
]

assert_condition(
    isinstance(
        crop_explanation,
        dict,
    ),
    "Crop explanation must be a dictionary.",
)

assert_condition(
    "feature_contributions" in crop_explanation,
    "Crop explanation must contain feature_contributions.",
)

feature_contributions = crop_explanation[
    "feature_contributions"
]

assert_condition(
    isinstance(
        feature_contributions,
        list,
    ),
    "feature_contributions must be a list.",
)

assert_condition(
    len(feature_contributions) == 7,
    (
        "Expected 7 SHAP feature contributions, "
        f"found {len(feature_contributions)}."
    ),
)

for contribution in feature_contributions:

    assert_condition(
        "feature" in contribution,
        "SHAP contribution missing feature.",
    )

    assert_condition(
        "value" in contribution,
        "SHAP contribution missing value.",
    )

    assert_condition(
        "contribution" in contribution,
        "SHAP contribution missing contribution.",
    )

print(
    "PASS: SHAP explanation contains 7 feature contributions."
)


# --------------------------------------------------
# 14. Soil health structure
# --------------------------------------------------

soil_health = decision[
    "soil_health"
]

assert_condition(
    isinstance(
        soil_health,
        dict,
    ),
    "Decision soil_health must be a dictionary.",
)

print(
    "PASS: Soil health section."
)


# --------------------------------------------------
# 15. Fertilizer planning structure
# --------------------------------------------------

fertilizer_planning = decision[
    "fertilizer_planning"
]

assert_condition(
    isinstance(
        fertilizer_planning,
        dict,
    ),
    "Fertilizer planning must be a dictionary.",
)

assert_condition(
    "available" in fertilizer_planning,
    "Fertilizer planning must contain available.",
)

print(
    "PASS: Fertilizer planning section."
)


# --------------------------------------------------
# 16. Input reliability structure
# --------------------------------------------------

input_reliability = decision[
    "input_reliability"
]

assert_condition(
    isinstance(
        input_reliability,
        dict,
    ),
    "Input reliability must be a dictionary.",
)

assert_condition(
    input_reliability["status"]
    == "within_training_range",
    "Normal unified input should be within training range.",
)

assert_condition(
    "warnings" in input_reliability,
    "Input reliability must contain warnings.",
)

assert_condition(
    "checked_features" in input_reliability,
    "Input reliability must contain checked_features.",
)

print(
    "PASS: Input reliability section."
)


# --------------------------------------------------
# 17. Unified endpoint invalid input
# --------------------------------------------------

print_section("UNIFIED DECISION VALIDATION")

response = client.post(
    "/agricultural-decision",
    json={
        "N": 90,
        "P": 42,
        "K": 43,
    },
)

assert_condition(
    response.status_code == 400,
    "Missing unified decision fields should return HTTP 400.",
)

body = response.get_json()

assert_condition(
    body["success"] is False,
    "Invalid unified decision input should return success=False.",
)

print(
    "PASS: Invalid unified decision input rejected."
)


# --------------------------------------------------
# 18. Final result
# --------------------------------------------------

print_section("API TEST SUMMARY")

print("PASS: /health")
print("PASS: /predict")
print("PASS: Crop input validation")
print("PASS: /soil/analyze")
print("PASS: /fertilizer/recommend")
print("PASS: Fertilizer input validation")
print("PASS: /agricultural-decision")
print("PASS: Unified decision structure")
print("PASS: SHAP explanation structure")
print("PASS: Soil health structure")
print("PASS: Fertilizer planning structure")
print("PASS: Input reliability structure")

print(
    "\nSUCCESS: "
    "All ML service API tests passed."
)