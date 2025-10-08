import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import apiClient from './client'
import type { Retrospective, RetrospectiveCreatePayload } from '@/types/retrospective'

const RETRO_QUERY_KEY = ['retrospectives']

async function createRetrospective(payload: RetrospectiveCreatePayload): Promise<Retrospective> {
  const response = await apiClient.post<Retrospective>('/retrospectives', payload)
  return response.data
}

async function attachTask(retrospectiveId: string, taskId: string): Promise<Retrospective> {
  const response = await apiClient.post<Retrospective>(`/retrospectives/${retrospectiveId}/tasks/${taskId}`)
  return response.data
}

async function getRetrospectiveByDate(date: string): Promise<Retrospective | null> {
  const response = await apiClient.get<Retrospective | null>(`/retrospectives/date/${date}`)
  return response.data
}

export function useRetrospective(date: string) {
  return useQuery({
    queryKey: [...RETRO_QUERY_KEY, date],
    queryFn: () => getRetrospectiveByDate(date),
    enabled: Boolean(date),
  })
}

export function useCreateRetrospective() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: createRetrospective,
    onSuccess: (data) => {
      if (data.date) {
        queryClient.invalidateQueries({ queryKey: [...RETRO_QUERY_KEY, data.date] })
      }
    },
  })
}

export function useAttachTask(date: string) {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ retrospectiveId, taskId }: { retrospectiveId: string; taskId: string }) =>
      attachTask(retrospectiveId, taskId),
    onSuccess: () => {
      if (date) {
        queryClient.invalidateQueries({ queryKey: [...RETRO_QUERY_KEY, date] })
      }
    },
  })
}


