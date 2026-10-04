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
        <div>
          <span class="text-2xl font-bold text-indigo-600">{{ predictions.prediction.class }}</span>
          <p class="text-xs text-gray-500">
            Clase {{predictions.prediction.index}}
          </p>
        </div>
        <span class="text-lg font-medium text-gray-700"> 
          {{ (predictions.prediction.confidence * 100).toFixed(1) }}% 
        </span>
      </div>
    </div>

    <div>
      <p class="text-sm text-gray-500 mb-3"> Top 5 predicciones </p> 
      <div v-for="(pred, idx) in predictions.top" :key="pred.index" class="flex items-center mb-3" > 
        <span class="w-8 font-medium text-gray-600"> {{ idx + 1 }} </span> 
        <div class="flex-1 mx-3"> 
          <div class="flex justify-between mb-1"> 
            <span class="text-sm font-medium text-gray-700"> {{ pred.class }} </span> 
            <span class="text-xs text-gray-500"> {{ (pred.confidence * 100).toFixed(1) }}% </span> 
          </div> 
          <div class="h-2 bg-gray-200 rounded-full overflow-hidden" > 
            <div :class=" idx === 0 ? 'bg-indigo-600' : 'bg-indigo-400' " class="h-full rounded-full transition-all duration-500" :style="{ width: `${pred.confidence * 100}%` }" ></div>
          </div>
        </div> 
      </div> 
    </div>
    <p class="mt-5 text-xs text-gray-400 text-right"> Modelo: {{ predictions.model }} </p> 
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
