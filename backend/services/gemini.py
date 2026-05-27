# backend/services/gemini.py
# Geração de petições com Groq (principal) + Gemini (fallback)

from groq import Groq
import google.generativeai as genai
from core.config import get_settings
from models.schemas import Processo

settings = get_settings()

# Clientes (singleton via módulo)
_groq = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None

if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
    _gemini = genai.GenerativeModel(settings.gemini_model)
else:
    _gemini = None

SYSTEM_PROMPT = """Você é um advogado especialista em direito civil e execução fiscal no Brasil.
Sua tarefa é adaptar o modelo de petição fornecido aos dados específicos do processo.
Mantenha a linguagem jurídica formal, a estrutura e o estilo do modelo.
Substitua apenas os dados variáveis (nomes, números, datas, fatos específicos).
Retorne SOMENTE o texto da petição, sem explicações adicionais."""


def _montar_prompt(processo: Processo, modelo_texto: str) -> str:
    """Monta o prompt final para geração. Conciso para economizar tokens."""
    return f"""DADOS DO PROCESSO:
- Número: {processo.numero}
- Parte Contrária: {processo.parte_contraria}
- Vara/Órgão: {processo.vara_orgao}
- Tipo de Tarefa: {processo.tipo_tarefa}
- Instrução: {processo.descricao_solicitacao}

MODELO BASE:
{modelo_texto}

Adapte o modelo acima aos dados do processo. Retorne apenas o texto da petição."""


async def gerar_peticao(processo: Processo, modelo_texto: str) -> str:
    """
    Gera petição com Groq (principal).
    Se falhar, tenta Gemini como fallback.
    """
    prompt = _montar_prompt(processo, modelo_texto)

    # Tenta Groq primeiro
    if _groq:
        try:
            resposta = _groq.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.temperatura,
                max_tokens=settings.max_tokens,
            )
            return resposta.choices[0].message.content.strip()
        except Exception as e_groq:
            # Fallback: Gemini
            if _gemini:
                try:
                    resposta = _gemini.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=settings.temperatura,
                            max_output_tokens=settings.max_tokens,
                        )
                    )
                    return resposta.text.strip()
                except Exception as e_gemini:
                    raise RuntimeError(
                        f"Groq falhou: {e_groq} | Gemini falhou: {e_gemini}"
                    )
            raise RuntimeError(f"Groq falhou e Gemini não configurado: {e_groq}")

    # Sem Groq — tenta só Gemini
    if _gemini:
        try:
            resposta = _gemini.generate_content(prompt)
            return resposta.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini falhou: {e}")

    raise RuntimeError("Nenhuma IA configurada. Verifique GROQ_API_KEY no .env")