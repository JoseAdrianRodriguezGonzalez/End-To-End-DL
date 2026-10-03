<template>
  <header class="bg-indigo-600 text-white">
    <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
      <h1 class="text-xl font-bold">Inference GUI</h1>
      <div class="flex items-center gap-2">
        <span class="text-sm text-indigo-100">Servidor:</span>
        <span :class="statusClass">{{ serverStatus }}</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { checkHealth } from '@/services/triton'

const serverStatus = ref('Desconocido')
const statusClass = ref('')

async function refreshStatus() {
  try {
    const data = await checkHealth()
    serverStatus.value = data.triton === 'ok' ? 'En lnea' : 'Offline'
    statusClass.value = data.triton === 'ok' ? 'text-green-300 font-medium' : 'text-red-300'
  } catch {
    serverStatus.value = 'Offline'
    statusClass.value = 'text-red-300'
  }
}

onMounted(() => {
  refreshStatus()
  setInterval(refreshStatus, 10000)
})
</script>
