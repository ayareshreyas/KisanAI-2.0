import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useLanguage } from '../i18n/LanguageContext'
import { detectIntent } from '../nlp/intentParser'
import './VoiceAssistant.css'

const LANGUAGE_MAP = {
  en: 'en-IN',
  hi: 'hi-IN',
  mr: 'mr-IN',
}

function VoiceAssistant() {
  const { language } = useLanguage()
  const navigate = useNavigate()

  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [confirmedText, setConfirmedText] = useState('')
  const [detectedIntent, setDetectedIntent] = useState(null)
  const [error, setError] = useState('')

  const recognitionRef = useRef(null)

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition

    if (!SpeechRecognition) {
      return
    }

    const recognition = new SpeechRecognition()

    recognition.continuous = false
    recognition.interimResults = true
    recognition.lang =
      LANGUAGE_MAP[language] || 'en-IN'

    recognition.onstart = () => {
      setIsListening(true)
      setError('')
    }

    recognition.onresult = (event) => {
      let currentTranscript = ''

      for (
        let index = event.resultIndex;
        index < event.results.length;
        index += 1
      ) {
        currentTranscript +=
          event.results[index][0].transcript
      }

      setTranscript(currentTranscript)
    }

    recognition.onerror = (event) => {
      setIsListening(false)

      if (event.error === 'not-allowed') {
        setError(
          'Microphone permission was denied.'
        )
      } else if (event.error === 'no-speech') {
        setError(
          'No speech was detected. Please try again.'
        )
      } else {
        setError(
          'Something went wrong with speech recognition.'
        )
      }
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      recognition.stop()
      recognitionRef.current = null
    }
  }, [language])

  const startListening = () => {
    if (!recognitionRef.current) {
      setError(
        'Speech recognition is not available in this browser.'
      )
      return
    }

    setTranscript('')
    setConfirmedText('')
    setDetectedIntent(null)
    setError('')

    try {
      recognitionRef.current.start()
    } catch (recognitionError) {
      if (
        recognitionError.name !==
        'InvalidStateError'
      ) {
        setError(
          'Unable to start speech recognition.'
        )
      }
    }
  }

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
  }

  const handleIntentAction = (intent) => {
    const routes = {
      crop_recommendation: '/crop-recommendation',
      soil_analysis: '/soil-health',
      fertilizer_recommendation: '/fertilizer',
      reports: '/reports',
    }

    const targetRoute = routes[intent]

    if (!targetRoute) {
      return
    }

    navigate(targetRoute, {
      state: {
        voiceRequest: confirmedText,
        voiceLanguage: language,
        voiceIntent: intent,
      },
    })
  }

  const confirmTranscript = () => {
    const cleanedTranscript = transcript.trim()

    if (!cleanedTranscript) {
      setError(
        'No speech was recognized. Please try again.'
      )
      return
    }

    setError('')
    setConfirmedText(cleanedTranscript)

    try {
      const result = detectIntent(
        cleanedTranscript,
        language
      )

      setDetectedIntent(result)
    } catch (parserError) {
      console.error(
        'Intent parser error:',
        parserError
      )

      setDetectedIntent({
        intent: 'unknown',
        confidence: 0,
        language,
      })

      setError(
        'The speech was recognized, but KisanAI could not process the request.'
      )
    }
  }

  const retrySpeech = () => {
    setTranscript('')
    setConfirmedText('')
    setDetectedIntent(null)
    setError('')

    startListening()
  }

  return (
    <div className="voice-assistant">
      <div className="voice-header">
        <div className="voice-icon">
          {isListening ? '🔴' : '🎙️'}
        </div>

        <div>
          <p className="voice-label">
            Voice Assistant
          </p>

          <h3>
            {isListening
              ? 'Listening...'
              : 'Talk to KisanAI'}
          </h3>
        </div>
      </div>

      <div className="voice-controls">
        {!isListening ? (
          <button
            type="button"
            className="voice-button"
            onClick={startListening}
          >
            🎙️ Start Talking
          </button>
        ) : (
          <button
            type="button"
            className="voice-button listening"
            onClick={stopListening}
          >
            ⏹ Stop Listening
          </button>
        )}
      </div>

      {isListening && (
        <div className="listening-indicator">
          <span />
          <span />
          <span />
          <span />
          <span />
        </div>
      )}

      {transcript && !confirmedText && (
        <div className="transcript-card">
          <p className="transcript-label">
            KisanAI heard
          </p>

          <p className="transcript-text">
            {transcript}
          </p>

          {!isListening && (
            <div className="transcript-actions">
              <button
                type="button"
                className="confirm-button"
                onClick={confirmTranscript}
              >
                ✓ Confirm
              </button>

              <button
                type="button"
                className="retry-button"
                onClick={retrySpeech}
              >
                ↻ Try Again
              </button>
            </div>
          )}
        </div>
      )}

      {confirmedText && (
        <div className="confirmed-card">
          <p className="transcript-label">
            Confirmed
          </p>

          <p className="transcript-text">
            {confirmedText}
          </p>

          {detectedIntent && (
            <div className="intent-result">
              <span className="intent-label">
                Detected request
              </span>

              <strong>
                {detectedIntent.intent}
              </strong>
            </div>
          )}

          {detectedIntent &&
            detectedIntent.intent !== 'unknown' && (
              <button
                type="button"
                className="intent-action-button"
                onClick={() =>
                  handleIntentAction(
                    detectedIntent.intent
                  )
                }
              >
                Continue with KisanAI →
              </button>
            )}

          {detectedIntent &&
            detectedIntent.intent === 'unknown' && (
              <div className="unknown-request">
                KisanAI couldn't identify this request.
                Please try asking about crop
                recommendations, soil health,
                fertilizers, or reports.
              </div>
            )}
        </div>
      )}

      {error && (
        <div className="voice-error">
          {error}
        </div>
      )}
    </div>
  )
}

export default VoiceAssistant