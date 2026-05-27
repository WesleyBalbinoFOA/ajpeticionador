# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.config import get_settings
from routers import processos, peticoes, exportar

settings = get_settings()

# --- Rate limiter ---
limiter = Limiter(key_func=get_remote_address)

# --- App ---
app = FastAPI(
    title="PeticIona AI",
    description="Geração automatizada de petições jurídicas com IA",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url=None,
)

# --- Segurança: CORS restrito ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST"],   # apenas o necessário
    allow_headers=["*"],
)

# --- Rate limiting ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Rotas ---
app.include_router(processos.router, prefix="/processos", tags=["Processos"])
app.include_router(peticoes.router, prefix="/peticoes", tags=["Petições"])
app.include_router(exportar.router, prefix="/exportar", tags=["Exportar"])


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}
