import React, { useState, useRef } from "react";
import axios from "axios";

function UploadForm({ setResult, loading, setLoading, onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [preview, setPreview] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(selectedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://localhost:5001/api/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setResult(res.data);
      
      // Notify parent of completed analysis
      if (onAnalysisComplete) {
        onAnalysisComplete();
      }
    } catch (error) {
      alert("Error analyzing image. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      handleFileSelect(droppedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  return (
    <div className="upload-section">
      <div 
        className={`upload-area ${dragOver ? 'dragover' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-icon">+</div>
        <div className="upload-text">
          {file ? 'Click to change image' : 'Drop an image here or click to browse'}
        </div>
        <input 
          ref={fileInputRef}
          type="file" 
          accept="image/*" 
          className="file-input"
          onChange={e => e.target.files[0] && handleFileSelect(e.target.files[0])} 
        />
      </div>

      {file && (
        <div className="file-preview">
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <div className="file-details">
              <div className="file-name">{file.name}</div>
              <div className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
              <div className="file-type">{file.type}</div>
            </div>
            <button 
              type="button" 
              className="remove-btn"
              onClick={() => {
                setFile(null);
                setPreview(null);
              }}
            >
              ×
            </button>
          </div>
        </div>
      )}

      <button 
        type="submit" 
        className="analyze-btn"
        onClick={handleSubmit}
        disabled={!file || loading}
      >
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            Analyzing...
          </div>
        ) : (
          'Analyze Image'
        )}
      </button>
    </div>
  );
}

export default UploadForm;
