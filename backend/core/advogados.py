# backend/core/advogados.py
# Cadastro de advogados da FOA
# Fase 2: substituir por consulta ao perfil de login

ADVOGADOS = {
    "Wesley Pinheiro Balbino":          {"nome": "Wesley Pinheiro Balbino",         "oab": "OAB/RJ 177.080"},
    "Jéssica Cristine dos Santos Souza":{"nome": "Jéssica Cristine dos Santos Souza","oab": "OAB/RJ 197.671"},
    "Jessica Cristine dos Santos Souza":{"nome": "Jéssica Cristine dos Santos Souza","oab": "OAB/RJ 197.671"},
    "Marina Carvalho do Nascimento":    {"nome": "Marina Carvalho do Nascimento",    "oab": "OAB/RJ 240.240"},
    "Denys Ribeiro Furtunato":          {"nome": "Denys Ribeiro Furtunato",          "oab": "OAB/RJ 164.024"},
}

ADVOGADO_PADRAO = {
    "nome": "Wesley Pinheiro Balbino",
    "oab":  "OAB/RJ 177.080"
}

ASSESSOR_JURIDICO = {
    "nome": "Denys Ribeiro Furtunato",
    "oab":  "OAB/RJ 164.024"
}


def buscar_advogado(nome: str) -> dict:
    """
    Busca advogado pelo nome (tolerante a variações).
    Retorna padrão se não encontrar.
    """
    if not nome:
        return ADVOGADO_PADRAO

    # Busca exata
    if nome in ADVOGADOS:
        return ADVOGADOS[nome]

    # Busca parcial (primeiro nome + sobrenome)
    nome_lower = nome.strip().lower()
    for chave, dados in ADVOGADOS.items():
        if nome_lower in chave.lower() or chave.lower() in nome_lower:
            return dados

    return ADVOGADO_PADRAO