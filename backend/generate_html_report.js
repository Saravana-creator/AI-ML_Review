const fs = require('fs');

function generateHTMLReport() {
  // Read analysis log
  const logData = fs.readFileSync('analysis_log.json', 'utf8')
    .split('\n')
    .filter(line => line.trim())
    .map(line => JSON.parse(line));

  const totalAnalyses = logData.length;
  const fakeCount = logData.filter(item => item.result === 'Fake').length;
  const realCount = logData.filter(item => item.result === 'Real').length;
  const avgConfidence = logData.reduce((sum, item) => sum + item.confidence, 0) / totalAnalyses;

  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepFake Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .header { text-align: center; margin-bottom: 30px; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: #667eea; color: white; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; }
        .stat-label { font-size: 0.9rem; opacity: 0.9; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
        .fake { color: #dc3545; font-weight: bold; }
        .real { color: #28a745; font-weight: bold; }
        .timestamp { font-size: 0.9rem; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 DeepFake Analysis Report</h1>
            <p>Generated on ${new Date().toLocaleString()}</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">${totalAnalyses}</div>
                <div class="stat-label">Total Analyses</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${realCount}</div>
                <div class="stat-label">Authentic Images</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${fakeCount}</div>
                <div class="stat-label">Deepfakes Detected</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${(avgConfidence * 100).toFixed(1)}%</div>
                <div class="stat-label">Avg Confidence</div>
            </div>
        </div>

        <h2>Analysis History</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>File Name</th>
                    <th>Result</th>
                    <th>Confidence</th>
                    <th>Processing Time</th>
                    <th>File Size</th>
                </tr>
            </thead>
            <tbody>
                ${logData.map(item => `
                    <tr>
                        <td class="timestamp">${new Date(item.timestamp).toLocaleString()}</td>
                        <td>${item.fileName}</td>
                        <td class="${item.result.toLowerCase()}">${item.result}</td>
                        <td>${(item.confidence * 100).toFixed(1)}%</td>
                        <td>${item.processingTime}ms</td>
                        <td>${(item.fileSize / 1024 / 1024).toFixed(2)} MB</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    </div>
</body>
</html>`;

  fs.writeFileSync('analysis_report.html', htmlContent);
  console.log('✅ HTML report generated: analysis_report.html');
}

module.exports = { generateHTMLReport };

// Run if called directly
if (require.main === module) {
  generateHTMLReport();
}