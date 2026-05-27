# backend/services/rag.py
# Indexa modelos de petição e identifica o mais adequado por similaridade

import os
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from core.config import get_settings

settings = get_settings()

CHROMA_PATH = "./chroma_db"
COLLECTION = "modelos_peticao"

# Cliente ChromaDB e coleção (singleton)
_chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _chroma_client.get_or_create_collection(COLLECTION)
_vector_store = ChromaVectorStore(chroma_collection=_collection)
_index = None


def _carregar_index() -> VectorStoreIndex:
    """Carrega o índice existente do ChromaDB."""
    global _index
    if _index is None:
        storage_context = StorageContext.from_defaults(vector_store=_vector_store)
        _index = VectorStoreIndex.from_vector_store(
            _vector_store,
            storage_context=storage_context,
        )
    return _index


def identificar_modelo(descricao: str, forcar: str | None = None) -> tuple[str, str]:
    """
    Busca o modelo de petição mais similar à descrição da tarefa.
    Retorna (nome_modelo, texto_modelo).
    """
    modelos_path = Path(settings.modelos_path)

    # Modo forçado: busca o arquivo diretamente
    if forcar:
        for docx in modelos_path.rglob("*.docx"):
            if forcar.lower() in docx.stem.lower():
                return docx.stem, _ler_docx(docx)
        return forcar, ""

    # RAG: busca semântica
    try:
        index = _carregar_index()
        engine = index.as_retriever(similarity_top_k=1)
        resultados = engine.retrieve(descricao)

        if resultados:
            node = resultados[0]
            nome = node.metadata.get("file_name", "desconhecido")
            return nome, node.get_content()
    except Exception:
        pass

    # Fallback: busca por palavra-chave simples
    return _busca_keyword(descricao, modelos_path)


def _busca_keyword(descricao: str, modelos_path: Path) -> tuple[str, str]:
    """Fallback simples: procura arquivo cujo nome contenha palavras da descrição."""
    desc_upper = descricao.upper()
    palavras = [p for p in desc_upper.split() if len(p) > 4]

    melhor = None
    melhor_score = 0

    for docx in modelos_path.rglob("*.docx"):
        nome_upper = docx.stem.upper()
        score = sum(1 for p in palavras if p in nome_upper)
        if score > melhor_score:
            melhor_score = score
            melhor = docx

    if melhor:
        return melhor.stem, _ler_docx(melhor)
    return "", ""


def _ler_docx(path: Path) -> str:
    """Extrai texto de um .docx."""
    try:
        from docx import Document
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return ""
