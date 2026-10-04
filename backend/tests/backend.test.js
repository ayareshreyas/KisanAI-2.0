const test = require('node:test')
const assert = require('node:assert/strict')

const app = require('../src/app')

function request(method, path, body = undefined) {
  return new Promise((resolve, reject) => {
    const server = app.listen(0, '127.0.0.1', () => {
      const address = server.address()
      const port = address.port

      const http = require('node:http')

      const requestOptions = {
        hostname: '127.0.0.1',
        port,
        path,
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      }

      const req = http.request(requestOptions, (res) => {
        let responseBody = ''

        res.on('data', (chunk) => {
          responseBody += chunk
        })

        res.on('end', () => {
          server.close(() => {
            let parsedBody = null

            try {
              parsedBody = JSON.parse(responseBody)
            } catch {
              parsedBody = responseBody
            }

            resolve({
              statusCode: res.statusCode,
              body: parsedBody,
            })
          })
        })
      })

      req.on('error', (error) => {
        server.close(() => {
          reject(error)
        })
      })

      if (body !== undefined) {
        req.write(JSON.stringify(body))
      }

      req.end()
    })

    server.on('error', reject)
  })
}

const validFarmInput = {
  N: 90,
  P: 42,
  K: 43,
  temperature: 25,
  humidity: 80,
  ph: 6.5,
  rainfall: 200,
}

test('GET /api/health returns healthy backend status', async () => {
  const response = await request('GET', '/api/health')

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.equal(response.body.service, 'KisanAI Backend')
  assert.equal(response.body.status, 'healthy')
})

test('Unknown route returns 404 JSON response', async () => {
  const response = await request('GET', '/api/does-not-exist')

  assert.equal(response.statusCode, 404)
  assert.equal(response.body.success, false)
  assert.equal(response.body.error, 'Route not found.')
})

test('GET /api/ml/health returns ML service health', async () => {
  const response = await request('GET', '/api/ml/health')

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.equal(response.body.backend, 'healthy')

  assert.ok(response.body.mlService)
  assert.equal(response.body.mlService.success, true)
})

test('GET /api/analysis/history returns analysis history', async () => {
  const response = await request('GET', '/api/analysis/history')

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.ok(Array.isArray(response.body.analyses))
})

test('GET /api/analysis/history respects the requested limit', async () => {
  const response = await request(
    'GET',
    '/api/analysis/history?limit=2'
  )

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.ok(Array.isArray(response.body.analyses))
  assert.ok(response.body.analyses.length <= 2)
})

test('GET /api/analysis/history/:id returns an existing analysis', async () => {
  const historyResponse = await request(
    'GET',
    '/api/analysis/history?limit=1'
  )

  assert.equal(historyResponse.statusCode, 200)
  assert.equal(historyResponse.body.success, true)

  if (historyResponse.body.analyses.length === 0) {
    return
  }

  const analysisId = historyResponse.body.analyses[0].id

  const response = await request(
    'GET',
    `/api/analysis/history/${analysisId}`
  )

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.ok(response.body.analysis)
  assert.equal(response.body.analysis.id, analysisId)
})

test('GET /api/analysis/history/:id returns 404 for missing analysis', async () => {
  const response = await request(
    'GET',
    '/api/analysis/history/999999999'
  )

  assert.equal(response.statusCode, 404)
  assert.equal(response.body.success, false)
  assert.equal(response.body.error, 'Analysis not found.')
})

test('Stored analysis contains the expected structure', async () => {
  const response = await request(
    'GET',
    '/api/analysis/history?limit=1'
  )

  assert.equal(response.statusCode, 200)

  if (response.body.analyses.length === 0) {
    return
  }

  const analysis = response.body.analyses[0]

  assert.ok(analysis.id)
  assert.ok(analysis.created_at)

  assert.ok(analysis.input)
  assert.equal(typeof analysis.input.N, 'number')
  assert.equal(typeof analysis.input.P, 'number')
  assert.equal(typeof analysis.input.K, 'number')
  assert.equal(typeof analysis.input.temperature, 'number')
  assert.equal(typeof analysis.input.humidity, 'number')
  assert.equal(typeof analysis.input.ph, 'number')
  assert.equal(typeof analysis.input.rainfall, 'number')

  assert.ok(analysis.crop_recommendation)
  assert.ok(analysis.crop_recommendation.crop)
  assert.equal(
    typeof analysis.crop_recommendation.confidence,
    'number'
  )

  assert.ok('soil_health' in analysis)
  assert.ok('fertilizer_planning' in analysis)
  assert.ok('input_reliability' in analysis)
})

test('POST /api/ml/crop/predict returns a crop prediction', async () => {
  const response = await request(
    'POST',
    '/api/ml/crop/predict',
    validFarmInput
  )

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)

  assert.ok(response.body.prediction)
  assert.ok(response.body.prediction.crop)
  assert.equal(
    typeof response.body.prediction.confidence,
    'number'
  )

  assert.ok(response.body.input_reliability)
})

test('POST /api/ml/agricultural-decision returns the unified decision', async () => {
  const response = await request(
    'POST',
    '/api/ml/agricultural-decision',
    validFarmInput
  )

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.ok(response.body.decision)

  const decision = response.body.decision

  assert.ok(decision.crop_recommendation)
  assert.ok(decision.crop_explanation)
  assert.ok(decision.soil_health)
  assert.ok(decision.fertilizer_planning)
  assert.ok(decision.input_reliability)
})

test('POST /api/ml/agricultural-decision rejects incomplete input', async () => {
  const response = await request(
    'POST',
    '/api/ml/agricultural-decision',
    {
      N: 90,
      P: 42,
      K: 43,
    }
  )

  assert.equal(response.statusCode, 400)
  assert.equal(response.body.success, false)
  assert.ok(response.body.error)
})

test('POST /api/ml/soil/analyze returns soil health analysis', async () => {
  const response = await request(
    'POST',
    '/api/ml/soil/analyze',
    {
      N: 90,
      P: 42,
      K: 43,
      ph: 6.5,
    }
  )

  assert.equal(response.statusCode, 200)
  assert.equal(response.body.success, true)
  assert.ok(response.body.soil_health)
})

test('POST /api/ml/crop/predict rejects incomplete request body', async () => {
  const response = await request(
    'POST',
    '/api/ml/crop/predict',
    {
      N: 90,
    }
  )

  assert.equal(response.statusCode, 400)
  assert.equal(response.body.success, false)
  assert.ok(response.body.error)
})