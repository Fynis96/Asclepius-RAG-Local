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

// Auth
export const login = (email, password) => 
  api.post('/login', new URLSearchParams({ username: email, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });

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

export default api;