# Execute UMA VEZ: python scripts/criar_tabelas.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv()
from core.supabase import get_supabase
from core.auth import hash_senha

sb = get_supabase()

USUARIOS = [
    {"nome":"Wesley Pinheiro Balbino",           "email":"wesley.balbino@foa.org.br",    "oab":"OAB/RJ 177.080","perfil":"advogado"},
    {"nome":"Jéssica Cristine dos Santos Souza", "email":"jessica.souza@foa.org.br",     "oab":"OAB/RJ 197.671","perfil":"advogado"},
    {"nome":"Marina Carvalho do Nascimento",     "email":"marina.nascimento@foa.org.br", "oab":"OAB/RJ 240.240","perfil":"advogado"},
    {"nome":"Denys Ribeiro Furtunato",           "email":"denys.furtunato@foa.org.br",   "oab":"OAB/RJ 164.024","perfil":"admin"},
]

print("Inserindo usuários...")
for u in USUARIOS:
    try:
        sb.table("usuarios").insert({**u, "senha_hash": hash_senha("foa2026"), "ativo": True}).execute()
        print(f"  ✅ {u['nome']}")
    except Exception as e:
        print(f"  ⚠️  {u['nome']}: {e}")
print("Pronto!")
