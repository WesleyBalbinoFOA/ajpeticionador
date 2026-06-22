<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from './services/api.js'
import LoginPage     from './components/LoginPage.vue'
import UploadZone    from './components/UploadZone.vue'
import FilaProcessos from './components/FilaProcessos.vue'
import FilaPeticoes  from './components/FilaPeticoes.vue'
import Dashboard     from './components/Dashboard.vue'
import LoadingModal  from './components/LoadingModal.vue'

const usuario     = ref(null)
const etapa       = ref('upload')
const processos   = ref([])
const peticoes    = ref([])
const paginaAtual = ref('peticionar')

// Restaura sessão ao carregar
onMounted(() => {
  const u = api.usuarioSalvo()
  if (u) usuario.value = u
})

function onLogin(user)  { usuario.value = user }
function onLogout()     { api.logout(); usuario.value = null; etapa.value = 'upload' }
function onProcessosExtraidos(lista) { processos.value = lista; etapa.value = 'processos' }
function onPeticoesGeradas(lista)    { peticoes.value = lista;  etapa.value = 'peticoes'  }
function voltar() { etapa.value = etapa.value === 'peticoes' ? 'processos' : 'upload' }

const etapaIdx = computed(() => ({ upload:1, processos:2, peticoes:3 }[etapa.value]))
const ETAPAS   = ['Upload','Processos','Revisão']

const S = {
  header: 'background:#003087;border-bottom:3px solid #C9A84C;font-family:"DM Sans",system-ui,sans-serif',
  inner:  'max-width:1280px;margin:0 auto;padding:0 1.5rem;display:flex;align-items:center;height:56px;gap:1rem',
  logo:   'background:#C9A84C;width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center',
  logoTxt:'color:#003087;font-weight:800;font-size:11px;letter-spacing:0.5px',
  appName:'color:white;font-size:15px;font-weight:600;font-family:"Playfair Display",serif',
  navBtn: (active) => `padding:6px 14px;border-radius:6px;font-size:13px;font-weight:500;border:none;cursor:pointer;transition:all 0.15s;font-family:"DM Sans",system-ui,sans-serif;${active?'background:#C9A84C;color:#003087':'background:transparent;color:rgba(255,255,255,0.65)'}`,
  step:   (active) => `font-size:12px;font-weight:${active?'600':'400'};color:${active?'#C9A84C':'rgba(255,255,255,0.4)'}`,
  avatar: 'width:32px;height:32px;border-radius:50%;background:#C9A84C;display:flex;align-items:center;justify-content:center;color:#003087;font-weight:700;font-size:12px;flex-shrink:0',
  main:   'max-width:1280px;margin:0 auto;padding:2rem 1.5rem;font-family:"DM Sans",system-ui,sans-serif',
  footer: 'text-align:center;padding:1rem;font-size:12px;color:#9BA8BB;border-top:1px solid #DDE3EF;font-family:"DM Sans",system-ui,sans-serif',
}
</script>

<template>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet"/>
  <LoadingModal />
  <LoginPage v-if="!usuario" @login="onLogin" />
  <div v-else style="min-height:100vh;display:flex;flex-direction:column;background:#F4F6FA">
    <header :style="S.header">
      <div :style="S.inner">
        <div style="display:flex;align-items:center;gap:10px;flex-shrink:0">
          <div :style="S.logo"><span :style="S.logoTxt">FOA</span></div>
          <span :style="S.appName">PeticIona AI</span>
        </div>
        <div style="width:1px;height:24px;background:rgba(255,255,255,0.15);margin:0 4px"></div>
        <nav style="display:flex;gap:4px">
          <button :style="S.navBtn(paginaAtual==='peticionar')" @click="paginaAtual='peticionar'">⚖️ Peticionamento</button>
          <button :style="S.navBtn(paginaAtual==='dashboard')"  @click="paginaAtual='dashboard'">📊 Dashboard</button>
        </nav>
        <div v-if="paginaAtual==='peticionar'" style="display:flex;align-items:center;gap:8px;margin-left:8px">
          <template v-for="(label,idx) in ETAPAS" :key="label">
            <span :style="S.step(etapaIdx===idx+1)">{{ idx+1 }}. {{ label }}</span>
            <span v-if="idx<2" style="color:rgba(255,255,255,0.2);font-size:12px">›</span>
          </template>
        </div>
        <div style="margin-left:auto;display:flex;align-items:center;gap:10px">
          <div style="text-align:right">
            <div style="color:white;font-size:13px;font-weight:500;line-height:1">
              {{ usuario.nome.split(' ')[0] }} {{ usuario.nome.split(' ').slice(-1)[0] }}
            </div>
            <div style="color:rgba(255,255,255,0.4);font-size:11px;margin-top:2px">{{ usuario.oab }}</div>
          </div>
          <div :style="S.avatar">{{ usuario.nome.charAt(0) }}</div>
          <button :style="'color:rgba(255,255,255,0.4);font-size:12px;background:transparent;border:none;cursor:pointer;font-family:inherit;padding:4px 8px;border-radius:6px'"
                  @click="onLogout"
                  @mouseover="e=>e.target.style.color='white'"
                  @mouseout="e=>e.target.style.color='rgba(255,255,255,0.4)'">Sair</button>
        </div>
      </div>
    </header>
    <main style="flex:1">
      <div :style="S.main">
        <Dashboard    v-if="paginaAtual==='dashboard'" :usuario="usuario" />
        <template v-else>
          <UploadZone    v-if="etapa==='upload'"    :usuario="usuario" @processos-extraidos="onProcessosExtraidos" />
          <FilaProcessos v-if="etapa==='processos'" :processos="processos" @peticoes-geradas="onPeticoesGeradas" @voltar="voltar" />
          <FilaPeticoes  v-if="etapa==='peticoes'"  :peticoes="peticoes" :usuario="usuario" @voltar="voltar" />
        </template>
      </div>
    </main>
    <footer :style="S.footer">Fundação Oswaldo Aranha · Assessoria Jurídica · PeticIona AI v1.0</footer>
  </div>
</template>
