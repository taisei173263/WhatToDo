import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// バックエンドのURLを設定
const API_URL = 'http://localhost:8000'; // 開発環境用
// const API_URL = 'https://your-production-api.com'; // 本番環境用

const apiClient = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// トークンを自動的にリクエストに付与
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;