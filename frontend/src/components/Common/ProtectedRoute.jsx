import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../utils/auth';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;