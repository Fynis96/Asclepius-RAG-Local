import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getKnowledgebase, getDocuments, createDocument, deleteDocument } from '../services/api';

const KnowledgebaseDetail = () => {
  const { id } = useParams();
  const [knowledgebase, setKnowledgebase] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);

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
    }
  };

  const fetchDocuments = async () => {
    try {
      const response = await getDocuments(id);
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
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
    }
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await deleteDocument(id, documentId);
      fetchDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  if (!knowledgebase) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">{knowledgebase.name}</h1>
      <p className="text-gray-600 mb-6">{knowledgebase.description}</p>

      <form onSubmit={handleUpload} className="mb-8">
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