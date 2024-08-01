import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [userEmail, setUserEmail] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get('http://localhost:80/users/me', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        setUserEmail(response.data.email);
      } catch (error) {
        console.error('Error fetching user data:', error);
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 max-w-sm mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Welcome to Your Dashboard</h2>
      {userEmail && (
        <p className="text-gray-600 mb-4">Logged in as: <span className="font-semibold">{userEmail}</span></p>
      )}
      <button
        onClick={handleLogout}
        className="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Log Out
      </button>
    </div>
  );
};

export default Dashboard;