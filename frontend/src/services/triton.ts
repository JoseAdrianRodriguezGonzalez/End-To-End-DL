import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || '/api'

export interface Prediction {
  class: string
  index: number
  confidence: number
}

export interface PredictResponse {
  model: string
  prediction: Prediction
  top: Prediction[]
  probabilites: number[]
}

export interface HealthResponse {
  status: string
  triton: string
  model: string
}

export const tritonApi = axios.create({
  baseURL: API_BASE,
  timeout: 60000
})

export async function predictImage(file: File): Promise<PredictResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await tritonApi.post<PredictResponse>('/predict', formData)

  return response.data
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await tritonApi.get<HealthResponse>('/health')
  return response.data
}

export async function listModels() {
  const response = await tritonApi.get('/models')
  return response.data
}
