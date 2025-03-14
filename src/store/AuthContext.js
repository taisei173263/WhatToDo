import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getCurrentUser, login as apiLogin, register as apiRegister, logout as apiLogout } from '../api/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 起動時に認証状態を確認
  useEffect(() => {
    const loadUser = async () => {
      try {
        const token = await AsyncStorage.getItem('token');
        if (token) {
          const response = await getCurrentUser();
          setUser(response.data);
        }
      } catch (err) {
        console.error('Loading user failed:', err);
        await AsyncStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  // ログイン処理
  const login = async (usernameOrEmail, password) => {
    setLoading(true);
    setError(null);
    try {
      await apiLogin(usernameOrEmail, password);
      const response = await getCurrentUser();
      setUser(response.data);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'ログインに失敗しました');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // 登録処理
  const register = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      await apiRegister(userData);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || '登録に失敗しました');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // ログアウト処理
  const logout = async () => {
    setLoading(true);
    try {
      await apiLogout();
      setUser(null);
    } catch (err) {
      console.error('Logout failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// カスタムフック
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};