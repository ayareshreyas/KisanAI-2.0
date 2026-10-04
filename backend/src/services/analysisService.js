const db = require('../database/database')

function saveAnalysis({
  input,
  decision,
}) {
  const cropRecommendation =
    decision.crop_recommendation

  const cropExplanation =
    decision.crop_explanation

  const soilHealth =
    decision.soil_health

  const fertilizerPlanning =
    decision.fertilizer_planning

  const inputReliability =
    decision.input_reliability

  const statement = db.prepare(`
    INSERT INTO analyses (
      N,
      P,
      K,
      temperature,
      humidity,
      ph,
      rainfall,
      predicted_crop,
      model_confidence,
      crop_explanation_json,
      soil_health_json,
      fertilizer_planning_json,
      input_reliability_json
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `)

  const result = statement.run(
    input.N,
    input.P,
    input.K,
    input.temperature,
    input.humidity,
    input.ph,
    input.rainfall,
    cropRecommendation.crop,
    cropRecommendation.confidence,
    JSON.stringify(cropExplanation),
    JSON.stringify(soilHealth),
    JSON.stringify(fertilizerPlanning),
    JSON.stringify(inputReliability)
  )

  return {
    id: Number(result.lastInsertRowid),
    created_at: getAnalysisTimestamp(
      Number(result.lastInsertRowid)
    ),
  }
}

function getAnalysisTimestamp(id) {
  const statement = db.prepare(`
    SELECT created_at
    FROM analyses
    WHERE id = ?
  `)

  const row = statement.get(id)

  return row?.created_at || null
}

function getRecentAnalyses(limit = 20) {
  const safeLimit = Math.min(
    Math.max(Number(limit) || 20, 1),
    100
  )

  const statement = db.prepare(`
    SELECT
      id,
      created_at,
      N,
      P,
      K,
      temperature,
      humidity,
      ph,
      rainfall,
      predicted_crop,
      model_confidence,
      crop_explanation_json,
      soil_health_json,
      fertilizer_planning_json,
      input_reliability_json
    FROM analyses
    ORDER BY created_at DESC, id DESC
    LIMIT ?
  `)

  const rows = statement.all(safeLimit)

  return rows.map(formatAnalysis)
}

function getAnalysisById(id) {
  const statement = db.prepare(`
    SELECT
      id,
      created_at,
      N,
      P,
      K,
      temperature,
      humidity,
      ph,
      rainfall,
      predicted_crop,
      model_confidence,
      crop_explanation_json,
      soil_health_json,
      fertilizer_planning_json,
      input_reliability_json
    FROM analyses
    WHERE id = ?
  `)

  const row = statement.get(Number(id))

  if (!row) {
    return null
  }

  return formatAnalysis(row)
}

function formatAnalysis(row) {
  return {
    id: row.id,
    created_at: row.created_at,

    input: {
      N: row.N,
      P: row.P,
      K: row.K,
      temperature: row.temperature,
      humidity: row.humidity,
      ph: row.ph,
      rainfall: row.rainfall,
    },

    crop_recommendation: {
      crop: row.predicted_crop,
      confidence: row.model_confidence,
    },

    crop_explanation: parseJson(
      row.crop_explanation_json
    ),

    soil_health: parseJson(
      row.soil_health_json
    ),

    fertilizer_planning: parseJson(
      row.fertilizer_planning_json
    ),

    input_reliability: parseJson(
      row.input_reliability_json
    ),
  }
}

function parseJson(value) {
  try {
    return JSON.parse(value)
  } catch {
    return null
  }
}

module.exports = {
  saveAnalysis,
  getRecentAnalyses,
  getAnalysisById,
}