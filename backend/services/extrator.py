# backend/services/extrator.py
# Lê o Excel exportado do sistema de gestão e retorna lista de processos
# Suporta .xlsx e .xls — cabeçalho detectado automaticamente

import pandas as pd
import io
from models.schemas import Processo

# Mapeamento de colunas conforme export real do sistema
MAPA_COLUNAS = {
    "id":                    ["(Processo) ID", "ID"],
    "numero":                ["(Processo) Número", "Número", "Numero"],
    "parte_contraria":       ["(Processo) Parte Contrária", "Parte Contrária"],
    "vara_orgao":            ["(Processo) Vara/Órgão", "Vara/Órgão", "Vara"],
    "responsavel":           ["Responsável", "Responsavel"],
    "data":                  ["Data"],
    "tipo_tarefa":           ["Tipo de Tarefa", "Subtipo"],
    "descricao_solicitacao": ["Descrição da Solicitação", "Descrição"],
    "cliente":               ["(Processo) Cliente", "Cliente"],
}


def _encontrar_coluna(df: pd.DataFrame, opcoes: list[str]) -> str | None:
    for op in opcoes:
        if op in df.columns:
            return op
    return None


def _detectar_header(conteudo: bytes, engine: str) -> int:
    """Detecta em qual linha está o cabeçalho real da planilha."""
    df_raw = pd.read_excel(io.BytesIO(conteudo), header=None, engine=engine, nrows=10)
    for i, row in df_raw.iterrows():
        valores = [str(v) for v in row if str(v).strip()]
        # Linha de cabeçalho contém colunas conhecidas
        if any("Processo" in v or "Responsável" in v or "Status" in v for v in valores):
            return i
    return 0


def extrair_processos_excel(conteudo: bytes) -> list[dict]:
    """
    Lê Excel (.xlsx ou .xls) em memória.
    Detecta automaticamente a linha do cabeçalho.
    Retorna lista de processos como dicts.
    """
    # Detecta engine pelo magic bytes
    engine = "xlrd" if conteudo[:8] != b'\x50\x4b\x03\x04' and conteudo[:2] == b'\xd0\xcf' else "openpyxl"
    # Fallback seguro
    try:
        header_row = _detectar_header(conteudo, engine)
    except Exception:
        engine = "xlrd"
        header_row = _detectar_header(conteudo, engine)

    df = pd.read_excel(
        io.BytesIO(conteudo),
        header=header_row,
        engine=engine,
        dtype=str
    )
    df = df.fillna("")

    processos = []
    for i, row in df.iterrows():
        dados = {}
        for campo, opcoes in MAPA_COLUNAS.items():
            col = _encontrar_coluna(df, opcoes)
            dados[campo] = str(row[col]).strip() if col else ""

        if not dados.get("numero") or dados["numero"] in ("", "nan"):
            continue

        # ID: remove .0 de números float
        if dados.get("id"):
            dados["id"] = dados["id"].replace(".0", "")
        else:
            dados["id"] = str(i)

        # Tipo de tarefa: usa Subtipo se Tipo de Tarefa estiver vazio
        if not dados.get("tipo_tarefa") or dados["tipo_tarefa"] in ("", "nan"):
            col_subtipo = _encontrar_coluna(df, ["Subtipo"])
            if col_subtipo:
                dados["tipo_tarefa"] = str(row[col_subtipo]).strip()

        processos.append(Processo(**dados).model_dump())

    return processos