# ⚖️ PeticIona AI — Documento Mestre do Projeto

> **Versão:** 1.0  
> **Criado em:** Maio de 2026  
> **Status atual:** 🟡 Fase de Planejamento — Análise concluída, arquitetura definida  
> **Repositório:** `github.com/[seu-usuario]/peticiona-ai` *(a criar)*

---

## 📌 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Problema que Resolve](#2-problema-que-resolve)
3. [Arquitetura Técnica](#3-arquitetura-técnica)
4. [Stack Tecnológica](#4-stack-tecnológica)
5. [Mapeamento de Modelos Disponíveis](#5-mapeamento-de-modelos-disponíveis)
6. [Fluxo de Funcionamento](#6-fluxo-de-funcionamento)
7. [Estrutura do Repositório](#7-estrutura-do-repositório)
8. [Plano de Implementação em Fases](#8-plano-de-implementação-em-fases)
9. [Status Atual e Próximos Passos](#9-status-atual-e-próximos-passos)
10. [Decisões Técnicas Registradas](#10-decisões-técnicas-registradas)
11. [Referências e Recursos](#11-referências-e-recursos)

---

## 1. Visão Geral do Projeto

**PeticIona AI** é uma plataforma web de geração automatizada de petições jurídicas com inteligência artificial. O sistema recebe dados de processos a partir de planilhas Excel ou prints de tela do sistema de gestão, identifica o tipo de petição necessário, gera o documento completo com base nos modelos do escritório, exibe em fila para revisão e exporta em Word (.docx) e PDF.

### Objetivos principais

- **Automatizar** a geração de petições repetitivas que consomem tempo do escritório
- **Padronizar** documentos com base nos modelos já existentes e validados
- **Reduzir erros** de preenchimento e formatação
- **Criar fila de revisão** para que o advogado valide antes de protocolar
- **Ser 100% web** — acessível de qualquer lugar, sem dependência de máquina local
- **Valorizar portfólio GitHub** com uma solução técnica real e relevante

---

## 2. Problema que Resolve

O escritório possui:
- Uma fila de tarefas jurídicas gerenciada em sistema de gestão próprio (tela identificada)
- **1.919 modelos de petição** em arquivos .docx organizados por processo e tipo
- **278 tipos distintos de petição** catalogados
- Um fluxo manual: advogado lê a descrição da tarefa → abre o modelo → adapta → salva → protocola

### Gargalos identificados
- Tempo gasto adaptando modelos repetitivos (Teimosinha, OJA, Planilha+GRERJ somam ~340 ocorrências sozinhos)
- Risco de inconsistência entre modelos
- Dependência de memória do operador para escolher o modelo correto
- Processo não escalável

---

## 3. Arquitetura Técnica

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                      │
│  Upload Excel/Print → Fila de Processos → Editor → Export   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP (REST)
┌────────────────────────▼────────────────────────────────────┐
│                      BACKEND (FastAPI)                       │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │  Extração   │  │  RAG Engine  │  │  Geração de Docs  │   │
│  │  de Dados   │  │  (LlamaIndex │  │  python-docx      │   │
│  │  pandas/OCR │  │  + ChromaDB) │  │  WeasyPrint       │   │
│  └──────┬──────┘  └──────┬───────┘  └─────────┬─────────┘   │
│         └────────────────▼───────────────────── ┘            │
│                    IA: Gemini 2.0 Flash                       │
│                    (geração da petição)                       │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    INFRAESTRUTURA                            │
│  Frontend: Vercel (gratuito)                                 │
│  Backend:  Render ou Railway (gratuito)                      │
│  Storage:  Supabase (500MB gratuito)                        │
└─────────────────────────────────────────────────────────────┘
```

### Estratégias de entrada de dados (3 modos)

| Modo | Como funciona | Prioridade |
|------|--------------|-----------|
| **Upload Excel/CSV** | Exporta do sistema de gestão → arrasta na plataforma | Fase 1 |
| **Upload de Print** | Tira screenshot da tela → Gemini Vision extrai dados | Fase 2 |
| **Extensão de Navegador** | Lê DOM do sistema de gestão diretamente | Fase 3 |

---

## 4. Stack Tecnológica

### Frontend
| Tecnologia | Função | Licença |
|-----------|--------|---------|
| React + Vite | Framework principal | MIT (gratuito) |
| Tailwind CSS | Estilização | MIT (gratuito) |
| TipTap | Editor rich text para edição inline das petições | MIT (gratuito) |
| Axios | Chamadas HTTP para o backend | MIT (gratuito) |

### Backend
| Tecnologia | Função | Licença |
|-----------|--------|---------|
| FastAPI | API REST principal | MIT (gratuito) |
| Uvicorn | Servidor ASGI | BSD (gratuito) |
| pandas | Leitura e processamento de Excel | BSD (gratuito) |
| openpyxl | Parsing de .xlsx | MIT (gratuito) |

### Inteligência Artificial
| Tecnologia | Função | Custo |
|-----------|--------|-------|
| **Gemini 2.0 Flash** | Geração das petições | **1.500 req/dia gratuito** |
| **Gemini Vision** | Leitura de prints/screenshots | **Incluso no tier gratuito** |
| **Groq + Llama 3.3 70B** | Fallback quando Gemini atinge limite | **~14.400 req/dia gratuito** |

### RAG (Recuperação de Modelos)
| Tecnologia | Função | Custo |
|-----------|--------|-------|
| LlamaIndex | Indexação e busca dos modelos de petição | Gratuito |
| ChromaDB | Banco vetorial para embeddings | Gratuito |
| Google Embeddings | Transformar modelos em vetores | Gratuito (tier Gemini) |

### Geração de Documentos
| Tecnologia | Função | Custo |
|-----------|--------|-------|
| python-docx | Leitura e geração de .docx | Gratuito |
| WeasyPrint | Geração de PDF | Gratuito |
| pdfplumber | Leitura de PDFs de modelos | Gratuito |

### Infraestrutura
| Serviço | Função | Plano |
|---------|--------|-------|
| Vercel | Deploy do frontend | Gratuito |
| Render ou Railway | Deploy do backend | Gratuito (com limitações de sleep) |
| Supabase | Banco de dados + armazenamento | Gratuito até 500MB |
| GitHub | Versionamento + portfólio | Gratuito |

---

## 5. Mapeamento de Modelos Disponíveis

> Análise realizada sobre **1.919 arquivos** da pasta de modelos do escritório.  
> **278 tipos únicos** identificados, agrupados em **9 categorias**.

### Resumo por categoria

| # | Categoria | Modelos | Ocorrências | Prioridade |
|---|-----------|---------|-------------|-----------|
| 1 | Penhora | 44 | 443 | 🔴 Alta |
| 2 | Planilha / GRERJ | 21 | 298 | 🔴 Alta |
| 3 | Citação | 36 | 249 | 🔴 Alta |
| 4 | Acordo / Homologação | 19 | 214 | 🔴 Alta |
| 5 | Recursos / Manifestação | 26 | 180 | 🟡 Média |
| 6 | Medidas Restritivas | 9 | 124 | 🟡 Média |
| 7 | Levantamento | 7 | 65 | 🟡 Média |
| 8 | Suspensão / Extinção | 13 | 62 | 🟢 Baixa |
| 9 | Intimação | 7 | 36 | 🟢 Baixa |
| — | Outros | 96 | 186 | 🟢 Baixa |

### Top 15 modelos por volume (MVP candidatos)

| Ranking | Tipo de Petição | Ocorrências | Fase |
|---------|----------------|-------------|------|
| 1 | PENHORA - TEIMOSINHA | 143 | MVP |
| 2 | CITAÇÃO POR OJA | 126 | MVP |
| 3 | PLANILHA + GRERJ | 107 | MVP |
| 4 | HOMOLOGAÇÃO DO ACORDO | 96 | MVP |
| 5 | ARRESTO - TEIMOSINHA | 89 | MVP |
| 6 | PLANILHA | 89 | MVP |
| 7 | LEVANTAMENTO E NOVA PENHORA | 67 | MVP |
| 8 | MANIFESTAÇÃO | 55 | MVP |
| 9 | JUNTADA DE PLANILHA | 48 | MVP |
| 10 | EXTINÇÃO - QUITAÇÃO | 47 | MVP |
| 11 | PENHORA ONLINE | 41 | Fase 2 |
| 12 | ANDAMENTO AO ACORDO | 36 | Fase 2 |
| 13 | MEDIDAS RESTRITIVAS | 33 | Fase 2 |
| 14 | RENAJUD | 33 | Fase 2 |
| 15 | SUSPENSÃO | 17 | Fase 2 |

---

## 6. Fluxo de Funcionamento

```
ENTRADA
  │
  ├── [Modo 1] Upload Excel exportado do sistema de gestão
  ├── [Modo 2] Upload de print da tela de gestão
  └── [Modo 3] Extensão de browser (futuro)
  │
  ▼
EXTRAÇÃO DE DADOS
  │  pandas lê colunas: ID, Número do Processo, Parte Contrária,
  │  Vara/Órgão, Responsável, Tipo de Tarefa, Descrição da Solicitação
  │
  ▼
IDENTIFICAÇÃO DO MODELO
  │  RAG (LlamaIndex + ChromaDB) busca qual modelo se encaixa
  │  com base na Descrição da Solicitação + Tipo de Tarefa
  │
  ▼
GERAÇÃO DA PETIÇÃO
  │  Gemini 2.0 Flash recebe:
  │   - Dados do processo
  │   - Modelo base (texto corrido do .docx)
  │   - Instrução de adaptação com base na descrição
  │  Gera petição personalizada
  │
  ▼
FILA DE REVISÃO (Frontend React)
  │  Petições geradas aparecem em cards na fila
  │  Advogado pode: Aprovar | Editar inline (TipTap) | Rejeitar
  │
  ▼
EXPORTAÇÃO
  ├── Download .docx (python-docx)
  └── Download .pdf (WeasyPrint)
```

---

## 7. Estrutura do Repositório

```
peticiona-ai/
│
├── README.md                        ← Apresentação do projeto (portfólio)
├── docker-compose.yml               ← Para rodar tudo local também
├── .env.example                     ← Variáveis de ambiente necessárias
│
├── frontend/                        ← React + Vite
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx       ← Drag-and-drop de Excel/Print
│   │   │   ├── FilaProcessos.jsx    ← Lista de processos extraídos
│   │   │   ├── CardPeticao.jsx      ← Card de petição gerada
│   │   │   ├── EditorPeticao.jsx    ← Editor TipTap para edição inline
│   │   │   ├── ExportButtons.jsx    ← Botões Word e PDF
│   │   │   └── StatusBadge.jsx      ← Status: Pendente/Gerada/Aprovada
│   │   ├── pages/
│   │   │   ├── Home.jsx             ← Dashboard principal
│   │   │   ├── Fila.jsx             ← Fila de petições
│   │   │   └── Modelos.jsx          ← Gestão dos modelos disponíveis
│   │   ├── services/
│   │   │   └── api.js               ← Chamadas ao backend
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                         ← FastAPI (Python)
│   ├── main.py                      ← Entry point
│   ├── requirements.txt
│   ├── routers/
│   │   ├── processos.py             ← Upload e extração de dados
│   │   ├── peticoes.py              ← Geração com IA
│   │   └── exportar.py              ← Download Word/PDF
│   ├── services/
│   │   ├── extrator.py              ← pandas + OCR
│   │   ├── gemini.py                ← Integração Gemini API
│   │   ├── rag.py                   ← LlamaIndex + ChromaDB
│   │   └── documentos.py            ← python-docx + WeasyPrint
│   ├── models/
│   │   └── schemas.py               ← Modelos Pydantic
│   └── core/
│       └── config.py                ← Configurações e variáveis de ambiente
│
├── modelos/                         ← Pasta com os .docx do escritório
│   ├── penhora/
│   ├── citacao/
│   ├── acordo/
│   ├── planilha_grerj/
│   └── ...
│
└── docs/
    ├── PROJETO.md                   ← Este arquivo
    ├── arquitetura.png
    └── demo.gif                     ← Para o README do portfólio
```

---

## 8. Plano de Implementação em Fases

---

### 🟢 FASE 0 — Preparação (Onde estamos agora)

**Status: ✅ Concluída**

- [x] Levantamento do problema e requisitos
- [x] Análise dos 1.919 modelos disponíveis
- [x] Identificação das 9 categorias e 278 tipos de petição
- [x] Definição da stack tecnológica (100% gratuita)
- [x] Escolha da arquitetura web (Vercel + Render + Supabase)
- [x] Criação deste documento mestre

---

### 🔵 FASE 1 — MVP (Próxima etapa)

**Meta: Sistema funcionando com os 10 modelos mais usados**  
**Prazo estimado: 3–4 semanas**

#### 1.1 Setup do repositório
- [ ] Criar repositório GitHub `peticiona-ai`
- [ ] Configurar estrutura de pastas conforme seção 7
- [ ] Criar `README.md` inicial com descrição do projeto
- [ ] Configurar `.env.example` com as variáveis necessárias
- [ ] Configurar `docker-compose.yml` para dev local

#### 1.2 Backend — Extração de dados
- [ ] Instalar FastAPI + Uvicorn + pandas + openpyxl
- [ ] Criar endpoint `POST /processos/upload-excel`
- [ ] Mapear colunas do Excel exportado do sistema de gestão:
  - ID, Número do Processo, Parte Contrária
  - Vara/Órgão, Responsável, Data
  - Tipo de Tarefa, Descrição da Solicitação
- [ ] Retornar lista de processos em JSON
- [ ] Testes unitários básicos

#### 1.3 Backend — RAG e identificação de modelos
- [ ] Instalar LlamaIndex + ChromaDB
- [ ] Organizar os 10 modelos MVP em `/modelos/`
- [ ] Indexar modelos no ChromaDB via LlamaIndex
- [ ] Criar função de matching: descrição → modelo mais similar
- [ ] Criar endpoint `POST /peticoes/identificar-modelo`

#### 1.4 Backend — Geração com Gemini
- [ ] Configurar API Key do Google Gemini
- [ ] Criar `services/gemini.py` com prompt estruturado:
  ```
  Sistema: Você é um advogado especialista em execução fiscal...
  Contexto: [dados do processo]
  Modelo base: [texto do .docx]
  Instrução: [descrição da tarefa]
  ```
- [ ] Criar endpoint `POST /peticoes/gerar`
- [ ] Implementar fallback para Groq quando limite diário atingido

#### 1.5 Backend — Exportação de documentos
- [ ] Instalar python-docx + WeasyPrint
- [ ] Criar `services/documentos.py`
- [ ] Endpoint `POST /exportar/docx` → retorna arquivo .docx
- [ ] Endpoint `POST /exportar/pdf` → retorna arquivo .pdf
- [ ] Garantir formatação: cabeçalho, rodapé, fonte padrão

#### 1.6 Frontend — Interface base
- [ ] Criar projeto React + Vite
- [ ] Configurar Tailwind CSS
- [ ] Instalar TipTap para edição
- [ ] Componente `UploadZone.jsx` — drag-and-drop do Excel
- [ ] Componente `FilaProcessos.jsx` — tabela com processos extraídos
- [ ] Componente `CardPeticao.jsx` — card com petição gerada
- [ ] Componente `EditorPeticao.jsx` — edição inline antes de exportar
- [ ] Componente `ExportButtons.jsx` — botões Word e PDF
- [ ] Conectar com backend via Axios

#### 1.7 Deploy MVP
- [ ] Deploy frontend na Vercel
- [ ] Deploy backend no Render
- [ ] Configurar variáveis de ambiente em produção
- [ ] Teste end-to-end com dados reais
- [ ] Gravar demo.gif para o README

**✅ Critério de aceite da Fase 1:**  
Usuário faz upload de Excel → sistema gera petição de Penhora Teimosinha, Citação OJA ou Homologação de Acordo → usuário edita → baixa em Word e PDF.

---

### 🟡 FASE 2 — Expansão (Após MVP validado)

**Meta: Cobrir todos os modelos de alta e média prioridade**  
**Prazo estimado: 4–6 semanas após Fase 1**

- [ ] Indexar todos os 278 modelos no ChromaDB
- [ ] Implementar leitura de print via Gemini Vision
  - [ ] Endpoint `POST /processos/upload-print`
  - [ ] OCR + extração estruturada dos campos
- [ ] Fila de processos em lote (gerar múltiplas petições de uma vez)
- [ ] Sistema de templates customizáveis (editar modelo base pela interface)
- [ ] Histórico de petições geradas
- [ ] Autenticação básica (login por usuário)
- [ ] Notificação visual quando petição está pronta

---

### 🔴 FASE 3 — Produção e Escala

**Meta: Sistema robusto, seguro e escalável**  
**Prazo estimado: A definir após Fase 2**

- [ ] Extensão de navegador Chrome para leitura direta do sistema de gestão
- [ ] Painel de gestão de modelos (upload, edição, versionamento)
- [ ] Relatórios: petições geradas por advogado, por tipo, por período
- [ ] Integração com protocolo eletrônico (se disponível no tribunal)
- [ ] Migrar para planos pagos da infraestrutura (se volume justificar)
- [ ] Suporte multiusuário com permissões por perfil
- [ ] Backup automático dos documentos gerados

---

## 9. Status Atual e Próximos Passos

### 📍 Onde estamos agora
> **Fase 0 concluída.** Planejamento completo realizado. Dados analisados. Arquitetura definida.

### ✅ O que já temos
- Análise completa dos 1.919 modelos de petição
- 278 tipos mapeados e categorizados em 9 grupos
- Top 10 modelos para o MVP definidos
- Stack tecnológica escolhida (100% gratuita)
- Arquitetura técnica desenhada
- Estrutura de repositório planejada
- Este documento mestre

### 🔜 Próximos passos imediatos (Fase 1)

| Ordem | Ação | Responsável |
|-------|------|-------------|
| 1 | Criar repositório GitHub | Você |
| 2 | Instalar Node.js + Python local | Você |
| 3 | Obter API Key do Google Gemini (gratuita) | Você |
| 4 | Separar os 10 modelos MVP em pasta local | Você |
| 5 | Iniciar backend FastAPI com Claude | Juntos |
| 6 | Testar extração do Excel exportado | Juntos |
| 7 | Configurar RAG com os modelos | Juntos |
| 8 | Construir frontend React | Juntos |
| 9 | Deploy na Vercel + Render | Juntos |

### ❓ Decisões pendentes
- [ ] Definir nome final do projeto (PeticIona AI, LexBot, outro?)
- [ ] Confirmar formato exato do Excel exportado do sistema de gestão
- [ ] Decidir se modelos .docx ficam no repositório ou num storage externo
- [ ] Definir política de segurança dos dados dos processos

---

## 10. Decisões Técnicas Registradas

| Data | Decisão | Motivo |
|------|---------|--------|
| Mai/2026 | Stack 100% gratuita | Sem custo inicial, validar antes de investir |
| Mai/2026 | Plataforma web (não desktop) | Disponibilidade ampla + portfólio GitHub |
| Mai/2026 | Gemini 2.0 Flash como IA principal | Melhor tier gratuito para geração jurídica |
| Mai/2026 | Groq + Llama como fallback | 14.400 req/dia gratuitos como backup |
| Mai/2026 | LlamaIndex + ChromaDB para RAG | Gratuitos e bem documentados |
| Mai/2026 | TipTap para editor inline | Melhor editor rich text open source |
| Mai/2026 | Vercel + Render para deploy | Gratuitos com boa DX |
| Mai/2026 | 3 modos de entrada (Excel, Print, Extensão) | Flexibilidade sem depender de integração |
| Mai/2026 | MVP com Top 10 modelos | Cobre ~70% do volume com menor esforço |

---

## 11. Referências e Recursos

### Documentações oficiais
- [FastAPI](https://fastapi.tiangolo.com/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [ChromaDB](https://docs.trychroma.com/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Groq API](https://console.groq.com/docs)
- [python-docx](https://python-docx.readthedocs.io/)
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/)
- [TipTap](https://tiptap.dev/docs)
- [Vercel Deploy](https://vercel.com/docs)
- [Render Deploy](https://render.com/docs)

### Prompts engineering jurídico (a desenvolver)
- Template de prompt para geração de petições
- Template de prompt para identificação de modelo via OCR
- Template de prompt para sumarização de descrições

---

*Documento gerado em sessão de planejamento com Claude (Anthropic) — Mai/2026*  
*Atualizar este arquivo a cada avanço significativo no projeto.*

---

## 📎 Apêndice — Premissas de desenvolvimento

> Estas premissas guiam todas as decisões técnicas do projeto e devem ser consultadas a cada nova sessão de desenvolvimento com IA.

### Economia de tokens
- **Componentes pequenos e focados** — cada arquivo faz uma coisa só
- **Sem bibliotecas de estado complexas** na Fase 1 — Vue `ref` e `emit` são suficientes
- **Pinia só na Fase 2** se o estado crescer — não antecipe complexidade
- **Prompts de IA concisos** — o prompt do Gemini usa apenas os campos necessários, sem repetição
- **Fallback simples** — Groq como backup, sem orquestração complexa de múltiplos modelos
- **CSS via Tailwind utilities** — sem CSS custom desnecessário, classes reutilizáveis via `@apply`
- **Vue `<script setup>`** sempre — é a forma mais concisa do Vue 3, sem boilerplate

### Segurança
- **API Keys somente no `.env`** — jamais hardcoded, jamais no repositório
- **`.env` no `.gitignore`** — verificar antes de cada commit
- **CORS restrito** — em produção, apenas o domínio Vercel autorizado
- **Rate limiting** em todas as rotas de IA — evita abuso e estouro do tier gratuito
- **Validação de upload** — extensão e tamanho verificados antes de processar
- **Dados de processos não persistidos** — sem banco de dados de documentos jurídicos no MVP
- **`docs_url` desabilitado em produção** — Swagger inacessível em ambiente público
- **Métodos HTTP restritos** — apenas GET e POST no CORS
- **Sem logs de conteúdo jurídico** — logs apenas de erros e métricas, não de conteúdo

### Arquitetura
- **Vue 3 + FastAPI** — frontend e backend desacoplados, comunicam via REST
- **Proxy Vite em dev** — `/api` redireciona para `localhost:8000`, sem CORS local
- **Serviço de API centralizado** — `api.js` é o único ponto de chamada HTTP no frontend
- **`lru_cache` no config** — settings lidos uma vez, sem I/O repetido
- **ChromaDB local** — banco vetorial no próprio servidor, sem dependência externa
- **Fallback keyword** no RAG — se ChromaDB falhar, busca por palavras-chave nos nomes dos arquivos

### Fluxo de trabalho com IA (Claude)
- Ao iniciar nova sessão: **anexar este documento** para retomar contexto
- Indicar sempre **em qual fase e etapa** estamos antes de pedir código
- Preferir **modificações cirúrgicas** a reescritas completas
- Confirmar **antes de alterar arquivos já funcionando**
