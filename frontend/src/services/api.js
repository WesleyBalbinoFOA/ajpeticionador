// frontend/src/services/api.js
import axios from 'axios'

const http = axios.create({ baseURL: '/api', timeout: 60000 })

// Injeta JWT automaticamente em todas as requisições
http.interceptors.request.use(config => {
  const token = localStorage.getItem('peticiona_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Se 401, limpa token e redireciona para login
http.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('peticiona_token')
      localStorage.removeItem('peticiona_usuario')
      window.location.reload()
    }
    return Promise.reject(err)
  }
)

export const api = {
  // Auth
  async login(email, senha) {
    const { data } = await http.post('/auth/login', { email, senha })
    localStorage.setItem('peticiona_token',   data.token)
    localStorage.setItem('peticiona_usuario', JSON.stringify(data.usuario))
    return data.usuario
  },

  logout() {
    localStorage.removeItem('peticiona_token')
    localStorage.removeItem('peticiona_usuario')
  },

  usuarioSalvo() {
    const u = localStorage.getItem('peticiona_usuario')
    return u ? JSON.parse(u) : null
  },

  // Processos
  async uploadExcel(arquivo) {
    const form = new FormData()
    form.append('arquivo', arquivo)
    const { data } = await http.post('/processos/upload-excel', form)
    return data
  },

  // Petições
  async gerarLote(processos) {
    const { data } = await http.post('/peticoes/gerar-lote', processos.map(p => ({ processo: p })))
    return data
  },

  // Exportação
  async baixarDocx(numero, conteudo, parte_contraria) {
    const resp = await http.post('/exportar/docx', { numero, conteudo, parte_contraria }, { responseType: 'blob' })
    _download(resp, `peticao_${numero.replace(/\//g,'-')}.docx`)
  },

  async baixarPdf(numero, conteudo, parte_contraria) {
    const resp = await http.post('/exportar/pdf', { numero, conteudo, parte_contraria }, { responseType: 'blob' })
    _download(resp, `peticao_${numero.replace(/\//g,'-')}.pdf`)
  },

  // Histórico RLHF
  async salvarHistorico(registro) {
    try {
      await http.post('/historico', registro)
    } catch {
      // fallback localStorage
      const h = JSON.parse(localStorage.getItem('peticiona_historico') || '[]')
      h.push({ ...registro, data: new Date().toISOString() })
      localStorage.setItem('peticiona_historico', JSON.stringify(h))
    }
  },
}

function _download(response, nome) {
  const url = URL.createObjectURL(new Blob([response.data]))
  const a = document.createElement('a')
  a.href = url; a.download = nome; a.click()
  URL.revokeObjectURL(url)
}
