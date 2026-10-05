import { useLocation } from 'react-router-dom'
import { useState } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import './CropRecommendation.css'
import API_BASE_URL from '../config/api'

function CropRecommendation() {
  const { t } = useLanguage()
  const location = useLocation()

  const voiceRequest = location.state?.voiceRequest
  const voiceLanguage = location.state?.voiceLanguage
  const voiceIntent = location.state?.voiceIntent

  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    setError('')
    setResult(null)

    const numericData = {
      N: Number(formData.N),
      P: Number(formData.P),
      K: Number(formData.K),
      temperature: Number(formData.temperature),
      humidity: Number(formData.humidity),
      ph: Number(formData.ph),
      rainfall: Number(formData.rainfall),
    }

    const hasInvalidValue = Object.values(numericData).some(
      (value) => Number.isNaN(value)
    )

    if (hasInvalidValue) {
      setError('Please enter valid values in all fields.')
      return
    }

    setLoading(true)

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/ml/crop/predict`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(numericData),
        }
      )

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(
          data.error ||
            'Unable to generate crop recommendation.'
        )
      }

      setResult(data)
    } catch (requestError) {
      console.error(
        'Crop recommendation error:',
        requestError
      )

      setError(
        requestError.message ||
          'Unable to connect to the KisanAI backend.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="crop-page">

      <section className="crop-hero">
        <div>
          <p className="section-eyebrow">
            {t.nav.cropRecommendation}
          </p>

          <h1>
            {t.home.cropRecommendation}
          </h1>

          <p className="crop-description">
            Enter the soil and environmental conditions
            to get an ML-based crop recommendation.
          </p>
        </div>
      </section>

      {voiceIntent === 'crop_recommendation' && (
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

            {voiceLanguage && (
              <span className="voice-request-language">
                Language: {voiceLanguage}
              </span>
            )}
          </div>
        </section>
      )}

      <section className="crop-content">

        <form
          className="crop-form-card"
          onSubmit={handleSubmit}
        >
          <div className="card-heading">
            <p className="section-eyebrow">
              Soil & Environment
            </p>

            <h2>
              Enter farming conditions
            </h2>

            <p>
              Provide the values from your soil test
              and current environmental conditions.
            </p>
          </div>

          <div className="crop-form-grid">

            <div className="form-field">
              <label htmlFor="N">
                Nitrogen (N)
              </label>

              <input
                id="N"
                name="N"
                type="number"
                step="any"
                value={formData.N}
                onChange={handleChange}
                placeholder="e.g. 90"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="P">
                Phosphorus (P)
              </label>

              <input
                id="P"
                name="P"
                type="number"
                step="any"
                value={formData.P}
                onChange={handleChange}
                placeholder="e.g. 42"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="K">
                Potassium (K)
              </label>

              <input
                id="K"
                name="K"
                type="number"
                step="any"
                value={formData.K}
                onChange={handleChange}
                placeholder="e.g. 43"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="temperature">
                Temperature (°C)
              </label>

              <input
                id="temperature"
                name="temperature"
                type="number"
                step="any"
                value={formData.temperature}
                onChange={handleChange}
                placeholder="e.g. 25"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="humidity">
                Humidity (%)
              </label>

              <input
                id="humidity"
                name="humidity"
                type="number"
                step="any"
                value={formData.humidity}
                onChange={handleChange}
                placeholder="e.g. 80"
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="ph">
                Soil pH
              </label>

              <input
                id="ph"
                name="ph"
                type="number"
                step="any"
                value={formData.ph}
                onChange={handleChange}
                placeholder="e.g. 6.5"
                required
              />
            </div>

            <div className="form-field form-field-wide">
              <label htmlFor="rainfall">
                Rainfall (mm)
              </label>

              <input
                id="rainfall"
                name="rainfall"
                type="number"
                step="any"
                value={formData.rainfall}
                onChange={handleChange}
                placeholder="e.g. 200"
                required
              />
            </div>

          </div>

          {error && (
            <div className="crop-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="crop-submit-button"
            disabled={loading}
          >
            {loading
              ? 'Analyzing...'
              : 'Get Crop Recommendation →'}
          </button>

        </form>

        {result && (
          <section className="crop-result-card">

            <div className="result-header">
              <div>
                <p className="section-eyebrow">
                  KisanAI recommendation
                </p>

                <h2>
                  {result.prediction}
                </h2>
              </div>

              <div className="confidence-card">
                <span>
                  Confidence
                </span>

                <strong>
                  {Math.round(
                    result.confidence * 100
                  )}
                  %
                </strong>
              </div>
            </div>

            {result.explanation && (
              <div className="explanation-section">

                <div className="card-heading">
                  <p className="section-eyebrow">
                    Explainable AI
                  </p>

                  <h3>
                    Why this prediction?
                  </h3>

                  <p>
                    These feature contributions show
                    which inputs influenced the model's
                    prediction.
                  </p>
                </div>

                <div className="explanation-list">

                  {result.explanation.feature_contributions?.map(
                    (item) => {
                      const contribution =
                        Number(item.contribution)

                      const absoluteContribution =
                        Math.abs(contribution)

                      let influence = 'Lower influence'

                      if (
                        absoluteContribution >= 0.1
                      ) {
                        influence =
                          'Strong influence'
                      } else if (
                        absoluteContribution >= 0.05
                      ) {
                        influence =
                          'Moderate influence'
                      }

                      return (
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

                          <div className="explanation-impact">
                            <span>
                              {influence}
                            </span>

                            <strong>
                              {contribution > 0
                                ? '+'
                                : ''}
                              {contribution.toFixed(3)}
                            </strong>
                          </div>
                        </div>
                      )
                    }
                  )}

                </div>

                <div className="explanation-note">
                  SHAP-based feature contribution explains
                  the model's prediction. It should not be
                  interpreted as a direct agronomic
                  prescription.
                </div>

              </div>
            )}

          </section>
        )}

      </section>

    </main>
  )
}

export default CropRecommendation