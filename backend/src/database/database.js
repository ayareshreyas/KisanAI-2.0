const fs = require('fs')
const path = require('path')
const { DatabaseSync } = require('node:sqlite')

const projectRoot = path.resolve(__dirname, '../../../')
const databaseDirectory = path.join(projectRoot, 'database')
const databasePath = path.join(
  databaseDirectory,
  'kisanai.sqlite'
)
const schemaPath = path.join(
  databaseDirectory,
  'schema.sql'
)

if (!fs.existsSync(databaseDirectory)) {
  fs.mkdirSync(databaseDirectory, {
    recursive: true,
  })
}

const db = new DatabaseSync(databasePath)

db.exec(`
  PRAGMA foreign_keys = ON;
  PRAGMA journal_mode = WAL;
`)

const schema = fs.readFileSync(
  schemaPath,
  'utf8'
)

db.exec(schema)

console.log(
  `KisanAI database connected: ${databasePath}`
)

module.exports = db