# backend/routers/processos.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from slowapi.util import get_remote_address
from slowapi import Limiter

from services.extrator import extrair_processos_excel
from core.config import get_settings

settings = get_settings()
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/upload-excel")
@limiter.limit("20/minute")
async def upload_excel(request: Request, arquivo: UploadFile = File(...)):
    """
    Recebe Excel exportado do sistema de gestão.
    Retorna lista de processos extraídos.
    """
    # Valida extensão
    extensao = arquivo.filename.split(".")[-1].lower()
    if extensao not in settings.extensions_list:
        raise HTTPException(
            status_code=400,
            detail=f"Formato não permitido: .{extensao}"
        )

    # Valida tamanho
    conteudo = await arquivo.read()
    if len(conteudo) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Arquivo muito grande. Máximo: {settings.max_upload_mb}MB"
        )

    try:
        processos = extrair_processos_excel(conteudo)
        return {
            "total": len(processos),
            "processos": processos
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Erro ao processar arquivo: {str(e)}")
