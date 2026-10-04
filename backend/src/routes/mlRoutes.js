const express = require('express')

const {
  checkMLServiceHealth,
  predictCrop,
  analyzeSoil,
  recommendFertilizer,
  generateAgriculturalDecision,
} = require('../services/mlService')

const {
  saveAnalysis,
} = require('../services/analysisService')

const router = express.Router()

router.get('/health', async (req, res) => {
  try {
    const result = await checkMLServiceHealth()

    res.json({
      success: true,
      backend: 'healthy',
      mlService: result,
    })
  } catch (error) {
    res.status(error.status || 500).json({
      success: false,
      error: error.message,
    })
  }
})

router.post('/crop/predict', async (req, res) => {
  try {
    const result = await predictCrop(req.body)

    res.status(200).json(result)
  } catch (error) {
    res.status(error.status || 500).json({
      success: false,
      error: error.message,
    })
  }
})

router.post('/soil/analyze', async (req, res) => {
  try {
    const result = await analyzeSoil(req.body)

    res.status(200).json(result)
  } catch (error) {
    res.status(error.status || 500).json({
      success: false,
      error: error.message,
    })
  }
})

router.post('/fertilizer/recommend', async (req, res) => {
  try {
    const result = await recommendFertilizer(req.body)

    res.status(200).json(result)
  } catch (error) {
    res.status(error.status || 500).json({
      success: false,
      error: error.message,
    })
  }
})

router.post('/agricultural-decision', async (req, res) => {
  try {
    const result = await generateAgriculturalDecision(
      req.body
    )

    const decision = result.decision

    const savedAnalysis = saveAnalysis({
      input: req.body,
      decision,
    })

    res.status(200).json({
      success: true,
      decision,
      analysis: {
        id: savedAnalysis.id,
        created_at: savedAnalysis.created_at,
      },
    })
  } catch (error) {
    console.error(
      'Agricultural decision error:',
      error
    )

    res.status(error.status || 500).json({
      success: false,
      error: error.message,
    })
  }
})

module.exports = router