import { useState } from 'react';
import { WeeklyReport as WeeklyReportType, emailAPI } from '../services/api';

interface WeeklyReportProps {
  report: WeeklyReportType;
}

const WeeklyReport: React.FC<WeeklyReportProps> = ({ report }) => {
  const [sendingEmail, setSendingEmail] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);

  const handleSendEmail = async () => {
    setSendingEmail(true);
    setEmailError(null);

    try {
      await emailAPI.sendDraft(report.id);
      setEmailSent(true);
    } catch (err: any) {
      setEmailError(err.response?.data?.detail || 'Failed to send email');
    } finally {
      setSendingEmail(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return '#4CAF50';
      case 'negative':
        return '#f44336';
      case 'neutral':
        return '#ff9800';
      default:
        return '#666';
    }
  };

  return (
    <div style={styles.container}>
      {/* Dashboard Header */}
      <div style={styles.dashboardHeader}>
        <div style={styles.headerLeft}>
          <div style={styles.badge}>📊 WEEKLY PULSE</div>
          <h2 style={styles.title}>App Review Insights</h2>
        </div>
        <div style={styles.headerRight}>
          <div style={styles.dateBadge}>
            {formatDate(report.week_start)} - {formatDate(report.week_end)}
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div style={styles.statsGrid}>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>📝</div>
          <div style={styles.statValue}>{report.total_reviews}</div>
          <div style={styles.statLabel}>Total Reviews Analyzed</div>
        </div>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>📏</div>
          <div style={styles.statValue}>{report.word_count}</div>
          <div style={styles.statLabel}>Word Count</div>
        </div>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>🎯</div>
          <div style={styles.statValue}>{report.top_themes.length}</div>
          <div style={styles.statLabel}>Key Themes</div>
        </div>
        <div style={styles.statCard}>
          <div style={styles.statIcon}>⚡</div>
          <div style={styles.statValue}>AI-Powered</div>
          <div style={styles.statLabel}>Analysis Engine</div>
        </div>
      </div>

      {/* Themes Section */}
      <div style={styles.themesContainer}>
        <div style={styles.sectionHeader}>
          <h3 style={styles.sectionTitle}>🔍 Key Insights This Week</h3>
          <div style={styles.sectionSubtitle}>
            Top themes identified from user reviews
          </div>
        </div>
        
        <div style={styles.themesList}>
          {report.top_themes.map((theme, index) => (
            <div key={index} style={styles.themeCard}>
              <div style={styles.themeCardHeader}>
                <div style={styles.themeRank}>{index + 1}</div>
                <div style={styles.themeContent}>
                  <div style={styles.themeTitleRow}>
                    <h4 style={styles.themeName}>{theme.theme_name}</h4>
                    <span
                      style={{
                        ...styles.sentimentBadge,
                        backgroundColor: getSentimentColor(theme.sentiment),
                      }}
                    >
                      {theme.sentiment === 'positive' ? '😊' : theme.sentiment === 'negative' ? '⚠️' : '😐'} {theme.sentiment.toUpperCase()}
                    </span>
                  </div>
                  <div style={styles.themeMetrics}>
                    <div style={styles.metricItem}>
                      <span style={styles.metricValue}>{theme.review_count}</span>
                      <span style={styles.metricLabel}>reviews</span>
                    </div>
                    <div style={styles.metricDivider}></div>
                    <div style={styles.metricItem}>
                      <span style={styles.metricValue}>{theme.percentage}%</span>
                      <span style={styles.metricLabel}>of total</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* User Quotes */}
              <div style={styles.quotesBox}>
                <div style={styles.boxHeader}>
                  <span style={styles.boxIcon}>💬</span>
                  <strong>What Users Are Saying</strong>
                </div>
                <ul style={styles.quotesList}>
                  {theme.quotes.map((quote, idx) => (
                    <li key={idx} style={styles.quoteItem}>
                      <span style={styles.quoteIcon}>"</span>
                      <span style={styles.quoteText}>{quote}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Action Ideas */}
              <div style={styles.actionsBox}>
                <div style={styles.boxHeader}>
                  <span style={styles.boxIcon}>💡</span>
                  <strong>Recommended Actions</strong>
                </div>
                <ol style={styles.actionsList}>
                  {theme.action_ideas.map((action, idx) => (
                    <li key={idx} style={styles.actionItem}>
                      <span style={styles.actionNumber}>{idx + 1}</span>
                      <span style={styles.actionText}>{action}</span>
                    </li>
                  ))}
                </ol>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer Actions */}
      <div style={styles.footerActions}>
        {emailError && <div style={styles.errorBanner}>⚠️ {emailError}</div>}
        {emailSent ? (
          <div style={styles.successBanner}>
            ✅ Email sent successfully!
          </div>
        ) : (
          <button
            onClick={handleSendEmail}
            disabled={sendingEmail}
            style={{
              ...styles.emailButton,
              ...(sendingEmail ? styles.buttonDisabled : {}),
            }}
          >
            {sendingEmail ? (
              <>
                <span style={styles.spinner}></span>
                Sending...
              </>
            ) : (
              <>
                📧 Send Email Digest
              </>
            )}
          </button>
        )}
        
        <div style={styles.timestamp}>
          Generated: {new Date(report.generated_at).toLocaleString()}
        </div>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    animation: 'slideUp 0.6s ease-out',
  },
  dashboardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '30px',
    paddingBottom: '25px',
    borderBottom: '3px solid #e2e8f0',
    background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)',
    padding: '25px',
    borderRadius: '16px',
  },
  headerLeft: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
  },
  badge: {
    display: 'inline-block',
    backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '6px 16px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: '700',
    letterSpacing: '1px',
    alignSelf: 'flex-start',
    boxShadow: '0 4px 8px rgba(102, 126, 234, 0.3)',
  },
  title: {
    margin: 0,
    color: '#2d3748',
    fontSize: '32px',
    fontWeight: '800',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  headerRight: {
    display: 'flex',
    alignItems: 'center',
  },
  dateBadge: {
    backgroundColor: '#edf2f7',
    color: '#4a5568',
    padding: '10px 20px',
    borderRadius: '12px',
    fontSize: '14px',
    fontWeight: '600',
    border: '2px solid #e2e8f0',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '20px',
    marginBottom: '35px',
  },
  statCard: {
    backgroundColor: 'linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%)',
    padding: '25px',
    borderRadius: '16px',
    textAlign: 'center',
    border: '2px solid rgba(102, 126, 234, 0.2)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
  },
  statIcon: {
    fontSize: '36px',
    marginBottom: '10px',
  },
  statValue: {
    fontSize: '36px',
    fontWeight: '800',
    color: '#667eea',
    marginBottom: '8px',
  },
  statLabel: {
    fontSize: '14px',
    color: '#718096',
    fontWeight: '600',
  },
  themesContainer: {
    marginBottom: '35px',
  },
  sectionHeader: {
    marginBottom: '25px',
    textAlign: 'center',
  },
  sectionTitle: {
    margin: '0 0 10px 0',
    color: '#2d3748',
    fontSize: '26px',
    fontWeight: '700',
  },
  sectionSubtitle: {
    color: '#718096',
    fontSize: '15px',
    fontStyle: 'italic',
  },
  themesList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '25px',
  },
  themeCard: {
    backgroundColor: '#fff',
    border: '2px solid #e2e8f0',
    borderRadius: '16px',
    padding: '30px',
    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    position: 'relative',
    overflow: 'hidden',
  },
  themeCardHeader: {
    display: 'flex',
    gap: '20px',
    marginBottom: '25px',
    alignItems: 'flex-start',
  },
  themeRank: {
    width: '50px',
    height: '50px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '24px',
    fontWeight: '800',
    flexShrink: 0,
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
  },
  themeContent: {
    flex: 1,
  },
  themeTitleRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
    flexWrap: 'wrap',
    gap: '10px',
  },
  themeName: {
    margin: 0,
    fontSize: '22px',
    color: '#2d3748',
    fontWeight: '700',
  },
  themeMetrics: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    backgroundColor: '#f7fafc',
    padding: '12px 16px',
    borderRadius: '12px',
    marginTop: '10px',
  },
  metricItem: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '4px',
  },
  metricValue: {
    fontSize: '20px',
    fontWeight: '700',
    color: '#667eea',
  },
  metricLabel: {
    fontSize: '12px',
    color: '#a0aec0',
    fontWeight: '500',
  },
  metricDivider: {
    width: '2px',
    height: '30px',
    backgroundColor: '#e2e8f0',
  },
  sentimentBadge: {
    color: 'white',
    padding: '6px 14px',
    borderRadius: '20px',
    fontSize: '12px',
    fontWeight: '800',
    letterSpacing: '0.5px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
  },
  quotesBox: {
    backgroundColor: 'rgba(247, 250, 252, 0.8)',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    padding: '20px',
    marginBottom: '20px',
  },
  boxHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '15px',
    color: '#4a5568',
    fontSize: '16px',
    fontWeight: '700',
  },
  boxIcon: {
    fontSize: '20px',
  },
  quotesList: {
    margin: 0,
    paddingLeft: 0,
    listStyle: 'none',
  },
  quoteItem: {
    display: 'flex',
    gap: '12px',
    marginBottom: '15px',
    color: '#4a5568',
    lineHeight: '1.6',
    fontSize: '15px',
    fontStyle: 'italic',
    backgroundColor: 'white',
    padding: '15px',
    borderRadius: '8px',
    border: '1px solid #e2e8f0',
  },
  quoteIcon: {
    fontSize: '24px',
    color: '#cbd5e0',
    fontWeight: 'bold',
    flexShrink: 0,
  },
  quoteText: {
    flex: 1,
  },
  actionsBox: {
    backgroundColor: 'rgba(240, 253, 244, 0.8)',
    border: '2px solid #c6f6d5',
    borderRadius: '12px',
    padding: '20px',
  },
  actionsList: {
    margin: '10px 0',
    paddingLeft: 0,
    listStyle: 'none',
  },
  actionItem: {
    display: 'flex',
    gap: '12px',
    marginBottom: '12px',
    color: '#2d3748',
    lineHeight: '1.6',
    fontSize: '15px',
    backgroundColor: 'white',
    padding: '15px',
    borderRadius: '8px',
    border: '1px solid #c6f6d5',
  },
  actionNumber: {
    width: '28px',
    height: '28px',
    borderRadius: '50%',
    backgroundColor: '#4CAF50',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '14px',
    fontWeight: '700',
    flexShrink: 0,
  },
  actionText: {
    flex: 1,
  },
  footerActions: {
    borderTop: '2px solid #e2e8f0',
    paddingTop: '25px',
    marginTop: '25px',
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    alignItems: 'center',
  },
  emailButton: {
    backgroundColor: '#2196F3',
    color: 'white',
    border: 'none',
    padding: '16px 50px',
    borderRadius: '12px',
    fontSize: '17px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 6px 16px rgba(33, 150, 243, 0.3)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    width: '100%',
    maxWidth: '400px',
  },
  buttonDisabled: {
    backgroundColor: '#cbd5e0',
    cursor: 'not-allowed',
    boxShadow: 'none',
  },
  errorBanner: {
    backgroundColor: 'linear-gradient(135deg, #fee 0%, #fcc 100%)',
    color: '#c53030',
    padding: '16px 20px',
    borderRadius: '12px',
    fontSize: '15px',
    fontWeight: '600',
    width: '100%',
    maxWidth: '600px',
    border: '2px solid #feb2b2',
    boxShadow: '0 4px 12px rgba(244, 67, 54, 0.2)',
  },
  successBanner: {
    backgroundColor: 'linear-gradient(135deg, #e6fffa 0%, #c6f6d5 100%)',
    color: '#276749',
    padding: '16px 20px',
    borderRadius: '12px',
    fontSize: '16px',
    fontWeight: '600',
    width: '100%',
    maxWidth: '600px',
    border: '2px solid #9ae6b4',
    boxShadow: '0 4px 12px rgba(76, 175, 80, 0.2)',
    textAlign: 'center',
  },
  timestamp: {
    textAlign: 'center',
    color: '#a0aec0',
    fontSize: '13px',
    marginTop: '10px',
    fontStyle: 'italic',
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
};

export default WeeklyReport;
