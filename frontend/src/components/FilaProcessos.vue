<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const props = defineProps({ processos: Array })
const emit = defineEmits(['peticoes-geradas', 'voltar'])

const selecionados = ref(new Set(props.processos.map(p => p.id)))
const gerando = ref(false)
const erro = ref('')

function toggleTodos(e) {
  if (e.target.checked) {
    selecionados.value = new Set(props.processos.map(p => p.id))
  } else {
    selecionados.value = new Set()
  }
}

function toggle(id) {
  if (selecionados.value.has(id)) {
    selecionados.value.delete(id)
  } else {
    selecionados.value.add(id)
  }
}

async function gerarPeticoes() {
  const lista = props.processos.filter(p => selecionados.value.has(p.id))
  if (!lista.length) return

  gerando.value = true
  erro.value = ''
  try {
    const resultado = await api.gerarLote(lista)
    // Aceita tanto {resultados: [...]} quanto array direto
    const peticoes = resultado.resultados || resultado
    if (!peticoes || peticoes.length === 0) {
      erro.value = 'Nenhuma petição foi gerada.'
      return
    }
    emit('peticoes-geradas', peticoes)
  } catch (e) {
    erro.value = e.response?.data?.detail || e.message || 'Erro ao gerar petições.'
  } finally {
    gerando.value = false
  }
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-gray-700">Processos encontrados</h2>
        <p class="text-gray-500 text-sm">{{ processos.length }} processos importados</p>
      </div>
      <div class="flex gap-3">
        <button class="btn-secondary" @click="emit('voltar')">← Voltar</button>
        <button
          class="btn-primary"
          :disabled="gerando || !selecionados.size"
          @click="gerarPeticoes"
        >
          {{ gerando ? '⏳ Gerando...' : `⚙️ Gerar petições (${selecionados.size})` }}
        </button>
      </div>
    </div>

    <p v-if="erro" class="mb-4 text-red-600 text-sm bg-red-50 rounded-lg p-3">
      ❌ {{ erro }}
    </p>

    <div class="card p-0 overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="p-3 w-8">
              <input type="checkbox" checked @change="toggleTodos" />
            </th>
            <th class="p-3 text-left text-gray-600 font-medium">Número</th>
            <th class="p-3 text-left text-gray-600 font-medium">Parte Contrária</th>
            <th class="p-3 text-left text-gray-600 font-medium">Vara</th>
            <th class="p-3 text-left text-gray-600 font-medium">Tipo de Tarefa</th>
            <th class="p-3 text-left text-gray-600 font-medium">Descrição</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="p in processos"
            :key="p.id"
            class="border-b border-gray-100 hover:bg-gray-50 transition-colors"
            :class="!selecionados.has(p.id) ? 'opacity-50' : ''"
          >
            <td class="p-3 text-center">
              <input
                type="checkbox"
                :checked="selecionados.has(p.id)"
                @change="toggle(p.id)"
              />
            </td>
            <td class="p-3 font-mono text-xs text-blue-700">{{ p.numero }}</td>
            <td class="p-3">{{ p.parte_contraria }}</td>
            <td class="p-3 text-gray-500">{{ p.vara_orgao }}</td>
            <td class="p-3 text-gray-500">{{ p.tipo_tarefa }}</td>
            <td class="p-3 text-gray-600 max-w-xs truncate" :title="p.descricao_solicitacao">
              {{ p.descricao_solicitacao }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>