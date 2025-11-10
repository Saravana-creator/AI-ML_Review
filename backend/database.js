const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

// Database configuration
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: '', // Add your MySQL password
  database: 'deepfake_detector'
};

// Create database connection
async function createConnection() {
  try {
    const connection = await mysql.createConnection(dbConfig);
    console.log('✅ Connected to MySQL database');
    return connection;
  } catch (error) {
    console.error('❌ Database connection failed:', error.message);
    throw error;
  }
}

// Initialize database and tables
async function initializeDatabase() {
  try {
    // Connect without database first
    const tempConnection = await mysql.createConnection({
      host: dbConfig.host,
      user: dbConfig.user,
      password: dbConfig.password
    });

    // Create database if not exists
    await tempConnection.execute(`CREATE DATABASE IF NOT EXISTS ${dbConfig.database}`);
    await tempConnection.end();

    // Connect to the database
    const connection = await createConnection();

    // Create analyses table
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS analyses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        original_name VARCHAR(255) NOT NULL,
        file_size INT NOT NULL,
        mime_type VARCHAR(100) NOT NULL,
        image_data LONGBLOB NOT NULL,
        result ENUM('Real', 'Fake') NOT NULL,
        confidence DECIMAL(5,4) NOT NULL,
        processing_time INT NOT NULL,
        ip_address VARCHAR(45),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_created_at (created_at),
        INDEX idx_result (result)
      )
    `);

    console.log('✅ Database tables initialized');
    await connection.end();
  } catch (error) {
    console.error('❌ Database initialization failed:', error.message);
    throw error;
  }
}

// Save analysis with image to database
async function saveAnalysis(analysisData) {
  const connection = await createConnection();
  
  try {
    const {
      filename,
      originalName,
      fileSize,
      mimeType,
      imagePath,
      result,
      confidence,
      processingTime,
      ipAddress
    } = analysisData;

    // Read image file as binary data
    const imageData = fs.readFileSync(imagePath);

    const [result_db] = await connection.execute(`
      INSERT INTO analyses (
        filename, original_name, file_size, mime_type, image_data,
        result, confidence, processing_time, ip_address
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `, [
      filename,
      originalName,
      fileSize,
      mimeType,
      imageData,
      result,
      confidence,
      processingTime,
      ipAddress
    ]);

    console.log(`✅ Analysis saved to database with ID: ${result_db.insertId}`);
    return result_db.insertId;
  } catch (error) {
    console.error('❌ Failed to save analysis:', error.message);
    throw error;
  } finally {
    await connection.end();
  }
}

// Get analysis history from database
async function getAnalysisHistory(limit = 50, offset = 0) {
  const connection = await createConnection();
  
  try {
    const [rows] = await connection.execute(`
      SELECT 
        id,
        filename,
        original_name,
        file_size,
        mime_type,
        result,
        confidence,
        processing_time,
        created_at,
        CONCAT('data:', mime_type, ';base64,', TO_BASE64(image_data)) as image_url
      FROM analyses 
      ORDER BY created_at DESC 
      LIMIT ? OFFSET ?
    `, [limit, offset]);

    return rows;
  } catch (error) {
    console.error('❌ Failed to get analysis history:', error.message);
    throw error;
  } finally {
    await connection.end();
  }
}

// Get analysis statistics
async function getAnalysisStats() {
  const connection = await createConnection();
  
  try {
    const [stats] = await connection.execute(`
      SELECT 
        COUNT(*) as total_analyses,
        SUM(CASE WHEN result = 'Real' THEN 1 ELSE 0 END) as real_count,
        SUM(CASE WHEN result = 'Fake' THEN 1 ELSE 0 END) as fake_count,
        AVG(confidence) as avg_confidence,
        AVG(processing_time) as avg_processing_time
      FROM analyses
    `);

    return stats[0];
  } catch (error) {
    console.error('❌ Failed to get analysis stats:', error.message);
    throw error;
  } finally {
    await connection.end();
  }
}

// Delete old analyses (keep last 1000)
async function cleanupOldAnalyses() {
  const connection = await createConnection();
  
  try {
    await connection.execute(`
      DELETE FROM analyses 
      WHERE id NOT IN (
        SELECT id FROM (
          SELECT id FROM analyses ORDER BY created_at DESC LIMIT 1000
        ) as keep_analyses
      )
    `);
    
    console.log('✅ Old analyses cleaned up');
  } catch (error) {
    console.error('❌ Failed to cleanup old analyses:', error.message);
  } finally {
    await connection.end();
  }
}

module.exports = {
  initializeDatabase,
  saveAnalysis,
  getAnalysisHistory,
  getAnalysisStats,
  cleanupOldAnalyses
};