# =============================================================
# PeticIona AI — Makefile
# =============================================================
# Comandos disponíveis:
#   make setup     → instala tudo (primeira vez)
#   make dev       → sobe backend + frontend juntos
#   make backend   → sobe só o backend
#   make frontend  → sobe só o frontend
#   make install   → reinstala dependências
#   make index     → indexa modelos de petição no ChromaDB
#   make lint      → verifica qualidade do código
#   make clean     → limpa arquivos temporários
# =============================================================

.PHONY: setup dev backend frontend install index lint clean

# --- Detecta SO para comandos corretos ---
ifeq ($(OS),Windows_NT)
    PYTHON=python
    VENV_ACTIVATE=.venv\Scripts\activate
    SEP=&
else
    PYTHON=python3
    VENV_ACTIVATE=source .venv/bin/activate
    SEP=;
endif

# --- Setup completo (primeira vez) ---
setup:
	@echo "🔧 Verificando Python..."
	@$(PYTHON) --version || (echo "❌ Python não encontrado. Instale em https://python.org" && exit 1)
	@echo "🔧 Verificando Node..."
	@node --version || (echo "❌ Node não encontrado. Instale em https://nodejs.org" && exit 1)
	@echo "📦 Criando ambiente virtual Python..."
	@$(PYTHON) -m venv .venv
	@echo "📦 Instalando dependências do backend..."
	@. .venv/bin/activate && pip install --upgrade pip && pip install -r backend/requirements.txt
	@echo "📦 Instalando dependências do frontend..."
	@cd frontend && npm install
	@echo "⚙️  Criando .env se não existir..."
	@test -f .env || cp .env.example .env
	@echo ""
	@echo "✅ Setup concluído!"
	@echo "👉 Edite o arquivo .env e adicione sua GEMINI_API_KEY"
	@echo "👉 Depois rode: make dev"

# --- Desenvolvimento (backend + frontend juntos) ---
dev:
	@echo "🚀 Subindo PeticIona AI..."
	@make -j2 backend frontend

# --- Backend ---
backend:
	@echo "⚙️  Backend rodando em http://localhost:8000"
	@. .venv/bin/activate && cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# --- Frontend ---
frontend:
	@echo "🖥️  Frontend rodando em http://localhost:5173"
	@cd frontend && npm run dev

# --- Reinstalar dependências ---
install:
	@. .venv/bin/activate && pip install -r backend/requirements.txt
	@cd frontend && npm install

# --- Indexar modelos no ChromaDB ---
index:
	@echo "📚 Indexando modelos de petição..."
	@. .venv/bin/activate && python backend/services/indexar_modelos.py
	@echo "✅ Modelos indexados!"

# --- Lint ---
lint:
	@. .venv/bin/activate && ruff check backend/
	@cd frontend && npm run lint

# --- Limpar temporários ---
clean:
	@echo "🧹 Limpando..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf backend/uploads/*.tmp 2>/dev/null || true
	@echo "✅ Limpo!"
