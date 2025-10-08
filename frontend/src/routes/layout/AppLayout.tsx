import { Outlet } from 'react-router-dom'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import LayoutShell from '@/components/LayoutShell'

const queryClient = new QueryClient()

function AppLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <LayoutShell>
        <Outlet />
      </LayoutShell>
      <ReactQueryDevtools initialIsOpen={false} position="bottom" />
    </QueryClientProvider>
  )
}

export default AppLayout


