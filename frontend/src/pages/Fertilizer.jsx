import { useMemo, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useLanguage } from '../i18n/LanguageContext'
import API_BASE_URL from '../config/api'
import './Fertilizer.css'

const CROPS = [
  'Rice',
  'Wheat',
  'Maize',
  'Sugarcane',
  'Cotton',
  'Soybean',
  'Potato',
  'Tomato',
  'Onion',
  'Chilli',
  'Brinjal',
  'Okra',
  'Cabbage',
  'Cauliflower',
  'Spinach',
]

const translations = {
  en: {
    back: 'Back to Home',
    eyebrow: 'Fertilizer Intelligence',
    title: 'Build a Fertilizer Plan',
    description:
      'Enter your crop and current soil nutrients. KisanAI will calculate a fertilizer combination based on nutrient requirements and your budget.',
    voiceRequest: 'Voice request',
    cropInformation: 'Crop information',
    crop: 'Crop',
    soilNutrients: 'Soil nutrients',
    calculationUnit: 'Calculation unit: kg/acre',
    nitrogen: 'Nitrogen (N)',
    phosphorus: 'Phosphorus (P)',
    potassium: 'Potassium (K)',
    budgetTitle: 'Fertilizer budget',
    budgetLabel: 'Maximum budget (₹)',
    budgetOptional: 'Optional',
    budgetHint:
      'Leave the budget empty to minimize the estimated fertilizer cost.',
    calculate: 'Calculate fertilizer plan',
    calculating: 'Calculating plan...',
    recommendation: 'KisanAI recommendation',
    costMinimization: 'Cost minimization',
    budgetAware: 'Budget aware',
    nutrientDeficit: 'Calculated nutrient deficit',
    required: 'Required',
    fertilizerPlan: 'Recommended fertilizer plan',
    quantity: 'Quantity',
    composition: 'Composition',
    estimatedCost: 'Estimated cost',
    pricePerKg: 'Price / kg',
    nutrientSupply: 'Nutrients supplied',
    totalCost: 'Total estimated cost',
    remainingBudget: 'Remaining budget',
    nutrientCoverage: 'Nutrient coverage',
    remainingDeficit: 'Remaining nutrient deficit',
    noDeficit: 'No remaining nutrient deficit',
    optimizationMessage: 'Optimization result',
    errorTitle: 'Unable to calculate recommendation',
    disclaimerTitle: 'Important',
    disclaimer:
      'These quantities are mathematical optimization results for decision support. They are not direct field-application prescriptions. Actual fertilizer use should be validated using appropriate soil-test interpretation, crop stage, local conditions, and agronomic guidance.',
    unitNote:
      'Fertilizer calculations use soil nutrient values expressed in kg/acre. This calculation should not be treated as a direct conversion of laboratory soil-test values from the Soil Health module.',
    invalidInput: 'Please enter valid non-negative nutrient values.',
    invalidBudget: 'Please enter a valid non-negative budget.',
    tryAgain: 'Try again',
    supportedCrops: 'Supported crops',
  },

  hi: {
    back: 'होम पर वापस जाएँ',
    eyebrow: 'उर्वरक इंटेलिजेंस',
    title: 'उर्वरक योजना बनाएँ',
    description:
      'अपनी फसल और वर्तमान मिट्टी के पोषक तत्व दर्ज करें। किसानAI पोषक आवश्यकता और बजट के आधार पर उर्वरक संयोजन की गणना करेगा।',
    voiceRequest: 'वॉइस अनुरोध',
    cropInformation: 'फसल की जानकारी',
    crop: 'फसल',
    soilNutrients: 'मिट्टी के पोषक तत्व',
    calculationUnit: 'गणना इकाई: kg/acre',
    nitrogen: 'नाइट्रोजन (N)',
    phosphorus: 'फॉस्फोरस (P)',
    potassium: 'पोटैशियम (K)',
    budgetTitle: 'उर्वरक बजट',
    budgetLabel: 'अधिकतम बजट (₹)',
    budgetOptional: 'वैकल्पिक',
    budgetHint:
      'अनुमानित उर्वरक लागत को कम करने के लिए बजट खाली छोड़ें।',
    calculate: 'उर्वरक योजना बनाएँ',
    calculating: 'योजना की गणना हो रही है...',
    recommendation: 'किसानAI सुझाव',
    costMinimization: 'लागत न्यूनतमकरण',
    budgetAware: 'बजट आधारित',
    nutrientDeficit: 'गणना की गई पोषक कमी',
    required: 'आवश्यकता',
    fertilizerPlan: 'अनुशंसित उर्वरक योजना',
    quantity: 'मात्रा',
    composition: 'संघटन',
    estimatedCost: 'अनुमानित लागत',
    pricePerKg: 'प्रति kg कीमत',
    nutrientSupply: 'दिए गए पोषक तत्व',
    totalCost: 'कुल अनुमानित लागत',
    remainingBudget: 'शेष बजट',
    nutrientCoverage: 'पोषक तत्व कवरेज',
    remainingDeficit: 'शेष पोषक कमी',
    noDeficit: 'कोई शेष पोषक कमी नहीं',
    optimizationMessage: 'ऑप्टिमाइज़ेशन परिणाम',
    errorTitle: 'सुझाव की गणना नहीं हो सकी',
    disclaimerTitle: 'महत्वपूर्ण',
    disclaimer:
      'ये मात्राएँ निर्णय-सहायता के लिए गणितीय ऑप्टिमाइज़ेशन के परिणाम हैं। इन्हें सीधे खेत में डालने की मात्रा न मानें। वास्तविक उपयोग के लिए मिट्टी की जाँच, फसल की अवस्था, स्थानीय परिस्थितियों और कृषि विशेषज्ञ की सलाह से सत्यापन आवश्यक है।',
    unitNote:
      'उर्वरक गणना में मिट्टी के पोषक तत्व kg/acre में लिए जाते हैं। इसे Soil Health मॉड्यूल के प्रयोगशाला soil-test मूल्यों का सीधा रूपांतरण न मानें।',
    invalidInput: 'कृपया मान्य और शून्य या उससे अधिक पोषक मान दर्ज करें।',
    invalidBudget: 'कृपया मान्य और शून्य या उससे अधिक बजट दर्ज करें।',
    tryAgain: 'फिर प्रयास करें',
    supportedCrops: 'समर्थित फसलें',
  },

  mr: {
    back: 'मुख्यपृष्ठावर जा',
    eyebrow: 'खत बुद्धिमत्ता',
    title: 'खताची योजना तयार करा',
    description:
      'तुमचे पीक आणि सध्याच्या मातीतील पोषक घटक भरा. किसानAI पोषक गरजा आणि बजेटनुसार खतांचे संयोजन मोजेल.',
    voiceRequest: 'व्हॉइस विनंती',
    cropInformation: 'पिकाची माहिती',
    crop: 'पीक',
    soilNutrients: 'मातीतील पोषक घटक',
    calculationUnit: 'गणना एकक: kg/acre',
    nitrogen: 'नायट्रोजन (N)',
    phosphorus: 'फॉस्फरस (P)',
    potassium: 'पोटॅशियम (K)',
    budgetTitle: 'खताचे बजेट',
    budgetLabel: 'कमाल बजेट (₹)',
    budgetOptional: 'पर्यायी',
    budgetHint:
      'अंदाजे खताचा खर्च कमी करण्यासाठी बजेट रिकामे ठेवा.',
    calculate: 'खताची योजना तयार करा',
    calculating: 'योजनेची गणना सुरू आहे...',
    recommendation: 'किसानAI शिफारस',
    costMinimization: 'किमान खर्च',
    budgetAware: 'बजेटनुसार',
    nutrientDeficit: 'गणना केलेली पोषक कमतरता',
    required: 'आवश्यकता',
    fertilizerPlan: 'शिफारस केलेली खत योजना',
    quantity: 'प्रमाण',
    composition: 'संघटन',
    estimatedCost: 'अंदाजे खर्च',
    pricePerKg: 'प्रति kg किंमत',
    nutrientSupply: 'पुरवलेले पोषक घटक',
    totalCost: 'एकूण अंदाजे खर्च',
    remainingBudget: 'शिल्लक बजेट',
    nutrientCoverage: 'पोषक घटक कव्हरेज',
    remainingDeficit: 'शिल्लक पोषक कमतरता',
    noDeficit: 'पोषक घटकांची शिल्लक कमतरता नाही',
    optimizationMessage: 'ऑप्टिमायझेशन निकाल',
    errorTitle: 'शिफारस मोजता आली नाही',
    disclaimerTitle: 'महत्त्वाचे',
    disclaimer:
      'ही प्रमाणे निर्णय-सहाय्यासाठी गणितीय ऑप्टिमायझेशनचे परिणाम आहेत. त्यांना थेट शेतात वापरण्याचे प्रमाण समजू नये. प्रत्यक्ष वापरासाठी माती परीक्षण, पिकाची अवस्था, स्थानिक परिस्थिती आणि कृषी तज्ज्ञांच्या मार्गदर्शनाने पडताळणी आवश्यक आहे.',
    unitNote:
      'खताची गणना मातीतील पोषक घटक kg/acre मध्ये घेते. Soil Health मॉड्यूलमधील प्रयोगशाळेच्या soil-test मूल्यांचे हे थेट रूपांतर समजू नये.',
    invalidInput: 'कृपया शून्य किंवा त्यापेक्षा जास्त वैध पोषक मूल्ये भरा.',
    invalidBudget: 'कृपया शून्य किंवा त्यापेक्षा जास्त वैध बजेट भरा.',
    tryAgain: 'पुन्हा प्रयत्न करा',
    supportedCrops: 'समर्थित पिके',
  },
}

function Fertilizer() {
  const { language } = useLanguage()
  const location = useLocation()

  const t = translations[language] || translations.en

  const [formData, setFormData] = useState({
    crop: 'Rice',
    N: '',
    P: '',
    K: '',
    budget: '',
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const voiceRequest = location.state?.voiceRequest
  const voiceIntent = location.state?.voiceIntent

  const isBudgetMode =
    result?.optimization_mode === 'budget_aware'

  const cropLabel = useMemo(() => {
    return formData.crop
  }, [formData.crop])

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    const nitrogen = Number(formData.N)
    const phosphorus = Number(formData.P)
    const potassium = Number(formData.K)

    if (
      !Number.isFinite(nitrogen) ||
      nitrogen < 0 ||
      !Number.isFinite(phosphorus) ||
      phosphorus < 0 ||
      !Number.isFinite(potassium) ||
      potassium < 0
    ) {
      setError(t.invalidInput)
      return
    }

    if (
      formData.budget !== '' &&
      (!Number.isFinite(Number(formData.budget)) ||
        Number(formData.budget) < 0)
    ) {
      setError(t.invalidBudget)
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const requestBody = {
        crop: formData.crop,
        N: nitrogen,
        P: phosphorus,
        K: potassium,
      }

      if (formData.budget !== '') {
        requestBody.budget = Number(formData.budget)
      }

      const response = await fetch(
        API_BASE_URL + '/api/ml/fertilizer/recommend',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        },
      )

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(
          data.error ||
            'Fertilizer recommendation failed.',
        )
      }

      // Backend response contract:
      // {
      //   success: true,
      //   fertilizer_plan: { ... }
      // }
      setResult(data.fertilizer_plan)
    } catch (requestError) {
      setError(
        requestError.message ||
          'Fertilizer recommendation failed.',
      )
    } finally {
      setLoading(false)
    }
  }

  function formatCurrency(value) {
    return `₹${Number(value).toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`
  }

  function formatNumber(value) {
    return Number(value).toFixed(2)
  }

  function getCoverage(value) {
    return Math.min(100, Math.max(0, Number(value) || 0))
  }

  return (
    <main className="fertilizer-page">
      <div className="fertilizer-container">
        <Link to="/" className="fertilizer-back-link">
          ← {t.back}
        </Link>

        <section className="fertilizer-hero">
          <div>
            <p className="fertilizer-eyebrow">
              {t.eyebrow}
            </p>

            <h1>{t.title}</h1>

            <p className="fertilizer-hero-description">
              {t.description}
            </p>
          </div>

          <div className="fertilizer-hero-badge">
            <span>🧪</span>
            <strong>{t.supportedCrops}</strong>
            <small>{CROPS.length} crops</small>
          </div>
        </section>

        {voiceIntent ===
          'fertilizer_recommendation' &&
          voiceRequest && (
            <section className="fertilizer-voice-card">
              <div className="fertilizer-voice-icon">
                🎙️
              </div>

              <div>
                <span>{t.voiceRequest}</span>
                <p>“{voiceRequest}”</p>
              </div>
            </section>
          )}

        <form
          className="fertilizer-form"
          onSubmit={handleSubmit}
        >
          <section className="fertilizer-form-section">
            <div className="fertilizer-section-heading">
              <span className="fertilizer-section-icon">
                🌾
              </span>

              <div>
                <p>{t.cropInformation}</p>
                <h2>{t.cropInformation}</h2>
              </div>
            </div>

            <div className="fertilizer-field">
              <label htmlFor="fertilizer-crop">
                {t.crop}
              </label>

              <select
                id="fertilizer-crop"
                name="crop"
                value={formData.crop}
                onChange={handleChange}
              >
                {CROPS.map((crop) => (
                  <option key={crop} value={crop}>
                    {crop}
                  </option>
                ))}
              </select>

              <small>{cropLabel}</small>
            </div>
          </section>

          <section className="fertilizer-form-section">
            <div className="fertilizer-section-heading">
              <span className="fertilizer-section-icon">
                🌱
              </span>

              <div>
                <p>{t.soilNutrients}</p>
                <h2>{t.soilNutrients}</h2>
              </div>
            </div>

            <div className="fertilizer-unit-note">
              <span>ℹ️</span>
              <p>{t.calculationUnit}</p>
            </div>

            <div className="fertilizer-input-grid">
              <div className="fertilizer-field">
                <label htmlFor="fertilizer-N">
                  {t.nitrogen}
                </label>

                <div className="fertilizer-input-wrap">
                  <input
                    id="fertilizer-N"
                    name="N"
                    type="number"
                    min="0"
                    step="any"
                    value={formData.N}
                    onChange={handleChange}
                    placeholder="60"
                    required
                  />
                  <span>kg</span>
                </div>
              </div>

              <div className="fertilizer-field">
                <label htmlFor="fertilizer-P">
                  {t.phosphorus}
                </label>

                <div className="fertilizer-input-wrap">
                  <input
                    id="fertilizer-P"
                    name="P"
                    type="number"
                    min="0"
                    step="any"
                    value={formData.P}
                    onChange={handleChange}
                    placeholder="30"
                    required
                  />
                  <span>kg</span>
                </div>
              </div>

              <div className="fertilizer-field">
                <label htmlFor="fertilizer-K">
                  {t.potassium}
                </label>

                <div className="fertilizer-input-wrap">
                  <input
                    id="fertilizer-K"
                    name="K"
                    type="number"
                    min="0"
                    step="any"
                    value={formData.K}
                    onChange={handleChange}
                    placeholder="20"
                    required
                  />
                  <span>kg</span>
                </div>
              </div>
            </div>

            <div className="fertilizer-unit-note subtle">
              <span>📐</span>
              <p>{t.unitNote}</p>
            </div>
          </section>

          <section className="fertilizer-form-section">
            <div className="fertilizer-section-heading">
              <span className="fertilizer-section-icon">
                💰
              </span>

              <div>
                <p>{t.budgetTitle}</p>
                <h2>{t.budgetTitle}</h2>
              </div>
            </div>

            <div className="fertilizer-field budget-field">
              <label htmlFor="fertilizer-budget">
                {t.budgetLabel}

                <span>{t.budgetOptional}</span>
              </label>

              <div className="fertilizer-input-wrap">
                <span className="currency-prefix">₹</span>

                <input
                  id="fertilizer-budget"
                  name="budget"
                  type="number"
                  min="0"
                  step="any"
                  value={formData.budget}
                  onChange={handleChange}
                  placeholder="4000"
                />
              </div>

              <small>{t.budgetHint}</small>
            </div>
          </section>

          <button
            className="fertilizer-submit"
            type="submit"
            disabled={loading}
          >
            <span>{loading ? '⏳' : '🧪'}</span>
            {loading ? t.calculating : t.calculate}
            {!loading && <strong>→</strong>}
          </button>
        </form>

        {error && (
          <section className="fertilizer-error">
            <div className="fertilizer-error-icon">
              !
            </div>

            <div>
              <h2>{t.errorTitle}</h2>
              <p>{error}</p>
            </div>

            <button
              type="button"
              onClick={() => setError('')}
            >
              {t.tryAgain}
            </button>
          </section>
        )}

        {result && (
          <section className="fertilizer-results">
            <div className="fertilizer-result-header">
              <div>
                <p className="fertilizer-eyebrow">
                  {t.recommendation}
                </p>

                <h2>{result.crop}</h2>

                <p>
                  {isBudgetMode
                    ? t.budgetAware
                    : t.costMinimization}
                </p>
              </div>

              <div className="optimization-badge">
                <span>✓</span>
                {isBudgetMode
                  ? t.budgetAware
                  : t.costMinimization}
              </div>
            </div>

            <div className="fertilizer-summary-grid">
              <div className="fertilizer-summary-card">
                <span>🎯</span>
                <small>{t.totalCost}</small>
                <strong>
                  {formatCurrency(
                    result.fertilizer_optimization
                      .total_cost,
                  )}
                </strong>
              </div>

              <div className="fertilizer-summary-card">
                <span>🌱</span>
                <small>{t.required}</small>
                <strong>
                  {formatNumber(
                    result.nutrient_deficit.N +
                      result.nutrient_deficit.P +
                      result.nutrient_deficit.K,
                  )}{' '}
                  kg
                </strong>
              </div>

              {isBudgetMode && (
                <div className="fertilizer-summary-card">
                  <span>💰</span>
                  <small>{t.remainingBudget}</small>
                  <strong>
                    {formatCurrency(
                      result.fertilizer_optimization
                        .remaining_budget,
                    )}
                  </strong>
                </div>
              )}
            </div>

            <section className="fertilizer-result-section">
              <div className="result-section-title">
                <div>
                  <span>📊</span>
                  <div>
                    <p>{t.nutrientDeficit}</p>
                    <h3>{t.nutrientDeficit}</h3>
                  </div>
                </div>
              </div>

              <div className="nutrient-cards">
                {[
                  ['N', t.nitrogen],
                  ['P', t.phosphorus],
                  ['K', t.potassium],
                ].map(([key, label]) => (
                  <div
                    className="nutrient-card"
                    key={key}
                  >
                    <div className="nutrient-card-top">
                      <span
                        className={`nutrient-symbol nutrient-${key}`}
                      >
                        {key}
                      </span>

                      <div>
                        <strong>{label}</strong>
                        <small>{t.required}</small>
                      </div>
                    </div>

                    <strong className="nutrient-value">
                      {formatNumber(
                        result.nutrient_deficit[key],
                      )}{' '}
                      kg
                    </strong>
                  </div>
                ))}
              </div>
            </section>

            <section className="fertilizer-result-section">
              <div className="result-section-title">
                <div>
                  <span>🧪</span>
                  <div>
                    <p>{t.fertilizerPlan}</p>
                    <h3>{t.fertilizerPlan}</h3>
                  </div>
                </div>
              </div>

              <div className="fertilizer-plan-grid">
                {result.fertilizer_optimization.selected_fertilizers.map(
                  (fertilizer) => (
                    <article
                      className="fertilizer-plan-card"
                      key={fertilizer.fertilizer}
                    >
                      <div className="fertilizer-plan-top">
                        <div className="fertilizer-product-icon">
                          🧪
                        </div>

                        <div>
                          <h4>
                            {fertilizer.fertilizer}
                          </h4>

                          <span>
                            {t.pricePerKg}:{' '}
                            {formatCurrency(
                              fertilizer.price_per_kg,
                            )}
                          </span>
                        </div>
                      </div>

                      <div className="fertilizer-quantity">
                        <small>{t.quantity}</small>
                        <strong>
                          {formatNumber(
                            fertilizer.quantity_kg,
                          )}{' '}
                          kg
                        </strong>
                      </div>

                      <div className="fertilizer-cost">
                        <span>{t.estimatedCost}</span>
                        <strong>
                          {formatCurrency(
                            fertilizer.estimated_cost,
                          )}
                        </strong>
                      </div>

                      <div className="fertilizer-details">
                        <div>
                          <span>{t.composition}</span>
                          <strong>
                            N {fertilizer.composition.N} · P{' '}
                            {fertilizer.composition.P} · K{' '}
                            {fertilizer.composition.K}
                          </strong>
                        </div>

                        <div>
                          <span>{t.nutrientSupply}</span>
                          <strong>
                            N{' '}
                            {formatNumber(
                              fertilizer.nutrients_supplied.N,
                            )}{' '}
                            · P{' '}
                            {formatNumber(
                              fertilizer.nutrients_supplied.P,
                            )}{' '}
                            · K{' '}
                            {formatNumber(
                              fertilizer.nutrients_supplied.K,
                            )}
                          </strong>
                        </div>
                      </div>
                    </article>
                  ),
                )}
              </div>
            </section>

            {isBudgetMode &&
              result.fertilizer_optimization
                .coverage_percentage && (
                <section className="fertilizer-result-section">
                  <div className="result-section-title">
                    <div>
                      <span>📈</span>
                      <div>
                        <p>{t.nutrientCoverage}</p>
                        <h3>{t.nutrientCoverage}</h3>
                      </div>
                    </div>
                  </div>

                  <div className="coverage-list">
                    {[
                      ['N', t.nitrogen],
                      ['P', t.phosphorus],
                      ['K', t.potassium],
                    ].map(([key, label]) => {
                      const coverage =
                        getCoverage(
                          result
                            .fertilizer_optimization
                            .coverage_percentage[key],
                        )

                      return (
                        <div
                          className="coverage-row"
                          key={key}
                        >
                          <div className="coverage-label">
                            <span
                              className={`nutrient-symbol nutrient-${key}`}
                            >
                              {key}
                            </span>

                            <strong>{label}</strong>

                            <b>{coverage.toFixed(2)}%</b>
                          </div>

                          <div className="coverage-track">
                            <div
                              className="coverage-fill"
                              style={{
                                width: `${coverage}%`,
                              }}
                            />
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </section>
              )}

            {isBudgetMode &&
              result.fertilizer_optimization
                .remaining_deficit && (
                <section className="fertilizer-result-section">
                  <div className="result-section-title">
                    <div>
                      <span>⚠️</span>
                      <div>
                        <p>{t.remainingDeficit}</p>
                        <h3>{t.remainingDeficit}</h3>
                      </div>
                    </div>
                  </div>

                  <div className="remaining-deficit-grid">
                    {[
                      ['N', t.nitrogen],
                      ['P', t.phosphorus],
                      ['K', t.potassium],
                    ].map(([key, label]) => {
                      const value =
                        Number(
                          result.fertilizer_optimization
                            .remaining_deficit[key],
                        ) || 0

                      return (
                        <div
                          className="remaining-deficit-card"
                          key={key}
                        >
                          <span
                            className={`nutrient-symbol nutrient-${key}`}
                          >
                            {key}
                          </span>

                          <div>
                            <strong>{label}</strong>
                            <small>
                              {value > 0
                                ? `${formatNumber(value)} kg`
                                : t.noDeficit}
                            </small>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </section>
              )}

            <section className="optimization-message">
              <span>💡</span>

              <div>
                <strong>{t.optimizationMessage}</strong>
                <p>
                  {
                    result.fertilizer_optimization
                      .message
                  }
                </p>
              </div>
            </section>

            <section className="fertilizer-disclaimer">
              <span>⚠️</span>

              <div>
                <strong>{t.disclaimerTitle}</strong>
                <p>{t.disclaimer}</p>
              </div>
            </section>
          </section>
        )}
      </div>
    </main>
  )
}

export default Fertilizer