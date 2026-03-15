import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { reviewsAPI } from '../services/api';

interface ReviewUploaderProps {
  onUploadComplete: (data: any) => void;
}

const ReviewUploader: React.FC<ReviewUploaderProps> = ({ onUploadComplete }) => {
  const [appStoreFile, setAppStoreFile] = useState<File | null>(null);
  const [playStoreFile, setPlayStoreFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onAppStoreDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setAppStoreFile(acceptedFiles[0]);
      setError(null);
    }
  }, []);

  const onPlayStoreDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setPlayStoreFile(acceptedFiles[0]);
      setError(null);
    }
  }, []);

  const {
    getRootProps: getAppStoreRootProps,
    getInputProps: getAppStoreInputProps,
    isDragActive: isAppStoreDragActive,
  } = useDropzone({
    onDrop: onAppStoreDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  });

  const {
    getRootProps: getPlayStoreRootProps,
    getInputProps: getPlayStoreInputProps,
    isDragActive: isPlayStoreDragActive,
  } = useDropzone({
    onDrop: onPlayStoreDrop,
    accept: { 'text/csv': ['.csv'] },
    multiple: false,
  });

  const handleUpload = async () => {
    if (!appStoreFile && !playStoreFile) {
      setError('Please select at least one CSV file');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const result = await reviewsAPI.upload(appStoreFile || undefined, playStoreFile || undefined);
      onUploadComplete(result);
      
      // Clear selected files
      setAppStoreFile(null);
      setPlayStoreFile(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload files');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.headerSection}>
        <h2 style={styles.title}>📁 Upload Review CSVs</h2>
        <p style={styles.description}>
          Export reviews from App Store Connect and Google Play Console, then upload them here.
        </p>
      </div>

      <div style={styles.dropzoneContainer}>
        <div
          {...getAppStoreRootProps()}
          style={{
            ...styles.dropzone,
            ...(isAppStoreDragActive ? styles.dragActive : {}),
            ...(appStoreFile ? styles.fileSelected : {}),
          }}
        >
          <input {...getAppStoreInputProps()} />
          <div style={styles.dropzoneContent}>
            <div style={styles.iconWrapper}>
              <span style={styles.icon}>📱</span>
            </div>
            <p style={styles.dropzoneText}>
              {appStoreFile 
                ? `✅ ${appStoreFile.name}` 
                : 'Drop Apple App Store CSV here\nor click to browse'}
            </p>
            <p style={styles.dropzoneSubtext}>
              Format: Date, Rating, Title, Review
            </p>
          </div>
        </div>

        <div
          {...getPlayStoreRootProps()}
          style={{
            ...styles.dropzone,
            ...(isPlayStoreDragActive ? styles.dragActive : {}),
            ...(playStoreFile ? styles.fileSelected : {}),
          }}
        >
          <input {...getPlayStoreInputProps()} />
          <div style={styles.dropzoneContent}>
            <div style={styles.iconWrapper}>
              <span style={styles.icon}>🤖</span>
            </div>
            <p style={styles.dropzoneText}>
              {playStoreFile 
                ? `✅ ${playStoreFile.name}` 
                : 'Drop Google Play Store CSV here\nor click to browse'}
            </p>
            <p style={styles.dropzoneSubtext}>
              Format: Date, Star Rating, Title, Text
            </p>
          </div>
        </div>
      </div>

      {error && <div style={styles.errorBanner}>⚠️ {error}</div>}

      <button
        onClick={handleUpload}
        disabled={uploading || (!appStoreFile && !playStoreFile)}
        style={{
          ...styles.uploadButton,
          ...(uploading || (!appStoreFile && !playStoreFile) ? styles.buttonDisabled : {}),
        }}
      >
        {uploading ? (
          <>
            <span style={styles.spinner}></span>
            Uploading & Processing...
          </>
        ) : (
          <>
            🚀 Upload & Process Reviews
          </>
        )}
      </button>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    backgroundColor: 'rgba(255, 255, 255, 0.98)',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
    marginBottom: '20px',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255, 255, 255, 0.3)',
    animation: 'slideUp 0.6s ease-out',
  },
  headerSection: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  title: {
    margin: '0 0 15px 0',
    color: '#2d3748',
    fontSize: '28px',
    fontWeight: '700',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
  },
  description: {
    color: '#718096',
    fontSize: '15px',
    lineHeight: '1.6',
    maxWidth: '600px',
    margin: '0 auto',
  },
  dropzoneContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '25px',
    marginBottom: '30px',
  },
  dropzone: {
    border: '3px dashed #e2e8f0',
    borderRadius: '16px',
    padding: '40px 30px',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    backgroundColor: 'rgba(247, 250, 252, 0.5)',
    position: 'relative',
    overflow: 'hidden',
  },
  dragActive: {
    borderColor: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.08)',
    transform: 'scale(1.02)',
    boxShadow: '0 8px 20px rgba(76, 175, 80, 0.2)',
  },
  fileSelected: {
    borderColor: '#2196F3',
    backgroundColor: 'rgba(33, 150, 243, 0.08)',
    transform: 'scale(1.02)',
    boxShadow: '0 8px 20px rgba(33, 150, 243, 0.2)',
  },
  dropzoneContent: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '15px',
  },
  iconWrapper: {
    width: '80px',
    height: '80px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '10px',
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)',
    animation: 'bounce 2s infinite',
  },
  icon: {
    fontSize: '40px',
  },
  dropzoneText: {
    margin: 0,
    color: '#4a5568',
    fontSize: '16px',
    fontWeight: '600',
    lineHeight: '1.5',
    whiteSpace: 'pre-line',
  },
  dropzoneSubtext: {
    margin: '8px 0 0 0',
    color: '#a0aec0',
    fontSize: '13px',
    fontStyle: 'italic',
  },
  errorBanner: {
    backgroundColor: 'linear-gradient(135deg, #fee 0%, #fcc 100%)',
    color: '#c53030',
    padding: '16px 20px',
    borderRadius: '12px',
    fontSize: '15px',
    fontWeight: '600',
    marginBottom: '20px',
    border: '2px solid #feb2b2',
    boxShadow: '0 4px 12px rgba(244, 67, 54, 0.2)',
    animation: 'shake 0.5s ease-out',
  },
  uploadButton: {
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    padding: '16px 40px',
    borderRadius: '12px',
    fontSize: '17px',
    fontWeight: '700',
    cursor: 'pointer',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: '0 6px 16px rgba(76, 175, 80, 0.3)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    width: '100%',
    position: 'relative',
    overflow: 'hidden',
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
};

export default ReviewUploader;
