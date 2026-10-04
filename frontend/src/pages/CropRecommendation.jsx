import { useLocation } from 'react-router-dom'
import { useState } from 'react'

import { useLanguage } from '../i18n/LanguageContext'
import API_BASE_URL from '../config/api'

import './CropRecommendation.css'

const INITIAL_FORM = {
  N: '',
  P: '',
  K: '',
  temperature: '',
  humidity: '',
  ph: '',
  rainfall: '',
}

function CropRecommendation() {
  const { t } = useLanguage()
  const location = useLocation()

  const [form, setForm] = useState(INITIAL_FORM)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showTechnicalDetails, setShowTechnicalDetails] =
    useState(false)

  const voiceRequest =
    location.state?.voiceRequest || null

  function handleChange(event) {
    const { name, value } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setLoading(true)
    setError('')
    setResult(null)
    setShowTechnicalDetails(false)

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/ml/agricultural-decision`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            N: Number(form.N),
            P: Number(form.P),
            K: Number(form.K),
            temperature: Number(form.temperature),
            humidity: Number(form.humidity),
            ph: Number(form.ph),
            rainfall: Number(form.rainfall),
          }),
        }
      )

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(
          data.error ||
            'Unable to generate agricultural analysis.'
        )
      }

      setResult(data.decision)
    } catch (submitError) {
      setError(
        submitError.message ||
          'Unable to generate agricultural analysis.'
      )
    } finally {
      setLoading(false)
    }
  }

  function handleReset() {
    setForm(INITIAL_FORM)
    setResult(null)
    setError('')
    setShowTechnicalDetails(false)
  }

  const cropRecommendation =
    result?.crop_recommendation || null

  const soilHealth =
    result?.soil_health || null

  const cropExplanation =
    result?.crop_explanation || null

  const fertilizerPlanning =
    result?.fertilizer_planning || null

  const inputReliability =
    result?.input_reliability || null

  const reliabilityIsOutsideRange =
    inputReliability?.status ===
    'outside_training_range'

  return (
    <main className="crop-page">
      <section className="crop-header">
        <div>
          <p className="crop-eyebrow">
            Agricultural Decision Support
          </p>

          <h1>
            {t.nav.cropRecommendation}
          </h1>

          <p className="crop-description">
            Enter your farm and soil conditions to receive
            an AI-assisted crop recommendation together with
            soil health and model reliability information.
          </p>
        </div>
      </section>

      {voiceRequest && (
        <section className="voice-request-card">
          <div className="voice-request-icon">
            🎙️
          </div>

          <div>
            <p className="voice-request-label">
              Voice request
            </p>

            <p className="voice-request-text">
              {voiceRequest}
            </p>
          </div>
        </section>
      )}

      <section className="crop-content">
        <div className="crop-form-card">
          <div className="card-heading">
            <p className="section-eyebrow">
              Farm conditions
            </p>

            <h2>
              Enter your farm information
            </h2>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <label>
                <span>Nitrogen (N)</span>

                <input
                  type="number"
                  name="N"
                  value={form.N}
                  onChange={handleChange}
                  min="0"
                  step="any"
                  placeholder="e.g. 90"
                  required
                />

                <small>kg/ha</small>
              </label>

              <label>
                <span>Phosphorus (P)</span>

                <input
                  type="number"
                  name="P"
                  value={form.P}
                  onChange={handleChange}
                  min="0"
                  step="any"
                  placeholder="e.g. 42"
                  required
                />

                <small>kg/ha</small>
              </label>

              <label>
                <span>Potassium (K)</span>

                <input
                  type="number"
                  name="K"
                  value={form.K}
                  onChange={handleChange}
                  min="0"
                  step="any"
                  placeholder="e.g. 43"
                  required
                />

                <small>kg/ha</small>
              </label>

              <label>
                <span>Temperature</span>

                <input
                  type="number"
                  name="temperature"
                  value={form.temperature}
                  onChange={handleChange}
                  step="any"
                  placeholder="e.g. 25"
                  required
                />

                <small>°C</small>
              </label>

              <label>
                <span>Humidity</span>

                <input
                  type="number"
                  name="humidity"
                  value={form.humidity}
                  onChange={handleChange}
                  min="0"
                  max="100"
                  step="any"
                  placeholder="e.g. 80"
                  required
                />

                <small>%</small>
              </label>

              <label>
                <span>Soil pH</span>

                <input
                  type="number"
                  name="ph"
                  value={form.ph}
                  onChange={handleChange}
                  min="0"
                  max="14"
                  step="any"
                  placeholder="e.g. 6.5"
                  required
                />

                <small>pH</small>
              </label>

              <label>
                <span>Rainfall</span>

                <input
                  type="number"
                  name="rainfall"
                  value={form.rainfall}
                  onChange={handleChange}
                  min="0"
                  step="any"
                  placeholder="e.g. 200"
                  required
                />

                <small>mm</small>
              </label>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="primary-button"
                disabled={loading}
              >
                {loading
                  ? 'Analyzing...'
                  : 'Analyze Farm'}
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={handleReset}
                disabled={loading}
              >
                Reset
              </button>
            </div>
          </form>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        {result && (
          <div className="crop-results">
            <section className="result-card recommendation-card">
              <div className="result-card-header">
                <div>
                  <p className="section-eyebrow">
                    AI recommendation
                  </p>

                  <h2>
                    Recommended Crop
                  </h2>
                </div>

                <span className="result-icon">
                  🌾
                </span>
              </div>

              <div className="recommendation-result">
                <div>
                  <span className="result-label">
                    Recommended crop
                  </span>

                  <h3>
                    {cropRecommendation?.crop || '—'}
                  </h3>
                </div>

                <div className="confidence-block">
                  <span className="result-label">
                    Model confidence
                  </span>

                  <strong>
                    {cropRecommendation
                      ? `${(
                          cropRecommendation.confidence *
                          100
                        ).toFixed(1)}%`
                      : '—'}
                  </strong>
                </div>
              </div>
            </section>

            {inputReliability && (
              <section
                className={`result-card reliability-card ${
                  reliabilityIsOutsideRange
                    ? 'reliability-warning'
                    : 'reliability-success'
                }`}
              >
                <div className="result-card-header">
                  <div>
                    <p className="section-eyebrow">
                      Model reliability
                    </p>

                    <h2>
                      Input Reliability
                    </h2>
                  </div>

                  <span className="reliability-status-icon">
                    {reliabilityIsOutsideRange
                      ? '⚠️'
                      : '✓'}
                  </span>
                </div>

                <div className="reliability-summary">
                  <strong>
                    {reliabilityIsOutsideRange
                      ? 'Prediction should be interpreted cautiously'
                      : 'Inputs are within the model training range'}
                  </strong>

                  <p>
                    {inputReliability.message}
                  </p>
                </div>

                {inputReliability.warnings?.length > 0 && (
                  <div className="reliability-warnings">
                    {inputReliability.warnings.map(
                      (warning) => (
                        <div
                          className="reliability-warning-item"
                          key={warning.feature}
                        >
                          <strong>
                            {warning.label}
                          </strong>

                          <span>
                            Supplied value: {warning.value}{' '}
                            {warning.unit}
                          </span>

                          <span>
                            Training maximum:{' '}
                            {warning.training_maximum}{' '}
                            {warning.unit}
                          </span>
                        </div>
                      )
                    )}
                  </div>
                )}

                <button
                  type="button"
                  className="technical-details-button"
                  onClick={() =>
                    setShowTechnicalDetails(
                      (current) => !current
                    )
                  }
                >
                  {showTechnicalDetails
                    ? 'Hide technical details'
                    : 'Show technical details'}
                </button>

                {showTechnicalDetails && (
                  <div className="technical-details">
                    <p>
                      These ranges represent the minimum and
                      maximum values observed in the dataset
                      used to train the crop recommendation
                      model. They are not agricultural
                      recommendations or safe farming limits.
                    </p>

                    <div className="technical-feature-list">
                      {inputReliability.checked_features?.map(
                        (feature) => (
                          <div
                            className="technical-feature"
                            key={feature.feature}
                          >
                            <span>
                              {feature.label}
                            </span>

                            <span>
                              {feature.value}{' '}
                              {feature.unit}
                            </span>

                            <span>
                              Observed training range:{' '}
                              {feature.training_minimum}
                              {' – '}
                              {feature.training_maximum}{' '}
                              {feature.unit}
                            </span>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}
              </section>
            )}

            {soilHealth && (
              <section className="result-card">
                <div className="result-card-header">
                  <div>
                    <p className="section-eyebrow">
                      Soil analysis
                    </p>

                    <h2>
                      Soil Health
                    </h2>
                  </div>

                  <span className="result-icon">
                    🌱
                  </span>
                </div>

                <div className="soil-grid">
                  <div className="soil-item">
                    <span>Nitrogen</span>

                    <strong>
                      {soilHealth.nitrogen?.status}
                    </strong>

                    <small>
                      {soilHealth.nitrogen?.value}{' '}
                      {soilHealth.nitrogen?.unit}
                    </small>
                  </div>

                  <div className="soil-item">
                    <span>Phosphorus</span>

                    <strong>
                      {soilHealth.phosphorus?.status}
                    </strong>

                    <small>
                      {soilHealth.phosphorus?.value}{' '}
                      {soilHealth.phosphorus?.unit}
                    </small>
                  </div>

                  <div className="soil-item">
                    <span>Potassium</span>

                    <strong>
                      {soilHealth.potassium?.status}
                    </strong>

                    <small>
                      {soilHealth.potassium?.value}{' '}
                      {soilHealth.potassium?.unit}
                    </small>
                  </div>

                  <div className="soil-item">
                    <span>pH</span>

                    <strong>
                      {soilHealth.ph?.status}
                    </strong>

                    <small>
                      {soilHealth.ph?.value}{' '}
                      {soilHealth.ph?.unit}
                    </small>
                  </div>
                </div>
              </section>
            )}

            {cropExplanation && (
              <section className="result-card">
                <div className="result-card-header">
                  <div>
                    <p className="section-eyebrow">
                      Explainable AI
                    </p>

                    <h2>
                      Why the model made this prediction
                    </h2>
                  </div>

                  <span className="result-icon">
                    🔍
                  </span>
                </div>

                <div className="explanation-list">
                  {cropExplanation.feature_contributions?.map(
                    (item) => (
                      <div
                        className="explanation-item"
                        key={item.feature}
                      >
                        <div>
                          <strong>
                            {item.feature}
                          </strong>

                          <span>
                            Value: {item.value}
                          </span>
                        </div>

                        <span
                          className={
                            item.contribution >= 0
                              ? 'positive-contribution'
                              : 'negative-contribution'
                          }
                        >
                          {item.contribution >= 0
                            ? '+'
                            : ''}
                          {item.contribution.toFixed(4)}
                        </span>
                      </div>
                    )
                  )}
                </div>
              </section>
            )}

            {fertilizerPlanning && (
              <section className="result-card">
                <div className="result-card-header">
                  <div>
                    <p className="section-eyebrow">
                      Fertilizer planning
                    </p>

                    <h2>
                      Fertilizer Planning
                    </h2>
                  </div>

                  <span className="result-icon">
                    🧪
                  </span>
                </div>

                {fertilizerPlanning.available ? (
                  <div className="planning-success">
                    Fertilizer optimization is available
                    for this analysis.
                  </div>
                ) : (
                  <div className="planning-info">
                    <strong>
                      Planning not generated yet
                    </strong>

                    <p>
                      {fertilizerPlanning.reason}
                    </p>
                  </div>
                )}
              </section>
            )}

            <section className="decision-support-notice">
              <span>ℹ️</span>

              <p>
                KisanAI provides AI-assisted decision
                support. Recommendations should be
                considered together with local agricultural
                knowledge, soil testing, weather conditions,
                and expert advice.
              </p>
            </section>
          </div>
        )}
      </section>
    </main>
  )
}

export default CropRecommendation