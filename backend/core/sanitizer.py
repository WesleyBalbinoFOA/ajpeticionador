# backend/core/sanitizer.py
# Sanitização centralizada de texto — remove/converte caracteres inválidos para XML/Word

import re


def limpar_para_xml(texto: str) -> str:
    """
    Converte ou remove caracteres inválidos para XML/Word.
    Caracteres de controle usados pela IA como separadores viram quebras de linha.
    """
    if not texto:
        return ''

    resultado = []
    for ch in texto:
        cp = ord(ch)

        # Newline — mantém
        if cp == 10:
            resultado.append(ch)

        # Carriage return — mantém
        elif cp == 13:
            resultado.append(ch)

        # Tab — vira espaço
        elif cp == 9:
            resultado.append(' ')

        # Caracteres de controle 1-31 (exceto 9,10,13)
        # A IA usa \x01 como separador de parágrafo — vira \n
        elif 1 <= cp <= 31:
            resultado.append('\n')

        # NULL — remove
        elif cp == 0:
            continue

        # DEL — remove
        elif cp == 127:
            continue

        # Substitutos Unicode inválidos — remove
        elif 55296 <= cp <= 57343:
            continue

        # Replacement char — remove
        elif cp == 65533:
            continue

        # Resto — mantém
        else:
            resultado.append(ch)

    texto = ''.join(resultado)

    # Normaliza espaços múltiplos (preserva quebras de linha)
    texto = re.sub(r'[ \t]{2,}', ' ', texto)

    # Remove espaço no início/fim de cada linha
    texto = '\n'.join(line.strip() for line in texto.split('\n'))

    # Limpa linhas em branco excessivas (mais de 6 seguidas)
    texto = re.sub(r'\n{7,}', '\n\n\n\n\n\n', texto)

    return texto.strip()