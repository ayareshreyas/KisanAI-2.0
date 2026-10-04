import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n/LanguageContext'
import VoiceAssistant from '../components/VoiceAssistant'
import './Home.css'

function Home() {
  const { t } = useLanguage()

  return (
    <main className="home-page">

      {/* Hero */}
      <section className="home-hero">

        <div>
          <p className="home-eyebrow">
            {t.home.eyebrow}
          </p>

          <h1>
            {t.home.greeting}
          </h1>

          <p className="home-description">
            {t.home.subtitle}
          </p>
        </div>

        <div className="home-status">
          <span className="status-dot" />
          {t.home.ready}
        </div>

      </section>


      {/* Voice Assistant */}
      <section className="home-voice-section">

        <VoiceAssistant />

      </section>


      {/* Farming Tools */}
      <section className="home-tools">

        <div className="section-heading">

          <div>
            <p className="section-eyebrow">
              {t.home.farmingTools}
            </p>

            <h2>
              {t.home.whatWouldYouLikeToDo}
            </h2>
          </div>

        </div>


        <div className="tool-grid">

          {/* Crop Recommendation */}
          <Link
            to="/crop-recommendation"
            className="tool-card"
          >
            <div className="tool-icon">
              🌾
            </div>

            <h3>
              {t.home.cropRecommendation}
            </h3>

            <p>
              {t.home.cropRecommendationDescription}
            </p>

            <span className="tool-arrow">
              →
            </span>
          </Link>


          {/* Soil Health */}
          <Link
            to="/soil-health"
            className="tool-card"
          >
            <div className="tool-icon">
              🌱
            </div>

            <h3>
              {t.home.soilHealth}
            </h3>

            <p>
              {t.home.soilHealthDescription}
            </p>

            <span className="tool-arrow">
              →
            </span>
          </Link>


          {/* Fertilizer */}
          <Link
            to="/fertilizer"
            className="tool-card"
          >
            <div className="tool-icon">
              🧪
            </div>

            <h3>
              {t.home.fertilizerPlan}
            </h3>

            <p>
              {t.home.fertilizerPlanDescription}
            </p>

            <span className="tool-arrow">
              →
            </span>
          </Link>


          {/* Reports */}
          <Link
            to="/reports"
            className="tool-card"
          >
            <div className="tool-icon">
              📄
            </div>

            <h3>
              {t.home.myReports}
            </h3>

            <p>
              {t.home.myReportsDescription}
            </p>

            <span className="tool-arrow">
              →
            </span>
          </Link>

        </div>

      </section>


      {/* How KisanAI Helps */}
      <section className="home-how">

        <div className="section-heading">

          <div>
            <p className="section-eyebrow">
              {t.home.simpleProcess}
            </p>

            <h2>
              {t.home.howKisanAIHelps}
            </h2>
          </div>

        </div>


        <div className="steps-grid">

          {/* Step 1 */}
          <div className="step-card">

            <span className="step-number">
              01
            </span>

            <div className="step-icon">
              🎙️
            </div>

            <h3>
              {t.home.stepOneTitle}
            </h3>

            <p>
              {t.home.stepOneDescription}
            </p>

          </div>


          {/* Step 2 */}
          <div className="step-card">

            <span className="step-number">
              02
            </span>

            <div className="step-icon">
              🧠
            </div>

            <h3>
              {t.home.stepTwoTitle}
            </h3>

            <p>
              {t.home.stepTwoDescription}
            </p>

          </div>


          {/* Step 3 */}
          <div className="step-card">

            <span className="step-number">
              03
            </span>

            <div className="step-icon">
              🌾
            </div>

            <h3>
              {t.home.stepThreeTitle}
            </h3>

            <p>
              {t.home.stepThreeDescription}
            </p>

          </div>

        </div>

      </section>


      {/* Transparency */}
      <section className="home-transparency">

        <div className="transparency-icon">
          🔍
        </div>

        <div>

          <p className="section-eyebrow">
            Explainable AI
          </p>

          <h2>
            {t.home.transparencyTitle}
          </h2>

          <p>
            {t.home.transparencyDescription}
          </p>

        </div>

      </section>


      {/* Footer */}
      <footer className="home-footer">

        <div className="footer-brand">
          🌱 KisanAI
        </div>

        <p>
          {t.home.footerTagline}
        </p>

      </footer>

    </main>
  )
}

export default Home