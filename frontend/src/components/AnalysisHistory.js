import React, { useState, useEffect } from "react";
import axios from "axios";

function AnalysisHistory({ clearHistory }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [filter, setFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  // Fetch history from database
  useEffect(() => {
    fetchHistory();
    fetchStats();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5001/api/history');
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const filteredHistory = history.filter(item => {
    if (filter === 'all') return true;
    return item.result.toLowerCase() === filter;
  });

  const sortedHistory = [...filteredHistory].sort((a, b) => {
    if (sortBy === 'newest') return new Date(b.created_at) - new Date(a.created_at);
    if (sortBy === 'oldest') return new Date(a.created_at) - new Date(b.created_at);
    if (sortBy === 'confidence') return b.confidence - a.confidence;
    return 0;
  });

  const exportHistory = () => {
    const csvContent = [
      ['Date', 'Time', 'File Name', 'Result', 'Confidence', 'Processing Time'],
      ...history.map(item => [
        new Date(item.createdAt).toLocaleDateString(),
        new Date(item.createdAt).toLocaleTimeString(),
        item.originalName,
        item.result,
        (item.confidence * 100).toFixed(1) + '%',
        item.processingTime + 'ms'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `deepfake_analysis_history_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleClearHistory = () => {
    if (window.confirm('Are you sure you want to clear all history? This action cannot be undone.')) {
      // Clear localStorage
      clearHistory();
      // Refresh from database
      fetchHistory();
      fetchStats();
    }
  };

  if (loading) {
    return (
      <div className="history-empty">
        <div className="empty-icon">...</div>
        <h3>Loading History...</h3>
        <p>Fetching analysis data from database</p>
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="history-empty">
        <div className="empty-icon">∅</div>
        <h3>No Analysis History</h3>
        <p>Start analyzing images to build your history</p>
      </div>
    );
  }

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Analysis History</h2>
        <div className="history-controls">
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Results</option>
            <option value="real">Authentic Only</option>
            <option value="fake">Deepfakes Only</option>
          </select>
          
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
            <option value="confidence">Highest Confidence</option>
          </select>
          
          <button onClick={exportHistory} className="export-btn">
            Export CSV
          </button>
          
          <button onClick={handleClearHistory} className="clear-btn">
            Clear History
          </button>
        </div>
      </div>

      <div className="history-stats">
        <div className="stat-card">
          <div className="stat-value">{stats?.totalAnalyses || 0}</div>
          <div className="stat-label">Total Analyses</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {stats?.totalAnalyses > 0 ? ((stats.realCount / stats.totalAnalyses) * 100).toFixed(1) : 0}%
          </div>
          <div className="stat-label">Authentic Rate</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {stats?.avgConfidence ? (stats.avgConfidence * 100).toFixed(1) : 0}%
          </div>
          <div className="stat-label">Avg Confidence</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">
            {stats?.avgProcessingTime ? Math.round(stats.avgProcessingTime) : 0}ms
          </div>
          <div className="stat-label">Avg Processing</div>
        </div>
      </div>

      <div className="history-list">
        {sortedHistory.map((item) => (
          <div key={item.id} className={`history-item ${item.result.toLowerCase()}`}>
            <div className="history-main">
              <div className="history-image">
                <img 
                  src={`http://localhost:5001${item.imageUrl}`} 
                  alt={item.originalName}
                  className="analysis-image"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0yMCAyMEg0NFY0NEgyMFYyMFoiIHN0cm9rZT0iIzlDQTNBRiIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIi8+CjxjaXJjbGUgY3g9IjI4IiBjeT0iMjgiIHI9IjMiIGZpbGw9IiM5Q0EzQUYiLz4KPHBhdGggZD0iTTIwIDM2TDI4IDI4TDM2IDM2TDQ0IDI4IiBzdHJva2U9IiM5Q0EzQUYiIHN0cm9rZS13aWR0aD0iMiIgZmlsbD0ibm9uZSIvPgo8L3N2Zz4K';
                  }}
                />
              </div>
              <div className="history-info">
                <div className="file-name">{item.originalName}</div>
                <div className="timestamp">
                  {new Date(item.createdAt).toLocaleDateString()} at {new Date(item.createdAt).toLocaleTimeString()}
                </div>
                <div className="file-details">
                  {(item.fileSize / 1024 / 1024).toFixed(2)} MB • {item.processingTime}ms
                </div>
              </div>
              <div className="history-result">
                <div className={`result-badge ${item.result.toLowerCase()}`}>
                  {item.result === 'Real' ? 'Authentic' : 'Deepfake'}
                </div>
                <div className="confidence-value">
                  {(item.confidence * 100).toFixed(1)}% confidence
                </div>
              </div>
            </div>
            <div className="confidence-bar-container">
              <div 
                className={`confidence-bar ${item.result.toLowerCase()}`}
                style={{ width: `${item.confidence * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AnalysisHistory;