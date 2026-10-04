import {
  createContext,
  useContext,
  useMemo,
  useState,
} from 'react'
import translations from './translations'

/* oxlint-disable react-refresh/only-export-components */

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en')

  const value = useMemo(() => {
    const dictionary = translations[language]

    return {
      language,
      setLanguage,
      t: dictionary,
    }
  }, [language])

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)

  if (!context) {
    throw new Error(
      'useLanguage must be used inside a LanguageProvider'
    )
  }

  return context
}