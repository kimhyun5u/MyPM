import { useState } from 'react'
import dayjs from 'dayjs'
import TaskBoard from '@/components/task/TaskBoard'
import RetrospectivePanel from '@/components/retrospective/RetrospectivePanel'
import '@/pages/DashboardPage.css'

function DashboardPage() {
  const [selectedStatus, setSelectedStatus] = useState<string>('all')
  const [retroDate, setRetroDate] = useState<string>(dayjs().format('YYYY-MM-DD'))

  return (
    <div className="dashboard">
      <section className="dashboard-controls">
        <div>
          <label className="form-label" htmlFor="status-filter">
            상태 필터
          </label>
          <select
            id="status-filter"
            className="select"
            value={selectedStatus}
            onChange={(event) => setSelectedStatus(event.target.value)}
          >
            <option value="all">전체</option>
            <option value="todo">할 일</option>
            <option value="in_progress">진행중</option>
            <option value="done">완료</option>
            <option value="blocked">차단됨</option>
          </select>
        </div>

        <div>
          <label className="form-label" htmlFor="retro-date">
            회고 날짜
          </label>
          <input
            id="retro-date"
            type="date"
            className="input"
            value={retroDate}
            onChange={(event) => setRetroDate(event.target.value)}
          />
        </div>
      </section>

      <section className="dashboard-grid">
        <TaskBoard statusFilter={selectedStatus === 'all' ? undefined : selectedStatus} retroDate={retroDate} />
        <RetrospectivePanel retroDate={retroDate} />
      </section>
    </div>
  )
}

export default DashboardPage


