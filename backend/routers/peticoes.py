# backend/routers/peticoes.py

from fastapi import APIRouter, HTTPException, Request
from slowapi.util import get_remote_address
from slowapi import Limiter

from models.schemas import SolicitacaoGeracao, PeticaoGerada
from services.gemini import gerar_peticao
from services.rag import identificar_modelo
from datetime import datetime

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


@router.post("/gerar", response_model=PeticaoGerada)
@limiter.limit("30/minute")
async def gerar(request: Request, solicitacao: SolicitacaoGeracao):
    processo = solicitacao.processo

    if solicitacao.forcar_modelo:
        modelo_nome = solicitacao.forcar_modelo
        modelo_texto = identificar_modelo(processo.descricao_solicitacao, forcar=modelo_nome)
    else:
        modelo_nome, modelo_texto = identificar_modelo(processo.descricao_solicitacao)

    if not modelo_texto:
        raise HTTPException(status_code=404, detail="Nenhum modelo encontrado.")

    try:
        conteudo = await gerar_peticao(processo, modelo_texto)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro na geração: {str(e)}")

    return PeticaoGerada(
        processo_id=processo.id,
        numero=processo.numero,
        tipo_modelo=modelo_nome,
        conteudo=conteudo,
        modelo_usado=modelo_nome,
        status="pendente",
        gerada_em=datetime.now(),
    )


@router.post("/gerar-lote")
@limiter.limit("5/minute")
async def gerar_lote(request: Request, solicitacoes: list[SolicitacaoGeracao]):
    if len(solicitacoes) > 20:
        raise HTTPException(status_code=400, detail="Máximo de 20 processos por lote.")

    resultados = []
    for s in solicitacoes:
        try:
            modelo_nome, modelo_texto = identificar_modelo(s.processo.descricao_solicitacao)
            conteudo = await gerar_peticao(s.processo, modelo_texto)
            resultados.append({
                "processo_id": s.processo.id,
                "numero": s.processo.numero,          # ← adicionado
                "parte_contraria": s.processo.parte_contraria,  # ← adicionado
                "status": "gerada",
                "conteudo": conteudo,
                "parte_contraria": s.processo.parte_contraria,
                "modelo_usado": modelo_nome,
            })
        except Exception as e:
            resultados.append({
                "processo_id": s.processo.id,
                "numero": s.processo.numero,          # ← adicionado
                "status": "erro",
                "erro": str(e),
                "conteudo": "",
                "modelo_usado": "",
            })

    return {"total": len(resultados), "resultados": resultados}