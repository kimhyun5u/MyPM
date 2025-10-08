import { type FormEvent, useMemo, useState } from 'react'
import dayjs from 'dayjs'
import {
  useCreateTask,
  useDeleteTask,
  useTasks,
  useUpdateTask,
} from '@/services/tasks'
import { useAttachTask, useRetrospective } from '@/services/retrospectives'
import type { Task, TaskCreatePayload, TaskStatus } from '@/types/task'
import { TASK_STATUS_LABELS, TASK_STATUS_ORDER } from '@/types/task'
import '@/components/task/TaskBoard.css'

interface TaskBoardProps {
  statusFilter?: string
  retroDate: string
}

interface TaskFormState {
  title: string
  description: string
  dueDate: string
}

const INITIAL_FORM_STATE: TaskFormState = {
  title: '',
  description: '',
  dueDate: '',
}

function normalizePayload({ title, description, dueDate }: TaskFormState): TaskCreatePayload {
  return {
    title,
    description: description.trim() ? description.trim() : null,
    due_date: dueDate ? dueDate : null,
  }
}

function TaskBoard({ statusFilter, retroDate }: TaskBoardProps) {
  const [isFormOpen, setIsFormOpen] = useState(false)
  const [form, setForm] = useState<TaskFormState>(INITIAL_FORM_STATE)

  const { data: tasks = [], isLoading, isError } = useTasks(statusFilter)
  const createMutation = useCreateTask()
  const updateMutation = useUpdateTask()
  const deleteMutation = useDeleteTask()

  const { data: retrospective } = useRetrospective(retroDate)
  const attachMutation = useAttachTask(retroDate)

  const groupedTasks = useMemo(() => {
    return tasks.reduce<Record<TaskStatus, Task[]>>(
      (accumulator, task) => {
        accumulator[task.status].push(task)
        return accumulator
      },
      {
        todo: [],
        in_progress: [],
        done: [],
        blocked: [],
      },
    )
  }, [tasks])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!form.title.trim()) {
      return
    }

    createMutation.mutate(normalizePayload(form), {
      onSuccess: () => {
        setForm(INITIAL_FORM_STATE)
        setIsFormOpen(false)
      },
    })
  }

  const handleStatusChange = (task: Task, nextStatus: TaskStatus) => {
    updateMutation.mutate({
      id: task.id,
      payload: {
        status: nextStatus,
      },
    })
  }

  const handleAttachTask = (taskId: string) => {
    if (!retrospective) {
      return
    }
    attachMutation.mutate({ retrospectiveId: retrospective.id, taskId })
  }

  const handleDeleteTask = (taskId: string) => {
    if (window.confirm('정말로 이 할 일을 삭제할까요?')) {
      deleteMutation.mutate(taskId)
    }
  }

  return (
    <section className="task-board">
      <header className="task-board__header">
        <div>
          <h2>할 일 목록</h2>
          <p className="task-board__meta">
            총 {tasks.length}개 작업 · 회고 날짜 {retroDate}
          </p>
        </div>
        <button type="button" className="button primary" onClick={() => setIsFormOpen((prev) => !prev)}>
          {isFormOpen ? '작성 취소' : '새 할 일' }
        </button>
      </header>

      {isFormOpen && (
        <form className="task-form" onSubmit={handleSubmit}>
          <div className="task-form__row">
            <label htmlFor="task-title">제목</label>
            <input
              id="task-title"
              type="text"
              value={form.title}
              onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
              placeholder="할 일을 입력하세요"
              required
            />
          </div>

          <div className="task-form__row">
            <label htmlFor="task-description">설명</label>
            <textarea
              id="task-description"
              value={form.description}
              onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
              rows={3}
              placeholder="선택 입력"
            />
          </div>

          <div className="task-form__row task-form__row--inline">
            <div>
              <label htmlFor="task-due-date">마감일</label>
              <input
                id="task-due-date"
                type="date"
                value={form.dueDate}
                onChange={(event) => setForm((prev) => ({ ...prev, dueDate: event.target.value }))}
              />
            </div>

            <button
              type="submit"
              className="button primary"
              disabled={createMutation.isPending}
            >
              {createMutation.isPending ? '저장 중...' : '저장'}
            </button>
          </div>
        </form>
      )}

      {isLoading && <p className="task-board__state">불러오는 중...</p>}
      {isError && <p className="task-board__state error">작업 목록을 불러오지 못했습니다.</p>}
      {!isLoading && !isError && tasks.length === 0 && (
        <p className="task-board__state">등록된 할 일이 없습니다. 새로 추가해보세요.</p>
      )}

      {!isLoading && !isError && tasks.length > 0 && (
        <div className="task-columns">
          {TASK_STATUS_ORDER.filter((status) => !statusFilter || status === statusFilter).map((status) => (
            <section key={status} className="task-column">
              <header className="task-column__header">
                <h3>{TASK_STATUS_LABELS[status]}</h3>
                <span>{groupedTasks?.[status]?.length ?? 0}</span>
              </header>

              <div className="task-column__list">
                {(groupedTasks?.[status] ?? []).map((task) => (
                  <article key={task.id} className="task-card">
                    <header className="task-card__header">
                      <h4>{task.title}</h4>
                      <select
                        value={task.status}
                        onChange={(event) => handleStatusChange(task, event.target.value as TaskStatus)}
                      >
                        {TASK_STATUS_ORDER.map((option) => (
                          <option key={option} value={option}>
                            {TASK_STATUS_LABELS[option]}
                          </option>
                        ))}
                      </select>
                    </header>

                    {task.description && <p className="task-card__description">{task.description}</p>}

                    <footer className="task-card__footer">
                      <div className="task-card__meta">
                        <span>마감일</span>
                        <strong>
                          {task.due_date ? dayjs(task.due_date).format('YYYY.MM.DD') : '미정'}
                        </strong>
                      </div>

                      <div className="task-card__actions">
                        {retrospective && task.retrospective_id !== retrospective.id && (
                          <button
                            type="button"
                            className="button subtle"
                            onClick={() => handleAttachTask(task.id)}
                            disabled={attachMutation.isPending}
                          >
                            회고에 추가
                          </button>
                        )}

                        <button
                          type="button"
                          className="button danger"
                          onClick={() => handleDeleteTask(task.id)}
                          disabled={deleteMutation.isPending}
                        >
                          삭제
                        </button>
                      </div>
                    </footer>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </section>
  )
}

export default TaskBoard


