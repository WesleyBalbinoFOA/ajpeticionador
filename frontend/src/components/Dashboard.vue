<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({ usuario: Object })

// Dados simulados — Fase 2 virão do backend
const stats = ref({
  total:    0,
  hoje:     0,
  semana:   0,
  aprovadas: 0,
})

const historico = ref([])

onMounted(() => {
  // Carrega histórico do localStorage (Fase 1)
  const h = JSON.parse(localStorage.getItem('peticiona_historico') || '[]')
  historico.value = h.slice(-20).reverse()

  const hoje = new Date().toDateString()
  const semanaAtras = new Date(Date.now() - 7 * 86400000)

  stats.value = {
    total:     h.length,
    hoje:      h.filter(p => new Date(p.data).toDateString() === hoje).length,
    semana:    h.filter(p => new Date(p.data) >= semanaAtras).length,
    aprovadas: h.filter(p => p.status === 'aprovada').length,
  }
})
</script>

<template>
  <div>
    <div class="mb-8">
      <h2 class="text-2xl font-bold" style="color: var(--foa-navy)">Dashboard</h2>
      <p style="color: var(--foa-muted)" class="text-sm mt-1">
        Visão geral do peticionamento
      </p>
    </div>

    <!-- Cards de métricas -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div class="card text-center">
        <p class="text-3xl font-bold" style="color: var(--foa-navy)">{{ stats.total }}</p>
        <p class="text-xs mt-1" style="color: var(--foa-muted)">Total geradas</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold" style="color: var(--foa-gold)">{{ stats.hoje }}</p>
        <p class="text-xs mt-1" style="color: var(--foa-muted)">Hoje</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold" style="color: var(--foa-blue)">{{ stats.semana }}</p>
        <p class="text-xs mt-1" style="color: var(--foa-muted)">Últimos 7 dias</p>
      </div>
      <div class="card text-center">
        <p class="text-3xl font-bold" style="color: #1A6B3C">{{ stats.aprovadas }}</p>
        <p class="text-xs mt-1" style="color: var(--foa-muted)">Aprovadas</p>
      </div>
    </div>

    <!-- Histórico -->
    <div class="card p-0 overflow-hidden">
      <div class="px-6 py-4" style="border-bottom: 1px solid var(--foa-border)">
        <h3 class="font-semibold" style="color: var(--foa-navy)">Histórico recente</h3>
      </div>

      <div v-if="historico.length === 0" class="px-6 py-12 text-center"
           style="color: var(--foa-muted)">
        <p class="text-4xl mb-3">📋</p>
        <p class="text-sm">Nenhuma petição registrada ainda.</p>
        <p class="text-xs mt-1">As petições geradas aparecerão aqui.</p>
      </div>

      <table v-else class="w-full text-sm">
        <thead style="background: var(--foa-gray)">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Processo</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Parte</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Tipo</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Advogado</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Data</th>
            <th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
                style="color: var(--foa-muted)">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in historico" :key="p.id"
              style="border-top: 1px solid var(--foa-border)"
              class="hover:bg-blue-50 transition-colors">
            <td class="px-6 py-3 font-mono text-xs" style="color: var(--foa-blue)">
              {{ p.numero }}
            </td>
            <td class="px-6 py-3" style="color: var(--foa-text)">{{ p.parte }}</td>
            <td class="px-6 py-3 text-xs" style="color: var(--foa-muted)">{{ p.tipo }}</td>
            <td class="px-6 py-3 text-xs" style="color: var(--foa-muted)">{{ p.advogado }}</td>
            <td class="px-6 py-3 text-xs" style="color: var(--foa-muted)">
              {{ new Date(p.data).toLocaleDateString('pt-BR') }}
            </td>
            <td class="px-6 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-medium"
                    :style="p.status === 'aprovada'
                      ? 'background:#D4EDDA; color:#1A6B3C'
                      : 'background:#FFF3CD; color:#856404'">
                {{ p.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
