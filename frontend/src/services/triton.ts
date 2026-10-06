import axios from 'axios'
import heic2any from 'heic2any'
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
export interface ObservabilityData {
  api: {
    status: string
  }

  triton: {
    status: string
    server: string
    model: string
    triton_ready: boolean
    model_ready: boolean
  }

  inference: {
    requests: {
      successful: number
      failed: number
    }

    inference: {
      count: number
      executions: number
    }

    latency_us: {
      request: number
      request_avg: number

      queue: number
      queue_avg: number

      compute_input: number
      compute_input_avg: number

      compute_infer: number
      compute_infer_avg: number

      compute_output: number
      compute_output_avg: number
    }

    pending_requests: number
  }
}



export const tritonApi = axios.create({
  baseURL: API_BASE,
  timeout: 60000
})
async function convertHeicToJpeg(file: File): Promise<File> {
  const result = await heic2any({
    blob: file,
    toType: "image/jpeg",
    quality: 0.9,
  })
  const blob = Array.isArray(result) ? result[0] : result
  return new File([blob], file.name.replace(/\.(heic | heif)$/i, '.jpg'), {
    type: 'image/jpeg',
  })
}
async function prepareImage(file: File): Promise<File> {
  const isHeic = file.type === 'image/heic' || file.type === 'image/heif' || /\.(heic|heif)$/i.test(file.name)
  if (!isHeic) {
    return file
  }
  return convertHeicToJpeg(file)
}
export async function predictImage(file: File): Promise<PredictResponse> {
  const prepareFile = await prepareImage(file)
  const formData = new FormData()
  formData.append('file', prepareFile)

  const response = await tritonApi.post<PredictResponse>('/predict', formData)
  return response.data
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await tritonApi.get<HealthResponse>('/health')
  return response.data
}

export async function listModels() {
  const response = await tritonApi.post('/models')
  return response.data
}
export const observability = async (): Promise<ObservabilityData> => {
  const response = await tritonApi.get<ObservabilityData>("/observability")
  return response.data
}
