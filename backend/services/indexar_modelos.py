# backend/services/indexar_modelos.py
# Indexa modelos usando ChromaDB com embedding local simples
# Nao requer OpenAI nem HuggingFace

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

import chromadb
from docx import Document as DocxDocument

CHROMA_PATH = "./chroma_db"
COLLECTION  = "modelos_peticao"
MODELOS_PATH = Path("./modelos")


def ler_docx(path: Path) -> str:
    try:
        doc = DocxDocument(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        print(f"  [!] Erro ao ler {path.name}: {e}")
        return ""


def indexar():
    print(f"[DIR] Pasta de modelos: {MODELOS_PATH.resolve()}")

    docx_files = list(MODELOS_PATH.rglob("*.docx"))
    print(f"[ARQ] Arquivos encontrados: {len(docx_files)}\n")

    if not docx_files:
        print("[!] Nenhum .docx encontrado. Coloque os modelos na pasta /modelos/")
        return

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        chroma_client.delete_collection(COLLECTION)
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(
        COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )

    ids        = []
    documentos = []
    metadatas  = []

    for path in docx_files:
        texto = ler_docx(path)
        if texto:
            categoria = path.parent.name
            doc_id    = path.stem.replace(" ", "_")[:50]
            ids.append(doc_id)
            documentos.append(texto[:2000])  # limita tokens
            metadatas.append({
                "file_name": path.stem,
                "categoria": categoria,
                "caminho":   str(path),
            })
            print(f"  [OK] {categoria}/{path.name}")
        else:
            print(f"  [--] Pulado (vazio): {path.name}")

    print(f"\n[IDX] Indexando {len(documentos)} modelos...")

    # Insere em lotes de 10
    lote = 10
    for i in range(0, len(ids), lote):
        collection.add(
            ids=ids[i:i+lote],
            documents=documentos[i:i+lote],
            metadatas=metadatas[i:i+lote],
        )
        print(f"  Lote {i//lote + 1} inserido ({min(i+lote, len(ids))}/{len(ids)})")

    print(f"\n[OK] {len(documentos)} modelos indexados com sucesso!")
    print(f"[SAL] Banco salvo em: {CHROMA_PATH}")
    print(f"\nProximo passo: inicie o backend com uvicorn.")


if __name__ == "__main__":
    indexar()