<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <main class="max-w-4xl mx-auto px-4 py-12">
      <div class="text-center mb-10">
        <h2 class="text-3xl font-bold text-gray-800 mb-3">
          Clasificación de imgenes con Triton Inference Server
        </h2>
        <p class="text-gray-600">
          Arrastra una imagen, enva al modelo de inferencia y recibe predicciones al instante.
        </p>
      </div>

      <div class="space-y-6">
        <Dropzone @selected="handleFileSelected" />
        <PredictionResult :predictions="prediction" :loading="loading" />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Header from '@/components/Header.vue'
import Dropzone from '@/components/Dropzone.vue'
import PredictionResult from '@/components/PredictionResult.vue'
import { predictImage, PredictResponse } from '@/services/triton'

const prediction = ref<PredictResponse | null>(null)
const loading = ref(false)

async function handleFileSelected(file: File) {
  loading.value = true
  try {
    prediction.value = await predictImage(file)
  } catch (error) {
    console.error('Error al predecir:', error)
    prediction.value = null
  } finally {
    loading.value = false
  }
}
</script>
