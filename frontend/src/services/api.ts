import axios from 'axios';

// API Base URL - Use local for development, Railway for production
const API_BASE_URL = (import.meta as any).env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Review {
  id: string;
  source: string;
  rating: number;
  title: string;
  text: string;
  date: string;
}

export interface ThemeAnalysis {
  theme_name: string;
  review_count: number;
  percentage: number;
  sentiment: 'positive' | 'negative' | 'neutral';
  quotes: string[];
  action_ideas: string[];
}

export interface WeeklyReport {
  id: string;
  week_start: string;
  week_end: string;
  total_reviews: number;
  top_themes: ThemeAnalysis[];
  generated_at: string;
  word_count: number;
}

export const reviewsAPI = {
  upload: async (appStoreFile?: File, playStoreFile?: File) => {
    const formData = new FormData();
    if (appStoreFile) formData.append('app_store_file', appStoreFile);
    if (playStoreFile) formData.append('play_store_file', playStoreFile);

    const response = await api.post('/api/reviews/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  getReviews: (limit: number = 100, source?: string) => {
    const params = { limit, source };
    return api.get<Review[]>('/api/reviews/', { params });
  },

  getStats: () => {
    return api.get('/api/reviews/stats');
  },

  deleteReviews: () => {
    return api.delete('/api/reviews/');
  },

  fetchPlayStoreReviews: async (params?: {
    weeks?: number;
    max_reviews?: number;
    demo_mode?: boolean;
  }) => {
    // Use fast endpoint for demo mode (instant loading)
    if (params?.demo_mode) {
      const response = await api.post('/api/reviews/fetch-play-store-fast');
      return response.data;
    }
    
    // Use real scraper for production
    const response = await api.post('/api/reviews/fetch-play-store', params);
    return response.data;
  },

  getSettings: () => {
    return api.get('/api/reviews/settings');
  },

  updateSettings: (settings: any) => {
    return api.post('/api/reviews/settings', settings);
  },
};

export const analysisAPI = {
  generateWeeklyReport: () => {
    return api.post<WeeklyReport>('/api/analysis/generate-weekly-report');
  },

  getThemes: () => {
    return api.get('/api/analysis/themes');
  },
};

export const reportsAPI = {
  getLatest: () => {
    return api.get<WeeklyReport>('/api/reports/latest');
  },

  getAll: () => {
    return api.get<WeeklyReport[]>('/api/reports/');
  },

  generateSummary: (reportId?: string) => {
    return api.post('/api/reports/generate-summary', null, { 
      params: { report_id: reportId } 
    });
  },
};

export const emailAPI = {
  sendDraft: (reportId?: string, recipientEmail?: string, customSubject?: string) => {
    return api.post('/api/email/send-draft', null, {
      params: { report_id: reportId, recipient_email: recipientEmail, custom_subject: customSubject }
    });
  },

  testConnection: () => {
    return api.post('/api/email/test-connection');
  },
};

export default api;
