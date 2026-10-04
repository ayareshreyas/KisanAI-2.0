# KisanAI 2.0 🌾

> **Voice-first, multilingual, explainable AI for agricultural decision support.**

KisanAI 2.0 is an AI-powered agricultural decision-support platform designed to help farmers make more informed decisions using soil and environmental data.

Unlike a basic rule-based agriculture application, KisanAI 2.0 combines a trained machine-learning model with soil analysis, fertilizer optimization, explainability, multilingual voice interaction, and persistent farm analysis reports.

The project is designed as a full-stack ML system rather than a standalone prediction notebook.

---

## 🚀 What KisanAI Does

KisanAI 2.0 currently provides four major decision-support capabilities.

### 🌱 Crop Recommendation

A trained **Random Forest classifier** predicts a suitable crop based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- Soil pH
- Rainfall

The production model was developed using the public `Crop_recommendation.csv` dataset containing:

- **2,200 samples**
- **7 input features**
- **22 crop classes**

### 🧪 Soil Health Analysis

KisanAI evaluates important soil parameters and classifies their status, including:

- Nitrogen
- Phosphorus
- Potassium
- Soil pH

The system provides human-readable soil-health information instead of exposing raw model output alone.

### 🧴 Fertilizer Recommendation

The fertilizer engine combines:

- Crop nutrient requirements
- Current soil nutrient levels
- Nutrient deficits
- Fertilizer composition
- Fertilizer cost
- Farmer budget

It then calculates a fertilizer plan while attempting to maximize nutrient coverage within the available budget.

### 📊 Explainable Agricultural Decision Support

KisanAI combines crop prediction, soil analysis, and fertilizer planning into a unified agricultural decision.

The system also provides feature-level explanations using **SHAP** so users can understand which input features contributed to the crop prediction.

---

# 🧠 Machine Learning

## Production Model

KisanAI currently uses a **Random Forest classifier** for crop recommendation.

The model-development process included:

1. Dataset inspection
2. Data preprocessing
3. Train/test splitting
4. Baseline Random Forest training
5. Cross-validation
6. Hyperparameter tuning
7. Hold-out evaluation
8. Model comparison
9. Production model promotion
10. Metadata generation

The final production model was trained on the complete 2,200-row dataset after model selection.

---

## 📈 Model Performance

The primary generalization result is based on an untouched hold-out test set.

| Metric | Result |
|---|---:|
| Hold-out Accuracy | **99.55%** |
| Weighted Precision | **99.57%** |
| Weighted Recall | **99.55%** |
| Weighted F1 | **99.55%** |
| Log Loss | **0.0572** |
| 5-Fold Cross-Validation | **99.60% ± 0.55%** |

### Important interpretation

These results describe performance on the available benchmark dataset.

They **do not mean that KisanAI is 99.55% accurate on real-world farms**.

Agricultural conditions can differ substantially from a benchmark dataset because of:

- Regional soil differences
- Measurement errors
- Weather variation
- Crop varieties
- Seasonal conditions
- Data distribution changes

The model's prediction confidence is therefore treated as model output rather than a guarantee of agricultural success.

---

# 🔬 Model Explainability

KisanAI uses **SHAP (SHapley Additive exPlanations)** to provide feature-level explanations for crop predictions.

The explanation layer helps answer questions such as:

> "Which soil or environmental factors influenced this prediction?"

The explanation is intended to improve transparency and user understanding.

### Important limitation

SHAP explanations describe how model features contributed to a prediction.

They should **not be interpreted as proof of causal relationships** between a feature and crop suitability.

---

# 🌾 Agricultural Decision Pipeline

```text
Farmer Input
     │
     ▼
Soil / Environmental Data
     │
     ▼
Input Validation & Reliability Checks
     │
     ▼
Machine Learning Model
     │
     ├───────────────► Crop Prediction
     │
     ▼
Agricultural Decision Engine
     │
     ├───────────────► Soil Health Analysis
     │
     └───────────────► Fertilizer Planning
                              │
                              ▼
                       Budget Optimization
                              │
                              ▼
                    Explainable Recommendation
                              │
                              ▼
                       Saved Farm Report