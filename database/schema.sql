PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    N REAL NOT NULL,
    P REAL NOT NULL,
    K REAL NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    ph REAL NOT NULL,
    rainfall REAL NOT NULL,

    predicted_crop TEXT NOT NULL,
    model_confidence REAL NOT NULL,

    crop_explanation_json TEXT NOT NULL,
    soil_health_json TEXT NOT NULL,
    fertilizer_planning_json TEXT NOT NULL,
    input_reliability_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_analyses_created_at
ON analyses(created_at);