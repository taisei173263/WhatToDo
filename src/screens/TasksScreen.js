import React, { useState, useEffect } from 'react';
import { View, FlatList, StyleSheet, TouchableOpacity, Text, Alert } from 'react-native';
import { Card, Button, Icon, CheckBox, FAB } from 'react-native-elements';
import { getTasks, updateTask, deleteTask } from '../api/tasks';

const TasksScreen = ({ navigation }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // タスク一覧を取得
  const fetchTasks = async () => {
    setLoading(true);
    try {
      const response = await getTasks();
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      Alert.alert('エラー', 'タスクの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchTasks();
    
    // 画面がフォーカスされるたびにタスクを再取得
    const unsubscribe = navigation.addListener('focus', () => {
      fetchTasks();
    });
    
    return unsubscribe;
  }, [navigation]);
  
  // タスク完了状態のトグル
  const toggleTaskCompletion = async (task) => {
    try {
      await updateTask(task.id, { is_completed: !task.is_completed });
      // 更新後のタスク一覧を再取得
      fetchTasks();
    } catch (error) {
      console.error('Error updating task:', error);
      Alert.alert('エラー', 'タスクの更新に失敗しました');
    }
  };
  
  // タスク削除
  const handleDeleteTask = (taskId) => {
    Alert.alert(
      '確認',
      'このタスクを削除しますか？',
      [
        { text: 'キャンセル', style: 'cancel' },
        {
          text: '削除',
          style: 'destructive',
          onPress: async () => {
            try {
              await deleteTask(taskId);
              // 更新後のタスク一覧を再取得
              fetchTasks();
            } catch (error) {
              console.error('Error deleting task:', error);
              Alert.alert('エラー', 'タスクの削除に失敗しました');
            }
          },
        },
      ]
    );
  };
  
  // タスク詳細画面へ遷移
  const navigateToTaskDetail = (task) => {
    navigation.navigate('TaskDetail', { task });
  };
  
  // タスク作成画面へ遷移
  const navigateToCreateTask = () => {
    navigation.navigate('CreateTask');
  };
  
  const renderItem = ({ item }) => (
    <Card>
      <TouchableOpacity onPress={() => navigateToTaskDetail(item)}>
        <Card.Title>{item.title}</Card.Title>
      </TouchableOpacity>
      <Card.Divider />
      
      {item.description && <Text style={styles.description}>{item.description}</Text>}
      
      <View style={styles.taskActions}>
        <CheckBox
          checked={item.is_completed}
          onPress={() => toggleTaskCompletion(item)}
          uncheckedColor="#ddd"
          checkedColor="#2089dc"
        />
        
        <View style={styles.actionButtons}>
          <Button
            icon={<Icon name="edit" type="material" size={20} />}
            type="clear"
            onPress={() => navigateToTaskDetail(item)}
          />
          <Button
            icon={<Icon name="delete" type="material" size={20} color="red" />}
            type="clear"
            onPress={() => handleDeleteTask(item.id)}
          />
        </View>
      </View>
    </Card>
  );
  
  return (
    <View style={styles.container}>
      <FlatList
        data={tasks}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        refreshing={loading}
        onRefresh={fetchTasks}
      />
      
      <FAB
        visible={true}
        icon={{ name: 'add', color: 'white' }}
        color="#2089dc"
        placement="right"
        onPress={navigateToCreateTask}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  description: {
    marginBottom: 10,
  },
  taskActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  actionButtons: {
    flexDirection: 'row',
  },
});

export default TasksScreen;