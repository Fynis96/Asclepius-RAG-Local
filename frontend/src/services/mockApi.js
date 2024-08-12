import { v4 as uuidv4 } from 'uuid';

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

let mockKnowledgebases = [
  { id: '1', name: 'Sample KB 1', description: 'Description 1', is_indexed: true },
  { id: '2', name: 'Sample KB 2', description: 'Description 2', is_indexed: false },
];

let mockDocuments = [
  { id: '1', knowledgebase_id: '1', filename: 'doc1.pdf', file_type: 'pdf' },
  { id: '2', knowledgebase_id: '1', filename: 'doc2.txt', file_type: 'txt' },
];

let mockUser = { id: '1', email: 'user@example.com' };

export const login = async (email, password) => {
  await delay(500);
  if (email === 'user@example.com' && password === 'password') {
    return { data: { access_token: 'mock_token', refresh_token: 'mock_refresh_token' } };
  }
  throw new Error('Invalid credentials');
};

export const refreshToken = async (refresh_token) => {
  await delay(500);
  return { data: { access_token: 'new_mock_token', refresh_token: 'new_mock_refresh_token' } };
};

export const logout = async () => {
  await delay(500);
  return { data: { message: 'Logged out successfully' } };
};

export const register = async (email, password) => {
  await delay(500);
  mockUser = { id: uuidv4(), email };
  return { data: mockUser };
};

export const getCurrentUser = async () => {
  await delay(500);
  return { data: mockUser };
};

export const getKnowledgebases = async () => {
  await delay(500);
  return { data: mockKnowledgebases };
};

export const createKnowledgebase = async (name, description) => {
  await delay(500);
  const newKb = { id: uuidv4(), name, description, is_indexed: false };
  mockKnowledgebases.push(newKb);
  return { data: newKb };
};

export const getKnowledgebase = async (id) => {
  await delay(500);
  const kb = mockKnowledgebases.find(kb => kb.id === id);
  if (!kb) throw new Error('Knowledgebase not found');
  return { data: kb };
};

export const updateKnowledgebase = async (id, name, description) => {
  await delay(500);
  const index = mockKnowledgebases.findIndex(kb => kb.id === id);
  if (index === -1) throw new Error('Knowledgebase not found');
  mockKnowledgebases[index] = { ...mockKnowledgebases[index], name, description };
  return { data: mockKnowledgebases[index] };
};

export const deleteKnowledgebase = async (id) => {
  await delay(500);
  mockKnowledgebases = mockKnowledgebases.filter(kb => kb.id !== id);
  return { data: { message: 'Knowledgebase deleted successfully' } };
};

export const createDocument = async (knowledgebaseId, file) => {
  await delay(500);
  const newDoc = { id: uuidv4(), knowledgebase_id: knowledgebaseId, filename: file.name, file_type: file.name.split('.').pop() };
  mockDocuments.push(newDoc);
  return { data: newDoc };
};

export const getDocuments = async (knowledgebaseId) => {
  await delay(500);
  return { data: mockDocuments.filter(doc => doc.knowledgebase_id === knowledgebaseId) };
};

export const deleteDocument = async (knowledgebaseId, documentId) => {
  await delay(500);
  mockDocuments = mockDocuments.filter(doc => doc.id !== documentId);
  return { data: { message: 'Document deleted successfully' } };
};

export const runKnowledgebaseIndexing = async (knowledgebaseId) => {
  await delay(1000);
  const index = mockKnowledgebases.findIndex(kb => kb.id === knowledgebaseId);
  if (index === -1) throw new Error('Knowledgebase not found');
  mockKnowledgebases[index].is_indexed = true;
  return { data: { message: 'Indexing completed successfully' } };
};