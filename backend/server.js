const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const { connectDB, saveAnalysis, getAnalysisHistory, getAnalysisImage, getAnalysisStats } = require('./mongodb');

const app = express();
app.use(cors());
app.use(express.json());

// Connect to MongoDB on startup
connectDB().catch(console.error);

const upload = multer({ dest: 'uploads/' });

app.post('/api/analyze', upload.single('file'), async (req, res) => {
  const filePath = path.join(__dirname, req.file.path);
  const startTime = Date.now();
  
  const python = spawn('python', [
    'model/model_inference.py',
    filePath
  ]);

  let output = '';
  python.stdout.on('data', data => output += data.toString());
  python.on('close', async () => {
    try {
      const [label, confidence] = output.trim().split(',');
      const processingTime = Date.now() - startTime;
      
      // Save to database with image
      const analysisData = {
        filename: req.file.filename,
        originalName: req.file.originalname,
        fileSize: req.file.size,
        mimeType: req.file.mimetype,
        imagePath: filePath,
        result: label,
        confidence: parseFloat(confidence),
        processingTime: processingTime,
        ipAddress: req.ip
      };
      
      const analysisId = await saveAnalysis(analysisData);
      
      // Also keep JSON log for backup
      const logEntry = {
        id: analysisId,
        timestamp: new Date().toISOString(),
        fileName: req.file.originalname,
        fileSize: req.file.size,
        result: label,
        confidence: parseFloat(confidence),
        processingTime: processingTime,
        ip: req.ip
      };
      
      const logLine = JSON.stringify(logEntry) + '\n';
      fs.appendFileSync('analysis_log.json', logLine);
      
      fs.unlinkSync(filePath); // cleanup temp file
      
      res.json({ 
        id: analysisId,
        result: label, 
        confidence: parseFloat(confidence),
        processingTime: processingTime
      });
    } catch (error) {
      console.error('Analysis error:', error);
      fs.unlinkSync(filePath); // cleanup on error
      res.status(500).json({ error: 'Analysis failed' });
    }
  });
});

// Get analysis history
app.get('/api/history', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const offset = parseInt(req.query.offset) || 0;
    const history = await getAnalysisHistory(limit, offset);
    res.json(history);
  } catch (error) {
    console.error('History fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch history' });
  }
});

// Get analysis statistics
app.get('/api/stats', async (req, res) => {
  try {
    const stats = await getAnalysisStats();
    res.json(stats);
  } catch (error) {
    console.error('Stats fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch stats' });
  }
});

// Get image by analysis ID
app.get('/api/image/:id', async (req, res) => {
  try {
    const analysis = await getAnalysisImage(req.params.id);
    if (!analysis) {
      return res.status(404).json({ error: 'Image not found' });
    }
    
    res.set({
      'Content-Type': analysis.mimeType,
      'Content-Length': analysis.imageData.length,
      'Cache-Control': 'public, max-age=31536000'
    });
    
    res.send(analysis.imageData);
  } catch (error) {
    console.error('Image fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch image' });
  }
});

const PORT = process.env.PORT || 5001;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
