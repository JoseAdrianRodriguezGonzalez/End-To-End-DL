<template>
  <div
    class="border-2 border-dashed border-indigo-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer bg-white"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
  >
    <input
      ref="fileInputRef"
      type="file"
      class="hidden"
      accept="image/*"
      @change="handleFileSelect"
    />

    <div v-if="previewUrl">
      <img :src="previewUrl" class="max-h-64 mx-auto rounded-lg" alt="Vista previa" />
      <p class="mt-4 text-sm text-gray-600">{{ fileName }}</p>
      <button
        @click.stop="clearImage"
        class="mt-3 text-indigo-600 hover:text-indigo-800 text-sm"
      >
        Eliminar
      </button>
    </div>

    <div v-else>
      <svg
        class="mx-auto h-12 w-12 text-indigo-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
        />
      </svg>
      <p class="mt-2 text-sm text-gray-600">
        Arrastra una imagen aqu o <span class="text-indigo-600 font-medium">selecciona un archivo</span>
      </p>
      <p class="mt-1 text-xs text-gray-500">PNG, JPG, WEBP (Procesamiento a  224x224)</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'selected', file: File): void
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const previewUrl = ref<string>('')
const fileName = ref<string>('')

function triggerFileInput() {
  fileInputRef.value?.click()
}

function handleDragOver(e: DragEvent) {
  e.preventDefault()
}

function handleDragLeave(e: DragEvent) {
  e.preventDefault()
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    selectFile(files[0])
  }
}

function handleFileSelect(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectFile(target.files[0])
  }
}

function selectFile(file: File) {
  if (!file.type.startsWith('image/')) {
    alert('Por favor sube un archivo de imagen vlido.')
    return
  }

  const url = URL.createObjectURL(file)
  previewUrl.value = url
  fileName.value = file.name
  emit('selected', file)
}

function clearImage() {
  if(previewUrl.value){
    URL.revokeObjectURL(previewUrl.value) 
  }
  previewUrl.value = ''
  fileName.value = ''
  if (fileInputRef.value) {
    fileInputRef.value.value = ''
  }
}
</script>
