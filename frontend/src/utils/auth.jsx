import { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, refreshToken, logout as apiLogout, getCurrentUser } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const refreshTokenValue = localStorage.getItem('refreshToken');
    if (token && refreshTokenValue) {
      fetchUser();
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await getCurrentUser();
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error fetching user:', error.response?.data || error.message);
      await refreshTokenAndRetry();
    }
  };

  const refreshTokenAndRetry = async () => {
    try {
      const refreshTokenValue = localStorage.getItem('refreshToken');
      const response = await refreshToken(refreshTokenValue);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      await fetchUser();
    } catch (error) {
      console.error('Error refreshing token:', error);
      logout();
    }
  };

  const login = async (email, password) => {
    try {
      const response = await apiLogin(email, password);
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);
      await fetchUser();
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiLogout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      setUser(null);
      setIsAuthenticated(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
