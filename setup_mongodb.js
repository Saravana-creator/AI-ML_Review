const { connectDB } = require('./backend/mongodb');

async function setup() {
  console.log('🚀 Setting up MongoDB for DeepFake Detector...');
  
  try {
    await connectDB();
    console.log('✅ MongoDB setup completed successfully!');
    console.log('\n📋 Next steps:');
    console.log('1. Install MongoDB dependencies: cd backend && npm install');
    console.log('2. Make sure MongoDB is running on localhost:27017');
    console.log('3. Start the backend server: node server.js');
    console.log('4. Start the frontend: cd ../frontend && npm start');
    
    console.log('\n📊 Database Info:');
    console.log('- Database: deepfake_detector');
    console.log('- Collection: analyses');
    console.log('- Images stored as Buffer data');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ MongoDB setup failed:', error.message);
    console.log('\n🔧 Troubleshooting:');
    console.log('1. Install MongoDB: https://www.mongodb.com/try/download/community');
    console.log('2. Start MongoDB service: mongod');
    console.log('3. Check if MongoDB is running on port 27017');
    console.log('4. Install dependencies: npm install mongoose');
    
    process.exit(1);
  }
}

setup();