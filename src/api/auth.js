import apiClient from './client';
import AsyncStorage from '@react-native-async-storage/async-storage';

// ログインAPI
export const login = async (usernameOrEmail, password) => {
  const formData = new FormData();
  formData.append('username', usernameOrEmail);
  formData.append('password', password);
  
  const response = await apiClient.post('/login/access-token', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  const { access_token } = response.data;
  await AsyncStorage.setItem('token', access_token);
  
  return access_token;
};

// ユーザー登録API
export const register = async (userData) => {
  return apiClient.post('/users/', userData);
};

// ログアウト処理
export const logout = async () => {
  await AsyncStorage.removeItem('token');
};

// 現在のユーザー情報取得
export const getCurrentUser = async () => {
  return apiClient.get('/users/me');
};