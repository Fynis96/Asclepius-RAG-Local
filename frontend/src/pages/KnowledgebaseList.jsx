import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getKnowledgebases, createKnowledgebase, deleteKnowledgebase } from '../services/api';

const KnowledgebaseList = () => {
  const [knowledgebases, setKnowledgebases] = useState([]);
  const [newKnowledgebaseName, setNewKnowledgebaseName] = useState('');
  const [newKnowledgebaseDescription, setNewKnowledgebaseDescription] = useState('');

  useEffect(() => {
    fetchKnowledgebases();
  }, []);

  const fetchKnowledgebases = async () => {
    try {
      const response = await getKnowledgebases();
      setKnowledgebases(response.data);
    } catch (error) {
      console.error('Error fetching knowledgebases:', error);
    }
  };

  const handleCreateKnowledgebase = async (e) => {
    e.preventDefault();
    try {
      await createKnowledgebase(newKnowledgebaseName, newKnowledgebaseDescription);
      setNewKnowledgebaseName('');
      setNewKnowledgebaseDescription('');
      fetchKnowledgebases();
    } catch (error) {
      console.error('Error creating knowledgebase:', error);
    }
  };

  const handleDeleteKnowledgebase = async (id) => {
    try {
      await deleteKnowledgebase(id);
      fetchKnowledgebases();
    } catch (error) {
      console.error('Error deleting knowledgebase:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Knowledgebases</h1>
      
      <form onSubmit={handleCreateKnowledgebase} className="mb-8">
        <input
          type="text"
          value={newKnowledgebaseName}
          onChange={(e) => setNewKnowledgebaseName(e.target.value)}
          placeholder="Knowledgebase Name"
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <textarea
          value={newKnowledgebaseDescription}
          onChange={(e) => setNewKnowledgebaseDescription(e.target.value)}
          placeholder="Description"
          className="w-full p-2 mb-2 border rounded"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Create Knowledgebase
        </button>
      </form>

      <ul>
        {knowledgebases.map((kb) => (
          <li key={kb.id} className="mb-4 p-4 border rounded">
            <Link to={`/knowledgebases/${kb.id}`} className="text-xl font-semibold text-blue-600 hover:underline">
              {kb.name}
            </Link>
            <p className="text-gray-600">{kb.description}</p>
            <button
              onClick={() => handleDeleteKnowledgebase(kb.id)}
              className="mt-2 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default KnowledgebaseList;