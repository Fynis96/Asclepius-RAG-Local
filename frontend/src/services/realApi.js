import axios from 'axios';

const API_URL = 'http://localhost:80/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response) {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        try {
          const refreshTokenValue = localStorage.getItem('refreshToken');
          const response = await refreshToken(refreshTokenValue);
          localStorage.setItem('token', response.data.access_token);
          localStorage.setItem('refreshToken', response.data.refresh_token);
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Handle refresh token failure (e.g., logout user)
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login'; // Redirect to login page
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

export const login = (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);
  
  return api.post('/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
};

export const refreshToken = (refresh_token) =>
  api.post('/refresh', { refresh_token });

export const logout = () =>
  api.post('/logout');


export const register = (email, password) => 
  api.post('/users/', { email, password });

export const getCurrentUser = () => 
  api.get('/users/me');

// Knowledgebases
export const createKnowledgebase = (name, description) => 
  api.post('/knowledgebases/', { name, description });

export const getKnowledgebases = () => 
  api.get('/knowledgebases/');

export const getKnowledgebase = (id) => 
  api.get(`/knowledgebases/${id}`);

export const updateKnowledgebase = (id, name, description) => 
  api.put(`/knowledgebases/${id}`, { name, description });

export const deleteKnowledgebase = (id) => 
  api.delete(`/knowledgebases/${id}`);

// Documents
export const createDocument = (knowledgebaseId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post(`/knowledgebases/${knowledgebaseId}/documents/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const getDocuments = (knowledgebaseId) => 
  api.get(`/knowledgebases/${knowledgebaseId}/documents/`);

export const deleteDocument = (knowledgebaseId, documentId) => 
  api.delete(`/knowledgebases/${knowledgebaseId}/documents/${documentId}`);

// Index documents in a knowledgebase
export const runKnowledgebaseIndexing = (knowledgebaseId) =>
  api.post(`/index/run/${knowledgebaseId}`);

export default api;
