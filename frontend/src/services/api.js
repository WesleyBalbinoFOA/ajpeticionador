// frontend/src/services/api.js
// Ponto único de comunicação com o backend — facilita manutenção

import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 60000,   // 60s para geração de IA
})

export const api = {
  // Processos
  async uploadExcel(arquivo) {
    const form = new FormData()
    form.append('arquivo', arquivo)
    const { data } = await http.post('/processos/upload-excel', form)
    return data
  },

  // Petições
  async gerarPeticao(processo) {
    const { data } = await http.post('/peticoes/gerar', { processo })
    return data
  },

  async gerarLote(processos) {
    const solicitacoes = processos.map(p => ({ processo: p }))
    const { data } = await http.post('/peticoes/gerar-lote', solicitacoes)
    return data
  },

  // Exportação
  async baixarDocx(numero, conteudo) {
    const resp = await http.post('/exportar/docx', { numero, conteudo }, {
      responseType: 'blob'
    })
    _download(resp, `peticao_${numero.replace(/\//g, '-')}.docx`)
  },

  async baixarPdf(numero, conteudo) {
    const resp = await http.post('/exportar/pdf', { numero, conteudo }, {
      responseType: 'blob'
    })
    _download(resp, `peticao_${numero.replace(/\//g, '-')}.pdf`)
  },
}

// Utilitário interno de download via blob
function _download(response, nomeArquivo) {
  const url = URL.createObjectURL(new Blob([response.data]))
  const a = document.createElement('a')
  a.href = url
  a.download = nomeArquivo
  a.click()
  URL.revokeObjectURL(url)
}
