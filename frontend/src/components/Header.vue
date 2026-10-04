<template>
  <header class="bg-indigo-600 text-white">
    <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
      <h1 class="text-xl font-bold">Inference GUI</h1>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2">
          <span class="text-sm text-indigo-100">Servidor:</span>
          <span :class="statusClass">{{ serverStatus }}</span>
        </div>
        <span v-if="modelName" class="text-xs bg-indigo-500 py-1 px-2 rounded">
        {{ modelName }}
        </span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted,onUnmounted } from 'vue'
import { checkHealth } from '@/services/triton'

const serverStatus = ref('Desconocido')
const statusClass = ref('')
const modelName = ref('')
let statusInterval:ReturnType<typeof setInterval> | undefined 
async function refreshStatus() {
  try {
    const data = await checkHealth()
    if(data.triton==='ok'){
      serverStatus.value='En línea'
      statusClass.value = 'text-green-300 font-medium' 
      modelName.value=data.model 
    }
    else{

      serverStatus.value='Offline'
      statusClass.value = 'text-red-300' 
      
    }
  } catch {
    serverStatus.value = 'Offline'
    statusClass.value = 'text-red-300'
  }
}

onMounted(() => {
  refreshStatus()
  statusInterval=setInterval(refreshStatus, 10000)
})
onUnmounted(() => {
  if (statusInterval){
    clearInterval(statusInterval)
  }
})
</script>
