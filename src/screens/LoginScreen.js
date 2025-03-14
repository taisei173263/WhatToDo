import React, { useState } from 'react';
import { View, StyleSheet, Text, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Input, Button } from 'react-native-elements';
import { useAuth } from '../store/AuthContext';

const LoginScreen = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();

  const handleLogin = async () => {
    if (!username || !password) {
      alert('ユーザー名とパスワードを入力してください');
      return;
    }
    
    const success = await login(username, password);
    if (success) {
      // ログイン成功の処理はAuthContextで処理されるため不要
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>WhatToDo</Text>
      <Text style={styles.subtitle}>ログイン</Text>
      
      <Input
        placeholder="ユーザー名またはメールアドレス"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      
      <Input
        placeholder="パスワード"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      
      {error && <Text style={styles.errorText}>{error}</Text>}
      
      <Button
        title="ログイン"
        onPress={handleLogin}
        containerStyle={styles.buttonContainer}
        disabled={loading}
      />
      
      {loading && <ActivityIndicator size="large" color="#0000ff" />}
      
      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={styles.registerText}>アカウントをお持ちでない方は登録</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 30,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 30,
    color: '#555',
  },
  buttonContainer: {
    marginTop: 20,
    marginBottom: 20,
  },
  errorText: {
    color: 'red',
    textAlign: 'center',
    marginBottom: 10,
  },
  registerText: {
    textAlign: 'center',
    color: 'blue',
    marginTop: 20,
  },
});

export default LoginScreen;