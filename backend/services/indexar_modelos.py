# backend/services/indexar_modelos.py
# Execute com: make index
# Varre a pasta /modelos, lê os .docx e indexa no ChromaDB

import sys
import os
from pathlib import Path

# Garante imports do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from docx import Document as DocxDocument
from core.config import get_settings

settings = get_settings()

CHROMA_PATH = "./chroma_db"
COLLECTION = "modelos_peticao"
MODELOS_PATH = Path(settings.modelos_path)


def ler_docx(path: Path) -> str:
    """Extrai texto de .docx."""
    try:
        doc = DocxDocument(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"  ⚠️  Erro ao ler {path.name}: {e}")
        return ""


def indexar():
    print(f"📁 Pasta de modelos: {MODELOS_PATH.resolve()}")

    docx_files = list(MODELOS_PATH.rglob("*.docx"))
    print(f"📄 Arquivos encontrados: {len(docx_files)}\n")

    if not docx_files:
        print("❌ Nenhum .docx encontrado. Coloque os modelos na pasta /modelos/")
        return

    # Prepara documentos LlamaIndex
    documentos = []
    for path in docx_files:
        texto = ler_docx(path)
        if texto:
            categoria = path.parent.name
            doc = Document(
                text=texto,
                metadata={
                    "file_name": path.stem,
                    "categoria": categoria,
                    "caminho": str(path),
                }
            )
            documentos.append(doc)
            print(f"  ✅ {categoria}/{path.name}")
        else:
            print(f"  ⏭️  Pulado (vazio): {path.name}")

    print(f"\n📚 Indexando {len(documentos)} modelos no ChromaDB...")

    # ChromaDB
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    # Recria coleção para garantir índice limpo
    chroma_client.delete_collection(COLLECTION)
    collection = chroma_client.get_or_create_collection(COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(
        documentos,
        storage_context=storage_context,
        show_progress=True,
    )

    print(f"\n✅ {len(documentos)} modelos indexados com sucesso!")
    print(f"💾 Banco salvo em: {CHROMA_PATH}")


if __name__ == "__main__":
    indexar()
