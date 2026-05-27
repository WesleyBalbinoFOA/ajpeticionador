# backend/models/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Processo(BaseModel):
    """Dados extraídos do Excel do sistema de gestão."""
    id: str
    numero: str
    parte_contraria: str
    vara_orgao: str
    responsavel: str
    data: Optional[str] = None
    tipo_tarefa: str
    descricao_solicitacao: str
    cliente: Optional[str] = None


class PeticaoGerada(BaseModel):
    """Petição gerada pela IA."""
    processo_id: str
    numero: str
    tipo_modelo: str
    conteudo: str
    modelo_usado: str
    status: str = "pendente"   # pendente | aprovada | rejeitada
    gerada_em: Optional[datetime] = None


class SolicitacaoGeracao(BaseModel):
    """Payload para solicitar geração de petição."""
    processo: Processo
    forcar_modelo: Optional[str] = None   # sobrescreve o RAG se informado


class RespostaExportacao(BaseModel):
    """Resposta após exportar documento."""
    formato: str   # docx | pdf
    nome_arquivo: str
    tamanho_bytes: int
