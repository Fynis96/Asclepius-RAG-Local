import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../utils/auth';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="bg-white shadow rounded-lg p-6 max-w-sm mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Welcome to Your Dashboard</h2>
      {user && (
        <p className="text-gray-600 mb-4">Logged in as: <span className="font-semibold">{user.email}</span></p>
      )}
      <Link
        to="/knowledgebases"
        className="block w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline text-center mb-4"
      >
        View Knowledgebases
      </Link>
    </div>
  );
};

export default Dashboard;