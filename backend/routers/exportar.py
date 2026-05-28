# backend/routers/exportar.py

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from slowapi.util import get_remote_address
from slowapi import Limiter
from pydantic import BaseModel
from typing import Optional
import io

from services.documentos import gerar_docx, gerar_pdf
from core.sanitizer import limpar_para_xml

limiter = Limiter(key_func=get_remote_address)
router  = APIRouter()


class PayloadExportar(BaseModel):
    numero: str
    conteudo: str
    parte_contraria: Optional[str] = None


@router.post("/docx")
@limiter.limit("30/minute")
async def exportar_docx(request: Request, payload: PayloadExportar):
    try:
        conteudo = limpar_para_xml(payload.conteudo)
        parte    = limpar_para_xml(payload.parte_contraria or '')
        buffer   = gerar_docx(payload.numero, conteudo, parte or None)
        nome     = f"peticao_{payload.numero.replace('/', '-')}.docx"
        return StreamingResponse(
            io.BytesIO(buffer),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={nome}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar Word: {str(e)}")


@router.post("/pdf")
@limiter.limit("30/minute")
async def exportar_pdf(request: Request, payload: PayloadExportar):
    try:
        conteudo = limpar_para_xml(payload.conteudo)
        parte    = limpar_para_xml(payload.parte_contraria or '')
        buffer   = gerar_pdf(payload.numero, conteudo, parte or None)
        nome     = f"peticao_{payload.numero.replace('/', '-')}.pdf"
        return StreamingResponse(
            io.BytesIO(buffer),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={nome}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")