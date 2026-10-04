const INTENT_KEYWORDS = {
  en: {
    crop_recommendation: [
      'crop recommendation',
      'recommend a crop',
      'recommend crops',
      'which crop',
      'what crop',
      'best crop',
      'crop advice',
      'crop suggestion',
      'choose a crop',
      'suggest a crop',
    ],

    soil_analysis: [
      'soil analysis',
      'soil health',
      'check my soil',
      'analyze my soil',
      'analyse my soil',
      'soil test',
      'soil report',
      'check soil',
      'soil condition',
    ],

    fertilizer_recommendation: [
      'fertilizer recommendation',
      'fertilizer advice',
      'which fertilizer',
      'what fertilizer',
      'fertilizer should i use',
      'recommend fertilizer',
      'fertilizer suggestion',
      'fertilizer needed',
      'i need fertilizer',
      'i need a fertilizer recommendation',
      'i want a fertilizer recommendation',
    ],

    reports: [
      'show my reports',
      'show reports',
      'my reports',
      'open reports',
      'view reports',
      'report history',
      'previous reports',
    ],
  },

  hi: {
    crop_recommendation: [
      'फसल की सलाह',
      'फसल की सिफारिश',
      'कौन सी फसल',
      'कौनसा फसल',
      'कौन सा फसल',
      'फसल बताओ',
      'फसल सुझाओ',
      'फसल चुनने',
      'मुझे फसल की सलाह चाहिए',
      'मुझे फसल की सिफारिश चाहिए',
      'मुझे फसल की recommendation चाहिए',

      'fasal ki salah',
      'fasal ki sifarish',
      'kaun si fasal',
      'kaunsi fasal',
      'kaun sa fasal',
      'fasal batao',
      'fasal sujhao',
      'fasal chunne',
      'fasal ki salah chahiye',
      'fasal ki sifarish chahiye',
      'mujhe fasal ki salah chahiye',
      'mujhe fasal ki sifarish chahiye',
      'mujhe fasal ki recommendation chahiye',
    ],

    soil_analysis: [
      'मिट्टी की जांच',
      'मिट्टी जांच',
      'मिट्टी का परीक्षण',
      'मिट्टी की जांच करो',
      'मिट्टी की रिपोर्ट',
      'मिट्टी का स्वास्थ्य',
      'मेरी मिट्टी',
      'मिट्टी की स्थिति',
      'मुझे मिट्टी की जांच चाहिए',
      'मुझे मिट्टी की जांच करवानी है',
      'मुझे अपनी मिट्टी की जांच चाहिए',

      'mitti ki jaanch',
      'mitti jaanch',
      'mitti ka parikshan',
      'mitti ki jaanch karo',
      'mitti ki report',
      'mitti ka swasthya',
      'meri mitti',
      'mitti ki sthiti',
      'mujhe mitti ki jaanch chahiye',
      'mujhe apni mitti ki jaanch chahiye',
    ],

    fertilizer_recommendation: [
      'खाद की सलाह',
      'खाद की सिफारिश',
      'कौन सा खाद',
      'कौन सी खाद',
      'कौनसा खाद',
      'कौन सा उर्वरक',
      'उर्वरक की सलाह',
      'उर्वरक बताओ',
      'उर्वरक की सिफारिश',
      'मुझे उर्वरक की सलाह चाहिए',
      'मुझे उर्वरक की सिफारिश चाहिए',
      'मुझे उर्वरक चाहिए',
      'मुझे खाद की सलाह चाहिए',
      'मुझे खाद की सिफारिश चाहिए',
      'मुझे खाद चाहिए',

      'khaad ki salah',
      'khaad ki sifarish',
      'kaun sa khaad',
      'kaun si khaad',
      'kaunsa khaad',
      'kaun sa urvarak',
      'urvarak ki salah',
      'urvarak batao',
      'urvarak ki sifarish',
      'mujhe urvarak ki salah chahiye',
      'mujhe urvarak ki sifarish chahiye',
      'mujhe urvarak chahiye',
      'mujhe khaad ki salah chahiye',
      'mujhe khaad ki sifarish chahiye',
      'mujhe khaad chahiye',
    ],

    reports: [
      'मेरी रिपोर्ट',
      'मेरी रिपोर्ट दिखाओ',
      'रिपोर्ट दिखाओ',
      'रिपोर्ट खोलो',
      'रिपोर्ट देखें',
      'रिपोर्ट इतिहास',
      'पुरानी रिपोर्ट',
      'मुझे मेरी रिपोर्ट चाहिए',
      'मेरी पुरानी रिपोर्ट चाहिए',

      'meri report',
      'meri report dikhao',
      'report dikhao',
      'report kholo',
      'report dekhen',
      'report itihas',
      'purani report',
      'mujhe meri report chahiye',
      'meri purani report chahiye',
    ],
  },

  mr: {
    crop_recommendation: [
      'पिकाची शिफारस',
      'पिकाची सलाह',
      'कोणते पीक',
      'कोणतं पीक',
      'कोणते पिक',
      'पीक सांगा',
      'पीक सुचवा',
      'पीक निवड',

      'pikachi shifaras',
      'pikachi salah',
      'konte pik',
      'kont pik',
      'pik sanga',
      'pik suchva',
      'pik nivad',
      'pikachi shifaras havi',
      'pikachi salah havi',

      'mala pikachi shifaras havi',
      'mala pikachi salah havi',
      'mala pik suchva',
      'mala pik sanga',

      'mala pikachi shifaras',
      'mala pikachi salah',
      'mala pikachi sifaras',
      'mala pikachi sifarash',
      'mala pikachi sifarish',

      'mala pikachu',
      'pikachu paras',
      'pikachu paras kavi',
      'mala pikachu paras',
    ],

    soil_analysis: [
      'मातीची तपासणी',
      'माती तपासा',
      'मातीचे परीक्षण',
      'मातीचा अहवाल',
      'मातीचे आरोग्य',
      'माझी माती',
      'मातीची स्थिती',
      'मला मातीची तपासणी हवी',
      'मला माझ्या मातीची तपासणी हवी',

      'matichi tapasani',
      'mati tapasa',
      'matice parikshan',
      'mati cha ahaval',
      'maticha ahaval',
      'matice aarogya',
      'majhi mati',
      'matichi sthiti',
      'majhi mati tapasa',
      'mala matichi tapasani havi',
      'mala majhya matichi tapasani havi',
    ],

    fertilizer_recommendation: [
      'खताची शिफारस',
      'खताचा सल्ला',
      'कोणते खत',
      'कोणतं खत',
      'कोणते खत वापरावे',
      'खत सुचवा',
      'खताचा सल्ला द्या',
      'खताची गरज',
      'मला खताची शिफारस हवी',
      'मला खताचा सल्ला हवा',
      'मला खत हवे',
      'उर्वरकाची शिफारस',
      'मला उर्वरकाची शिफारस हवी',

      'khatachi shifaras',
      'khatacha salla',
      'konte khat',
      'kont khat',
      'konte khat vaparave',
      'khat suchva',
      'khatacha salla dya',
      'khatachi garaj',
      'mala khatachi shifaras havi',
      'mala khatacha salla hava',
      'mala khat have',
      'mala urvarakachi shifaras havi',
    ],

    reports: [
      'माझे रिपोर्ट',
      'माझे अहवाल',
      'रिपोर्ट दाखवा',
      'अहवाल दाखवा',
      'रिपोर्ट उघडा',
      'अहवाल उघडा',
      'जुने रिपोर्ट',
      'मला माझे रिपोर्ट हवे',
      'मला माझे अहवाल हवे',

      'majhe report',
      'majhe ahaval',
      'report dakhva',
      'ahaval dakhva',
      'report ughda',
      'ahaval ughda',
      'june report',
      'mala majhe report have',
      'mala majhe ahaval have',
    ],
  },
}

function normalizeText(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/[?!.,]/g, '')
    .replace(/\s+/g, ' ')
}

function detectIntent(text, language = 'en') {
  const normalizedText = normalizeText(text)

  if (!normalizedText) {
    return {
      intent: 'unknown',
      confidence: 0,
      language,
    }
  }

  const allMatches = []

  Object.entries(INTENT_KEYWORDS).forEach(
    ([detectedLanguage, intents]) => {
      Object.entries(intents).forEach(
        ([intent, phrases]) => {
          phrases.forEach((phrase) => {
            const normalizedPhrase =
              normalizeText(phrase)

            if (
              normalizedText.includes(
                normalizedPhrase
              )
            ) {
              allMatches.push({
                intent,
                language: detectedLanguage,
                phrase: normalizedPhrase,
              })
            }
          })
        }
      )
    }
  )

  if (allMatches.length === 0) {
    return {
      intent: 'unknown',
      confidence: 0,
      language,
    }
  }

  const intentCounts = {}

  allMatches.forEach((match) => {
    intentCounts[match.intent] =
      (intentCounts[match.intent] || 0) + 1
  })

  const sortedIntents =
    Object.entries(intentCounts).sort(
      (a, b) => b[1] - a[1]
    )

  const [bestIntent, matchCount] =
    sortedIntents[0]

  const bestIntentMatches =
    allMatches.filter(
      (match) => match.intent === bestIntent
    )

  const languageCounts = {}

  bestIntentMatches.forEach((match) => {
    languageCounts[match.language] =
      (languageCounts[match.language] || 0) + 1
  })

  const detectedLanguage =
    Object.entries(languageCounts).sort(
      (a, b) => b[1] - a[1]
    )[0][0]

  const confidence = Math.min(
    1,
    0.6 + (matchCount - 1) * 0.15
  )

  return {
    intent: bestIntent,
    confidence,
    language: detectedLanguage,
    matchedPhrases: bestIntentMatches.map(
      (match) => match.phrase
    ),
  }
}

export {
  detectIntent,
}