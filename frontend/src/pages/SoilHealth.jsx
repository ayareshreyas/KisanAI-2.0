import { useLocation, Link } from 'react-router-dom'
import { useState } from 'react'
import { useLanguage } from '../i18n/LanguageContext'
import './SoilHealth.css'

const translations = {
  en: {
    eyebrow: 'Soil Intelligence',
    title: 'Understand your soil',
    description:
      'Analyze nitrogen, phosphorus, potassium and soil pH to understand the current condition of your soil.',
    voiceRequest: 'Voice request',
    language: 'Language',
    inputTitle: 'Enter soil test values',
    inputDescription:
      'Enter the values from your soil laboratory report.',
    nitrogen: 'Nitrogen (N)',
    phosphorus: 'Phosphorus (P)',
    potassium: 'Potassium (K)',
    ph: 'Soil pH',
    analyze: 'Analyze Soil',
    analyzing: 'Analyzing...',
    resultEyebrow: 'Soil Analysis',
    overview: 'Soil overview',
    attention: 'Needs attention',
    healthy: 'Healthy range',
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    veryHigh: 'Very High',
    stronglyAcidic: 'Strongly Acidic',
    moderatelyAcidic: 'Moderately Acidic',
    neutral: 'Neutral',
    moderatelyAlkaline: 'Moderately Alkaline',
    stronglyAlkaline: 'Strongly Alkaline',
    interpretation:
      'This analysis classifies the supplied soil-test values using KisanAI soil interpretation rules.',
    disclaimer:
      'This result is an informational interpretation of soil-test values and should not replace advice from an agricultural expert or soil laboratory.',
    error: 'Unable to analyze the soil.',
    back: 'Back to dashboard',
    pageBadge: 'Soil Health',
    nitrogenDescription: 'Soil nitrogen level',
    phosphorusDescription: 'Soil phosphorus level',
    potassiumDescription: 'Soil potassium level',
    phDescription: 'Soil acidity / alkalinity',
    nutrientValue: 'Current value',
    soilPh: 'pH level',
    interpretationTitle: 'How to read this result',
    interpretationDescription:
      'The nutrient classifications describe the supplied soil-test values according to KisanAI rules. They are intended to help understand the current soil condition.',
    noAttention:
      'No low or very-high nutrient classifications were detected.',
  },

  hi: {
    eyebrow: 'मिट्टी की जानकारी',
    title: 'अपनी मिट्टी को समझें',
    description:
      'नाइट्रोजन, फास्फोरस, पोटैशियम और मिट्टी के pH का विश्लेषण करके अपनी मिट्टी की स्थिति समझें।',
    voiceRequest: 'वॉइस अनुरोध',
    language: 'भाषा',
    inputTitle: 'मिट्टी की जांच के मान दर्ज करें',
    inputDescription:
      'अपनी मिट्टी की प्रयोगशाला रिपोर्ट से मान दर्ज करें।',
    nitrogen: 'नाइट्रोजन (N)',
    phosphorus: 'फास्फोरस (P)',
    potassium: 'पोटैशियम (K)',
    ph: 'मिट्टी का pH',
    analyze: 'मिट्टी का विश्लेषण करें',
    analyzing: 'विश्लेषण हो रहा है...',
    resultEyebrow: 'मिट्टी का विश्लेषण',
    overview: 'मिट्टी का अवलोकन',
    attention: 'ध्यान देने योग्य',
    healthy: 'स्वस्थ सीमा',
    low: 'कम',
    medium: 'मध्यम',
    high: 'अधिक',
    veryHigh: 'बहुत अधिक',
    stronglyAcidic: 'अत्यधिक अम्लीय',
    moderatelyAcidic: 'मध्यम अम्लीय',
    neutral: 'तटस्थ',
    moderatelyAlkaline: 'मध्यम क्षारीय',
    stronglyAlkaline: 'अत्यधिक क्षारीय',
    interpretation:
      'यह विश्लेषण KisanAI के मिट्टी वर्गीकरण नियमों के आधार पर दिए गए मिट्टी परीक्षण मानों की व्याख्या करता है।',
    disclaimer:
      'यह परिणाम मिट्टी परीक्षण मानों की जानकारीपूर्ण व्याख्या है और इसे कृषि विशेषज्ञ या मिट्टी प्रयोगशाला की सलाह का विकल्प नहीं माना जाना चाहिए।',
    error: 'मिट्टी का विश्लेषण नहीं हो सका।',
    back: 'डैशबोर्ड पर वापस जाएं',
    pageBadge: 'मिट्टी का स्वास्थ्य',
    nitrogenDescription: 'मिट्टी में नाइट्रोजन का स्तर',
    phosphorusDescription: 'मिट्टी में फास्फोरस का स्तर',
    potassiumDescription: 'मिट्टी में पोटैशियम का स्तर',
    phDescription: 'मिट्टी की अम्लीय / क्षारीय स्थिति',
    nutrientValue: 'वर्तमान मान',
    soilPh: 'pH स्तर',
    interpretationTitle: 'इस परिणाम को कैसे समझें',
    interpretationDescription:
      'पोषक तत्वों की श्रेणियां KisanAI के नियमों के अनुसार दिए गए मिट्टी परीक्षण मानों को दर्शाती हैं। इनका उपयोग वर्तमान मिट्टी की स्थिति समझने के लिए किया जा सकता है।',
    noAttention:
      'कम या बहुत अधिक पोषक तत्व की कोई श्रेणी नहीं मिली।',
  },

  mr: {
    eyebrow: 'मातीची माहिती',
    title: 'तुमची माती समजून घ्या',
    description:
      'नायट्रोजन, फॉस्फरस, पोटॅशियम आणि मातीचा pH तपासून मातीची सध्याची स्थिती समजून घ्या.',
    voiceRequest: 'व्हॉइस विनंती',
    language: 'भाषा',
    inputTitle: 'माती तपासणीचे मूल्य भरा',
    inputDescription:
      'तुमच्या मातीच्या प्रयोगशाळेच्या अहवालातील मूल्ये भरा.',
    nitrogen: 'नायट्रोजन (N)',
    phosphorus: 'फॉस्फरस (P)',
    potassium: 'पोटॅशियम (K)',
    ph: 'मातीचा pH',
    analyze: 'मातीचे विश्लेषण करा',
    analyzing: 'विश्लेषण सुरू आहे...',
    resultEyebrow: 'मातीचे विश्लेषण',
    overview: 'मातीचा आढावा',
    attention: 'लक्ष देण्याची गरज',
    healthy: 'योग्य श्रेणी',
    low: 'कमी',
    medium: 'मध्यम',
    high: 'जास्त',
    veryHigh: 'खूप जास्त',
    stronglyAcidic: 'तीव्र आम्लीय',
    moderatelyAcidic: 'मध्यम आम्लीय',
    neutral: 'तटस्थ',
    moderatelyAlkaline: 'मध्यम क्षारीय',
    stronglyAlkaline: 'तीव्र क्षारीय',
    interpretation:
      'हे विश्लेषण KisanAI च्या माती वर्गीकरण नियमांनुसार दिलेल्या माती तपासणी मूल्यांचे स्पष्टीकरण करते.',
    disclaimer:
      'हा निकाल माती तपासणी मूल्यांचे माहितीपूर्ण स्पष्टीकरण आहे. तो कृषी तज्ज्ञ किंवा माती प्रयोगशाळेच्या सल्ल्याचा पर्याय नाही.',
    error: 'मातीचे विश्लेषण करता आले नाही.',
    back: 'डॅशबोर्डवर परत जा',
    pageBadge: 'मातीचे आरोग्य',
    nitrogenDescription: 'मातीतील नायट्रोजनची पातळी',
    phosphorusDescription: 'मातीतील फॉस्फरसची पातळी',
    potassiumDescription: 'मातीतील पोटॅशियमची पातळी',
    phDescription: 'मातीची आम्लीय / क्षारीय स्थिती',
    nutrientValue: 'सध्याचे मूल्य',
    soilPh: 'pH पातळी',
    interpretationTitle: 'हा निकाल कसा समजून घ्यावा',
    interpretationDescription:
      'पोषक घटकांच्या श्रेणी KisanAI च्या नियमांनुसार दिलेल्या माती तपासणी मूल्यांचे वर्णन करतात. यामुळे मातीची सध्याची स्थिती समजण्यास मदत होते.',
    noAttention:
      'कमी किंवा खूप जास्त पोषक घटकांची कोणतीही श्रेणी आढळली नाही.',
  },
}

function SoilHealth() {
  const { language } = useLanguage()
  const location = useLocation()

  const t = translations[language] || translations.en

  const voiceRequest = location.state?.voiceRequest
  const voiceLanguage = location.state?.voiceLanguage
  const voiceIntent = location.state?.voiceIntent

  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    ph: '',
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
      ph: Number(formData.ph),
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
        'http://localhost:5002/api/ml/soil/analyze',
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
        throw new Error(data.error || t.error)
      }

      // The backend returns the soil analysis under `soil_health`.
      setResult(data.soil_health)
    } catch (requestError) {
      console.error(
        'Soil analysis error:',
        requestError
      )

      setError(
        requestError.message || t.error
      )
    } finally {
      setLoading(false)
    }
  }

  const getStatusLabel = (status) => {
    const statusMap = {
      Low: t.low,
      Medium: t.medium,
      High: t.high,
      'Very High': t.veryHigh,
      'Strongly Acidic': t.stronglyAcidic,
      'Moderately Acidic': t.moderatelyAcidic,
      Neutral: t.neutral,
      'Moderately Alkaline': t.moderatelyAlkaline,
      'Strongly Alkaline': t.stronglyAlkaline,
    }

    return statusMap[status] || status
  }

  const getStatusClass = (status) => {
    if (!status) {
      return 'moderate'
    }

    if (
      status === 'Low' ||
      status === 'Very High' ||
      status === 'Strongly Acidic' ||
      status === 'Strongly Alkaline'
    ) {
      return 'warning'
    }

    if (
      status === 'Medium' ||
      status === 'Moderately Acidic' ||
      status === 'Moderately Alkaline'
    ) {
      return 'moderate'
    }

    if (
      status === 'High' ||
      status === 'Neutral'
    ) {
      return 'healthy'
    }

    return 'moderate'
  }

  const getNutrientWidth = (status) => {
    const widths = {
      Low: '30%',
      Medium: '60%',
      High: '85%',
      'Very High': '100%',
    }

    return widths[status] || '50%'
  }

  const getNutrientDescription = (key) => {
    const descriptions = {
      nitrogen: t.nitrogenDescription,
      phosphorus: t.phosphorusDescription,
      potassium: t.potassiumDescription,
    }

    return descriptions[key]
  }

  const getPhMarkerPosition = (value) => {
    const numericValue = Number(value)

    if (Number.isNaN(numericValue)) {
      return '50%'
    }

    const percentage = (numericValue / 14) * 100

    return `${Math.min(
      Math.max(percentage, 0),
      100
    )}%`
  }

  const nutrientItems = result
    ? [
        {
          key: 'nitrogen',
          label: t.nitrogen,
          symbol: 'N',
          data: result.nitrogen,
        },
        {
          key: 'phosphorus',
          label: t.phosphorus,
          symbol: 'P',
          data: result.phosphorus,
        },
        {
          key: 'potassium',
          label: t.potassium,
          symbol: 'K',
          data: result.potassium,
        },
      ]
    : []

  const attentionItems = nutrientItems.filter(
    (item) =>
      item.data.status === 'Low' ||
      item.data.status === 'Very High'
  )

  return (
    <main className="soil-page">
      <div className="soil-container">
        <div className="soil-topbar">
          <Link
            to="/"
            className="soil-back"
          >
            ← {t.back}
          </Link>

          <div className="soil-page-badge">
            🌱 {t.pageBadge}
          </div>
        </div>

        <section className="soil-heading">
          <p className="soil-eyebrow">
            {t.eyebrow}
          </p>

          <h1>
            {t.title}
          </h1>

          <p className="soil-heading-description">
            {t.description}
          </p>
        </section>

        {voiceIntent === 'soil_analysis' &&
          voiceRequest && (
            <section className="soil-voice-card">
              <div className="soil-voice-icon">
                🎙️
              </div>

              <div className="soil-voice-content">
                <p className="soil-voice-label">
                  {t.voiceRequest}
                </p>

                <p>
                  {voiceRequest}
                </p>

                {voiceLanguage && (
                  <span className="soil-voice-language">
                    {t.language}: {voiceLanguage}
                  </span>
                )}
              </div>
            </section>
          )}

        <form
          className="soil-form-card"
          onSubmit={handleSubmit}
        >
          <div className="soil-section-header">
            <div>
              <span className="soil-section-number">
                01
              </span>

              <div>
                <h2>
                  {t.inputTitle}
                </h2>

                <p>
                  {t.inputDescription}
                </p>
              </div>
            </div>
          </div>

          <div className="soil-form">
            <div className="soil-field">
              <label htmlFor="N">
                <span className="soil-field-icon">
                  N
                </span>

                <span>
                  <span>
                    {t.nitrogen}
                  </span>

                  <small>
                    kg/ha
                  </small>
                </span>
              </label>

              <input
                id="N"
                name="N"
                type="number"
                step="any"
                min="0"
                value={formData.N}
                onChange={handleChange}
                placeholder="e.g. 250"
                required
              />
            </div>

            <div className="soil-field">
              <label htmlFor="P">
                <span className="soil-field-icon">
                  P
                </span>

                <span>
                  <span>
                    {t.phosphorus}
                  </span>

                  <small>
                    kg/ha
                  </small>
                </span>
              </label>

              <input
                id="P"
                name="P"
                type="number"
                step="any"
                min="0"
                value={formData.P}
                onChange={handleChange}
                placeholder="e.g. 18"
                required
              />
            </div>

            <div className="soil-field">
              <label htmlFor="K">
                <span className="soil-field-icon">
                  K
                </span>

                <span>
                  <span>
                    {t.potassium}
                  </span>

                  <small>
                    kg/ha
                  </small>
                </span>
              </label>

              <input
                id="K"
                name="K"
                type="number"
                step="any"
                min="0"
                value={formData.K}
                onChange={handleChange}
                placeholder="e.g. 150"
                required
              />
            </div>

            <div className="soil-field">
              <label htmlFor="ph">
                <span className="soil-field-icon">
                  pH
                </span>

                <span>
                  <span>
                    {t.ph}
                  </span>

                  <small>
                    0–14
                  </small>
                </span>
              </label>

              <input
                id="ph"
                name="ph"
                type="number"
                step="0.1"
                min="0"
                max="14"
                value={formData.ph}
                onChange={handleChange}
                placeholder="e.g. 6.8"
                required
              />
            </div>

            <button
              type="submit"
              className="soil-submit"
              disabled={loading}
            >
              <span>
                {loading
                  ? t.analyzing
                  : t.analyze}
              </span>

              {!loading && (
                <span className="soil-submit-arrow">
                  →
                </span>
              )}
            </button>
          </div>

          {error && (
            <div className="soil-error">
              <span>
                ⚠️
              </span>

              <p>
                {error}
              </p>
            </div>
          )}
        </form>

        {result && (
          <section className="soil-results">
            <div className="soil-results-header">
              <div>
                <div className="soil-results-icon">
                  🌱
                </div>

                <div>
                  <p className="soil-eyebrow">
                    {t.resultEyebrow}
                  </p>

                  <h2>
                    {t.overview}
                  </h2>

                  <p>
                    {t.interpretation}
                  </p>
                </div>
              </div>
            </div>

            <div className="soil-results-grid">
              {nutrientItems.map((item) => {
                const statusClass =
                  getStatusClass(
                    item.data.status
                  )

                return (
                  <div
                    className="soil-result-card"
                    key={item.key}
                  >
                    <div className="soil-result-top">
                      <div className="soil-result-title">
                        <span className="result-nutrient-icon">
                          {item.symbol}
                        </span>

                        <div>
                          <h3>
                            {item.label}
                          </h3>

                          <span>
                            {getNutrientDescription(
                              item.key
                            )}
                          </span>
                        </div>
                      </div>

                      <span
                        className={`soil-status ${statusClass}`}
                      >
                        {getStatusLabel(
                          item.data.status
                        )}
                      </span>
                    </div>

                    <div className="soil-result-value">
                      {item.data.value}
                    </div>

                    <div className="soil-progress">
                      <div
                        className={`soil-progress-fill ${statusClass}`}
                        style={{
                          width:
                            getNutrientWidth(
                              item.data.status
                            ),
                        }}
                      />
                    </div>

                    <span className="soil-result-description">
                      {t.nutrientValue} · {item.data.unit}
                    </span>
                  </div>
                )
              })}

              <div className="soil-result-card">
                <div className="soil-result-top">
                  <div className="soil-result-title">
                    <span className="result-nutrient-icon">
                      pH
                    </span>

                    <div>
                      <h3>
                        {t.ph}
                      </h3>

                      <span>
                        {t.phDescription}
                      </span>
                    </div>
                  </div>

                  <span
                    className={`soil-status ${getStatusClass(
                      result.ph.status
                    )}`}
                  >
                    {getStatusLabel(
                      result.ph.status
                    )}
                  </span>
                </div>

                <div className="soil-result-value">
                  {result.ph.value}
                </div>

                <div className="ph-scale">
                  <div className="ph-scale-track">
                    <div
                      className="ph-scale-marker"
                      style={{
                        left:
                          getPhMarkerPosition(
                            result.ph.value
                          ),
                      }}
                    />
                  </div>

                  <div className="ph-scale-labels">
                    <span>0</span>
                    <span>3.5</span>
                    <span>7</span>
                    <span>10.5</span>
                    <span>14</span>
                  </div>
                </div>

                <span className="soil-result-description">
                  {t.soilPh}
                </span>
              </div>
            </div>

            <div className="soil-overview-grid">
              <div className="soil-overview-card">
                <div className="soil-overview-icon">
                  ✓
                </div>

                <div>
                  <span className="soil-card-eyebrow">
                    {t.healthy}
                  </span>

                  <h3>
                    {t.interpretationTitle}
                  </h3>

                  <p>
                    {t.interpretationDescription}
                  </p>
                </div>
              </div>

              <div className="soil-attention-card">
                <div className="soil-attention-header">
                  <div className="soil-attention-icon">
                    !
                  </div>

                  <span className="soil-card-eyebrow">
                    {t.attention}
                  </span>
                </div>

                {attentionItems.length > 0 ? (
                  <div className="soil-attention-list">
                    {attentionItems.map((item) => (
                      <div
                        className="soil-attention-item"
                        key={item.key}
                      >
                        <span>
                          {item.label}
                        </span>

                        <strong>
                          {getStatusLabel(
                            item.data.status
                          )}
                        </strong>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="soil-attention-list">
                    <div className="soil-attention-item">
                      <span>
                        {t.noAttention}
                      </span>

                      <strong>
                        ✓
                      </strong>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="soil-interpretation">
              <div className="soil-interpretation-icon">
                💡
              </div>

              <div>
                <h3>
                  {t.interpretationTitle}
                </h3>

                <p>
                  {t.disclaimer}
                </p>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  )
}

export default SoilHealth