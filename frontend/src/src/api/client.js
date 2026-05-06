import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000' });

export const uploadPDF = (file) => {
  const form = new FormData();
  form.append('file', file);
  return API.post('/upload/pdf', form);
};

export const uploadAudio = (file) => {
  const form = new FormData();
  form.append('file', file);
  return API.post('/upload/audio', form);
};

export const askQuestion = (doc_id, question) =>
  API.post('/chat/ask', { doc_id, question });

export const getDocuments = () => API.get('/upload/documents');

export const getSummary = (doc_id) => API.get(`/chat/summary/${doc_id}`);