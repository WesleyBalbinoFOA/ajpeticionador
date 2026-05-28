<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const props  = defineProps({ usuario: Object })
const emit   = defineEmits(['processos-extraidos'])
const arrastando = ref(false)
const carregando = ref(false)
const erro       = ref('')

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
  processarArquivo(e.dataTransfer.files[0])
}
function onInput(e) { processarArquivo(e.target.files[0]) }
</script>

<template>
  <div class="max-w-2xl mx-auto mt-8">

    <!-- Saudação -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold" style="color: var(--foa-navy); font-family: 'Playfair Display', serif">
        Olá, {{ usuario.nome.split(' ')[0] }}
      </h2>
      <p style="color: var(--foa-muted)" class="text-sm mt-1">
        Importe a fila de processos para começar a gerar petições.
      </p>
    </div>

    <div class="card">
      <!-- Zona de drop -->
      <label
        class="block border-2 border-dashed rounded-xl p-12 cursor-pointer transition-all text-center"
        :style="arrastando
          ? 'border-color: var(--foa-gold); background: rgba(201,168,76,0.05)'
          : 'border-color: var(--foa-border); background: var(--foa-gray)'"
        @dragover.prevent="arrastando = true"
        @dragleave="arrastando = false"
        @drop.prevent="onDrop"
      >
        <div v-if="!carregando">
          <div class="text-5xl mb-4">📂</div>
          <p class="font-semibold mb-1" style="color: var(--foa-navy)">
            Arraste o arquivo exportado do sistema
          </p>
          <p class="text-sm" style="color: var(--foa-muted)">
            ou clique para selecionar · .xls e .xlsx aceitos
          </p>
        </div>
        <div v-else>
          <div class="text-4xl mb-3 animate-spin inline-block">⏳</div>
          <p style="color: var(--foa-muted)">Processando arquivo...</p>
        </div>
        <input type="file" class="hidden" accept=".xlsx,.xls" @change="onInput" />
      </label>

      <p v-if="erro" class="mt-4 text-sm rounded-lg p-3"
         style="color: #C0392B; background: #FDECEA">
        ❌ {{ erro }}
      </p>

      <!-- Instruções -->
      <div class="mt-6 pt-6 grid grid-cols-3 gap-4 text-center text-xs"
           style="border-top: 1px solid var(--foa-border); color: var(--foa-muted)">
        <div>
          <div class="text-2xl mb-1">📤</div>
          <p>Exporte do sistema de gestão</p>
        </div>
        <div>
          <div class="text-2xl mb-1">🤖</div>
          <p>IA gera as petições automaticamente</p>
        </div>
        <div>
          <div class="text-2xl mb-1">✅</div>
          <p>Revise, edite e baixe</p>
        </div>
      </div>
    </div>
  </div>
</template>
