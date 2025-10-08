import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import apiClient from './client'
import type { Task, TaskCreatePayload, TaskUpdatePayload } from '@/types/task'

const TASKS_QUERY_KEY = ['tasks']

async function fetchTasks(status?: string): Promise<Task[]> {
  const response = await apiClient.get<Task[]>('/tasks', {
    params: {
      status_filter: status,
    },
  })
  return response.data
}

async function createTask(payload: TaskCreatePayload): Promise<Task> {
  const response = await apiClient.post<Task>('/tasks', payload)
  return response.data
}

async function updateTask({ id, payload }: { id: string; payload: TaskUpdatePayload }): Promise<Task> {
  const response = await apiClient.patch<Task>(`/tasks/${id}`, payload)
  return response.data
}

async function deleteTask(id: string): Promise<void> {
  await apiClient.delete(`/tasks/${id}`)
}

export function useTasks(status?: string) {
  return useQuery({
    queryKey: [...TASKS_QUERY_KEY, status],
    queryFn: () => fetchTasks(status),
    staleTime: 1000 * 30,
  })
}

export function useCreateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: TASKS_QUERY_KEY })
    },
  })
}

export function useUpdateTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: updateTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: TASKS_QUERY_KEY })
    },
  })
}

export function useDeleteTask() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: TASKS_QUERY_KEY })
    },
  })
}


