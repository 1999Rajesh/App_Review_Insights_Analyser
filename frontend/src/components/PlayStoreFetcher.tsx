import React, { useState } from 'react';
import { reviewsAPI } from '../services/api';

interface PlayStoreFetcherProps {
  onFetchComplete: (data: any) => void;
}

const PlayStoreFetcher: React.FC<PlayStoreFetcherProps> = ({ onFetchComplete }) => {
  const [appId, setAppId] = useState('');
  const [weeks, setWeeks] = useState(8);
  const [maxReviews, setMaxReviews] = useState(500);
  const [country, setCountry] = useState('us');
  const [language, setLanguage] = useState('en');
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    if (!appId.trim()) {
      setError('Please enter a Google Play Store app ID');
      return;
    }

    // Basic validation
    const appIdRegex = /^[a-z][a-z0-9_]+(\.[a-z0-9_]+)+$/i;
    if (!appIdRegex.test(appId)) {
      setError('Invalid app ID format. Example: com.whatsapp or com.instagram.android');
      return;
    }

    setFetching(true);
    setError(null);

    try {
      const result = await reviewsAPI.fetchPlayStoreReviews({
        app_id: appId,
        weeks: weeks,
        max_reviews: maxReviews,
        country: country,
        language: language,
      });

      onFetchComplete(result.data);
      
      // Clear form
      setAppId('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch reviews from Play Store');
    } finally {
      setFetching(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>🤖 Auto-Fetch from Google Play Store</h3>
        <p style={styles.description}>
          Automatically fetch reviews directly from Google Play Store - no CSV upload needed!
        </p>
      </div>

      <div style={styles.form}>
        <div style={styles.mainInput}>
          <label style={styles.label}>Google Play Store App ID</label>
          <input
            type="text"
            value={appId}
            onChange={(e) => setAppId(e.target.value)}
            placeholder="e.g., com.whatsapp, com.spotify.music, com.instagram.android"
            style={styles.input}
            disabled={fetching}
          />
          <p style={styles.helpText}>
            Find the app ID in the Play Store URL: play.google.com/store/apps/details?id=<strong>com.example.app</strong>
          </p>
        </div>

        <div style={styles.optionsRow}>
          <div style={styles.optionGroup}>
            <label style={styles.label}>Weeks</label>
            <input
              type="number"
              value={weeks}
              onChange={(e) => setWeeks(parseInt(e.target.value))}
              style={styles.smallInput}
              min="1"
              max="52"
              disabled={fetching}
            />
          </div>

          <div style={styles.optionGroup}>
            <label style={styles.label}>Max Reviews</label>
            <input
              type="number"
              value={maxReviews}
              onChange={(e) => setMaxReviews(parseInt(e.target.value))}
              style={styles.smallInput}
              min="10"
              max="5000"
              disabled={fetching}
            />
          </div>

          <div style={styles.optionGroup}>
            <label style={styles.label}>Country</label>
            <select
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              style={styles.smallInput}
              disabled={fetching}
            >
              <option value="us">🇺🇸 US</option>
              <option value="uk">🇬🇧 UK</option>
              <option value="in">🇮🇳 India</option>
              <option value="ca">🇨🇦 Canada</option>
              <option value="au">🇦🇺 Australia</option>
              <option value="de">🇩🇪 Germany</option>
              <option value="fr">🇫🇷 France</option>
              <option value="jp">🇯🇵 Japan</option>
              <option value="br">🇧🇷 Brazil</option>
            </select>
          </div>

          <div style={styles.optionGroup}>
            <label style={styles.label}>Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              style={styles.smallInput}
              disabled={fetching}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="pt">Portuguese</option>
              <option value="ja">Japanese</option>
              <option value="hi">Hindi</option>
            </select>
          </div>
        </div>

        {error && <div style={styles.errorBanner}>⚠️ {error}</div>}

        <button
          onClick={handleFetch}
          disabled={fetching || !appId.trim()}
          style={{
            ...styles.fetchButton,
            ...(fetching || !appId.trim() ? styles.buttonDisabled : {}),
          }}
        >
          {fetching ? (
            <>
              <span style={styles.spinner}></span>
              Fetching Reviews...
            </>
          ) : (
            <>
              🚀 Fetch Play Store Reviews
            </>
          )}
        </button>

        <div style={styles.infoBox}>
          <strong>💡 How to find App ID:</strong>
          <ol style={styles.steps}>
            <li>Go to Google Play Store website</li>
            <li>Search for your app</li>
            <li>Copy the ID from URL after <code>?id=</code></li>
            <li>Example: <code>com.whatsapp</code> from <code>play.google.com/store/apps/details?id=com.whatsapp</code></li>
          </ol>
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    padding: '35px',
    borderRadius: '16px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
    marginBottom: '20px',
    backdropFilter: 'blur(10px)',
    border: '2px solid rgba(102, 126, 234, 0.2)',
    animation: 'slideUp 0.5s ease-out',
  },
  header: {
    marginBottom: '25px',
  },
  title: {
    margin: '0 0 10px 0',
    color: '#2d3748',
    fontSize: '22px',
    fontWeight: '700',
  },
  description: {
    color: '#718096',
    fontSize: '14px',
    margin: 0,
    lineHeight: '1.6',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  mainInput: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    color: '#4a5568',
    fontSize: '14px',
    fontWeight: '600',
  },
  input: {
    padding: '14px 18px',
    border: '2px solid #e2e8f0',
    borderRadius: '10px',
    fontSize: '16px',
    color: '#2d3748',
    transition: 'all 0.2s',
    backgroundColor: 'white',
  },
  helpText: {
    color: '#a0aec0',
    fontSize: '13px',
    fontStyle: 'italic',
  },
  optionsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
    gap: '15px',
  },
  optionGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  smallInput: {
    padding: '12px 14px',
    border: '2px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '15px',
    color: '#2d3748',
    backgroundColor: 'white',
  },
  errorBanner: {
    backgroundColor: 'linear-gradient(135deg, #fee 0%, #fcc 100%)',
    color: '#c53030',
    padding: '14px 18px',
    borderRadius: '10px',
    fontSize: '14px',
    fontWeight: '600',
    border: '2px solid #feb2b2',
    animation: 'shake 0.5s ease-out',
  },
  fetchButton: {
    backgroundColor: '#667eea',
    color: 'white',
    border: 'none',
    padding: '16px 30px',
    borderRadius: '12px',
    fontSize: '17px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 6px 16px rgba(102, 126, 234, 0.3)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
  },
  buttonDisabled: {
    backgroundColor: '#cbd5e0',
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
  spinner: {
    display: 'inline-block',
    width: '20px',
    height: '20px',
    border: '3px solid rgba(255,255,255,0.3)',
    borderTopColor: 'white',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  infoBox: {
    backgroundColor: 'rgba(240, 253, 244, 0.8)',
    border: '2px solid #c6f6d5',
    borderRadius: '12px',
    padding: '18px',
    marginTop: '10px',
  },
  steps: {
    margin: '10px 0 0 0',
    paddingLeft: '20px',
    color: '#276749',
    fontSize: '13px',
    lineHeight: '1.8',
  },
};

export default PlayStoreFetcher;
