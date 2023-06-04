const mysql = require('mysql2/promise')

const { db } = require('./keys')
const pool = mysql.createPool(db)


module.exports = pool


