export type TaskStatus = 'todo' | 'in_progress' | 'done' | 'blocked'

export interface Task {
  id: string
  title: string
  description: string | null
  status: TaskStatus
  due_date: string | null
  retrospective_id: string | null
}

export interface TaskCreatePayload {
  title: string
  description?: string | null
  due_date?: string | null
}

export interface TaskUpdatePayload {
  title?: string
  description?: string | null
  status?: TaskStatus
  due_date?: string | null
}

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  todo: '할 일',
  in_progress: '진행중',
  done: '완료',
  blocked: '차단됨',
}

export const TASK_STATUS_ORDER: TaskStatus[] = ['todo', 'in_progress', 'done', 'blocked']


