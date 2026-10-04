const config = require('../config/env')

async function requestMLService(path, options = {}) {
  const response = await fetch(`${config.mlServiceUrl}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })

  const data = await response.json()

  if (!response.ok) {
    const error = new Error(
      data.error || `ML service returned HTTP ${response.status}`
    )

    error.status = response.status

    throw error
  }

  return data
}

async function checkMLServiceHealth() {
  return requestMLService('/health', {
    method: 'GET',
    headers: {},
  })
}

async function predictCrop(input) {
  return requestMLService('/predict', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

async function analyzeSoil(input) {
  return requestMLService('/soil/analyze', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

async function recommendFertilizer(input) {
  return requestMLService('/fertilizer/recommend', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

async function generateAgriculturalDecision(input) {
  return requestMLService('/agricultural-decision', {
    method: 'POST',
    body: JSON.stringify(input),
  })
}

module.exports = {
  checkMLServiceHealth,
  predictCrop,
  analyzeSoil,
  recommendFertilizer,
  generateAgriculturalDecision,
}