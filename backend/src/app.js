require('dotenv').config()

const express = require('express')
const cors = require('cors')

const mlRoutes = require('./routes/mlRoutes')
const analysisRoutes = require('./routes/analysisRoutes')

const app = express()

const PORT = Number(process.env.PORT) || 5002

const frontendUrl = process.env.FRONTEND_URL || 'http://localhost:5173'

app.use(
  cors({
    origin: [
      frontendUrl,
      'http://localhost:5173',
      'http://127.0.0.1:5173',
      'http://localhost:5174',
      'http://127.0.0.1:5174',
    ],
  })
)

app.use(express.json())

// ------------------------------------------------------------
// Health check
// ------------------------------------------------------------

app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    service: 'KisanAI Backend',
    status: 'healthy',
  })
})

// ------------------------------------------------------------
// API routes
// ------------------------------------------------------------

app.use('/api/ml', mlRoutes)
app.use('/api/analysis', analysisRoutes)

// ------------------------------------------------------------
// 404 handler
// ------------------------------------------------------------

app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found.',
  })
})

// ------------------------------------------------------------
// Error handler
// ------------------------------------------------------------

app.use((error, req, res, next) => {
  console.error('Unhandled backend error:', error)

  res.status(500).json({
    success: false,
    error: 'Internal server error.',
  })
})

// ------------------------------------------------------------
// Export application for testing
// ------------------------------------------------------------

module.exports = app

// ------------------------------------------------------------
// Start server only when this file is executed directly
// ------------------------------------------------------------

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`KisanAI backend running on port ${PORT}`)
    console.log(
      `ML service configured at ${
        process.env.ML_SERVICE_URL || 'http://127.0.0.1:5001'
      }`
    )
  })
}