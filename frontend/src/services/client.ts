import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (import.meta.env.DEV) {
      // eslint-disable-next-line no-console
      console.error('API Error:', error)
    }
    return Promise.reject(error)
  },
)

export default apiClient


