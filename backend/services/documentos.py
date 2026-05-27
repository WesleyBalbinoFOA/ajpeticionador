# backend/services/documentos.py
# Gera .docx com python-docx e .pdf com reportlab (sem dependências externas)

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io


def gerar_docx(numero_processo: str, conteudo: str) -> bytes:
    doc = Document()

    for section in doc.sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2)

    cabecalho = doc.add_heading(f"Processo nº {numero_processo}", level=1)
    cabecalho.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    for bloco in conteudo.split("\n"):
        if bloco.strip():
            p = doc.add_paragraph(bloco.strip())
            p.style.font.size = Pt(12)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(1.25)
            p.paragraph_format.space_after = Pt(6)

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def gerar_pdf(numero_processo: str, conteudo: str) -> bytes:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=3*cm,
        bottomMargin=2*cm,
        leftMargin=3*cm,
        rightMargin=2*cm,
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        'titulo',
        parent=styles['Normal'],
        fontSize=13,
        fontName='Times-Roman',
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    estilo_corpo = ParagraphStyle(
        'corpo',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Times-Roman',
        alignment=TA_JUSTIFY,
        firstLineIndent=1.25*cm,
        spaceAfter=6,
        leading=18,
    )

    elementos = []
    elementos.append(Paragraph(f"Processo nº {numero_processo}", estilo_titulo))
    elementos.append(Spacer(1, 0.5*cm))

    for bloco in conteudo.split("\n"):
        if bloco.strip():
            # Escapa caracteres especiais do XML do ReportLab
            texto = (bloco.strip()
                     .replace('&', '&amp;')
                     .replace('<', '&lt;')
                     .replace('>', '&gt;'))
            elementos.append(Paragraph(texto, estilo_corpo))

    doc.build(elementos)
    return buffer.getvalue()