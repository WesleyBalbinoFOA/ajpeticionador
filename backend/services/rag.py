# backend/services/rag.py
# Busca semantica usando ChromaDB diretamente — sem LlamaIndex

from pathlib import Path
import chromadb
from core.config import get_settings

settings = get_settings()

CHROMA_PATH = "./chroma_db"
COLLECTION  = "modelos_peticao"

_client     = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client     = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_or_create_collection(COLLECTION)
    return _collection


def identificar_modelo(descricao: str, forcar: str | None = None) -> tuple[str, str]:
    """
    Busca o modelo mais similar à descrição.
    Retorna (nome_modelo, texto_modelo).
    """
    modelos_path = Path(settings.modelos_path)

    # Modo forçado
    if forcar:
        for docx in modelos_path.rglob("*.docx"):
            if forcar.lower() in docx.stem.lower():
                return docx.stem, _ler_docx(docx)
        return forcar, ""

    # Busca semantica no ChromaDB
    try:
        col = _get_collection()
        resultados = col.query(
            query_texts=[descricao],
            n_results=1,
        )
        if resultados and resultados["documents"] and resultados["documents"][0]:
            meta  = resultados["metadatas"][0][0]
            texto = resultados["documents"][0][0]
            nome  = meta.get("file_name", "desconhecido")
            return nome, texto
    except Exception as e:
        print(f"[RAG] Erro na busca semantica: {e}")

    # Fallback: busca por palavra-chave
    return _busca_keyword(descricao, modelos_path)


def _busca_keyword(descricao: str, modelos_path: Path) -> tuple[str, str]:
    desc_upper = descricao.upper()
    palavras   = [p for p in desc_upper.split() if len(p) > 4]

    melhor       = None
    melhor_score = 0

    for docx in modelos_path.rglob("*.docx"):
        nome_upper = docx.stem.upper()
        score      = sum(1 for p in palavras if p in nome_upper)
        if score > melhor_score:
            melhor_score = score
            melhor       = docx

    if melhor:
        return melhor.stem, _ler_docx(melhor)
    return "", ""


def _ler_docx(path: Path) -> str:
    try:
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""