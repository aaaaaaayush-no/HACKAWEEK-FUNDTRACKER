import api from './axios';

export const loginUser = async (username, password) => {
  const response = await api.post('/auth/login/', { username, password });
  return response.data;
};

export const registerUser = async (data) => {
  const response = await api.post('/auth/register/', data);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/profile/');
  return response.data;
};
