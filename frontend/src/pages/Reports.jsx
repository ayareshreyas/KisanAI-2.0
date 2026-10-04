import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n/LanguageContext'
import './Reports.css'

function Reports() {
  const { t } = useLanguage()

  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadHistory() {
      try {
        setLoading(true)
        setError('')

        const response = await fetch(
          'http://localhost:5002/api/analysis/history'
        )

        const data = await response.json()

        if (!response.ok || !data.success) {
          throw new Error(
            data.error || 'Unable to load analysis history.'
          )
        }

        setAnalyses(data.analyses || [])
      } catch (requestError) {
        console.error(
          'Failed to load analysis history:',
          requestError
        )

        setError(
          'Unable to load your previous analyses. Please try again.'
        )
      } finally {
        setLoading(false)
      }
    }

    loadHistory()
  }, [])

  function formatDate(dateString) {
    if (!dateString) {
      return ''
    }

    const date = new Date(
      dateString.replace(' ', 'T') + 'Z'
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

  return (
    <main className="reports-page">

      {/* Header */}
      <section className="reports-header">

        <div>
          <p className="reports-eyebrow">
            {t.home.myReports}
          </p>

          <h1>
            My Reports
          </h1>

          <p className="reports-description">
            View your previous farm analyses and
            recommendation results.
          </p>
        </div>

        <Link
          to="/crop-recommendation"
          className="reports-new-button"
        >
          <span>＋</span>
          New Farm Analysis
        </Link>

      </section>


      {/* Loading */}
      {loading && (
        <section className="reports-state-card">

          <div className="reports-state-icon">
            ⏳
          </div>

          <h2>
            Loading your reports
          </h2>

          <p>
            Please wait while we retrieve your
            previous farm analyses.
          </p>

        </section>
      )}


      {/* Error */}
      {!loading && error && (
        <section className="reports-state-card reports-error-card">

          <div className="reports-state-icon">
            ⚠️
          </div>

          <h2>
            Something went wrong
          </h2>

          <p>
            {error}
          </p>

          <button
            type="button"
            className="reports-retry-button"
            onClick={() => window.location.reload()}
          >
            Try Again
          </button>

        </section>
      )}


      {/* Empty state */}
      {!loading &&
        !error &&
        analyses.length === 0 && (
          <section className="reports-state-card">

            <div className="reports-state-icon">
              🌱
            </div>

            <h2>
              No farm analyses yet
            </h2>

            <p>
              Your completed farm analyses will
              appear here automatically.
            </p>

            <Link
              to="/crop-recommendation"
              className="reports-primary-button"
            >
              Start Farm Analysis
            </Link>

          </section>
        )}


      {/* History */}
      {!loading &&
        !error &&
        analyses.length > 0 && (
          <section className="reports-history">

            <div className="reports-section-heading">

              <div>
                <p className="reports-section-eyebrow">
                  Your activity
                </p>

                <h2>
                  Previous Analyses
                </h2>
              </div>

              <span className="reports-count">
                {analyses.length}{' '}
                {analyses.length === 1
                  ? 'analysis'
                  : 'analyses'}
              </span>

            </div>


            <div className="reports-list">

              {analyses.map((analysis) => {

                const crop =
                  analysis.crop_recommendation?.crop

                const confidence =
                  analysis.crop_recommendation
                    ?.confidence ?? 0

                const soil =
                  analysis.soil_health

                return (
                  <article
                    key={analysis.id}
                    className="report-card"
                  >

                    {/* Main information */}
                    <div className="report-main">

                      <div className="report-crop-icon">
                        🌾
                      </div>

                      <div className="report-content">

                        <div className="report-title-row">

                          <h3>
                            {formatCropName(crop)}
                          </h3>

                          <span className="report-confidence">
                            {Math.round(
                              confidence * 100
                            )}
                            % confidence
                          </span>

                        </div>

                        <p className="report-date">
                          Analysis #{analysis.id}
                          {' · '}
                          {formatDate(
                            analysis.created_at
                          )}
                        </p>

                        <div className="report-soil-summary">

                          <span>
                            <strong>
                              N
                            </strong>
                            {' '}
                            {soil?.nitrogen?.status ||
                              '—'}
                          </span>

                          <span>
                            <strong>
                              P
                            </strong>
                            {' '}
                            {soil?.phosphorus?.status ||
                              '—'}
                          </span>

                          <span>
                            <strong>
                              K
                            </strong>
                            {' '}
                            {soil?.potassium?.status ||
                              '—'}
                          </span>

                          <span>
                            <strong>
                              pH
                            </strong>
                            {' '}
                            {soil?.ph?.status ||
                              '—'}
                          </span>

                        </div>

                      </div>

                    </div>


                    {/* Action */}
                    <Link
                      to={`/reports/${analysis.id}`}
                      className="report-view-button"
                    >
                      View Analysis
                      <span>
                        →
                      </span>
                    </Link>

                  </article>
                )
              })}

            </div>

          </section>
        )}

    </main>
  )
}

export default Reports