import apiClient from './client';

// タスク一覧取得
export const getTasks = () => {
  return apiClient.get('/tasks/');
};

// タスク作成
export const createTask = (taskData) => {
  return apiClient.post('/tasks/', taskData);
};

// タスク更新
export const updateTask = (taskId, taskData) => {
  return apiClient.put(`/tasks/${taskId}`, taskData);
};

// タスク削除
export const deleteTask = (taskId) => {
  return apiClient.delete(`/tasks/${taskId}`);
};