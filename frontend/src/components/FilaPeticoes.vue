<script setup>
import { computed } from 'vue'
import CardPeticao from './CardPeticao.vue'

const props = defineProps({ peticoes: Array, usuario: Object })
const emit  = defineEmits(['voltar'])

const geradas   = computed(() => props.peticoes.filter(p => p.status === 'gerada').length)
const erros     = computed(() => props.peticoes.filter(p => p.status === 'erro').length)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold"
            style="color: var(--foa-navy); font-family: 'Playfair Display', serif">
          Revisão das petições
        </h2>
        <p class="text-sm mt-1" style="color: var(--foa-muted)">
          {{ geradas }} geradas com sucesso
          <span v-if="erros" style="color: #C0392B"> · {{ erros }} com erro</span>
        </p>
      </div>
      <button class="btn-secondary" @click="emit('voltar')">← Voltar</button>
    </div>

    <div class="space-y-4">
      <CardPeticao
        v-for="p in peticoes" :key="p.processo_id"
        :peticao="p"
        :usuario="usuario"
      />
    </div>
  </div>
</template>
