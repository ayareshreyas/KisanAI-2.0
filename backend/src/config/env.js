const requiredEnv = (name, fallback = undefined) => {
  const value = process.env[name] ?? fallback

  if (value === undefined || value === '') {
    throw new Error(`Missing required environment variable: ${name}`)
  }

  return value
}

const config = {
  port: Number(requiredEnv('PORT', '5002')),
  mlServiceUrl: requiredEnv(
    'ML_SERVICE_URL',
    'http://127.0.0.1:5001'
  ),
  frontendUrl: requiredEnv(
    'FRONTEND_URL',
    'http://localhost:5173'
  ),
}

module.exports = config