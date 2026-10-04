import { detectIntent } from './intentParser'

const testCases = [
  {
    text: 'I want a crop recommendation',
    language: 'en',
  },
  {
    text: 'Check my soil',
    language: 'en',
  },
  {
    text: 'Which fertilizer should I use?',
    language: 'en',
  },
  {
    text: 'Show my reports',
    language: 'en',
  },

  {
    text: 'मुझे फसल की सलाह चाहिए',
    language: 'hi',
  },
  {
    text: 'मेरी मिट्टी की जांच करो',
    language: 'hi',
  },
  {
    text: 'मुझे कौन सा खाद इस्तेमाल करना चाहिए',
    language: 'hi',
  },

  {
    text: 'मला पिकाची शिफारस हवी आहे',
    language: 'mr',
  },
  {
    text: 'माझी माती तपासा',
    language: 'mr',
  },
  {
    text: 'मला कोणते खत वापरावे',
    language: 'mr',
  },
]

testCases.forEach((testCase) => {
  const result = detectIntent(
    testCase.text,
    testCase.language
  )

  console.log(
    `${testCase.language} | ${testCase.text}`
  )

  console.log(result)
  console.log('-------------------------')
})