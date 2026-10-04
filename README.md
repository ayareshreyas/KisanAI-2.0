# 🌾 KisanAI 2.0

AI-powered agricultural decision-support platform for crop recommendation, soil health analysis, fertilizer planning, explainable AI, and farmer-friendly reports.

## Features

- Crop recommendation using a production Random Forest model
- Input reliability checks against training ranges
- Soil health analysis
- SHAP-based explainability
- Fertilizer recommendation and optimization
- Agricultural decision engine
- Multilingual React interface
- Voice-assisted navigation
- Persistent analysis reports
- React + Node.js + Flask + SQLite architecture

## Machine Learning

The production crop model is a Random Forest classifier trained on 2,200 samples across 22 crop classes.

### Supported crops

Apple, Banana, Blackgram, Chickpea, Coconut, Coffee, Cotton, Grapes, Jute, Kidneybeans, Lentil, Maize, Mango, Mothbeans, Mungbean, Muskmelon, Orange, Papaya, Pigeonpeas, Pomegranate, Rice, Watermelon.

### Production model

- Algorithm: Random Forest Classifier
- Estimators: 200
- Minimum samples split: 5
- Maximum features: sqrt
- Random state: 42
- Cross-validation: 5-fold GridSearchCV
- Best CV accuracy: 99.60%
- Held-out accuracy: 99.55%
- Precision: 99.57%
- Recall: 99.55%
- F1 score: 99.55%
- Log loss: 0.0572

The production artifact is trained on the complete dataset after controlled model selection. Held-out metrics come from the separate model-selection experiment.

## Explainable AI

SHAP values are generated for crop predictions to show the relative contribution of input features. These explanations describe model behavior and are not causal agricultural claims.

## Input Reliability

Inference inputs are compared against the training ranges:

- Nitrogen: 0–140 kg/ha
- Phosphorus: 5–145 kg/ha
- Potassium: 5–205 kg/ha
- Temperature: 8.83–43.68 °C
- Humidity: 14.26–99.98%
- pH: 3.50–9.94
- Rainfall: 20.21–298.56 mm

Out-of-range values produce reliability warnings rather than being silently treated as normal training-distribution inputs.

## Fertilizer Engine

The fertilizer knowledge base supports all 22 production crop classes. Recommendations use crop nutrient requirements, soil nutrient inputs, fertilizer nutrient composition, fertilizer prices, and budget constraints.

The fertilizer engine uses **kg/acre** inputs. The ML crop model and soil-health analysis use **kg/ha**. The system does not silently convert between these units; fertilizer optimization requires explicitly compatible kg/acre inputs.

Fertilizer outputs are mathematical decision-support results and should not be treated as universal field prescriptions. Real agricultural recommendations should consider soil testing, local agronomy, crop stage, yield targets, climate, and local extension guidance.

## Architecture

```text
React Frontend
      |
      v
Node.js / Express Backend
      |
      +------ SQLite Database
      |
      v
Flask ML Service
      |
      +------ Random Forest Crop Model
      +------ Soil Analyzer
      +------ SHAP Explainer
      +------ Fertilizer Engine
      +------ Agricultural Decision Engine