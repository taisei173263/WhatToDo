import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Icon } from 'react-native-elements';

// 認証画面
import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';

// メイン画面
import TasksScreen from '../screens/TasksScreen';
import TaskDetailScreen from '../screens/TaskDetailScreen';
import CreateTaskScreen from '../screens/CreateTaskScreen';
import TimelineScreen from '../screens/TimelineScreen';
import ProfileScreen from '../screens/ProfileScreen';
import StatsScreen from '../screens/StatsScreen';

import { useAuth } from '../store/AuthContext';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();
const TaskStack = createStackNavigator();

// タスク関連の画面スタック
const TasksStackNavigator = () => {
  return (
    <TaskStack.Navigator>
      <TaskStack.Screen name="TasksList" component={TasksScreen} options={{ title: 'マイタスク' }} />
      <TaskStack.Screen name="TaskDetail" component={TaskDetailScreen} options={{ title: 'タスク詳細' }} />
      <TaskStack.Screen name="CreateTask" component={CreateTaskScreen} options={{ title: 'タスク作成' }} />
    </TaskStack.Navigator>
  );
};

// メインのタブナビゲーター
const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#2089dc',
        tabBarInactiveTintColor: 'gray',
      }}
    >
      <Tab.Screen
        name="Tasks"
        component={TasksStackNavigator}
        options={{
          tabBarLabel: 'タスク',
          headerShown: false,
          tabBarIcon: ({ color }) => (
            <Icon name="check-box" type="material" color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Timeline"
        component={TimelineScreen}
        options={{
          tabBarLabel: 'タイムライン',
          tabBarIcon: ({ color }) => (
            <Icon name="timeline" type="material" color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Stats"
        component={StatsScreen}
        options={{
          tabBarLabel: '統計',
          tabBarIcon: ({ color }) => (
            <Icon name="bar-chart" type="material" color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarLabel: 'プロフィール',
          tabBarIcon: ({ color }) => (
            <Icon name="person" type="material" color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

// メインのアプリナビゲーター
const AppNavigator = () => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return null; // またはローディングインジケーターを表示
  }
  
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          <Stack.Screen name="Main" component={MainTabNavigator} />
        ) : (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;