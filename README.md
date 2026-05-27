# ⚖️ PeticIona AI

> Plataforma web de geração automatizada de petições jurídicas com Inteligência Artificial.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.4-brightgreen)](https://vuejs.org)
[![Licença](https://img.shields.io/badge/Licença-MIT-yellow)]()

---

## 🎯 O que é

O PeticIona AI lê a fila de tarefas do sistema de gestão jurídica (via Excel exportado ou print de tela), identifica o tipo de petição necessário, gera o documento completo com base nos modelos do escritório usando IA, exibe em fila para revisão e exporta em Word (.docx) e PDF.

---

## 🚀 Começando

### Pré-requisitos instalados automaticamente

```bash
git clone https://github.com/seu-usuario/peticiona-ai
cd peticiona-ai
cp .env.example .env        # preencha sua API Key do Gemini
make setup                  # instala Python 3.11, Node 20 e dependências
make dev                    # sobe backend + frontend juntos
```

Acesse: **http://localhost:5173**

---

## 🏗️ Arquitetura

```
Upload Excel/Print
      ↓
FastAPI (extração com pandas)
      ↓
RAG: LlamaIndex + ChromaDB (identifica modelo)
      ↓
Gemini 2.0 Flash (gera petição)
      ↓
Vue 3 (fila de revisão + edição inline)
      ↓
python-docx + WeasyPrint (exporta Word e PDF)
```

---

## 🧰 Stack

| Camada | Tecnologia | Motivo |
|--------|-----------|--------|
| Backend | FastAPI + Python 3.11 | Rápido, tipado, async nativo |
| Frontend | Vue 3 + Vite + Tailwind | Conciso, sem overhead de hooks |
| IA Principal | Gemini 2.0 Flash | 1.500 req/dia gratuito |
| IA Fallback | Groq + Llama 3.3 70B | 14.400 req/dia gratuito |
| RAG | LlamaIndex + ChromaDB | Busca semântica dos modelos |
| Documentos | python-docx + WeasyPrint | Geração Word e PDF |
| Deploy Frontend | Vercel | Gratuito |
| Deploy Backend | Render | Gratuito |
| Banco/Storage | Supabase | 500MB gratuito |

---

## 📁 Modelos disponíveis

278 tipos de petição mapeados em 9 categorias a partir de 1.919 modelos do escritório:

| Categoria | Modelos | Volume |
|-----------|---------|--------|
| Penhora | 44 | 443 ocorrências |
| Planilha / GRERJ | 21 | 298 ocorrências |
| Citação | 36 | 249 ocorrências |
| Acordo / Homologação | 19 | 214 ocorrências |
| Recursos / Manifestação | 26 | 180 ocorrências |
| Medidas Restritivas | 9 | 124 ocorrências |
| Levantamento | 7 | 65 ocorrências |
| Suspensão / Extinção | 13 | 62 ocorrências |
| Intimação | 7 | 36 ocorrências |

---

## 📋 Fluxo de uso

1. Exporte a planilha do sistema de gestão (.xlsx)
2. Faça upload na plataforma
3. Aguarde a IA gerar as petições em fila
4. Revise e edite inline se necessário
5. Baixe em Word ou PDF

---

## 🗺️ Roadmap

- [x] Análise e mapeamento dos modelos
- [x] Definição de arquitetura
- [ ] **MVP** — Top 10 modelos + upload Excel + exportação
- [ ] Fase 2 — Leitura de prints, todos os modelos, autenticação
- [ ] Fase 3 — Extensão de browser, painel de gestão, relatórios

---

## 🔐 Segurança

- Variáveis sensíveis exclusivamente via `.env` (nunca no código)
- `.env` no `.gitignore` — jamais sobe para o repositório
- Dados dos processos não são armazenados permanentemente no servidor
- Rate limiting nas rotas de geração de IA
- CORS restrito ao domínio do frontend em produção

---

## 🤝 Desenvolvido com

- [FastAPI](https://fastapi.tiangolo.com)
- [Vue 3](https://vuejs.org)
- [Google Gemini](https://ai.google.dev)
- [LlamaIndex](https://llamaindex.ai)
- [python-docx](https://python-docx.readthedocs.io)

---

*Projeto desenvolvido em parceria com Claude (Anthropic) — 2026*
