import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def _header_footer(canvas_obj: canvas.Canvas, doc):
    canvas_obj.saveState()
    header_text = getattr(doc, 'title', '')
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.drawString(72, doc.height + doc.topMargin + 15, header_text)
    page_num = canvas_obj.getPageNumber()
    footer_text = f"Page {page_num}"
    canvas_obj.drawRightString(doc.width + doc.leftMargin, 15, footer_text)
    canvas_obj.restoreState()

def _add_toc(story, styles):
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name='TOCHeading1', fontSize=14, leftIndent=20, firstLineIndent=-20, spaceBefore=5, leading=16),
        ParagraphStyle(name='TOCHeading2', fontSize=12, leftIndent=40, firstLineIndent=-20, spaceBefore=0, leading=12),
    ]
    story.append(Paragraph('Table of Contents', styles['Heading1']))
    story.append(Spacer(1, 12))
    story.append(toc)
    story.append(PageBreak())

def _add_image(story, img_path, caption, figure_num, max_width=500):
    if not os.path.exists(img_path):
        return
    img = Image(img_path)
    if img.drawWidth > max_width:
        ratio = max_width / float(img.drawWidth)
        img.drawWidth = max_width
        img.drawHeight = img.drawHeight * ratio
    caption_par = Paragraph(f"Figure {figure_num}: {caption}",
                            ParagraphStyle(name='Caption', alignment=TA_CENTER, fontSize=10, spaceAfter=12))
    story.append(KeepTogether([img, caption_par]))
    story.append(Spacer(1, 12))

def generate_pdf(paper, sections, author="", institute="", date=None, output_dir="storage/exports"):
    if date is None:
        date = datetime.today().strftime('%B %d, %Y')
    if not os.path.isabs(output_dir):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)

    filename = "".join([c for c in paper.title if c.isalnum() or c == ' ']).rstrip()
    if not filename:
        filename = "paper"
    filepath = os.path.join(output_dir, f"{filename}.pdf")

    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            leftMargin=72, rightMargin=72,
                            topMargin=72, bottomMargin=72)
    doc.title = paper.title
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=24, spaceAfter=30)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Heading2'], alignment=TA_CENTER, fontSize=18, spaceAfter=20)
    author_style = ParagraphStyle('AuthorStyle', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12, spaceAfter=10)
    section_title_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=16, spaceAfter=12)
    content_style = ParagraphStyle('Content', parent=styles['Normal'], fontSize=11, leading=14, spaceAfter=8)

    story = []
    # Cover page
    story.append(Spacer(1, 150))
    story.append(Paragraph(paper.title, title_style))
    if paper.subtitle:
        story.append(Paragraph(paper.subtitle, subtitle_style))
    story.append(Spacer(1, 30))
    if author: story.append(Paragraph(author, author_style))
    if institute: story.append(Paragraph(institute, author_style))
    story.append(Paragraph(date, author_style))
    story.append(PageBreak())

    # TOC
    _add_toc(story, styles)

    # Sections
    fig_count = 1
    for sec in sections:
        story.append(Paragraph(f"{sec.section_number}. {sec.section_title}",
                               section_title_style, bookmark=f"sec{sec.section_number}"))
        story.append(Spacer(1, 12))
        paragraphs = sec.content.split('\n\n')
        for p in paragraphs:
            if not p.strip(): continue
            if p.strip().startswith('[Image:') and p.strip().endswith(']'):
                img_name = p.strip()[7:-1].strip()
                img_path = os.path.join('uploads', img_name)
                _add_image(story, img_path, img_name, fig_count)
                fig_count += 1
                continue
            p_text = p.replace('**', '<b>', 1).replace('**', '</b>', 1)
            story.append(Paragraph(p_text.replace('\n', '<br/>'), content_style))
            story.append(Spacer(1, 6))
        story.append(PageBreak())

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return filepath
