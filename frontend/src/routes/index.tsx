import { createBrowserRouter } from 'react-router-dom'
import AppLayout from '@/routes/layout/AppLayout'
import DashboardPage from '@/pages/DashboardPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
    ],
  },
])

export default router


