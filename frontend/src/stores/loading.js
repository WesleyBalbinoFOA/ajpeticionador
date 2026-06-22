import { reactive, computed } from 'vue'

const state = reactive({ count: 0 })

export const loading = {
  get active() { return state.count > 0 },
  start() { state.count++ },
  stop()  { if (state.count > 0) state.count-- },
}
