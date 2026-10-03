<template>
  <div v-if="loading" class="bg-white rounded-lg shadow-md p-6 text-center">
    <div class="animate-spin rounded-full h-10 w-10 border-4 border-indigo-600 border-t-transparent mx-auto"></div>
    <p class="mt-3 text-gray-600">Analizando imagen...</p>
  </div>

  <div v-else-if="predictions" class="bg-white rounded-lg shadow-md p-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Resultados</h3>

    <div class="mb-6">
      <p class="text-sm text-gray-500 mb-1">Clase seleccionada</p>
      <div class="flex items-center justify-between bg-indigo-50 rounded-lg p-4">
        <span class="text-3xl font-bold text-indigo-600">{{ predictions.top[0]?.index }}</span>
        <span class="text-lg font-medium text-gray-700">
          {{ (predictions.top[0]?.confidence * 100).toFixed(1) }}%
        </span>
      </div>
    </div>

    <div class="space-y-3">
      <div v-for="(pred, idx) in predictions.top" :key="idx" class="flex items-center">
        <span class="w-8 font-medium text-gray-600">{{ idx + 1 }}</span>
        <div class="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden mx-3">
          <div
            :class="idx === 0 ? 'bg-indigo-600' : 'bg-indigo-400'"
            class="h-full rounded-full transition-all duration-500"
            :style="{ width: (pred.confidence * 100) + '%' }"
          ></div>
        </div>
        <span class="w-16 text-right text-sm font-medium text-gray-700">
          {{ (pred.confidence * 100).toFixed(1) }}%
        </span>
      </div>
    </div>
  </div>

  <div v-else class="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
    Selecciona una imagen para ver las predicciones
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { PredictResponse } from '@/services/triton'

defineProps<{
  predictions: PredictResponse | null
  loading: boolean
}>()
</script>
