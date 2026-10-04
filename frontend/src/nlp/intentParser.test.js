import test from 'node:test'
import assert from 'node:assert/strict'

import { detectIntent } from './intentParser.js'

test('detects English crop recommendation intent', () => {
  const result = detectIntent(
    'I want a crop recommendation',
    'en'
  )

  assert.equal(result.intent, 'crop_recommendation')
  assert.equal(result.language, 'en')
  assert.ok(result.confidence > 0)
  assert.ok(result.matchedPhrases.length > 0)
})

test('detects English soil analysis intent', () => {
  const result = detectIntent(
    'Check my soil',
    'en'
  )

  assert.equal(result.intent, 'soil_analysis')
  assert.equal(result.language, 'en')
  assert.ok(result.confidence > 0)
})

test('detects English fertilizer recommendation intent', () => {
  const result = detectIntent(
    'Which fertilizer should I use?',
    'en'
  )

  assert.equal(
    result.intent,
    'fertilizer_recommendation'
  )
  assert.equal(result.language, 'en')
  assert.ok(result.confidence > 0)
})

test('detects English reports intent', () => {
  const result = detectIntent(
    'Show my reports',
    'en'
  )

  assert.equal(result.intent, 'reports')
  assert.equal(result.language, 'en')
  assert.ok(result.confidence > 0)
})

test('detects Hindi crop recommendation intent', () => {
  const result = detectIntent(
    'मुझे फसल की सलाह चाहिए',
    'hi'
  )

  assert.equal(result.intent, 'crop_recommendation')
  assert.equal(result.language, 'hi')
  assert.ok(result.confidence > 0)
})

test('detects Hindi soil analysis intent', () => {
  const result = detectIntent(
    'मेरी मिट्टी की जांच करो',
    'hi'
  )

  assert.equal(result.intent, 'soil_analysis')
  assert.equal(result.language, 'hi')
  assert.ok(result.confidence > 0)
})

test('detects Hindi fertilizer recommendation intent', () => {
  const result = detectIntent(
    'मुझे कौन सा खाद इस्तेमाल करना चाहिए',
    'hi'
  )

  assert.equal(
    result.intent,
    'fertilizer_recommendation'
  )
  assert.equal(result.language, 'hi')
  assert.ok(result.confidence > 0)
})

test('detects Marathi crop recommendation intent', () => {
  const result = detectIntent(
    'मला पिकाची शिफारस हवी आहे',
    'mr'
  )

  assert.equal(result.intent, 'crop_recommendation')
  assert.equal(result.language, 'mr')
  assert.ok(result.confidence > 0)
})

test('detects Marathi soil analysis intent', () => {
  const result = detectIntent(
    'माझी माती तपासा',
    'mr'
  )

  assert.equal(result.intent, 'soil_analysis')
  assert.equal(result.language, 'mr')
  assert.ok(result.confidence > 0)
})

test('detects Marathi fertilizer recommendation intent', () => {
  const result = detectIntent(
    'मला कोणते खत वापरावे',
    'mr'
  )

  assert.equal(
    result.intent,
    'fertilizer_recommendation'
  )
  assert.equal(result.language, 'mr')
  assert.ok(result.confidence > 0)
})

test('detects Hindi romanized crop recommendation', () => {
  const result = detectIntent(
    'mujhe fasal ki salah chahiye',
    'hi'
  )

  assert.equal(result.intent, 'crop_recommendation')
  assert.equal(result.language, 'hi')
})

test('detects Marathi romanized soil analysis', () => {
  const result = detectIntent(
    'mala matichi tapasani havi',
    'mr'
  )

  assert.equal(result.intent, 'soil_analysis')
  assert.equal(result.language, 'mr')
})

test('detects Marathi romanized fertilizer recommendation', () => {
  const result = detectIntent(
    'mala khatachi shifaras havi',
    'mr'
  )

  assert.equal(
    result.intent,
    'fertilizer_recommendation'
  )
  assert.equal(result.language, 'mr')
})

test('handles punctuation and extra spaces', () => {
  const result = detectIntent(
    '   Which fertilizer should I use?!   ',
    'en'
  )

  assert.equal(
    result.intent,
    'fertilizer_recommendation'
  )
  assert.equal(result.language, 'en')
})

test('returns unknown for an empty string', () => {
  const result = detectIntent('', 'en')

  assert.equal(result.intent, 'unknown')
  assert.equal(result.confidence, 0)
  assert.equal(result.language, 'en')
})

test('returns unknown for whitespace-only input', () => {
  const result = detectIntent('     ', 'en')

  assert.equal(result.intent, 'unknown')
  assert.equal(result.confidence, 0)
  assert.equal(result.language, 'en')
})

test('returns unknown for unrelated text', () => {
  const result = detectIntent(
    'The weather is beautiful today',
    'en'
  )

  assert.equal(result.intent, 'unknown')
  assert.equal(result.confidence, 0)
  assert.equal(result.language, 'en')
})

test('returns matched phrases for a successful detection', () => {
  const result = detectIntent(
    'I want a crop recommendation',
    'en'
  )

  assert.ok(Array.isArray(result.matchedPhrases))
  assert.ok(result.matchedPhrases.length >= 1)
  assert.ok(
    result.matchedPhrases.includes(
      'crop recommendation'
    )
  )
})

test('confidence stays within the valid range', () => {
  const testInputs = [
    ['I want a crop recommendation', 'en'],
    ['Check my soil', 'en'],
    ['Which fertilizer should I use?', 'en'],
    ['Show my reports', 'en'],
    ['मुझे फसल की सलाह चाहिए', 'hi'],
    ['मेरी मिट्टी की जांच करो', 'hi'],
    ['मला पिकाची शिफारस हवी आहे', 'mr'],
    ['माझी माती तपासा', 'mr'],
  ]

  for (const [text, language] of testInputs) {
    const result = detectIntent(text, language)

    assert.ok(result.confidence >= 0)
    assert.ok(result.confidence <= 1)
  }
})