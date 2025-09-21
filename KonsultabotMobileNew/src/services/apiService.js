import axios from 'axios';
import Constants from 'expo-constants';

// Dynamic API URL configuration for web and mobile
const getApiUrl = () => {
  // Check if running in web browser
  if (typeof window !== 'undefined') {
    return 'http://localhost:8000/api';
  }
  
  // For mobile, use the configured URL or fallback
  return Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000/api';
};

const API_BASE_URL = getApiUrl();

console.log('API Base URL:', API_BASE_URL);

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for auth token
    this.api.interceptors.request.use(
      (config) => {
        if (this.authToken) {
          config.headers.Authorization = `Token ${this.authToken}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => {
        console.log('API Response:', response.status, response.config.url);
        return response;
      },
      (error) => {
        console.error('API Error:', {
          url: error.config?.url,
          method: error.config?.method,
          status: error.response?.status,
          message: error.message,
          data: error.response?.data
        });
        
        if (error.response?.status === 401) {
          // Handle unauthorized access
          this.authToken = null;
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token) {
    this.authToken = token;
  }

  // Auth endpoints
  async login(email, password) {
    return this.api.post('/users/login/', { email, password });
  }

  async register(userData) {
    return this.api.post('/users/register/', userData);
  }

  async logout() {
    return this.api.post('/users/logout/');
  }

  async getProfile() {
    return this.api.get('/users/profile/');
  }

  async updateProfile(profileData) {
    return this.api.put('/users/profile/update/', profileData);
  }

  // Chat endpoints
  async sendMessage(message, language = 'english', sessionId = null) {
    const payload = {
      message,
      language,
    };
    
    // Only include session_id if it's not null
    if (sessionId) {
      payload.session_id = sessionId;
    }
    
    return this.api.post('/chat/send/', payload);
  }

  async getConversationHistory() {
    return this.api.get('/chat/history/');
  }

  async getChatSessions() {
    return this.api.get('/chat/sessions/');
  }

  async endChatSession(sessionId) {
    return this.api.post('/chat/sessions/end/', { session_id: sessionId });
  }

  async getKnowledgeBase(language = 'english', category = null) {
    const params = { language };
    if (category) params.category = category;
    return this.api.get('/chat/knowledge/', { params });
  }

  async getCampusInfo(language = 'english', category = null) {
    const params = { language };
    if (category) params.category = category;
    return this.api.get('/chat/campus-info/', { params });
  }

  async searchKnowledge(query, language = 'english') {
    return this.api.get('/chat/search/', {
      params: { q: query, language },
    });
  }

  // General endpoints
  async healthCheck() {
    return this.api.get('/health/');
  }

  async getApiStatus() {
    return this.api.get('/status/');
  }
}

export const apiService = new ApiService();
