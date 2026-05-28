<script setup>
import { ref, computed } from 'vue'
import { api } from '../services/api.js'

const props = defineProps({ peticao: Object, usuario: Object })

const expandido    = ref(false)
const salvando     = ref(false)
const status       = ref(props.peticao.status || 'gerada')
const conteudoEdit = ref(props.peticao.conteudo || '')
const conteudoOriginalIA = props.peticao.conteudo || ''  // para RLHF

const parteContraria = computed(() => props.peticao.parte_contraria || '')

function salvarHistorico(statusFinal, conteudoFinal) {
  // Registro RLHF — guarda input, output IA e output editado
  const historico = JSON.parse(localStorage.getItem('peticiona_historico') || '[]')
  historico.push({
    id:               Date.now(),
    numero:           props.peticao.numero,
    parte:            parteContraria.value,
    tipo:             props.peticao.modelo_usado,
    advogado:         props.usuario?.nome || '',
    data:             new Date().toISOString(),
    status:           statusFinal,
    // RLHF
    output_ia:        conteudoOriginalIA,
    output_editado:   conteudoFinal,
    foi_editado:      conteudoFinal !== conteudoOriginalIA,
  })
  localStorage.setItem('peticiona_historico', JSON.stringify(historico))
}

async function baixarDocx() {
  salvando.value = true
  try {
    await api.baixarDocx(props.peticao.numero, conteudoEdit.value, parteContraria.value)
    status.value = 'aprovada'
    salvarHistorico('aprovada', conteudoEdit.value)
  } catch (e) {
    alert('Erro ao gerar Word: ' + e.message)
  } finally {
    salvando.value = false
  }
}

async function baixarPdf() {
  salvando.value = true
  try {
    await api.baixarPdf(props.peticao.numero, conteudoEdit.value, parteContraria.value)
    status.value = 'aprovada'
    salvarHistorico('aprovada', conteudoEdit.value)
  } catch (e) {
    alert('Erro ao gerar PDF: ' + e.message)
  } finally {
    salvando.value = false
  }
}

function rejeitar() {
  status.value = 'rejeitada'
  salvarHistorico('rejeitada', conteudoEdit.value)
}

const statusConfig = {
  gerada:    { bg: '#FFF8E1', color: '#856404', label: 'Pendente revisão' },
  aprovada:  { bg: '#D4EDDA', color: '#1A6B3C', label: 'Aprovada'         },
  rejeitada: { bg: '#FDECEA', color: '#C0392B', label: 'Rejeitada'        },
  erro:      { bg: '#FDECEA', color: '#C0392B', label: 'Erro'             },
}
</script>

<template>
  <div class="card" :style="status === 'aprovada' ? 'border-color: #1A6B3C' :
                             status === 'rejeitada' ? 'border-color: #C0392B' : ''">

    <!-- Cabeçalho -->
    <div class="flex items-start justify-between gap-4">
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-1 flex-wrap">
          <span class="text-xs font-medium px-2.5 py-0.5 rounded-full"
                :style="`background: ${statusConfig[status]?.bg}; color: ${statusConfig[status]?.color}`">
            {{ statusConfig[status]?.label }}
          </span>
          <span class="text-xs px-2 py-0.5 rounded"
                style="background: var(--foa-gray); color: var(--foa-muted)">
            {{ peticao.modelo_usado }}
          </span>
        </div>

        <h3 class="font-mono font-bold text-sm truncate" style="color: var(--foa-blue)">
          {{ peticao.numero }}
        </h3>
        <p class="text-xs mt-0.5" style="color: var(--foa-muted)">
          {{ parteContraria }}
        </p>
      </div>

      <!-- Ações -->
      <div class="flex gap-2 flex-shrink-0 flex-wrap justify-end">
        <template v-if="status !== 'erro' && status !== 'rejeitada'">
          <button class="btn-success text-xs py-1.5 px-3"
                  :disabled="salvando" @click="baixarDocx">
            📄 Word
          </button>
          <button class="btn-primary text-xs py-1.5 px-3"
                  :disabled="salvando" @click="baixarPdf">
            📕 PDF
          </button>
        </template>
        <button class="btn-secondary text-xs py-1.5 px-3"
                @click="expandido = !expandido">
          {{ expandido ? '▲ Fechar' : '✏️ Editar' }}
        </button>
        <button v-if="status === 'gerada'"
                class="btn-danger text-xs py-1.5 px-3"
                @click="rejeitar">✕</button>
      </div>
    </div>

    <!-- Preview -->
    <p v-if="!expandido && status !== 'erro'"
       class="mt-3 text-xs line-clamp-2 font-mono"
       style="color: var(--foa-muted)">
      {{ (peticao.conteudo || '').substring(0, 150) }}...
    </p>

    <!-- Erro -->
    <p v-if="status === 'erro'" class="mt-3 text-sm" style="color: #C0392B">
      ❌ {{ peticao.erro }}
    </p>

    <!-- Editor -->
    <div v-if="expandido && status !== 'erro'" class="mt-4">
      <div class="flex items-center justify-between mb-2">
        <p class="text-xs font-medium" style="color: var(--foa-navy)">
          Edição inline
        </p>
        <span v-if="conteudoEdit !== conteudoOriginalIA"
              class="text-xs px-2 py-0.5 rounded"
              style="background: #FFF8E1; color: #856404">
          ✏️ Modificado
        </span>
      </div>
      <textarea
        v-model="conteudoEdit"
        style="width:100%;box-sizing:border-box;padding:1.25rem 1.5rem;
               font-family:'Times New Roman',serif;font-size:13px;line-height:1.8;
               border:1.5px solid #DDE3EF;border-radius:10px;color:#1A2340;
               resize:vertical;min-height:500px;outline:none;
               background:#FAFBFD;transition:border-color 0.2s"
        rows="25"
        @focus="e=>e.target.style.borderColor='#003087'"
        @blur="e=>e.target.style.borderColor='#DDE3EF'"
      />
      <p class="text-xs mt-1" style="color: var(--foa-muted)">
        Edições são registradas para refinamento futuro da IA.
      </p>
    </div>
  </div>
</template>