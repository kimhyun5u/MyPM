export interface Retrospective {
  id: string
  title: string
  summary: string | null
  date: string
  tasks: string[]
}

export interface RetrospectiveCreatePayload {
  title: string
  summary?: string | null
  date?: string | null
}


