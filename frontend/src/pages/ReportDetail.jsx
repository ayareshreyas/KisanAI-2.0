import { Link, useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'

import './ReportDetail.css'

function formatDate(dateString) {
  if (!dateString) {
    return ''
  }

  const normalizedDateString =
    dateString.includes('T')
      ? dateString
      : dateString.replace(' ', 'T')

  const date = new Date(
    normalizedDateString.endsWith('Z')
      ? normalizedDateString
      : `${normalizedDateString}Z`
  )

  if (Number.isNaN(date.getTime())) {
    return dateString
  }

  return date.toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

function formatCropName(crop) {
  if (!crop) {
    return 'Unknown crop'
  }

  return crop
    .split(' ')
    .map(
      (word) =>
        word.charAt(0).toUpperCase() +
        word.slice(1)
    )
    .join(' ')
}

function formatFeatureName(feature) {
  if (!feature) {
    return 'Feature'
  }

  const featureNames = {
    N: 'Nitrogen (N)',
    P: 'Phosphorus (P)',
    K: 'Potassium (K)',
    temperature: 'Temperature',
    humidity: 'Humidity',
    ph: 'Soil pH',
    rainfall: 'Rainfall',
  }

  return featureNames[feature] || feature
}

function formatNumber(value, decimals = 2) {
  const number = Number(value)

  if (Number.isNaN(number)) {
    return value
  }

  return number.toFixed(decimals)
}

function formatCurrency(value) {
  const number = Number(value)

  if (Number.isNaN(number)) {
    return '—'
  }

  return `₹${number.toFixed(2)}`
}

function ReportDetail() {
  const { id } = useParams()

  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadAnalysis() {
      try {
        setLoading(true)
        setError('')

        const response = await fetch(
          `http://localhost:5002/api/analysis/history/${id}`
        )

        const data = await response.json()

        if (!response.ok || !data.success) {
          throw new Error(
            data.error || 'Unable to load the analysis.'
          )
        }

        setAnalysis(data.analysis)
      } catch (requestError) {
        console.error(
          'Report detail error:',
          requestError
        )

        setError(
          requestError.message ||
            'Unable to load the analysis.'
        )
      } finally {
        setLoading(false)
      }
    }

    loadAnalysis()
  }, [id])

  if (loading) {
    return (
      <main className="report-detail-page">
        <div className="report-detail-shell">
          <div className="report-detail-state">
            <p>Loading analysis...</p>
          </div>
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="report-detail-page">
        <div className="report-detail-shell">
          <div className="report-detail-state report-detail-error">
            <p>{error}</p>

            <Link
              to="/reports"
              className="report-detail-back-button"
            >
              ← Back to Reports
            </Link>
          </div>
        </div>
      </main>
    )
  }

  if (!analysis) {
    return (
      <main className="report-detail-page">
        <div className="report-detail-shell">
          <div className="report-detail-state">
            <p>Analysis not found.</p>

            <Link
              to="/reports"
              className="report-detail-back-button"
            >
              ← Back to Reports
            </Link>
          </div>
        </div>
      </main>
    )
  }

  const reliability =
    analysis.input_reliability

  const cropRecommendation =
    analysis.crop_recommendation

  const soilHealth =
    analysis.soil_health

  const cropExplanation =
    analysis.crop_explanation

  const fertilizerPlanning =
    analysis.fertilizer_planning

  const featureContributions =
    cropExplanation?.feature_contributions || []

  const reliabilityIsWarning =
    reliability?.status ===
    'outside_training_range'

  const fertilizerAvailable =
    fertilizerPlanning?.available === true

  const fertilizerUnavailable =
    fertilizerPlanning?.available === false

  return (
    <main className="report-detail-page">
      <div className="report-detail-shell">
        <header className="report-detail-header">
          <div>
            <Link
              to="/reports"
              className="report-detail-back-link"
            >
              ← Back to Reports
            </Link>

            <p className="report-detail-eyebrow">
              Saved Farm Analysis
            </p>

            <h1>Analysis Report #{analysis.id}</h1>

            <p className="report-detail-date">
              {formatDate(analysis.created_at)}
            </p>
          </div>

          <Link
            to="/crop-recommendation"
            className="report-detail-new-button"
          >
            + New Analysis
          </Link>
        </header>

        <section className="report-detail-card report-detail-recommendation">
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                AI Recommendation
              </p>

              <h2>Recommended Crop</h2>
            </div>

            <span className="report-detail-crop-icon">
              🌾
            </span>
          </div>

          <div className="report-detail-recommendation-content">
            <div>
              <p className="report-detail-label">
                Recommended crop
              </p>

              <h3>
                {formatCropName(
                  cropRecommendation?.crop
                )}
              </h3>
            </div>

            <div className="report-detail-confidence">
              <span>Model confidence</span>

              <strong>
                {(
                  Number(
                    cropRecommendation?.confidence || 0
                  ) * 100
                ).toFixed(1)}
                %
              </strong>
            </div>
          </div>
        </section>

        <section
          className={`report-detail-card report-detail-reliability ${
            reliabilityIsWarning
              ? 'report-detail-reliability-warning'
              : 'report-detail-reliability-success'
          }`}
        >
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                Model Reliability
              </p>

              <h2>Input Reliability</h2>
            </div>

            <span className="report-detail-reliability-icon">
              {reliabilityIsWarning ? '⚠️' : '✓'}
            </span>
          </div>

          {reliability ? (
            <>
              <h3>
                {reliabilityIsWarning
                  ? 'Inputs are outside the model training range'
                  : 'Inputs are within the model training range'}
              </h3>

              <p className="report-detail-reliability-message">
                {reliability.message}
              </p>

              {reliabilityIsWarning &&
                reliability.warnings?.length > 0 && (
                  <div className="report-detail-warning-list">
                    <p className="report-detail-label">
                      Reliability warnings
                    </p>

                    <ul>
                      {reliability.warnings.map(
                        (warning, index) => (
                          <li
                            key={`${warning.feature}-${index}`}
                          >
                            {warning.message}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

              {reliability.checked_features?.length >
                0 && (
                <details className="report-detail-technical">
                  <summary>
                    Technical details
                  </summary>

                  <div className="report-detail-feature-list">
                    {reliability.checked_features.map(
                      (feature) => (
                        <div
                          className="report-detail-feature"
                          key={feature.feature}
                        >
                          <div>
                            <strong>
                              {feature.label}
                            </strong>

                            <span>
                              {feature.value}{' '}
                              {feature.unit}
                            </span>
                          </div>

                          <p>
                            Observed training range:{' '}
                            {feature.training_minimum} –{' '}
                            {feature.training_maximum}{' '}
                            {feature.unit}
                          </p>
                        </div>
                      )
                    )}
                  </div>
                </details>
              )}

              <p className="report-detail-reliability-note">
                These ranges represent the minimum and
                maximum values observed in the dataset used
                to train the crop recommendation model. They
                are not agricultural recommendations or safe
                farming limits.
              </p>
            </>
          ) : (
            <div className="report-detail-legacy-message">
              <h3>
                Reliability information unavailable
              </h3>

              <p>
                This analysis was created before input
                reliability information was added to
                KisanAI.
              </p>
            </div>
          )}
        </section>

        <section className="report-detail-card">
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                Farm Conditions
              </p>

              <h2>Input Values</h2>
            </div>

            <span className="report-detail-card-icon">
              🌱
            </span>
          </div>

          <div className="report-detail-input-grid">
            <div>
              <span>Nitrogen (N)</span>
              <strong>{analysis.input.N} kg/ha</strong>
            </div>

            <div>
              <span>Phosphorus (P)</span>
              <strong>{analysis.input.P} kg/ha</strong>
            </div>

            <div>
              <span>Potassium (K)</span>
              <strong>{analysis.input.K} kg/ha</strong>
            </div>

            <div>
              <span>Temperature</span>
              <strong>
                {analysis.input.temperature} °C
              </strong>
            </div>

            <div>
              <span>Humidity</span>
              <strong>{analysis.input.humidity} %</strong>
            </div>

            <div>
              <span>Soil pH</span>
              <strong>{analysis.input.ph} pH</strong>
            </div>

            <div>
              <span>Rainfall</span>
              <strong>{analysis.input.rainfall} mm</strong>
            </div>
          </div>
        </section>

        <section className="report-detail-card">
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                Soil Analysis
              </p>

              <h2>Soil Health</h2>
            </div>

            <span className="report-detail-card-icon">
              🌱
            </span>
          </div>

          <div className="report-detail-soil-grid">
            <div>
              <span>Nitrogen</span>
              <strong>
                {soilHealth?.nitrogen?.status || '—'}
              </strong>
              <small>
                {analysis.input.N} kg/ha
              </small>
            </div>

            <div>
              <span>Phosphorus</span>
              <strong>
                {soilHealth?.phosphorus?.status || '—'}
              </strong>
              <small>
                {analysis.input.P} kg/ha
              </small>
            </div>

            <div>
              <span>Potassium</span>
              <strong>
                {soilHealth?.potassium?.status || '—'}
              </strong>
              <small>
                {analysis.input.K} kg/ha
              </small>
            </div>

            <div>
              <span>pH</span>
              <strong>
                {soilHealth?.ph?.status || '—'}
              </strong>
              <small>
                {analysis.input.ph} pH
              </small>
            </div>
          </div>
        </section>

        <section className="report-detail-card">
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                Explainable AI
              </p>

              <h2>Why the Model Made This Prediction</h2>
            </div>

            <span className="report-detail-card-icon">
              🔍
            </span>
          </div>

          <div className="report-detail-explanation-list">
            {featureContributions.length > 0 ? (
              featureContributions.map(
                (item, index) => (
                  <div
                    className="report-detail-explanation-item"
                    key={`${item.feature}-${index}`}
                  >
                    <div>
                      <strong>
                        {formatFeatureName(
                          item.feature
                        )}
                      </strong>

                      <span>
                        Value: {item.value}
                      </span>
                    </div>

                    <strong
                      className={
                        Number(item.contribution) >= 0
                          ? 'report-detail-positive'
                          : 'report-detail-negative'
                      }
                    >
                      {Number(item.contribution) >= 0
                        ? '+'
                        : ''}
                      {Number(
                        item.contribution
                      ).toFixed(4)}
                    </strong>
                  </div>
                )
              )
            ) : (
              <p>
                Explainability information is unavailable
                for this analysis.
              </p>
            )}
          </div>
        </section>

        <section className="report-detail-card">
          <div className="report-detail-card-heading">
            <div>
              <p className="report-detail-eyebrow">
                Fertilizer Planning
              </p>

              <h2>Fertilizer Planning</h2>
            </div>

            <span className="report-detail-card-icon">
              🧪
            </span>
          </div>

          {fertilizerAvailable && (
            <div className="report-detail-fertilizer-success">
              <h3>
                Fertilizer plan available for{' '}
                {formatCropName(
                  fertilizerPlanning.crop
                )}
              </h3>

              {fertilizerPlanning.requirements && (
                <div className="report-detail-fertilizer-summary">
                  <div>
                    <span>N requirement</span>
                    <strong>
                      {formatNumber(
                        fertilizerPlanning.requirements
                          .N
                      )}{' '}
                      kg/ha
                    </strong>
                  </div>

                  <div>
                    <span>P requirement</span>
                    <strong>
                      {formatNumber(
                        fertilizerPlanning.requirements
                          .P
                      )}{' '}
                      kg/ha
                    </strong>
                  </div>

                  <div>
                    <span>K requirement</span>
                    <strong>
                      {formatNumber(
                        fertilizerPlanning.requirements
                          .K
                      )}{' '}
                      kg/ha
                    </strong>
                  </div>
                </div>
              )}

              {fertilizerPlanning.total_cost !==
                undefined && (
                <p className="report-detail-fertilizer-cost">
                  Estimated fertilizer cost:{' '}
                  <strong>
                    {formatCurrency(
                      fertilizerPlanning.total_cost
                    )}
                  </strong>
                </p>
              )}

              <details className="report-detail-technical">
                <summary>
                  View fertilizer calculation details
                </summary>

                <pre className="report-detail-fertilizer">
                  {JSON.stringify(
                    fertilizerPlanning,
                    null,
                    2
                  )}
                </pre>
              </details>
            </div>
          )}

          {fertilizerUnavailable && (
            <div className="report-detail-fertilizer-unavailable">
              <div className="report-detail-fertilizer-status-icon">
                ℹ️
              </div>

              <div>
                <h3>
                  Fertilizer planning unavailable
                </h3>

                <p>
                  We currently do not have a compatible
                  fertilizer requirement profile for{' '}
                  <strong>
                    {formatCropName(
                      fertilizerPlanning.crop
                    )}
                  </strong>{' '}
                  in the KisanAI fertilizer knowledge base.
                </p>

                {fertilizerPlanning.reason && (
                  <p className="report-detail-fertilizer-note">
                    {fertilizerPlanning.reason}
                  </p>
                )}
              </div>
            </div>
          )}

          {!fertilizerAvailable &&
            !fertilizerUnavailable && (
              <div className="report-detail-fertilizer-empty">
                <h3>Planning not generated yet</h3>

                <p>
                  Fertilizer planning information is not
                  available for this analysis.
                </p>
              </div>
            )}
        </section>

        <section className="report-detail-notice">
          <span>ℹ️</span>

          <p>
            KisanAI provides AI-assisted decision support.
            Recommendations should be considered together
            with local agricultural knowledge, soil testing,
            weather conditions, and expert advice.
          </p>
        </section>
      </div>
    </main>
  )
}

export default ReportDetail