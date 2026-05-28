# backend/routers/auth.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from core.auth import hash_senha, verificar_senha, criar_token, usuario_atual
from core.supabase import get_supabase

router = APIRouter()


class LoginPayload(BaseModel):
    email: str
    senha: str


class CriarUsuarioPayload(BaseModel):
    nome:   str
    email:  str
    senha:  str
    oab:    str
    perfil: str = "advogado"


@router.post("/login")
def login(payload: LoginPayload):
    sb = get_supabase()
    res = sb.table("usuarios").select("*").eq("email", payload.email.lower()).execute()

    if not res.data:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    user = res.data[0]

    if not verificar_senha(payload.senha, user["senha_hash"]):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    if not user.get("ativo", True):
        raise HTTPException(status_code=403, detail="Usuário inativo.")

    token = criar_token({
        "sub":    str(user["id"]),
        "nome":   user["nome"],
        "email":  user["email"],
        "oab":    user["oab"],
        "perfil": user["perfil"],
    })

    # Registra último acesso
    sb.table("usuarios").update({"ultimo_acesso": "now()"}).eq("id", user["id"]).execute()

    return {
        "token":  token,
        "usuario": {
            "id":    user["id"],
            "nome":  user["nome"],
            "email": user["email"],
            "oab":   user["oab"],
            "perfil":user["perfil"],
        }
    }


@router.get("/me")
def me(usuario: dict = Depends(usuario_atual)):
    """Retorna dados do usuário autenticado."""
    return usuario


@router.post("/usuarios", dependencies=[Depends(usuario_atual)])
def criar_usuario(payload: CriarUsuarioPayload, usuario: dict = Depends(usuario_atual)):
    """Cria novo usuário — apenas admins."""
    if usuario.get("perfil") != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem criar usuários.")

    sb = get_supabase()

    # Verifica se email já existe
    existe = sb.table("usuarios").select("id").eq("email", payload.email.lower()).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    novo = sb.table("usuarios").insert({
        "nome":        payload.nome,
        "email":       payload.email.lower(),
        "senha_hash":  hash_senha(payload.senha),
        "oab":         payload.oab,
        "perfil":      payload.perfil,
        "ativo":       True,
    }).execute()

    return {"mensagem": "Usuário criado.", "id": novo.data[0]["id"]}


@router.get("/usuarios", dependencies=[Depends(usuario_atual)])
def listar_usuarios(usuario: dict = Depends(usuario_atual)):
    """Lista usuários — apenas admins."""
    if usuario.get("perfil") != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado.")

    sb = get_supabase()
    res = sb.table("usuarios").select("id,nome,email,oab,perfil,ativo,ultimo_acesso").execute()
    return res.data
