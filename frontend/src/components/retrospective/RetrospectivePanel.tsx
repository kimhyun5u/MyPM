import { type FormEvent, useEffect, useState } from 'react'
import dayjs from 'dayjs'
import { useCreateRetrospective, useRetrospective } from '@/services/retrospectives'
import { useTasks } from '@/services/tasks'
import type { RetrospectiveCreatePayload } from '@/types/retrospective'
import '@/components/retrospective/RetrospectivePanel.css'

interface RetrospectivePanelProps {
  retroDate: string
}

const INITIAL_FORM: RetrospectiveCreatePayload = {
  title: '',
  summary: '',
  date: dayjs().format('YYYY-MM-DD'),
}

function RetrospectivePanel({ retroDate }: RetrospectivePanelProps) {
  const [form, setForm] = useState<RetrospectiveCreatePayload>({ ...INITIAL_FORM, date: retroDate })
  const { data: retrospective, isLoading } = useRetrospective(retroDate)
  const { data: tasks = [] } = useTasks()
  const createMutation = useCreateRetrospective()

  useEffect(() => {
    setForm((prev) => ({ ...prev, date: retroDate }))
  }, [retroDate])

  useEffect(() => {
    if (retrospective) {
      setForm({
        title: retrospective.title,
        summary: retrospective.summary ?? '',
        date: retrospective.date,
      })
    } else {
      setForm({ ...INITIAL_FORM, date: retroDate })
    }
  }, [retrospective, retroDate])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!form.title.trim()) {
      return
    }

    createMutation.mutate(form, {
      onSuccess: () => {
        // No additional action needed; query will refetch
      },
    })
  }

  return (
    <aside className="retro-panel">
      <header className="retro-panel__header">
        <h2>회고</h2>
        <span>{dayjs(retroDate).format('YYYY.MM.DD')}</span>
      </header>

      {isLoading ? (
        <p className="retro-panel__state">회고를 불러오는 중...</p>
      ) : (
        <form className="retro-form" onSubmit={handleSubmit}>
          <div className="retro-form__row">
            <label htmlFor="retro-title">제목</label>
            <input
              id="retro-title"
              type="text"
              value={form.title}
              onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
              placeholder="오늘의 회고 제목"
              required
            />
          </div>

          <div className="retro-form__row">
            <label htmlFor="retro-summary">요약</label>
            <textarea
              id="retro-summary"
              value={form.summary ?? ''}
              onChange={(event) => setForm((prev) => ({ ...prev, summary: event.target.value }))}
              rows={6}
              placeholder="오늘의 회고를 작성하세요"
            />
          </div>

          <button type="submit" className="button primary" disabled={createMutation.isPending}>
            {retrospective ? '회고 업데이트' : '새 회고 생성'}
          </button>
        </form>
      )}

      {retrospective && retrospective.tasks.length > 0 && (
        <section className="retro-tasks">
          <h3>회고에 포함된 할 일</h3>
          <ul>
            {retrospective.tasks.map((taskId) => {
              const task = tasks.find((item) => item.id === taskId)
              return (
                <li key={taskId}>
                  <strong>{task?.title ?? '삭제된 작업'}</strong>
                  {task?.description && <p>{task.description}</p>}
                </li>
              )
            })}
          </ul>
        </section>
      )}
    </aside>
  )
}

export default RetrospectivePanel


