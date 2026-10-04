# KisanAI Crop Recommendation Model Card

## 1. Model Overview

**Model name:** KisanAI Crop Recommendation Model

**Model type:** Random Forest Classifier

**Task:** Multi-class crop recommendation

**Framework:** scikit-learn

**Primary purpose:**  
Predict a suitable crop class from a set of soil and environmental input features.

The model is one component of KisanAI's broader agricultural decision-support system. Its prediction is combined with soil-health analysis, input-reliability checks, explainability, and downstream recommendation logic.

The model is intended to provide decision support and should not be treated as an autonomous agricultural prescription system.

---

## 2. Input Features

The model uses seven input features:

| Feature | Description | Unit |
|---|---|---|
| N | Nitrogen | kg/ha |
| P | Phosphorus | kg/ha |
| K | Potassium | kg/ha |
| temperature | Temperature | °C |
| humidity | Relative humidity | % |
| ph | Soil pH | pH |
| rainfall | Rainfall | mm |

The model predicts one crop class from the crop labels present in the training dataset.

---

## 3. Dataset

**Dataset file:**

`ml-service/data/raw/Crop_recommendation.csv`

### Dataset characteristics

- Total samples: **2,200**
- Input features: **7**
- Crop classes: **22**
- Samples per crop: **100**
- Duplicate rows: **None identified**
- Target column: `label`

The dataset is a benchmark crop-recommendation dataset used for development and evaluation.

### Important limitation

The dataset should not be assumed to represent all agricultural regions, soil conditions, climates, farming practices, or crop varieties.

Therefore, benchmark performance should not be interpreted as guaranteed real-world field accuracy.

---

## 4. Model Architecture

The production crop recommendation model is a:

**Random Forest Classifier**

Current configuration:

```text
n_estimators = 300
random_state = 42
n_jobs = -1