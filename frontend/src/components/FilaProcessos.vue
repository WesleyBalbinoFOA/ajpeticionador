<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const props = defineProps({ processos: Array })
const emit  = defineEmits(['peticoes-geradas', 'voltar'])

const selecionados = ref(new Set(props.processos.map(p => p.id)))
const gerando      = ref(false)
const progresso    = ref(0)
const erro         = ref('')

function toggleTodos(e) {
  selecionados.value = e.target.checked
    ? new Set(props.processos.map(p => p.id))
    : new Set()
}
function toggle(id) {
  selecionados.value.has(id)
    ? selecionados.value.delete(id)
    : selecionados.value.add(id)
}

async function gerarPeticoes() {
  const lista = props.processos.filter(p => selecionados.value.has(p.id))
  if (!lista.length) return
  gerando.value  = true
  progresso.value = 0
  erro.value     = ''
  try {
    const resultado = await api.gerarLote(lista)
    const peticoes  = resultado.resultados || resultado
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
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold" style="color: var(--foa-navy); font-family: 'Playfair Display', serif">
          Processos importados
        </h2>
        <p class="text-sm mt-1" style="color: var(--foa-muted)">
          {{ processos.length }} processos encontrados ·
          {{ selecionados.size }} selecionados
        </p>
      </div>
      <div class="flex gap-3">
        <button class="btn-secondary" @click="emit('voltar')">← Voltar</button>
        <button
          class="btn-gold"
          :disabled="gerando || !selecionados.size"
          @click="gerarPeticoes"
        >
          <span v-if="gerando">⏳ Gerando petições...</span>
          <span v-else>🤖 Gerar {{ selecionados.size }} petições</span>
        </button>
      </div>
    </div>

    <!-- Erro -->
    <p v-if="erro" class="mb-4 text-sm rounded-lg p-3"
       style="color: #C0392B; background: #FDECEA">❌ {{ erro }}</p>

    <!-- Tabela -->
    <div class="card p-0 overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr style="background: var(--foa-navy)">
            <th class="p-3 w-10">
              <input type="checkbox" checked @change="toggleTodos" />
            </th>
            <th class="p-3 text-left text-xs font-medium uppercase tracking-wider text-blue-200">Número</th>
            <th class="p-3 text-left text-xs font-medium uppercase tracking-wider text-blue-200">Parte Contrária</th>
            <th class="p-3 text-left text-xs font-medium uppercase tracking-wider text-blue-200">Vara</th>
            <th class="p-3 text-left text-xs font-medium uppercase tracking-wider text-blue-200">Tipo</th>
            <th class="p-3 text-left text-xs font-medium uppercase tracking-wider text-blue-200">Descrição</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="p in processos" :key="p.id"
            class="transition-colors hover:bg-blue-50"
            style="border-bottom: 1px solid var(--foa-border)"
            :class="!selecionados.has(p.id) ? 'opacity-40' : ''"
          >
            <td class="p-3 text-center">
              <input type="checkbox"
                     :checked="selecionados.has(p.id)"
                     @change="toggle(p.id)" />
            </td>
            <td class="p-3 font-mono text-xs font-bold" style="color: var(--foa-blue)">
              {{ p.numero }}
            </td>
            <td class="p-3 font-medium text-xs" style="color: var(--foa-text)">
              {{ p.parte_contraria }}
            </td>
            <td class="p-3 text-xs" style="color: var(--foa-muted)">{{ p.vara_orgao }}</td>
            <td class="p-3 text-xs" style="color: var(--foa-muted)">{{ p.tipo_tarefa }}</td>
            <td class="p-3 text-xs max-w-xs truncate" style="color: var(--foa-muted)"
                :title="p.descricao_solicitacao">
              {{ p.descricao_solicitacao }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
