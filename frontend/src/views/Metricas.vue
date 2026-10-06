<template>
  <div class="min-h-screen bg-gray-50">
    <Header />
    <main class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-gray-800 mb-3">Observability</h1>

    <p v-if="loading">
      Loading...
    </p>

    <p v-else-if="error">
      Error loading observability data.
    </p>
<table
  v-else-if="data"
  class="w-full overflow-hidden rounded-xl border border-gray-200 bg-white text-sm shadow-sm"
>
  <thead class="bg-gray-50">
    <tr class="border-b border-gray-200">
      <th
        class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500"
      >
        Section
      </th>

      <th
        class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500"
      >
        Metric
      </th>

      <th
        class="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-gray-500"
      >
        Value
      </th>
    </tr>
  </thead>

  <tbody class="divide-y divide-gray-100">

    <!-- API -->
    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4">
        <span
          class="inline-flex rounded-md bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
        >
          API
        </span>
      </td>

      <td class="px-6 py-4 font-medium text-gray-700">
        Status
      </td>

      <td class="px-6 py-4 text-right">
        <span
          class="inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700"
        >
          <span class="h-2 w-2 rounded-full bg-green-500"></span>
          {{ data.api.status }}
        </span>
      </td>
    </tr>


    <!-- TRITON -->
    <tr class="bg-gray-50/50">
      <td
        rowspan="5"
        class="px-6 py-4 align-top"
      >
        <span
          class="inline-flex rounded-md bg-purple-50 px-2.5 py-1 text-xs font-semibold text-purple-700"
        >
          Triton
        </span>
      </td>

      <td class="px-6 py-4 font-medium text-gray-700">
        Status
      </td>

      <td class="px-6 py-4 text-right">
        <span
          class="inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700"
        >
          <span class="h-2 w-2 rounded-full bg-green-500"></span>
          {{ data.triton.status }}
        </span>
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Server
      </td>

      <td class="px-6 py-4 text-right font-mono text-xs text-gray-500">
        {{ data.triton.server }}
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Model
      </td>

      <td class="px-6 py-4 text-right">
        <span
          class="rounded-md bg-gray-100 px-2.5 py-1 font-mono text-xs text-gray-700"
        >
          {{ data.triton.model }}
        </span>
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Triton Ready
      </td>

      <td class="px-6 py-4 text-right">
        <span
          v-if="data.triton.triton_ready"
          class="inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700"
        >
          <span class="h-2 w-2 rounded-full bg-green-500"></span>
          Ready
        </span>

        <span
          v-else
          class="inline-flex items-center gap-2 rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-700"
        >
          <span class="h-2 w-2 rounded-full bg-red-500"></span>
          Not Ready
        </span>
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Model Ready
      </td>

      <td class="px-6 py-4 text-right">
        <span
          v-if="data.triton.model_ready"
          class="inline-flex items-center gap-2 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700"
        >
          <span class="h-2 w-2 rounded-full bg-green-500"></span>
          Ready
        </span>

        <span
          v-else
          class="inline-flex items-center gap-2 rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-700"
        >
          <span class="h-2 w-2 rounded-full bg-red-500"></span>
          Not Ready
        </span>
      </td>
    </tr>


    <!-- REQUESTS -->
    <tr class="bg-gray-50/50">
      <td
        rowspan="2"
        class="px-6 py-4 align-top"
      >
        <span
          class="inline-flex rounded-md bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
        >
          Requests
        </span>
      </td>

      <td class="px-6 py-4 font-medium text-gray-700">
        Successful
      </td>

      <td class="px-6 py-4 text-right font-semibold text-green-600">
        {{ data.inference.requests.successful }}
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Failed
      </td>

      <td
        class="px-6 py-4 text-right font-semibold"
        :class="
          data.inference.requests.failed > 0
            ? 'text-red-600'
            : 'text-gray-500'
        "
      >
        {{ data.inference.requests.failed }}
      </td>
    </tr>


    <!-- INFERENCE -->
    <tr class="bg-gray-50/50">
      <td
        rowspan="3"
        class="px-6 py-4 align-top"
      >
        <span
          class="inline-flex rounded-md bg-orange-50 px-2.5 py-1 text-xs font-semibold text-orange-700"
        >
          Inference
        </span>
      </td>

      <td class="px-6 py-4 font-medium text-gray-700">
        Inference Count
      </td>

      <td class="px-6 py-4 text-right font-semibold text-gray-800">
        {{ data.inference.inference.count }}
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Executions
      </td>

      <td class="px-6 py-4 text-right font-semibold text-gray-800">
        {{ data.inference.inference.executions }}
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Pending Requests
      </td>

      <td class="px-6 py-4 text-right font-semibold text-gray-800">
        {{ data.inference.pending_requests }}
      </td>
    </tr>


<!-- LATENCY -->
<tr class="bg-gray-50/50">
  <td
    rowspan="10"
    class="px-6 py-4 align-top"
  >
    <span
      class="inline-flex rounded-md bg-yellow-50 px-2.5 py-1 text-xs font-semibold text-yellow-700"
    >
      Latency
    </span>
  </td>

  <td class="px-6 py-4 font-medium text-gray-700">
    Request
  </td>

  <td class="px-6 py-4 text-right font-mono text-gray-700">
    {{ data.inference.latency_us.request }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Request Average
  </td>

  <td class="px-6 py-4 text-right font-mono font-semibold text-blue-600">
    {{ data.inference.latency_us.request_avg.toFixed(2) }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Queue
  </td>

  <td class="px-6 py-4 text-right font-mono text-gray-700">
    {{ data.inference.latency_us.queue }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Queue Average
  </td>

  <td class="px-6 py-4 text-right font-mono font-semibold text-blue-600">
    {{ data.inference.latency_us.queue_avg.toFixed(2) }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Input
  </td>

  <td class="px-6 py-4 text-right font-mono text-gray-700">
    {{ data.inference.latency_us.compute_input }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Input Average
  </td>

  <td class="px-6 py-4 text-right font-mono font-semibold text-blue-600">
    {{ data.inference.latency_us.compute_input_avg.toFixed(2) }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Infer
  </td>

  <td class="px-6 py-4 text-right font-mono text-gray-700">
    {{ data.inference.latency_us.compute_infer }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Infer Average
  </td>

  <td class="px-6 py-4 text-right font-mono font-semibold text-blue-600">
    {{ data.inference.latency_us.compute_infer_avg.toFixed(2) }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Output
  </td>

  <td class="px-6 py-4 text-right font-mono text-gray-700">
    {{ data.inference.latency_us.compute_output }} μs
  </td>
</tr>

<tr class="transition hover:bg-gray-50">
  <td class="px-6 py-4 font-medium text-gray-700">
    Compute Output Average
  </td>

  <td class="px-6 py-4 text-right font-mono font-semibold text-blue-600">
    {{ data.inference.latency_us.compute_output_avg.toFixed(2) }} μs
  </td>
</tr>    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Compute Infer
      </td>

      <td class="px-6 py-4 text-right font-mono text-gray-700">
        {{ data.inference.latency_us.compute_infer }} μs
      </td>
    </tr>

    <tr class="transition hover:bg-gray-50">
      <td class="px-6 py-4 font-medium text-gray-700">
        Compute Output
      </td>

      <td class="px-6 py-4 text-right font-mono text-gray-700">
        {{ data.inference.latency_us.compute_output }} μs
      </td>
    </tr>

  </tbody>
</table>

    </main>
  </div>

</template>

<script setup lang="ts">
import Header from '@/components/Header.vue'
import { observability,ObservabilityData  } from '@/services/triton'

import {onMounted,ref} from "vue"
const data=ref<ObservabilityData|null>(null)
const loading= ref(true)
const error =ref<unknown>(null)
onMounted(async () => {
  try {
    data.value = await observability()
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
})
</script>
