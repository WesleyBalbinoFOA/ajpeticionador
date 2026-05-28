# backend/services/gemini.py

from groq import Groq
import google.generativeai as genai
from datetime import datetime
from core.config import get_settings
from core.advogados import buscar_advogado, ASSESSOR_JURIDICO
from core.sanitizer import limpar_para_xml
from models.schemas import Processo
import re

settings = get_settings()

_groq = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None

if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
    _gemini = genai.GenerativeModel(settings.gemini_model)
else:
    _gemini = None

SYSTEM_PROMPT = """Você é um advogado especialista em direito civil e execução fiscal no Brasil.
Redija APENAS os parágrafos intermediários da petição.
NÃO inclua: endereçamento, qualificação das partes, número do processo, fecho, data, assinatura.
Comece direto com a exposição dos fatos e fundamentos.
Cada parágrafo separado por linha em branco.
Linguagem jurídica formal. Máximo 3 parágrafos curtos e objetivos."""


def _data_extenso() -> str:
    meses = {1:'janeiro',2:'fevereiro',3:'março',4:'abril',5:'maio',6:'junho',
             7:'julho',8:'agosto',9:'setembro',10:'outubro',11:'novembro',12:'dezembro'}
    hoje = datetime.now()
    return f"Volta Redonda, {hoje.day} de {meses[hoje.month]} de {hoje.year}."


def _tipo_acao(modelo_texto: str, descricao: str) -> str:
    """Detecta o tipo de ação a partir do modelo ou da descrição."""
    texto = (modelo_texto + ' ' + descricao).upper()
    tipos = [
        'EXECUÇÃO DE TÍTULO EXTRAJUDICIAL',
        'EXECUÇÃO FISCAL',
        'AÇÃO DE COBRANÇA',
        'AÇÃO MONITÓRIA',
        'AÇÃO ORDINÁRIA',
        'EXECUÇÃO',
    ]
    for t in tipos:
        if t in texto:
            return t
    return 'EXECUÇÃO DE TÍTULO EXTRAJUDICIAL'


def _prompt_corpo(processo: Processo, modelo_texto: str) -> str:
    return f"""Instrução: {processo.descricao_solicitacao}
Parte Contrária: {processo.parte_contraria}
Vara: {processo.vara_orgao}

Modelo de referência (siga o estilo e argumentação):
{modelo_texto[:1200]}

Redija apenas os parágrafos intermediários da petição — exposição dos fatos e pedido principal.
NÃO repita a qualificação das partes nem inclua fecho.
Separe parágrafos com linha em branco."""


def _limpar_corpo(corpo: str) -> str:
    """Remove elementos estruturais que a IA insistiu em incluir."""
    corpo = limpar_para_xml(corpo)
    # Remove linhas com elementos estruturais
    linhas = []
    for linha in corpo.split('\n'):
        l = linha.strip()
        if re.match(r'^Ao Douto', l, re.I): continue
        if re.match(r'^Processo\s+n', l, re.I): continue
        if re.match(r'^Volta Redonda', l, re.I): continue
        if re.match(r'^P\.\s*Defer', l, re.I): continue
        if re.match(r'^Nestes termos', l, re.I): continue
        if re.match(r'OAB/RJ', l, re.I): continue
        if re.match(r'^Advogado', l, re.I): continue
        if re.match(r'FUNDAÇÃO OSWALDO ARANHA.*FOA.*vem', l, re.I): continue
        linhas.append(linha)
    return '\n'.join(linhas).strip()


def _montar_peticao(processo: Processo, corpo: str, modelo_texto: str) -> str:
    advogado  = buscar_advogado(processo.responsavel)
    assessor  = ASSESSOR_JURIDICO
    tipo_acao = _tipo_acao(modelo_texto, processo.descricao_solicitacao)
    cliente   = (processo.cliente or 'FUNDAÇÃO OSWALDO ARANHA').upper()
    if 'FOA' not in cliente and 'FUNDAÇÃO' in cliente:
        cliente += ' – FOA'

    parte = processo.parte_contraria.upper() if processo.parte_contraria else '[PARTE CONTRÁRIA]'

    # Primeiro parágrafo fixo — qualificação
    primeiro_paragrafo = (
        f"{cliente}, devidamente qualificada nos autos da "
        f"{tipo_acao} que move em face de {parte}, "
        f"vem respeitosamente a presença de V. Exa., por intermédio de seu(a) procurador(a), "
        f"expor e requerer o que segue."
    )

    # Parágrafo do assessor
    paragrafo_assessor = (
        f"Por fim, requer que as publicações e intimações eletrônicas sejam realizadas "
        f"exclusivamente em nome do Assessor Jurídico da Fundação, "
        f"{assessor['nome'].upper()} - {assessor['oab']}."
    )

    peticao = (
        f"Ao Douto Juízo da {processo.vara_orgao} da Comarca de Volta Redonda – RJ.\n"
        f"\n\n\n\n\n"
        f"Processo nº {processo.numero}\n"
        f"\n"
        f"{primeiro_paragrafo}\n"
        f"\n"
        f"{corpo}\n"
        f"\n"
        f"{paragrafo_assessor}\n"
        f"\n"
        f"P. Deferimento.\n"
        f"{_data_extenso()}\n"
        f"\n\n\n\n\n"
        f"{advogado['nome']}\n"
        f"Advogado(a) FOA\n"
        f"{advogado['oab']}"
    )
    return peticao


async def gerar_peticao(processo: Processo, modelo_texto: str) -> str:
    prompt = _prompt_corpo(processo, modelo_texto)
    corpo  = None

    if _groq:
        try:
            resp  = _groq.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": prompt},
                ],
                temperature=settings.temperatura,
                max_tokens=settings.max_tokens,
            )
            corpo = resp.choices[0].message.content.strip()
        except Exception as e_groq:
            if _gemini:
                try:
                    corpo = _gemini.generate_content(prompt).text.strip()
                except Exception as e_gemini:
                    raise RuntimeError(f"Groq: {e_groq} | Gemini: {e_gemini}")
            else:
                raise RuntimeError(f"Groq falhou: {e_groq}")
    elif _gemini:
        try:
            corpo = _gemini.generate_content(prompt).text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini falhou: {e}")
    else:
        raise RuntimeError("Nenhuma IA configurada.")

    corpo = _limpar_corpo(corpo)
    return _montar_peticao(processo, corpo, modelo_texto)