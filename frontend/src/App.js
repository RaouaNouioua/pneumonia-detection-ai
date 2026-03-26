import React, { useState } from 'react';
import { Upload, ZoomIn, ZoomOut, RotateCcw, Moon, Grid3x3, Maximize2, Activity, Shield, AlertCircle, CheckCircle } from 'lucide-react';

export default function PneumoniaAIScan() {
  const [overlayOpacity, setOverlayOpacity] = useState(50);
  const [heatmapEnabled, setHeatmapEnabled] = useState(true);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // API integration functions
  const analyzeImage = async (file) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    
    console.log("Sending image to backend for analysis...");
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error: ${response.status} - ${errorText}`);
      }
      
      const result = await response.json();
      console.log("Analysis result:", result);
      
      setAnalysisResult(result);
      
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert(`Failed to analyze image: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setUploadedImage(imageUrl);
      analyzeImage(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const imageUrl = URL.createObjectURL(file);
      setUploadedImage(imageUrl);
      analyzeImage(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  // Get severity color based on analysis
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'moderate': return 'bg-orange-100 text-orange-800';
      case 'low': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-green-100 text-green-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-4">
          <Activity className="text-blue-600" size={28} />
          <h1 className="text-xl font-bold text-slate-800 tracking-tight">Pneumonia AI Scan</h1>
        </div>
        
        <div className="flex items-center gap-4">
          <span className="px-4 py-2 bg-red-50 text-red-700 text-sm font-semibold rounded-lg border border-red-200">
            AI ASSISTED DIAGNOSIS - RADIOLOGIST REVIEW REQUIRED
          </span>
          <div className="w-10 h-10 bg-gradient-to-br from-teal-400 to-teal-500 rounded-full flex items-center justify-center shadow-md">
            <span className="text-white text-sm font-bold">JD</span>
          </div>
        </div>
      </header>

      <div className="flex gap-6 p-6 max-w-[1800px] mx-auto">
        {/* Left Sidebar */}
        <div className="w-80 space-y-6 flex-shrink-0">
          {/* Patient Information */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <h2 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">Patient Information</h2>
            
            <div className="flex items-center gap-4 mb-6">
              <div className="w-14 h-14 bg-gradient-to-br from-amber-300 to-amber-400 rounded-full flex items-center justify-center shadow-md">
                <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-slate-900 text-lg">John Doe</h3>
                <p className="text-sm text-slate-500">ID: 12345789</p>
              </div>
            </div>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-2 border-b border-slate-100">
                <span className="font-semibold text-slate-600">DOB:</span>
                <span className="text-slate-900">1985-05-22</span>
              </div>
              <div className="flex justify-between py-2 border-b border-slate-100">
                <span className="font-semibold text-slate-600">Gender:</span>
                <span className="text-slate-900">Male</span>
              </div>
              <div className="flex justify-between py-2">
                <span className="font-semibold text-slate-600">Scan Date:</span>
                <span className="text-slate-900">2023-10-27</span>
              </div>
            </div>
          </div>

          {/* Image Upload & Controls */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <h2 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">Image Upload & Controls</h2>
            
            <div 
              className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-blue-400 hover:bg-blue-50/50 transition-all cursor-pointer mb-4"
              onClick={() => !uploadedImage && document.getElementById('file-upload').click()}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
            >
              <input
                id="file-upload"
                type="file"
                accept="image/*,.dcm"
                onChange={handleFileUpload}
                className="hidden"
              />
              
              {!uploadedImage ? (
                <>
                  <Upload className="w-10 h-10 text-slate-400 mx-auto mb-3" />
                  <p className="text-sm text-slate-600">
                    Drag & drop or <span className="text-blue-600 font-semibold">browse files</span>
                  </p>
                  <p className="text-xs text-slate-500 mt-2">Supports: PNG, JPG, JPEG, DICOM</p>
                </>
              ) : (
                <div className="relative">
                  <img 
                    src={uploadedImage} 
                    alt="Uploaded X-Ray" 
                    className="w-full h-auto rounded-lg shadow-md"
                  />
                  <div className="absolute inset-0 bg-black/20 rounded-lg flex items-center justify-center">
                    {isLoading && (
                      <div className="bg-white/90 p-4 rounded-lg shadow-lg">
                        <div className="flex items-center gap-3">
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                          <span className="text-sm font-medium text-slate-800">Analyzing...</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-2">
              {uploadedImage && (
                <div className="flex items-center gap-3 p-3 rounded-xl bg-blue-50 border-2 border-blue-500 shadow-md">
                  <div className="w-12 h-12 bg-slate-800 rounded-lg overflow-hidden shadow-sm">
                    <img 
                      src={uploadedImage} 
                      alt="Thumbnail" 
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1">
                    <p className="font-semibold text-slate-900 text-sm">Uploaded Image</p>
                    <p className="text-xs text-green-600 font-medium">Active</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Main Content - Image Viewer */}
        <div className="flex-1 bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
          <div className="relative w-full h-[850px] bg-black">
            {/* X-Ray Image */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="relative w-full h-full max-w-[600px] max-h-[800px]">
                {/* Display uploaded image or default simulation */}
                {uploadedImage ? (
                  <img 
                    src={uploadedImage} 
                    alt="X-Ray Analysis" 
                    className="w-full h-full object-contain"
                  />
                ) : (
                  <>
                    {/* Simulated X-ray with gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-b from-slate-700 via-slate-600 to-slate-700 opacity-30" />
                    
                    {/* Chest X-ray simulation */}
                    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 400 500" preserveAspectRatio="xMidYMid meet">
                      {/* Ribcage structure */}
                      <g opacity="0.3" stroke="#94a3b8" strokeWidth="1.5" fill="none">
                        {[...Array(8)].map((_, i) => (
                          <ellipse 
                            key={`rib-${i}`}
                            cx="200" 
                            cy={120 + i * 25} 
                            rx={80 - i * 5} 
                            ry={15 + i * 2}
                          />
                        ))}
                      </g>
                      
                      {/* Spine */}
                      <line x1="200" y1="100" x2="200" y2="450" stroke="#64748b" strokeWidth="3" opacity="0.4" />
                      
                      {/* Lungs - lighter areas */}
                      <ellipse cx="140" cy="250" rx="70" ry="120" fill="#475569" opacity="0.2" />
                      <ellipse cx="260" cy="250" rx="70" ry="120" fill="#475569" opacity="0.2" />
                      
                      {/* Heart shadow */}
                      <ellipse cx="180" cy="280" rx="50" ry="80" fill="#334155" opacity="0.3" />
                    </svg>
                  </>
                )}

                {/* Heatmap overlay for pneumonia detection */}
                {heatmapEnabled && analysisResult && analysisResult.diagnosis === "Pneumonia Detected" && (
                  <div 
                    className="absolute inset-0 pointer-events-none"
                    style={{ opacity: overlayOpacity / 100 }}
                  >
                    <div className="absolute left-[15%] bottom-[30%] w-40 h-40">
                      <div className="w-full h-full bg-gradient-to-br from-yellow-300/60 via-orange-400/50 to-red-500/40 rounded-full blur-3xl" />
                    </div>
                    <div className="absolute left-[15%] bottom-[25%] w-32 h-32">
                      <div className="w-full h-full bg-gradient-to-br from-amber-400/50 via-orange-500/40 to-red-600/30 rounded-full blur-2xl" />
                    </div>
                  </div>
                )}

                {/* Medical overlay markers */}
                <div className="absolute top-4 left-4 text-slate-400 text-sm font-mono">R</div>
                <div className="absolute top-4 right-4 text-slate-400 text-xs font-mono opacity-50">HIMA<br/>JPS</div>
              </div>
            </div>

            {/* Bottom Controls */}
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/70 to-transparent p-6">
              <div className="flex items-center justify-between max-w-4xl mx-auto">
                <div className="flex gap-3">
                  <button className="p-3 bg-white/10 hover:bg-white/20 rounded-xl backdrop-blur-sm transition-all">
                    <ZoomIn className="w-5 h-5 text-white" />
                  </button>
                  <button className="p-3 bg-white/10 hover:bg-white/20 rounded-xl backdrop-blur-sm transition-all">
                    <ZoomOut className="w-5 h-5 text-white" />
                  </button>
                  <button className="p-3 bg-white/10 hover:bg-white/20 rounded-xl backdrop-blur-sm transition-all">
                    <RotateCcw className="w-5 h-5 text-white" />
                  </button>
                  <button className="p-3 bg-white/10 hover:bg-white/20 rounded-xl backdrop-blur-sm transition-all">
                    <Moon className="w-5 h-5 text-white" />
                  </button>
                  <button className="p-3 bg-white/10 hover:bg-white/20 rounded-xl backdrop-blur-sm transition-all">
                    <Grid3x3 className="w-5 h-5 text-white" />
                  </button>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-3">
                    <span className="text-white text-sm font-medium">Original</span>
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      value={overlayOpacity}
                      onChange={(e) => setOverlayOpacity(Number(e.target.value))}
                      className="w-32 accent-blue-500"
                    />
                    <span className="text-white text-sm font-medium">AI Overlay</span>
                  </div>
                  
                  <button 
                    onClick={() => setHeatmapEnabled(!heatmapEnabled)}
                    className={`px-6 py-2.5 rounded-xl font-semibold transition-all flex items-center gap-2 ${
                      heatmapEnabled 
                        ? 'bg-blue-500 hover:bg-blue-600 text-white shadow-lg' 
                        : 'bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm'
                    }`}
                  >
                    <Maximize2 className="w-4 h-4" />
                    Toggle Heatmap
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Sidebar - AI Analysis Results */}
        <div className="w-96 space-y-6 flex-shrink-0">
          {/* AI Analysis Results */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <h2 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">AI Analysis Results</h2>
            
            {isLoading ? (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-slate-600 font-medium">Analyzing X-Ray Image...</p>
                <p className="text-sm text-slate-500 mt-2">This may take a few seconds</p>
              </div>
            ) : analysisResult ? (
              <>
                <div className={`rounded-xl p-4 mb-6 ${
                  analysisResult.diagnosis === "Pneumonia Detected" 
                    ? 'bg-gradient-to-br from-red-50 to-red-100 border-2 border-red-300' 
                    : 'bg-gradient-to-br from-green-50 to-green-100 border-2 border-green-300'
                }`}>
                  <div className="flex items-center justify-center gap-3">
                    {analysisResult.diagnosis === "Pneumonia Detected" ? (
                      <AlertCircle className="text-red-600" size={24} />
                    ) : (
                      <CheckCircle className="text-green-600" size={24} />
                    )}
                    <p className={`text-lg font-bold ${
                      analysisResult.diagnosis === "Pneumonia Detected" ? 'text-red-700' : 'text-green-700'
                    }`}>
                      {analysisResult.diagnosis}
                    </p>
                  </div>
                </div>

                <div className="mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold text-slate-700">Confidence Score</span>
                    <span className={`text-2xl font-bold ${
                      analysisResult.diagnosis === "Pneumonia Detected" ? 'text-red-600' : 'text-green-600'
                    }`}>
                      {analysisResult.confidence}%
                    </span>
                  </div>
                  <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full shadow-sm ${
                        analysisResult.diagnosis === "Pneumonia Detected" 
                          ? 'bg-gradient-to-r from-red-500 to-red-600' 
                          : 'bg-gradient-to-r from-green-500 to-green-600'
                      }`} 
                      style={{ width: `${analysisResult.confidence}%` }} 
                    />
                  </div>
                </div>

                {analysisResult.severity && analysisResult.severity !== "None" && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-slate-700">Severity Level</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(analysisResult.severity)}`}>
                        {analysisResult.severity}
                      </span>
                    </div>
                  </div>
                )}

                <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded-lg">
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-6 h-6 bg-amber-400 rounded-full flex items-center justify-center mt-0.5">
                      <span className="text-white font-bold text-sm">!</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-amber-800 mb-1">Confidence Threshold Alert</h3>
                      <p className="text-sm text-amber-700">
                        {analysisResult.diagnosis === "Pneumonia Detected" 
                          ? "AI confidence is high, but manual verification is crucial for definitive diagnosis."
                          : "No abnormalities detected. Routine follow-up recommended."
                        }
                      </p>
                    </div>
                  </div>
                </div>

                {/* Model Information */}
                <div className="mt-6 pt-6 border-t border-slate-200">
                  <div className="flex justify-between text-sm text-slate-600">
                    <span>Model Used:</span>
                    <span className="font-medium">{analysisResult.model_used || "Pneumonia Detection CNN"}</span>
                  </div>
                  <div className="flex justify-between text-sm text-slate-600 mt-2">
                    <span>Processing Time:</span>
                    <span className="font-medium">{analysisResult.processing_time || "1.5s"}</span>
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-8">
                <Activity className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600 font-medium">No Analysis Yet</p>
                <p className="text-sm text-slate-500 mt-2">Upload an X-ray image to get AI analysis results</p>
              </div>
            )}
          </div>

          {/* Clinical Recommendations */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-slate-200">
            <h2 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">Clinical Recommendations</h2>
            
            {analysisResult ? (
              <ul className="space-y-4 text-sm">
                {analysisResult.recommendations.map((rec, index) => (
                  <li key={index} className="flex gap-3">
                    <Shield className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                    <p className="text-slate-700 leading-relaxed">
                      {rec}
                    </p>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="text-center py-4">
                <p className="text-slate-500 text-sm">Upload and analyze an image to see recommendations</p>
              </div>
            )}
          </div>

          {/* System Status */}
          <div className="bg-white rounded-2xl p=6 shadow-lg border border-slate-200">
            <h2 className="text-sm font-bold text-slate-900 mb-4 uppercase tracking-wide">System Status</h2>
            
            <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-start gap-3">
              <div className="flex-shrink-0 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mt-0.5">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-semibold text-green-800 mb-1">
                  {analysisResult 
                    ? "AI analysis complete. System nominal." 
                    : "System ready. Awaiting image upload."
                  }
                </p>
                {analysisResult && (
                  <p className="text-xs text-green-700">Analysis timestamp: {analysisResult.timestamp}</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}