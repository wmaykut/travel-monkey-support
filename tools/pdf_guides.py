from pathlib import Path
import re, math, html
from tempfile import TemporaryDirectory
from datetime import datetime
from fontTools.ttLib import TTFont as FontFile
from fontTools.varLib.instancer import instantiateVariableFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, CondPageBreak, Table, TableStyle, Image, KeepTogether, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT
OUT = ROOT / 'exports/pdf'
UPDATED = ''


def register_fonts(font_directory):
    for name, family, weight in [('Display', 'Fraunces', 600), ('Body', 'Karla', 400), ('Bold', 'Karla', 700), ('Symbols', 'NotoSansSymbols', 400)]:
        font = FontFile(ROOT / f'tools/assets/fonts/{family}-Variable.ttf')
        axes = {axis.axisTag: axis.defaultValue for axis in font['fvar'].axes}
        axes['wght'] = weight
        font_path = font_directory / f'{name}.ttf'
        instantiateVariableFont(font, axes, inplace=True).save(font_path)
        pdfmetrics.registerFont(TTFont(name, str(font_path)))
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='Bold', italic='Body', boldItalic='Bold')

PAPER, INK, BODY, GREEN, BRASS, RULE, MUTED, SHADE = [HexColor(value) for value in
    ['#F6F1E4', '#23281F', '#3D4237', '#2F4F3A', '#C08A2E', '#D8CEB4', '#6B6B60', '#F1EADB']]
W, H, M = 612, 792, 54
WIDTH = W - M * 2
STYLES = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=11, leading=15.4,
        textColor=BODY, spaceAfter=9),
    'lead': ParagraphStyle('lead', fontName='Body', fontSize=13, leading=19,
        textColor=BODY, spaceAfter=14),
    'h2': ParagraphStyle('h2', fontName='Display', fontSize=27, leading=31,
        textColor=GREEN, spaceAfter=17, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Display', fontSize=17, leading=21,
        textColor=INK, spaceBefore=9, spaceAfter=9, keepWithNext=True),
    'caption': ParagraphStyle('caption', fontName='Body', fontSize=9, leading=12,
        textColor=MUTED, spaceBefore=6, spaceAfter=13),
    'bullet': ParagraphStyle('bullet', fontName='Body', fontSize=11, leading=15.4,
        textColor=BODY, leftIndent=14, firstLineIndent=-14, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='Body', fontSize=10.1, leading=13.3,
        textColor=BODY),
    'th': ParagraphStyle('th', fontName='Bold', fontSize=9, leading=12,
        textColor=GREEN),
}

def slug(text):
    return re.sub(r'[^a-z0-9\-]', '', text.lower().replace(' ', '-'))

def link_target(url):
    if url.startswith('#'):
        return url
    if url.startswith('https:'):
        return url
    document, _, anchor = url.partition('#')
    if document in ('quick-start.md', 'user-guide.md'):
        return f'https://github.com/wmaykut/travel-monkey-support/blob/main/{document}' + ('#'+anchor if anchor else '')
    if document == 'README.md':
        return 'https://github.com/wmaykut/travel-monkey-support#' + anchor if anchor else 'https://github.com/wmaykut/travel-monkey-support'
    return 'https://github.com/wmaykut/travel-monkey-support/blob/main/' + document + ('#'+anchor if anchor else '')

def inline(text):
    text = re.sub(r'\s+', ' ', text.strip()).replace('—', '-').replace('–', '-')
    text = html.escape(text)
    text = text.replace('→', '<font name="Symbols">→</font>').replace('ⓘ', '<font name="Symbols">ⓘ</font>')
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda match:
        f'<a href="{html.escape(link_target(html.unescape(match[2])), quote=True)}" color="#2F4F3A"><u>{match[1]}</u></a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    return text

class SectionHeading(Paragraph):
    def __init__(self, title, number):
        super().__init__(inline(title), STYLES['h2'])
        self.section_title, self.anchor, self.number = title, slug(title), number

class SectionLabel(Flowable):
    def __init__(self, number):
        super().__init__()
        self.number, self.height = number, 28
        self.keepWithNext = True
    def draw(self):
        canvas = self.canv
        canvas.setFillColor(BRASS)
        canvas.setFont('Bold', 10)
        canvas.drawString(0, 12, f'{self.number:02d}  /  FIELD GUIDE')
        canvas.setStrokeColor(RULE)
        canvas.line(125, 16, WIDTH, 16)

class Cover(Flowable):
    def __init__(self, title, subtitle):
        super().__init__()
        self.width, self.height, self.title, self.subtitle = WIDTH, 405, title, subtitle
    def draw(self):
        canvas = self.canv
        canvas.setFillColor(GREEN)
        canvas.rect(-M, 0, W, 405 + 98, stroke=0, fill=1)
        canvas.setStrokeColor(HexColor('#56715A'))
        canvas.setLineWidth(.6)
        for track in range(8):
            path = canvas.beginPath()
            for step in range(160):
                x = -M + step * 4.5
                y = 47 + track * 13 + 29 * math.sin(step / 19 + track * .19)
                (path.moveTo if step == 0 else path.lineTo)(x, y)
            canvas.drawPath(path)
        canvas.drawImage(str(ROOT / 'tools/assets/monkey-mark.png'), 0, 310, 56, 56, mask='auto', preserveAspectRatio=True)
        canvas.setFillColor(PAPER)
        canvas.setFont('Display', 25)
        canvas.drawString(69, 332, 'Travel Monkey')
        canvas.setFont('Bold', 10)
        canvas.drawString(0, 275, 'YOUR HOUSEHOLD’S TRAVEL CONCIERGE')
        canvas.setFont('Display', 56)
        canvas.drawString(0, 200, self.title)
        canvas.setFont('Body', 14)
        canvas.drawString(0, 167, self.subtitle)
        canvas.setFillColor(BRASS)
        canvas.circle(420, 95, 4, fill=1, stroke=0)
        canvas.setFillColor(PAPER)
        canvas.setFont('Bold', 9)
        canvas.drawString(0, 25, 'FIELD GUIDE  /  ' + datetime.strptime(UPDATED, '%B %d, %Y').strftime('%B %Y').upper())

class GuideDoc(BaseDocTemplate):
    def __init__(self, filename, label):
        super().__init__(str(filename), pagesize=(W,H), leftMargin=M, rightMargin=M,
            topMargin=78, bottomMargin=58, title=f'Travel Monkey {label}', author='Travel Monkey')
        self.label, self.current_section = label, ''
        frame = Frame(M, 58, WIDTH, H-136, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='guide', frames=[frame], onPage=self.paint))
    def paint(self, canvas, doc):
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        if doc.page > 1:
            canvas.setFillColor(GREEN)
            canvas.setFont('Bold', 9)
            canvas.drawString(M, H-39, 'TRAVEL MONKEY')
            canvas.setFillColor(MUTED)
            canvas.setFont('Body', 9)
            canvas.drawRightString(W-M, H-39, self.label.upper())
            canvas.setStrokeColor(RULE)
            canvas.line(M, H-50, W-M, H-50)
        canvas.setStrokeColor(RULE)
        canvas.line(M, 43, W-M, 43)
        canvas.setFillColor(MUTED)
        canvas.setFont('Body', 8)
        canvas.drawString(M, 27, 'Travel Monkey  /  ' + (self.label if doc.page > 1 else 'Last updated ' + UPDATED))
        canvas.setFont('Bold', 9)
        canvas.drawRightString(W-M, 27, f'{doc.page:02d}')
    def afterFlowable(self, flowable):
        if isinstance(flowable, SectionHeading):
            self.current_section = flowable.section_title
            self.canv.bookmarkPage(flowable.anchor)
            self.canv.addOutlineEntry(flowable.section_title, flowable.anchor, 0, False)
            self.notify('TOCEntry', (0, flowable.section_title, self.page, flowable.anchor))
        elif isinstance(flowable, Paragraph) and hasattr(flowable, 'subanchor'):
            self.canv.bookmarkPage(flowable.subanchor)

def screenshot(image_path, caption, compact=False):
    with PILImage.open(image_path) as picture:
        iw, ih = picture.size
    max_height = 135 if compact else 245
    max_width = WIDTH if ih/iw < 1.4 else 210
    factor = min(max_height / ih, max_width / iw)
    picture = Image(str(image_path), iw*factor, ih*factor)
    picture.hAlign = 'LEFT'
    portrait = ih/iw > 1.4
    if portrait:
        note = Paragraph('<font name="Bold" color="#C08A2E">IN THE APP</font><br/><br/>'+inline(caption), STYLES['caption'])
        panel = Table([[picture, note]], colWidths=[iw*factor+24, WIDTH-iw*factor-24])
    else:
        panel = Table([[picture]], colWidths=[iw*factor+24], hAlign='LEFT')
    panel.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),SHADE),
        ('BOX',(0,0),(-1,-1),.5,RULE),('LEFTPADDING',(0,0),(-1,-1),12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    return KeepTogether([Spacer(1,5), panel, Spacer(1,12)] if portrait else
        [Spacer(1,5), panel, Paragraph(inline(caption), STYLES['caption'])])

def blocks(text, compact=False):
    lines, index, elements = text.strip().splitlines(), 0, []
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith('### '):
            title = line[4:]
            if title == 'Settings': elements.append(PageBreak())
            heading = Paragraph(inline(title), STYLES['h2' if title == 'Settings' else 'h3'])
            heading.subanchor = slug(title)
            elements.append(heading)
            index += 1
            continue
        image_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if image_match:
            index += 1
            while index < len(lines) and not lines[index].strip(): index += 1
            caption_lines = []
            if index < len(lines) and lines[index].startswith('*') and not lines[index].startswith('**'):
                while index < len(lines) and lines[index].strip():
                    caption_lines.append(lines[index].strip())
                    index += 1
            caption = ' '.join(caption_lines).strip('*') or image_match[1]
            elements.append(screenshot(SOURCE / image_match[2], caption, compact))
            continue
        if line.startswith('|'):
            rows = []
            while index < len(lines) and lines[index].strip().startswith('|'):
                cells = [cell.strip() for cell in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', cell) for cell in cells): rows.append(cells)
                index += 1
            contents = [[Paragraph(inline(cell), STYLES['th' if r==0 else 'cell']) for cell in row] for r,row in enumerate(rows)]
            table = Table(contents, colWidths=[139, WIDTH-139], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LINEBELOW',(0,0),(-1,0),1,GREEN),('LINEBELOW',(0,1),(-1,-1),.4,RULE),
                ('BACKGROUND',(0,0),(-1,0),SHADE),('LEFTPADDING',(0,0),(-1,-1),9),
                ('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            elements.extend([table, Spacer(1,13)])
            continue
        list_match = re.match(r'(- |\d+\. )(.*)', line)
        if list_match:
            prefix = '•' if list_match[1].startswith('-') else list_match[1].strip()
            paragraph_lines = [list_match[2]]
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r'(- |\d+\. )', lines[index]):
                paragraph_lines.append(lines[index].strip())
                index += 1
            elements.append(Paragraph(prefix+'  '+inline(' '.join(paragraph_lines)), STYLES['bullet']))
            continue
        paragraph_lines = []
        while index < len(lines) and lines[index].strip():
            paragraph_lines.append(lines[index].strip())
            index += 1
        elements.append(Paragraph(inline(' '.join(paragraph_lines)), STYLES['body']))
    return elements

def build(kind):
    global UPDATED
    markdown = (SOURCE / f'{kind}.md').read_text(encoding='utf-8')
    metadata = re.search(r'^Last updated:\s*(.+)$', markdown, re.M)
    if metadata is None:
        raise ValueError(f'{kind}.md needs a Last updated date')
    UPDATED = metadata[1].strip()
    sections = re.split(r'^## (.+)\n', markdown, flags=re.M)
    opening = re.split(r'^Last updated:[^\n]*\n', sections[0], maxsplit=1, flags=re.M)[1].strip()
    is_quick = kind == 'quick-start'
    saved_styles = {name: style for name, style in STYLES.items()}
    if is_quick:
        for name in ['body', 'bullet']:
            STYLES[name] = ParagraphStyle(name+'Quick', parent=STYLES[name], fontSize=10.5,
                leading=14, spaceAfter=7 if name=='body' else 4)
        STYLES['h2'] = ParagraphStyle('h2Quick', parent=STYLES['h2'], fontSize=23, leading=27, spaceAfter=12)
    title = 'Quick start' if is_quick else 'User guide'
    subtitle = 'Set up. Explore. Choose. Go.' if is_quick else 'A companion for better days away.'
    story = [Cover(title, subtitle), Spacer(1,24)]
    story.extend(blocks(opening))
    story.append(Spacer(1,9))
    story.append(Paragraph(inline('[Support](README.md)  ·  ['+('Full user guide](user-guide.md)' if is_quick else 'Quick start](quick-start.md)')+'  ·  [Privacy Policy](privacy.md)'), STYLES['caption']))
    if not is_quick:
        story.extend([PageBreak(), Paragraph('In this guide', STYLES['h2']),
            Paragraph('Find a feature, follow the steps, and return whenever you need a hand.', STYLES['body']), Spacer(1,12)])
        toc = TableOfContents()
        toc.levelStyles = [ParagraphStyle('toc', fontName='Body', fontSize=11, leading=14, textColor=GREEN, spaceBefore=4, spaceAfter=0)]
        story.append(toc)
    number = 0
    for index in range(1,len(sections),2):
        heading, content = sections[index], sections[index+1]
        if heading == 'Contents': continue
        number += 1
        if is_quick and number in (1,2,4): story.append(PageBreak())
        elif not is_quick: story.append(PageBreak())
        elif is_quick: story.append(Spacer(1,14))
        display_heading = re.sub(r'^\d+\. ', '', heading)
        story.extend([SectionLabel(number), SectionHeading(display_heading, number)])
        story.extend(blocks(content, compact=is_quick))
    filename = OUT / f'travel-monkey-{kind}.pdf'
    document = GuideDoc(filename, title)
    document.multiBuild(story)
    reader = PdfReader(filename)
    print(filename.name, 'pages:',len(reader.pages), 'links:',sum(len(page.get('/Annots',[])) for page in reader.pages))
    STYLES.update(saved_styles)

def build_pdfs(source_root, output_directory):
    global ROOT, SOURCE, OUT
    ROOT = source_root
    SOURCE = source_root
    OUT = output_directory
    OUT.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix='travel-monkey-fonts-') as font_directory:
        register_fonts(Path(font_directory))
        for kind in ['quick-start', 'user-guide']:
            build(kind)
