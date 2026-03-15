import React, { useState, useEffect } from 'react';
import { reviewsAPI } from '../services/api';

interface AppSettings {
  review_weeks_range: number;
  max_reviews_to_fetch: number;
  max_themes: number;
  max_words: number;
  play_store_country: string;
  play_store_language: string;
  scheduler_interval_minutes: number;
}

const SettingsPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [settings, setSettings] = useState<AppSettings>({
    review_weeks_range: 8,
    max_reviews_to_fetch: 500,
    max_themes: 5,
    max_words: 250,
    play_store_country: 'us',
    play_store_language: 'en',
    scheduler_interval_minutes: 5,
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await reviewsAPI.getSettings();
      setSettings(response.data);
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    setMessage(null);

    try {
      await reviewsAPI.updateSettings(settings);
      setMessage({ type: 'success', text: '✅ Settings saved successfully!' });
      
      // Clear message after 3 seconds
      setTimeout(() => setMessage(null), 3000);
    } catch (error: any) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to save settings' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (key: keyof AppSettings, value: string | number) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <>
      {/* Settings Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={styles.toggleButton}
      >
        ⚙️ {isOpen ? 'Close Settings' : 'Settings'}
      </button>

      {/* Settings Panel */}
      {isOpen && (
        <div style={styles.container}>
          <div style={styles.header}>
            <h2 style={styles.title}>⚙️ Application Settings</h2>
            <p style={styles.subtitle}>
              Configure review fetching and analysis preferences
            </p>
          </div>

          {/* Review Fetching Settings */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>📊 Review Fetching</h3>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Weeks of Reviews to Analyze</label>
              <input
                type="number"
                value={settings.review_weeks_range}
                onChange={(e) => handleChange('review_weeks_range', parseInt(e.target.value))}
                style={styles.input}
                min="1"
                max="52"
              />
              <p style={styles.helpText}>
                Fetch reviews from the last {settings.review_weeks_range} weeks
              </p>
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Maximum Reviews to Fetch</label>
              <input
                type="number"
                value={settings.max_reviews_to_fetch}
                onChange={(e) => handleChange('max_reviews_to_fetch', parseInt(e.target.value))}
                style={styles.input}
                min="10"
                max="5000"
              />
              <p style={styles.helpText}>
                Limit fetched reviews to {settings.max_reviews_to_fetch}
              </p>
            </div>
          </div>

          {/* Google Play Store Settings */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>🤖 Google Play Store</h3>
            
            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Country Code</label>
                <input
                  type="text"
                  value={settings.play_store_country}
                  onChange={(e) => handleChange('play_store_country', e.target.value)}
                  style={styles.inputSmall}
                  placeholder="us"
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Language Code</label>
                <input
                  type="text"
                  value={settings.play_store_language}
                  onChange={(e) => handleChange('play_store_language', e.target.value)}
                  style={styles.inputSmall}
                  placeholder="en"
                />
              </div>
            </div>

            <p style={styles.helpText}>
              Country: us, uk, in, etc. | Language: en, es, fr, etc.
            </p>
          </div>

          {/* AI Analysis Settings */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>🤖 AI Analysis</h3>
            
            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Max Themes</label>
                <input
                  type="number"
                  value={settings.max_themes}
                  onChange={(e) => handleChange('max_themes', parseInt(e.target.value))}
                  style={styles.inputSmall}
                  min="1"
                  max="10"
                />
              </div>

              <div style={styles.formGroup}>
                <label style={styles.label}>Max Words</label>
                <input
                  type="number"
                  value={settings.max_words}
                  onChange={(e) => handleChange('max_words', parseInt(e.target.value))}
                  style={styles.inputSmall}
                  min="100"
                  max="1000"
                />
              </div>
            </div>

            <p style={styles.helpText}>
              Generate up to {settings.max_themes} themes with {settings.max_words} words
            </p>
          </div>

          {/* Scheduler Settings */}
          <div style={styles.section}>
            <h3 style={styles.sectionTitle}>🕐 Automated Scheduler</h3>
            
            <div style={styles.formGroup}>
              <label style={styles.label}>Run Every (minutes)</label>
              <input
                type="number"
                value={settings.scheduler_interval_minutes}
                onChange={(e) => handleChange('scheduler_interval_minutes', parseInt(e.target.value))}
                style={styles.input}
                min="1"
                max="1440"
              />
              <p style={styles.helpText}>
                Scheduler runs every {settings.scheduler_interval_minutes} minutes
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={styles.buttonContainer}>
            {message && (
              <div style={message.type === 'success' ? styles.successMessage : styles.errorMessage}>
                {message.text}
              </div>
            )}
            
            <button
              onClick={handleSave}
              disabled={loading}
              style={{
                ...styles.saveButton,
                ...(loading ? styles.buttonDisabled : {}),
              }}
            >
              {loading ? 'Saving...' : '💾 Save Settings'}
            </button>
            
            <p style={styles.note}>
              ⚠️ Note: Settings reset on server restart. For permanent changes, update .env file
            </p>
          </div>
        </div>
      )}
    </>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  toggleButton: {
    position: 'fixed',
    top: '20px',
    right: '20px',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    color: '#4a5568',
    border: '2px solid #e2e8f0',
    padding: '12px 20px',
    borderRadius: '12px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    zIndex: 1000,
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  container: {
    position: 'fixed',
    top: '70px',
    right: '20px',
    width: '450px',
    maxHeight: 'calc(100vh - 90px)',
    overflowY: 'auto',
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    borderRadius: '16px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
    zIndex: 999,
    padding: '30px',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    animation: 'slideUp 0.3s ease-out',
  },
  header: {
    marginBottom: '25px',
  },
  title: {
    margin: '0 0 10px 0',
    color: '#2d3748',
    fontSize: '24px',
    fontWeight: '700',
  },
  subtitle: {
    color: '#718096',
    fontSize: '14px',
    margin: 0,
  },
  section: {
    marginBottom: '25px',
    paddingBottom: '25px',
    borderBottom: '2px solid #e2e8f0',
  },
  sectionTitle: {
    margin: '0 0 15px 0',
    color: '#4a5568',
    fontSize: '18px',
    fontWeight: '600',
  },
  formGroup: {
    marginBottom: '15px',
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '15px',
  },
  label: {
    display: 'block',
    color: '#4a5568',
    fontSize: '14px',
    fontWeight: '600',
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '10px 14px',
    border: '2px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '15px',
    color: '#2d3748',
    transition: 'all 0.2s',
  },
  inputSmall: {
    width: '100%',
    padding: '10px 14px',
    border: '2px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '15px',
    color: '#2d3748',
    transition: 'all 0.2s',
  },
  helpText: {
    color: '#a0aec0',
    fontSize: '13px',
    marginTop: '6px',
    fontStyle: 'italic',
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '10px',
  },
  saveButton: {
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    padding: '14px 30px',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 6px 16px rgba(76, 175, 80, 0.3)',
    width: '100%',
  },
  buttonDisabled: {
    backgroundColor: '#cbd5e0',
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
  successMessage: {
    backgroundColor: 'linear-gradient(135deg, #e6fffa 0%, #c6f6d5 100%)',
    color: '#276749',
    padding: '12px 16px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    width: '100%',
    border: '2px solid #9ae6b4',
    textAlign: 'center',
  },
  errorMessage: {
    backgroundColor: 'linear-gradient(135deg, #fee 0%, #fcc 100%)',
    color: '#c53030',
    padding: '12px 16px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    width: '100%',
    border: '2px solid #feb2b2',
    textAlign: 'center',
  },
  note: {
    color: '#a0aec0',
    fontSize: '12px',
    fontStyle: 'italic',
    textAlign: 'center',
    marginTop: '10px',
  },
};

export default SettingsPanel;
