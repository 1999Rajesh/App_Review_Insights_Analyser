import React, { useState } from 'react';
import { reviewsAPI } from '../services/api';

interface PlayStoreFetcherProps {
  onFetchComplete: (data: any) => void;
}

const PlayStoreFetcher: React.FC<PlayStoreFetcherProps> = ({ onFetchComplete }) => {
  const [weeks, setWeeks] = useState(8);
  const [maxReviews, setMaxReviews] = useState(500);
  const [recipientName, setRecipientName] = useState('');
  const [recipientEmail, setRecipientEmail] = useState('');
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFetch = async () => {
    // Validation
    if (!recipientName.trim()) {
      setError('Please enter recipient name');
      return;
    }

    if (!recipientEmail.trim()) {
      setError('Please enter recipient email');
      return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(recipientEmail)) {
      setError('Please enter a valid email address');
      return;
    }

    setFetching(true);
    setError(null);

    try {
      const result = await reviewsAPI.fetchPlayStoreReviews({
        weeks: weeks,
        max_reviews: maxReviews,
        recipient_name: recipientName,
        recipient_email: recipientEmail,
      });

      onFetchComplete(result.data);
      
      // Clear form
      setRecipientName('');
      setRecipientEmail('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch reviews from Play Store');
    } finally {
      setFetching(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>📊 Weekly Review Insights</h3>
        <p style={styles.description}>
          Automatically fetch and analyze reviews from Google Play Store
        </p>
      </div>

      <div style={styles.form}>
        <div style={styles.mainSection}>
          <h4 style={styles.sectionTitle}>📥 Analysis Settings</h4>
          
          <div style={styles.optionsRow}>
            <div style={styles.optionGroup}>
              <label style={styles.label}>📅 Weeks to Analyze</label>
              <input
                type="number"
                value={weeks}
                onChange={(e) => setWeeks(parseInt(e.target.value))}
                style={styles.input}
                min="1"
                max="52"
                disabled={fetching}
              />
            </div>

            <div style={styles.optionGroup}>
              <label style={styles.label}>📊 Max Reviews</label>
              <input
                type="number"
                value={maxReviews}
                onChange={(e) => setMaxReviews(parseInt(e.target.value))}
                style={styles.input}
                min="10"
                max="5000"
                disabled={fetching}
              />
            </div>
          </div>
        </div>

        <div style={styles.divider}></div>

        <div style={styles.emailSection}>
          <h4 style={styles.sectionTitle}>📧 Recipient Details</h4>
          
          <div style={styles.inputGroup}>
            <label style={styles.label}>Recipient Name</label>
            <input
              type="text"
              value={recipientName}
              onChange={(e) => setRecipientName(e.target.value)}
              placeholder="e.g., John Doe"
              style={styles.input}
              disabled={fetching}
            />
          </div>

          <div style={styles.inputGroup}>
            <label style={styles.label}>Recipient Email</label>
            <input
              type="email"
              value={recipientEmail}
              onChange={(e) => setRecipientEmail(e.target.value)}
              placeholder="e.g., john@example.com"
              style={styles.input}
              disabled={fetching}
            />
          </div>
        </div>

        {error && <div style={styles.errorBanner}>⚠️ {error}</div>}

        <button
          onClick={handleFetch}
          disabled={fetching}
          style={{
            ...styles.fetchButton,
            ...(fetching ? styles.buttonDisabled : {}),
          }}
        >
          {fetching ? (
            <>
              <span style={styles.spinner}></span>
              Fetching & Analyzing Reviews...
            </>
          ) : (
            <>
              ✨ Generate Weekly Insights Report
            </>
          )}
        </button>

        <div style={styles.infoBox}>
          <strong>💡 How it works:</strong>
          <ol style={styles.steps}>
            <li>Fetches reviews from configured Play Store app</li>
            <li>AI analyzes sentiment and key themes</li>
            <li>Generates actionable insights report</li>
            <li>Emails digest to specified recipient</li>
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
    fontSize: '24px',
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
  mainSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
  },
  sectionTitle: {
    margin: '0 0 10px 0',
    color: '#4a5568',
    fontSize: '16px',
    fontWeight: '700',
  },
  optionsRow: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
  },
  optionGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  input: {
    padding: '14px 18px',
    border: '2px solid #e2e8f0',
    borderRadius: '10px',
    fontSize: '15px',
    color: '#2d3748',
    backgroundColor: 'white',
    transition: 'all 0.2s',
  },
  emailSection: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  label: {
    color: '#4a5568',
    fontSize: '14px',
    fontWeight: '600',
  },
  divider: {
    height: '2px',
    backgroundColor: '#e2e8f0',
    margin: '10px 0',
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
    backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
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
