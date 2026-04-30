const API_BASE_URL = 'http://localhost:8000/api';
const API_KEY = 'aura_secret_key_123'; // Matches the backend default for demo

const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-API-Key': API_KEY,
});

export const createContext = async (contextData) => {
  const response = await fetch(`${API_BASE_URL}/context`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(contextData),
  });
  if (!response.ok) throw new Error('Failed to create context');
  return response.json();
};

export const sendMessage = async (conversationId, message) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify({ conversation_id: conversationId, message }),
  });
  if (!response.ok) throw new Error('Failed to send message');
  return response.json();
};

export const getConversation = async (conversationId) => {
  const response = await fetch(`${API_BASE_URL}/conversation/${conversationId}`, {
    headers: getHeaders(),
  });
  if (!response.ok) throw new Error('Failed to fetch conversation');
  return response.json();
};
