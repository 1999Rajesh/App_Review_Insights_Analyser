import React from 'react';

const themeLegendData = [
  { name: 'Onboarding/Sign-up', icon: '🎯', color: '#2196F3' },
  { name: 'KYC Verification', icon: '🔐', color: '#9C27B0' },
  { name: 'Payments/Transactions', icon: '💳', color: '#f44336' },
  { name: 'Account Statements', icon: '📊', color: '#FF9800' },
  { name: 'Withdrawals/Cash-out', icon: '💸', color: '#4CAF50' },
  { name: 'Customer Support', icon: '🎧', color: '#00BCD4' },
  { name: 'App Performance/Bugs', icon: '⚡', color: '#E91E63' },
  { name: 'UI/UX Issues', icon: '🎨', color: '#795548' },
];

const ThemeLegend: React.FC = () => {
  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Theme Legend</h3>
      <div style={styles.grid}>
        {themeLegendData.map((theme) => (
          <div key={theme.name} style={styles.themeItem}>
            <span style={{ ...styles.icon, backgroundColor: theme.color }}>
              {theme.icon}
            </span>
            <span style={styles.label}>{theme.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  title: {
    margin: '0 0 15px 0',
    color: '#333',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
    gap: '10px',
  },
  themeItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '8px',
    borderRadius: '4px',
    backgroundColor: '#f5f5f5',
  },
  icon: {
    width: '32px',
    height: '32px',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '18px',
  },
  label: {
    fontSize: '13px',
    color: '#333',
  },
};

export default ThemeLegend;
