import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getKnowledgebase, getDocuments, createDocument, deleteDocument, runKnowledgebaseIndexing } from '../services/api';
import { useNavigate } from 'react-router-dom';

const KnowledgebaseDetail = () => {
  const { id } = useParams();
  const [knowledgebase, setKnowledgebase] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchKnowledgebase();
    fetchDocuments();
  }, [id]);

  const fetchKnowledgebase = async () => {
    try {
      const response = await getKnowledgebase(id);
      setKnowledgebase(response.data);
    } catch (error) {
      console.error('Error fetching knowledgebase:', error);
      setError('Failed to fetch knowledgebase. Please try again.');
    }
  };

  const fetchDocuments = async () => {
    try {
      const response = await getDocuments(id);
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
      setError('Failed to fetch documents. Please try again.');
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;

    try {
      await createDocument(id, file);
      setFile(null);
      fetchDocuments();
    } catch (error) {
      console.error('Error uploading document:', error);
      setError('Failed to upload document. Please try again.');
    }
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await deleteDocument(id, documentId);
      fetchDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
      setError('Failed to delete document. Please try again.');
    }
  };

  const handleRunIndexing = async () => {
    try {
      const response = await runKnowledgebaseIndexing(id);
      alert(response.data.message);
    } catch (error) {
      console.error('Error starting indexing process:', error);
      setError('Failed to start indexing process. Please try again.');
    }
  };

  if (!knowledgebase) return <div className="text-center mt-8">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">{knowledgebase.name}</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <p className="text-gray-600 mb-6">{knowledgebase.description}</p>

      <div className="flex justify-between items-center mb-8">
        <form onSubmit={handleUpload} className="flex-grow mr-4">
          <input
            type="file"
            onChange={handleFileChange}
            className="mb-2"
            required
          />
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Upload Document
          </button>
        </form>
        <button
          onClick={handleRunIndexing}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        >
          Run Indexing
        </button>
      </div>

      <h2 className="text-2xl font-bold mb-4">Documents</h2>
      <ul>
        {documents.map((doc) => (
          <li key={doc.id} className="mb-4 p-4 border rounded">
            <span className="text-xl">{doc.filename}</span>
            <p className="text-gray-600">Type: {doc.file_type}</p>
            <button
              onClick={() => handleDeleteDocument(doc.id)}
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

export default KnowledgebaseDetail;
