import apiClient from './client';

// タイムライン取得
export const getTimeline = () => {
  return apiClient.get('/timeline/');
};

// 探索（公開タスク）取得
export const explorePublicTasks = () => {
  return apiClient.get('/timeline/explore');
};