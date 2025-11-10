import React, { useState, useEffect } from "react";
import UploadForm from "./components/UploadForm";
import ResultDisplay from "./components/ResultDisplay";
import AnalysisHistory from "./components/AnalysisHistory";
import axios from "axios";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ totalAnalyses: 0, realCount: 0, fakeCount: 0 });
  const [activeTab, setActiveTab] = useState('analyze');

  // Load stats on component mount
  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  // Refresh stats after new analysis
  const handleAnalysisComplete = () => {
    fetchStats();
  };

  const clearHistory = () => {
    localStorage.removeItem('deepfakeHistory');
    fetchStats();
  };

  return (
    <div className="app">
      <div className="header">
        <div className="brand">
          <h1 className="title">AI Image Analyzer</h1>
          <p className="subtitle">Advanced AI-powered image authenticity verification</p>
        </div>
        <div className="stats">
          <div className="stat-item">
            <span className="stat-number">{stats.totalAnalyses || 0}</span>
            <span className="stat-label">Analyses</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{stats.realCount || 0}</span>
            <span className="stat-label">Authentic</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{stats.fakeCount || 0}</span>
            <span className="stat-label">Deepfakes</span>
          </div>
        </div>
      </div>
      
      <div className="nav-tabs">
        <button 
          className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyze')}
        >
          Analyze Image
        </button>
        <button 
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Analysis History ({stats.totalAnalyses || 0})
        </button>
      </div>

      <div className="main-container">
        {activeTab === 'analyze' ? (
          <>
            <UploadForm 
              setResult={setResult} 
              loading={loading} 
              setLoading={setLoading}
              onAnalysisComplete={handleAnalysisComplete}
            />
            <ResultDisplay result={result} />
          </>
        ) : (
          <AnalysisHistory 
            clearHistory={clearHistory}
          />
        )}
      </div>
    </div>
  );
}

export default App;
