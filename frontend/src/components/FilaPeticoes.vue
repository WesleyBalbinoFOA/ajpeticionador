<script setup>
import { ref } from 'vue'
import CardPeticao from './CardPeticao.vue'

const props = defineProps({ peticoes: Array })
const emit = defineEmits(['voltar'])

const aprovadas = props.peticoes.filter(p => p.status === 'gerada').length
const erros = props.peticoes.filter(p => p.status === 'erro').length
</script>

<template>
  <div>
    <!-- Cabeçalho -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-gray-700">Revisão das petições</h2>
        <p class="text-gray-500 text-sm">
          {{ aprovadas }} geradas com sucesso
          <span v-if="erros" class="text-red-500 ml-2">· {{ erros }} com erro</span>
        </p>
      </div>
      <button class="btn-secondary" @click="emit('voltar')">← Voltar</button>
    </div>

    <!-- Cards das petições -->
    <div class="space-y-6">
      <CardPeticao
        v-for="p in peticoes"
        :key="p.processo_id"
        :peticao="p"
      />
    </div>
  </div>
</template>
