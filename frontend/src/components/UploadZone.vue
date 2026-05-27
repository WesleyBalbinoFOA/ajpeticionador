<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const emit = defineEmits(['processos-extraidos'])

const arrastando = ref(false)
const carregando = ref(false)
const erro = ref('')

async function processarArquivo(arquivo) {
  if (!arquivo) return
  erro.value = ''
  carregando.value = true
  try {
    const resultado = await api.uploadExcel(arquivo)
    emit('processos-extraidos', resultado.processos)
  } catch (e) {
    erro.value = e.response?.data?.detail || 'Erro ao processar arquivo.'
  } finally {
    carregando.value = false
  }
}

function onDrop(e) {
  arrastando.value = false
  const arquivo = e.dataTransfer.files[0]
  processarArquivo(arquivo)
}

function onInput(e) {
  processarArquivo(e.target.files[0])
}
</script>

<template>
  <div class="max-w-2xl mx-auto mt-12">
    <div class="card text-center">
      <h2 class="text-xl font-bold text-gray-700 mb-2">Importar fila de processos</h2>
      <p class="text-gray-500 text-sm mb-6">
        Exporte a planilha do seu sistema de gestão e arraste aqui.
      </p>

      <!-- Zona de drop -->
      <label
        class="block border-2 border-dashed rounded-xl p-12 cursor-pointer transition-colors"
        :class="arrastando ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'"
        @dragover.prevent="arrastando = true"
        @dragleave="arrastando = false"
        @drop.prevent="onDrop"
      >
        <div v-if="!carregando">
          <div class="text-5xl mb-3">📂</div>
          <p class="text-gray-600 font-medium">Arraste o arquivo .xlsx aqui</p>
          <p class="text-gray-400 text-sm mt-1">ou clique para selecionar</p>
        </div>
        <div v-else class="text-gray-500">
          <div class="text-4xl mb-3 animate-spin">⏳</div>
          <p>Processando arquivo...</p>
        </div>
        <input type="file" class="hidden" accept=".xlsx,.xls" @change="onInput" />
      </label>

      <!-- Erro -->
      <p v-if="erro" class="mt-4 text-red-600 text-sm bg-red-50 rounded-lg p-3">
        ❌ {{ erro }}
      </p>
    </div>
  </div>
</template>
