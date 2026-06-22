# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from core.config import get_settings
from routers import processos, peticoes, exportar, auth as auth_router

settings = get_settings()
limiter  = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="PeticIona AI",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Erro interno no servidor."})

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router.router, prefix="/auth",      tags=["Auth"])
app.include_router(processos.router,   prefix="/processos", tags=["Processos"])
app.include_router(peticoes.router,    prefix="/peticoes",  tags=["Petições"])
app.include_router(exportar.router,    prefix="/exportar",  tags=["Exportar"])


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}
