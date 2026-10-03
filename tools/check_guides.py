"""Fail the build if content, screenshots, or document navigation is lost."""
from pathlib import Path
from zipfile import ZipFile
import re
import unicodedata
import xml.etree.ElementTree as ET
from pypdf import PdfReader
from google_docs_title_sanitize import check_docx

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
DRAWING = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'


def normalize(text):
    return re.sub(r'[^a-z0-9]+','',unicodedata.normalize('NFKC',text).lower())


def source_units(markdown):
    markdown = re.split(r'^Last updated:[^\n]*\n',markdown,maxsplit=1,flags=re.M)[1]
    markdown = re.sub(r'^## Contents\n.*?(?=^## )','',markdown,flags=re.M|re.S)
    markdown = re.sub(r'^!\[.*$','',markdown,flags=re.M)
    markdown = re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',markdown)
    units=[]
    for block in re.split(r'\n\s*\n',markdown):
        if not block.strip(): continue
        if block.startswith('|'):
            candidates = [cell.strip() for line in block.splitlines() for cell in line.strip('|').split('|') if not re.fullmatch(r'[-: ]*',cell)]
        elif re.match(r'(- |\d+\. )',block):
            candidates = re.split(r'\n(?=- |\d+\. )',block)
        else: candidates=[block]
        for candidate in candidates:
            candidate = re.sub(r'^#+\s*','',candidate)
            candidate = re.sub(r'^\d+\.\s*','',candidate)
            units.append(candidate)
    return units


def verify_text(markdown, rendered, filename):
    if '\x00' in rendered: raise ValueError(f'{filename}: missing font glyph')
    # Page furniture can appear between two lines of a source paragraph.
    rendered = re.sub(r'TRAVEL MONKEY\s+(?:QUICK START|USER GUIDE)','',rendered)
    rendered = re.sub(r'Travel Monkey\s*/\s*(?:Quick start|User guide)\s*\d+','',rendered)
    actual = normalize(rendered)
    missing = [unit for unit in source_units(markdown) if normalize(unit) not in actual]
    if missing: raise ValueError(f'{filename}: source content missing: {missing}')
    date = re.search(r'^Last updated:\s*(.+)$',markdown,re.M)[1].strip()
    if normalize(date) not in actual: raise ValueError(f'{filename}: outdated document date')


def verify_pdf(markdown, filename):
    reader = PdfReader(filename)
    verify_text(markdown,'\n'.join(page.extract_text() for page in reader.pages),filename)
    sections = [title for title in re.findall(r'^## (.+)$',markdown,re.M) if title!='Contents']
    if len(reader.outline)!=len(sections): raise ValueError(f'{filename}: missing section bookmarks')
    image_count = sum(len(list(page.images)) for page in reader.pages)
    if image_count < len(re.findall(r'^!\[',markdown,re.M))+1:
        raise ValueError(f'{filename}: missing screenshots or cover artwork')
    for page in reader.pages:
        for reference in page.get('/Annots',[]):
            annotation = reference.get_object()
            if '/A' not in annotation and '/Dest' not in annotation:
                raise ValueError(f'{filename}: incomplete link annotation')
    print(f'{filename.name}: full content verified, {len(reader.pages)} pages, {len(reader.outline)} bookmarks')


def verify_docx(markdown, filename):
    with ZipFile(filename) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
        text = '\n'.join(''.join(node.itertext()) for node in root.iter(W+'t'))
        verify_text(markdown,text,filename)
        expected = len(re.findall(r'^!\[',markdown,re.M))+1
        if len(list(root.iter(DRAWING+'docPr')))!=expected: raise ValueError(f'{filename}: missing images')
        bookmarks = {node.get(W+'name') for node in root.iter(W+'bookmarkStart')}
        for link in root.iter(W+'hyperlink'):
            anchor = link.get(W+'anchor')
            if anchor and anchor not in bookmarks: raise ValueError(f'{filename}: unresolved link {anchor}')
        title_count = sum(node.get(W+'val')=='Title' for node in root.iter(W+'pStyle'))
        if title_count!=1: raise ValueError(f'{filename}: document needs exactly one Title paragraph')
    issues=check_docx(filename,leading_nonempty_paragraphs=3)
    if issues: raise ValueError(f'{filename}: {issues}')
    print(f'{filename.name}: full content, screenshots, native headings and links verified')


def check_guides(source_root, output_directory):
    for kind in ['quick-start','user-guide']:
        markdown = (source_root/f'{kind}.md').read_text(encoding='utf-8')
        verify_pdf(markdown,output_directory/'pdf'/f'travel-monkey-{kind}.pdf')
        verify_docx(markdown,output_directory/'docs'/f'travel-monkey-{kind}.docx')
