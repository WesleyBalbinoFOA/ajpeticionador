<script setup>
import { ref } from 'vue'
import UploadZone from './components/UploadZone.vue'
import FilaProcessos from './components/FilaProcessos.vue'
import FilaPeticoes from './components/FilaPeticoes.vue'

// Estado global mínimo — sem Pinia na Fase 1
const etapa = ref('upload')       // upload | processos | peticoes
const processos = ref([])
const peticoes = ref([])

function onProcessosExtraidos(lista) {
  processos.value = lista
  etapa.value = 'processos'
}

function onPeticoesGeradas(lista) {
  peticoes.value = lista
  etapa.value = 'peticoes'
}
</script>

<template>
  <div class="min-h-screen">
    <!-- Header -->
    <header class="bg-blue-800 text-white px-6 py-4 shadow-md">
      <div class="max-w-6xl mx-auto flex items-center gap-3">
        <span class="text-2xl">⚖️</span>
        <div>
          <h1 class="text-xl font-bold leading-none">PeticIona AI</h1>
          <p class="text-blue-200 text-xs">Geração automatizada de petições</p>
        </div>

        <!-- Breadcrumb de etapas -->
        <nav class="ml-auto flex gap-2 text-sm">
          <span :class="etapa === 'upload' ? 'text-white font-bold' : 'text-blue-300'">
            1. Upload
          </span>
          <span class="text-blue-400">›</span>
          <span :class="etapa === 'processos' ? 'text-white font-bold' : 'text-blue-300'">
            2. Processos
          </span>
          <span class="text-blue-400">›</span>
          <span :class="etapa === 'peticoes' ? 'text-white font-bold' : 'text-blue-300'">
            3. Revisão
          </span>
        </nav>
      </div>
    </header>

    <!-- Conteúdo -->
    <main class="max-w-6xl mx-auto px-6 py-8">
      <UploadZone
        v-if="etapa === 'upload'"
        @processos-extraidos="onProcessosExtraidos"
      />

      <FilaProcessos
        v-if="etapa === 'processos'"
        :processos="processos"
        @peticoes-geradas="onPeticoesGeradas"
        @voltar="etapa = 'upload'"
      />

      <FilaPeticoes
        v-if="etapa === 'peticoes'"
        :peticoes="peticoes"
        @voltar="etapa = 'processos'"
      />
    </main>
  </div>
</template>
