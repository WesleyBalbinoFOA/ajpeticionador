<script setup>
import { ref } from 'vue'
import { api } from '../services/api.js'

const emit     = defineEmits(['login'])
const email    = ref('')
const senha    = ref('')
const erro     = ref('')
const carregando = ref(false)

async function entrar() {
  if (!email.value || !senha.value) { erro.value = 'Preencha e-mail e senha.'; return }
  erro.value   = ''
  carregando.value = true
  try {
    const usuario = await api.login(email.value, senha.value)
    emit('login', usuario)
  } catch (e) {
    erro.value = e.response?.data?.detail || 'Erro ao conectar. Tente novamente.'
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <div style="min-height:100vh;display:flex;align-items:center;justify-content:center;
              background:linear-gradient(135deg,#001a4d 0%,#003087 55%,#1a5276 100%);
              font-family:'DM Sans',system-ui,sans-serif;padding:1rem">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet"/>
    <div style="width:100%;max-width:420px">
      <div style="background:white;border-radius:20px;overflow:hidden;box-shadow:0 25px 60px rgba(0,0,0,0.3)">
        <div style="background:#003087;padding:2rem 2.5rem;border-bottom:3px solid #C9A84C">
          <div style="display:flex;align-items:center;gap:1rem">
            <div style="background:#C9A84C;width:44px;height:44px;border-radius:10px;display:flex;align-items:center;justify-content:center">
              <span style="color:#003087;font-weight:800;font-size:14px;letter-spacing:0.5px">FOA</span>
            </div>
            <div>
              <div style="color:rgba(255,255,255,0.55);font-size:10px;letter-spacing:2px;text-transform:uppercase;font-weight:500">Assessoria Jurídica</div>
              <div style="color:white;font-size:16px;font-weight:600;font-family:'Playfair Display',serif;line-height:1.2">PeticIona AI</div>
            </div>
          </div>
        </div>
        <div style="padding:2rem 2.5rem 2.5rem">
          <h2 style="margin:0 0 0.25rem;font-size:22px;font-weight:700;color:#003087;font-family:'Playfair Display',serif">Bem-vindo</h2>
          <p style="margin:0 0 1.75rem;color:#6B7A9A;font-size:14px">Acesse com suas credenciais</p>
          <div style="margin-bottom:1rem">
            <label style="display:block;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#003087;margin-bottom:6px">E-mail</label>
            <input v-model="email" type="email" placeholder="seu@foa.org.br" @keyup.enter="entrar"
                   style="width:100%;padding:12px 14px;border:1.5px solid #DDE3EF;border-radius:10px;font-size:14px;color:#1A2340;outline:none;font-family:inherit;box-sizing:border-box"
                   @focus="e=>e.target.style.borderColor='#003087'"
                   @blur="e=>e.target.style.borderColor='#DDE3EF'" />
          </div>
          <div style="margin-bottom:1.25rem">
            <label style="display:block;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#003087;margin-bottom:6px">Senha</label>
            <input v-model="senha" type="password" placeholder="••••••••" @keyup.enter="entrar"
                   style="width:100%;padding:12px 14px;border:1.5px solid #DDE3EF;border-radius:10px;font-size:14px;color:#1A2340;outline:none;font-family:inherit;box-sizing:border-box"
                   @focus="e=>e.target.style.borderColor='#003087'"
                   @blur="e=>e.target.style.borderColor='#DDE3EF'" />
          </div>
          <div v-if="erro" style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;padding:10px 14px;margin-bottom:1rem;font-size:13px;color:#991B1B">
            {{ erro }}
          </div>
          <button @click="entrar" :disabled="carregando"
                  style="width:100%;padding:13px;background:#003087;color:white;border:none;border-radius:10px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:background 0.2s"
                  @mouseover="e=>!carregando&&(e.target.style.background='#0051A5')"
                  @mouseout="e=>e.target.style.background='#003087'">
            {{ carregando ? 'Entrando...' : 'Entrar' }}
          </button>
          <p style="text-align:center;margin:1.5rem 0 0;font-size:12px;color:#9BA8BB">Acesso restrito · Assessoria Jurídica FOA</p>
        </div>
      </div>
      <p style="text-align:center;margin-top:1.5rem;font-size:12px;color:rgba(255,255,255,0.35)">Fundação Oswaldo Aranha · {{ new Date().getFullYear() }}</p>
    </div>
  </div>
</template>
