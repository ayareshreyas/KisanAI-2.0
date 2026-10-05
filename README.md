# KisanAI 2.0 🌾

> **Voice-first, multilingual, explainable AI for agricultural decision support.**

KisanAI 2.0 is a full-stack AI-powered agricultural decision-support platform designed to help farmers make more informed decisions using **soil and environmental data**.

Instead of returning only a crop prediction, KisanAI combines **machine learning, soil-health analysis, fertilizer planning, explainable AI, multilingual interaction, and persistent farm reports** into one application.

The project is built as a production-style system with separate **React, Node.js, and Python/Flask services**, rather than as a standalone machine-learning notebook.

---

## 🚀 Live Demo

**Frontend:**
https://kisan-ai-2-0.vercel.app/

**Backend API:**
https://kisanai-backend-api.onrender.com/

**ML Service:**
https://kisanai-ml-service.onrender.com/health

> The deployed services may take a short time to wake up when running on free hosting infrastructure.

---

## ✨ Key Features

### 🌱 AI Crop Recommendation

KisanAI uses a trained **Random Forest classifier** to recommend a suitable crop based on:

* Nitrogen (N)
* Phosphorus (P)
* Potassium (K)
* Temperature
* Humidity
* Soil pH
* Rainfall

The system also checks whether the supplied values fall within the observed training ranges before presenting the recommendation.

---

### 🧪 Soil Health Analysis

The platform evaluates:

* Nitrogen
* Phosphorus
* Potassium
* Soil pH

and converts the numerical values into understandable statuses such as:

* Low
* Medium
* High
* Acidic
* Neutral
* Alkaline

The goal is to make the output understandable to users who may not have a machine-learning background.

---

### 🧴 Fertilizer Planning

KisanAI includes a separate fertilizer decision engine that considers:

* Crop nutrient requirements
* Current nutrient levels
* Nutrient deficits
* Fertilizer composition
* Fertilizer prices
* Available farmer budget

The optimizer calculates fertilizer quantities and attempts to maximize nutrient coverage while remaining within the available budget.

The fertilizer engine uses a **kg/acre calculation basis**, while the crop-model inputs are evaluated in **kg/ha** where applicable. The system intentionally avoids silently converting between these units because doing so without an explicitly compatible calculation basis could produce misleading recommendations.

---

### 🔍 Explainable AI

KisanAI uses **SHAP (SHapley Additive exPlanations)** to show which input features contributed to a crop prediction.

For example, the system can show contributions from:

* Nitrogen
* Phosphorus
* Potassium
* Temperature
* Humidity
* Soil pH
* Rainfall

This provides users with more transparency than simply displaying a predicted crop.

> SHAP values explain model behavior. They should not be interpreted as proof that a particular feature causally determines crop suitability.

---

### 📊 Persistent Farm Reports

Every completed agricultural decision can be saved as an analysis report.

Reports preserve:

* Recommended crop
* Model confidence
* Input reliability
* Original farm conditions
* Training ranges
* Soil-health analysis
* SHAP explanations
* Fertilizer-planning status
* Agricultural decision-support disclaimer

Users can return to previous analyses through the Reports section.

---

### 🎙️ Voice Interaction

The frontend includes a voice-first interaction layer designed to make the platform easier to use.

The interface supports multilingual presentation in:

* English
* हिन्दी
* मराठी

The language selector updates the application interface and voice-assistant presentation.

---

## 🧠 Machine Learning

### Production Model

KisanAI currently uses a **Random Forest Classifier** for crop recommendation.

The model-development workflow included:

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

The final production artifact was trained on the complete dataset after model selection.

### Dataset

The production crop model was developed using the public `Crop_recommendation.csv` dataset containing:

| Property       | Value |
| -------------- | ----: |
| Samples        | 2,200 |
| Input features |     7 |
| Crop classes   |    22 |

The supported crop classes include:

`apple`, `banana`, `blackgram`, `chickpea`, `coconut`, `coffee`, `cotton`, `grapes`, `jute`, `kidneybeans`, `lentil`, `maize`, `mango`, `mothbeans`, `mungbean`, `muskmelon`, `orange`, `papaya`, `pigeonpeas`, `pomegranate`, `rice`, `watermelon`

---

## 📈 Model Performance

The primary generalization result is based on an untouched hold-out test set.

| Metric                  |             Result |
| ----------------------- | -----------------: |
| Hold-out Accuracy       |         **99.55%** |
| Weighted Precision      |         **99.57%** |
| Weighted Recall         |         **99.55%** |
| Weighted F1             |         **99.55%** |
| Log Loss                |         **0.0572** |
| 5-Fold Cross-Validation | **99.60% ± 0.55%** |

### Important interpretation

These results describe performance on the available benchmark dataset.

They **do not mean that KisanAI is 99.55% accurate on real-world farms**.

Real agricultural environments can differ because of:

* Regional soil differences
* Measurement errors
* Weather variation
* Crop varieties
* Seasonal conditions
* Dataset distribution differences

Model confidence is therefore treated as model output rather than a guarantee of agricultural success.

---

## 🏗️ System Architecture

KisanAI 2.0 uses a multi-service architecture:

```text
                         ┌─────────────────────┐
                         │      Farmer/User     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   React + Vite      │
                         │     Frontend        │
                         │      Vercel         │
                         └──────────┬──────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌─────────────────────┐
                         │   Node.js + Express │
                         │      Backend        │
                         │       Render        │
                         └───────┬─────┬───────┘
                                 │     │
                    ┌────────────┘     └─────────────┐
                    ▼                                ▼
          ┌──────────────────┐              ┌─────────────────┐
          │   Python / Flask │              │     SQLite      │
          │    ML Service    │              │    Database     │
          │      Render      │              │                 │
          └────────┬─────────┘              └─────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Random Forest    │
          │ Crop Prediction  │
          └──────────────────┘

                   +
                   
          ┌──────────────────────────┐
          │ Agricultural Decision    │
          │ Engine                   │
          │                          │
          │ • Soil Health            │
          │ • Fertilizer Planning    │
          │ • Budget Optimization    │
          │ • Explainability         │
          └──────────────────────────┘
```

### Request flow

```text
Farmer Input
     │
     ▼
Frontend Validation
     │
     ▼
Node.js / Express API
     │
     ▼
Python ML Service
     │
     ├──► Crop Prediction
     │
     └──► Model Confidence
              │
              ▼
     Agricultural Decision Engine
              │
       ┌──────┼─────────┐
       ▼      ▼         ▼
     Soil   Fertilizer  SHAP
    Health   Planning   Explanation
       │      │         │
       └──────┼─────────┘
              ▼
       Saved Farm Analysis
              │
              ▼
          Reports UI
```

---

## 🛠️ Tech Stack

### Frontend

* React
* React Router
* Vite
* JavaScript
* CSS
* Browser Speech APIs

### Backend

* Node.js
* Express
* REST APIs
* CORS
* dotenv
* SQLite

### Machine Learning

* Python
* Flask
* scikit-learn
* Random Forest
* SHAP
* Joblib
* NumPy
* Pandas

### Deployment

* Vercel — frontend
* Render — backend API
* Render — ML service

---

## 📁 Project Structure

```text
KisanAI-2.0/
│
├── backend/
│   ├── src/
│   │   ├── app.js
│   │   ├── config/
│   │   ├── routes/
│   │   └── services/
│   ├── tests/
│   └── package.json
│
├── database/
│   └── schema.sql
│
├── docs/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── i18n/
│   │   └── nlp/
│   ├── public/
│   ├── vercel.json
│   └── package.json
│
├── ml-service/
│   ├── api.py
│   ├── models/
│   ├── fertilizer/
│   ├── decision/
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## ⚙️ Running Locally

### Prerequisites

Make sure the following are installed:

* Node.js
* npm
* Python 3
* Git

---

### 1. Clone the repository

```bash
git clone https://github.com/ayareshreyas/KisanAI-2.0.git
cd KisanAI-2.0
```

---

### 2. Start the ML service

```bash
cd ml-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn api:app
```

The ML service runs on:

```text
http://127.0.0.1:5001
```

---

### 3. Start the backend

Open another terminal:

```bash
cd KisanAI-2.0
npm --prefix backend install
npm --prefix backend start
```

The backend runs on:

```text
http://localhost:5002
```

---

### 4. Start the frontend

Open another terminal:

```bash
cd KisanAI-2.0
npm --prefix frontend install
npm --prefix frontend run dev
```

The frontend runs on:

```text
http://localhost:5173
```

---

## 🔌 Main API Endpoints

The backend exposes the following ML-related routes:

| Method | Endpoint                        | Purpose                        |
| ------ | ------------------------------- | ------------------------------ |
| GET    | `/api/ml/health`                | Check ML service health        |
| POST   | `/api/ml/crop/predict`          | Crop prediction                |
| POST   | `/api/ml/soil/analyze`          | Soil-health analysis           |
| POST   | `/api/ml/fertilizer/recommend`  | Fertilizer planning            |
| POST   | `/api/ml/agricultural-decision` | Complete agricultural decision |

---

## 🧪 Testing

Backend tests can be executed with:

```bash
npm --prefix backend test
```

Frontend NLP tests:

```bash
npm --prefix frontend test
```

Frontend production build:

```bash
npm --prefix frontend run build
```

The project also contains dedicated validation/testing for the fertilizer decision engine and ML-service functionality.

---

## 🔐 Environment Configuration

### Backend

The backend uses environment variables for deployment configuration.

Example:

```env
PORT=5002
ML_SERVICE_URL=http://127.0.0.1:5001
FRONTEND_URL=http://localhost:5173
```

For production, the ML service URL and frontend URL are configured through the hosting platform's environment variables.

### Frontend

The frontend uses:

```env
VITE_API_BASE_URL=http://localhost:5002
```

For production, this points to the deployed backend API.

---

## 🌾 Fertilizer Engine Design

The fertilizer engine is intentionally separated from the crop-prediction model.

The crop model operates on the crop-recommendation feature space, while fertilizer planning uses explicit **kg/acre nutrient inputs** and crop nutrient requirements.

This separation prevents the system from silently mixing incompatible measurement bases.

The fertilizer engine is therefore treated as a **decision-support prototype**, not as a universal fertilizer prescription system.

Formal agricultural recommendations should consider:

* Soil testing
* Crop variety
* Expected yield
* Local conditions
* Weather
* Irrigation
* Regional agricultural recommendations
* Expert/local agricultural guidance

---

## ⚠️ Limitations

KisanAI 2.0 is an AI-assisted agricultural decision-support system and should not be treated as a replacement for professional agricultural advice.

Important limitations include:

1. The crop model is trained on a benchmark dataset rather than a comprehensive real-world agricultural dataset.
2. High benchmark accuracy does not guarantee real-world field accuracy.
3. Model confidence is not a guarantee of crop success.
4. SHAP explanations describe model behavior and are not causal explanations.
5. Fertilizer planning is based on the assumptions and nutrient requirements encoded in the prototype knowledge base.
6. Fertilizer calculations require compatible kg/acre inputs.
7. Local soil testing and agricultural expertise should be considered before making field-level decisions.

---

## 🔮 Future Improvements

Potential future development includes:

* Larger region-specific agricultural datasets
* Real soil-test integrations
* Weather API integration
* Location-aware crop recommendations
* Crop disease detection
* Satellite/remote-sensing data
* Yield prediction
* More advanced fertilizer optimization
* Calibrated model probabilities
* User authentication and farmer profiles
* Mobile application
* Offline-first support
* More Indian languages
* Integration with agricultural extension services

---

## 🎯 Why This Project Matters

KisanAI 2.0 was built to explore how machine learning can be turned into a **usable end-to-end product** rather than remaining only as a trained model.

The project combines:

**Machine Learning + Explainable AI + Backend APIs + Decision Systems + Database Persistence + Frontend Engineering + Cloud Deployment**

This makes KisanAI 2.0 both an agricultural decision-support prototype and a practical demonstration of building and deploying an AI-enabled full-stack application.

---

## 👨‍💻 Author

**Shreyas Ayare**

CSE (AI & ML) Student
Mumbai University

GitHub: https://github.com/ayareshreyas

---

## 📄 Disclaimer

KisanAI 2.0 provides **AI-assisted agricultural decision support for educational and prototype purposes**.

Its recommendations should be considered together with soil testing, local agricultural knowledge, weather conditions, crop-specific requirements, and qualified agricultural advice.

The system does not guarantee crop yield, profitability, or agricultural outcomes.
