/**
 * API service with error handling and response formatting
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      const errorMessage = error.response.data?.detail || error.response.data?.message || 'An error occurred';
      throw new Error(errorMessage);
    } else if (error.request) {
      throw new Error('No response from server. Please check your connection.');
    } else {
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

/**
 * API service methods
 */
export const api = {
  // Health check
  healthCheck: async () => {
    return apiClient.get('/health');
  },

  // Articles
  getArticles: async (params = {}) => {
    return apiClient.get('/articles', { params });
  },

  getArticle: async (articleId) => {
    return apiClient.get(`/articles/${articleId}`);
  },

  getArticleSummary: async (articleId) => {
    return apiClient.get(`/articles/${articleId}/summary`);
  },

  // Clusters
  getClusters: async () => {
    return apiClient.get('/clusters');
  },

  getClusterArticles: async (clusterId, params = {}) => {
    return apiClient.get(`/clusters/${clusterId}/articles`, { params });
  },

  // Admin
  triggerFetch: async (count = 20) => {
    return apiClient.post('/articles/fetch', null, { params: { count } });
  },

  // Stats
  getStats: async () => {
    return apiClient.get('/stats');
  },
};

export default api;
