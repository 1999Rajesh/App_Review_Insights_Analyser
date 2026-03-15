import React, { useState } from 'react';
import ReviewUploader from './components/ReviewUploader';
import WeeklyReport from './components/WeeklyReport';
import ThemeLegend from './components/ThemeLegend';
import SettingsPanel from './components/SettingsPanel';
import PlayStoreFetcher from './components/PlayStoreFetcher';
import { analysisAPI, reportsAPI, reviewsAPI } from './services/api';
import type { WeeklyReport as WeeklyReportType } from './services/api';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState<'upload' | 'report'>('upload');
  const [latestReport, setLatestReport] = useState<WeeklyReportType | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);

  const handleUploadComplete = async (uploadData: any) => {
    setUploadMessage(
      `Successfully uploaded ${uploadData.total_reviews} reviews (${uploadData.app_store_count} from App Store, ${uploadData.play_store_count} from Play Store)`
    );
  };

  const handleGenerateReport = async () => {
    setLoading(true);
    setError(null);

    try {
      // Generate weekly report
      const reportResponse = await analysisAPI.generateWeeklyReport();
      setLatestReport(reportResponse.data);
      setCurrentView('report');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToUpload = () => {
    setCurrentView('upload');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 App Review Insights Analyzer</h1>
        <p className="subtitle">Turn app store reviews into actionable weekly insights</p>
      </header>

      <main className="app-main">
        {/* Settings Panel - Always visible */}
        <SettingsPanel />

        {currentView === 'upload' ? (
          <div className="upload-section">
            {/* New: Google Play Store Auto-Fetch */}
            <PlayStoreFetcher onFetchComplete={handleUploadComplete} />
            
            {/* Traditional CSV Upload */}
            <ReviewUploader onUploadComplete={handleUploadComplete} />
            
            {uploadMessage && (
              <div className="success-message">
                <p>✓ {uploadMessage}</p>
              </div>
            )}

            <div className="action-buttons">
              <button
                onClick={handleGenerateReport}
                disabled={loading}
                className="generate-button"
              >
                {loading ? 'Generating...' : '✨ Generate Weekly Report'}
              </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <ThemeLegend />
          </div>
        ) : (
          <div className="report-section">
            <button onClick={handleBackToUpload} className="back-button">
              ← Back to Upload
            </button>
            
            {latestReport && <WeeklyReport report={latestReport} />}
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by Groq AI • Fast • Private • Actionable</p>
      </footer>
    </div>
  );
}

export default App;
