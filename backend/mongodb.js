const mongoose = require('mongoose');
const fs = require('fs');

// MongoDB connection
const connectDB = async () => {
  try {
    await mongoose.connect('mongodb://localhost:27017/deepfake_detector');
    console.log('✅ Connected to MongoDB');
  } catch (error) {
    console.error('❌ MongoDB connection failed:', error.message);
    throw error;
  }
};

// Analysis Schema
const analysisSchema = new mongoose.Schema({
  filename: { type: String, required: true },
  originalName: { type: String, required: true },
  fileSize: { type: Number, required: true },
  mimeType: { type: String, required: true },
  imageData: { type: Buffer, required: true },
  result: { type: String, enum: ['Real', 'Fake'], required: true },
  confidence: { type: Number, required: true, min: 0, max: 1 },
  processingTime: { type: Number, required: true },
  ipAddress: { type: String },
  createdAt: { type: Date, default: Date.now }
}, {
  timestamps: true
});

// Create indexes for better performance
analysisSchema.index({ createdAt: -1 });
analysisSchema.index({ result: 1 });

const Analysis = mongoose.model('Analysis', analysisSchema);

// Save analysis with image to MongoDB
async function saveAnalysis(analysisData) {
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

    const analysis = new Analysis({
      filename,
      originalName,
      fileSize,
      mimeType,
      imageData,
      result,
      confidence,
      processingTime,
      ipAddress
    });

    const savedAnalysis = await analysis.save();
    console.log(`✅ Analysis saved to MongoDB with ID: ${savedAnalysis._id}`);
    return savedAnalysis._id;
  } catch (error) {
    console.error('❌ Failed to save analysis:', error.message);
    throw error;
  }
}

// Get analysis history from MongoDB
async function getAnalysisHistory(limit = 50, offset = 0) {
  try {
    const analyses = await Analysis
      .find()
      .sort({ createdAt: -1 })
      .limit(limit)
      .skip(offset)
      .select('-imageData') // Exclude image data for list view
      .lean();

    // Add image URL for each analysis
    const analysesWithImages = analyses.map(analysis => ({
      ...analysis,
      imageUrl: `/api/image/${analysis._id}`
    }));

    return analysesWithImages;
  } catch (error) {
    console.error('❌ Failed to get analysis history:', error.message);
    throw error;
  }
}

// Get single image by ID
async function getAnalysisImage(id) {
  try {
    const analysis = await Analysis.findById(id).select('imageData mimeType originalName');
    return analysis;
  } catch (error) {
    console.error('❌ Failed to get analysis image:', error.message);
    throw error;
  }
}

// Get analysis statistics
async function getAnalysisStats() {
  try {
    const stats = await Analysis.aggregate([
      {
        $group: {
          _id: null,
          totalAnalyses: { $sum: 1 },
          realCount: {
            $sum: { $cond: [{ $eq: ['$result', 'Real'] }, 1, 0] }
          },
          fakeCount: {
            $sum: { $cond: [{ $eq: ['$result', 'Fake'] }, 1, 0] }
          },
          avgConfidence: { $avg: '$confidence' },
          avgProcessingTime: { $avg: '$processingTime' }
        }
      }
    ]);

    return stats[0] || {
      totalAnalyses: 0,
      realCount: 0,
      fakeCount: 0,
      avgConfidence: 0,
      avgProcessingTime: 0
    };
  } catch (error) {
    console.error('❌ Failed to get analysis stats:', error.message);
    throw error;
  }
}

// Delete old analyses (keep last 1000)
async function cleanupOldAnalyses() {
  try {
    const totalCount = await Analysis.countDocuments();
    if (totalCount > 1000) {
      const analyses = await Analysis
        .find()
        .sort({ createdAt: -1 })
        .skip(1000)
        .select('_id');
      
      const idsToDelete = analyses.map(a => a._id);
      await Analysis.deleteMany({ _id: { $in: idsToDelete } });
      
      console.log(`✅ Cleaned up ${idsToDelete.length} old analyses`);
    }
  } catch (error) {
    console.error('❌ Failed to cleanup old analyses:', error.message);
  }
}

module.exports = {
  connectDB,
  saveAnalysis,
  getAnalysisHistory,
  getAnalysisImage,
  getAnalysisStats,
  cleanupOldAnalyses,
  Analysis
};