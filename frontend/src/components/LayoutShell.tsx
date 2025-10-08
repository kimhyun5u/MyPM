import type { PropsWithChildren } from 'react'
import { NavLink } from 'react-router-dom'
import '@/components/LayoutShell.css'

function LayoutShell({ children }: PropsWithChildren) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">MyPM</div>
        <nav className="nav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
            대시보드
          </NavLink>
        </nav>
      </aside>
      <main className="content">
        <header className="header">
          <h1>오늘의 업무 현황</h1>
        </header>
        <section className="main-content">{children}</section>
      </main>
    </div>
  )
}

export default LayoutShell


