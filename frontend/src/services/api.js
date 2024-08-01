import axios from 'axios';

const API_URL = 'http://localhost:80';

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

export const login = (email, password) => 
  api.post('/token', new URLSearchParams({ username: email, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });

export const register = (email, password) => 
  api.post('/register', { email, password });

export const getCurrentUser = () => 
  api.get('/users/me');

export default api;