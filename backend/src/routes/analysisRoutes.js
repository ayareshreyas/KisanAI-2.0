const express = require('express')

const {
  getRecentAnalyses,
  getAnalysisById,
} = require('../services/analysisService')

const router = express.Router()

router.get('/history', (req, res) => {
  try {
    const analyses = getRecentAnalyses(
      req.query.limit
    )

    res.json({
      success: true,
      analyses,
    })
  } catch (error) {
    console.error(
      'Analysis history error:',
      error
    )

    res.status(500).json({
      success: false,
      error: 'Unable to load analysis history.',
    })
  }
})

router.get('/history/:id', (req, res) => {
  try {
    const analysis = getAnalysisById(
      req.params.id
    )

    if (!analysis) {
      return res.status(404).json({
        success: false,
        error: 'Analysis not found.',
      })
    }

    res.json({
      success: true,
      analysis,
    })
  } catch (error) {
    console.error(
      'Analysis detail error:',
      error
    )

    res.status(500).json({
      success: false,
      error: 'Unable to load the analysis.',
    })
  }
})

module.exports = router