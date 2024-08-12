import * as realApi from './realApi';
import * as mockApi from './mockApi';

// const api = import.meta.env.VITE_USE_MOCK_API === 'true' ? mockApi : realApi;
const api = mockApi;

export const {
  login,
  refreshToken,
  logout,
  register,
  getCurrentUser,
  getKnowledgebases,
  createKnowledgebase,
  getKnowledgebase,
  updateKnowledgebase,
  deleteKnowledgebase,
  createDocument,
  getDocuments,
  deleteDocument,
  runKnowledgebaseIndexing
} = api;

export default api;