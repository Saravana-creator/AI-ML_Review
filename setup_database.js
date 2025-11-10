const { initializeDatabase } = require('./backend/database');

async function setup() {
  console.log('🚀 Setting up MySQL database for DeepFake Detector...');
  
  try {
    await initializeDatabase();
    console.log('✅ Database setup completed successfully!');
    console.log('\n📋 Next steps:');
    console.log('1. Install MySQL dependencies: cd backend && npm install');
    console.log('2. Update database credentials in backend/database.js');
    console.log('3. Start the backend server: node server.js');
    console.log('4. Start the frontend: cd ../frontend && npm start');
  } catch (error) {
    console.error('❌ Database setup failed:', error.message);
    console.log('\n🔧 Troubleshooting:');
    console.log('1. Make sure MySQL is installed and running');
    console.log('2. Check database credentials in backend/database.js');
    console.log('3. Ensure MySQL user has CREATE DATABASE privileges');
  }
}

setup();