<script setup>
import { computed } from 'vue'
import { loading } from '../stores/loading.js'
const visible = computed(() => loading.active)
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="visible" class="lm-overlay">
        <div class="lm-box">
          <div class="lm-spinner"></div>
          <p class="lm-txt">Aguardando resposta…</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.lm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}

.lm-box {
  background: #fff;
  border-radius: 14px;
  padding: 2rem 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 8px 32px rgba(0, 48, 135, 0.18);
  border-top: 4px solid #C9A84C;
  min-width: 180px;
}

.lm-spinner {
  width: 44px;
  height: 44px;
  border: 4px solid #DDE3EF;
  border-top-color: #003087;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

.lm-txt {
  margin: 0;
  font-family: "DM Sans", system-ui, sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #3D4E6B;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
