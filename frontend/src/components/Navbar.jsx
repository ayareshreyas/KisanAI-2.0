import { useLanguage } from '../i18n/LanguageContext'
import './Navbar.css'

function Navbar() {
  const { language, setLanguage, t } = useLanguage()

  const languages = [
    { code: 'en', label: 'English' },
    { code: 'hi', label: 'हिन्दी' },
    { code: 'mr', label: 'मराठी' },
  ]

  return (
    <nav className="navbar">
      <div className="navbar-inner">

        <div className="navbar-brand">
          <span className="navbar-logo">
            🌱
          </span>

          <div>
            <strong>KisanAI</strong>

            <span>
              {t.home.footerTagline}
            </span>
          </div>
        </div>


        <div className="navbar-links">

          <a href="/">
            {t.nav.home}
          </a>

          <a href="/crop-recommendation">
            {t.nav.cropRecommendation}
          </a>

          <a href="/soil-health">
            {t.nav.soilHealth}
          </a>

          <a href="/fertilizer">
            {t.nav.fertilizer}
          </a>

          <a href="/reports">
            {t.nav.reports}
          </a>

        </div>


        <div className="language-selector">

          <span className="language-icon">
            🌐
          </span>

          <select
            value={language}
            onChange={(event) =>
              setLanguage(event.target.value)
            }
            aria-label="Select language"
          >
            {languages.map((item) => (
              <option
                key={item.code}
                value={item.code}
              >
                {item.label}
              </option>
            ))}
          </select>

          <span className="language-current">
            {
              languages.find(
                (item) => item.code === language
              )?.label
            }
          </span>

        </div>

      </div>
    </nav>
  )
}

export default Navbar