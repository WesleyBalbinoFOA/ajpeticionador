# backend/core/auth.py
# JWT + bcrypt para autenticação

import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import get_settings

settings = get_settings()
bearer   = HTTPBearer()

JWT_ALGO  = "HS256"
JWT_HORAS = 8


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha: str, hash_: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_.encode())


def criar_token(payload: dict) -> str:
    data = payload.copy()
    data["exp"] = datetime.utcnow() + timedelta(hours=JWT_HORAS)
    return jwt.encode(data, settings.secret_key, algorithm=JWT_ALGO)


def verificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sessão expirada. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")


def usuario_atual(credentials: HTTPAuthorizationCredentials = Security(bearer)) -> dict:
    """Dependency — injeta usuário autenticado nas rotas protegidas."""
    return verificar_token(credentials.credentials)
