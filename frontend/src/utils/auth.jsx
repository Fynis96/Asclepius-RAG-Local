import { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, getCurrentUser } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
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
      logout();
    }
  };

  const login = async (email, password) => {
    try {
      console.log('Attempting login');
      const response = await apiLogin(email, password);
      console.log('Login response:', response);
      localStorage.setItem('token', response.data.access_token);
      await fetchUser();
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);