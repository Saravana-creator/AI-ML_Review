import React from "react";

function ResultDisplay({ result }) {
  if (!result) return null;

  const isReal = result.result === "Real";
  const confidence = result.confidence ? (result.confidence * 100).toFixed(1) : 0;
  
  return (
    <div className={`result-section ${isReal ? 'result-real' : 'result-fake'}`}>
      <div className="result-title">
        {isReal ? 'Authentic' : 'Deepfake Detected'}
      </div>
      <div className="result-confidence">
        Confidence: {confidence}%
      </div>
      <div className="confidence-bar">
        <div 
          className="confidence-fill" 
          style={{ width: `${confidence}%` }}
        ></div>
      </div>
    </div>
  );
}

export default ResultDisplay;
