#!/usr/bin/env python3
"""Build PDF and Google Docs-ready DOCX editions from the support Markdown."""
import argparse
from pathlib import Path
from pdf_guides import build_pdfs
from docx_guides import build_docxs
from check_guides import check_guides


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir',type=Path)
    options = parser.parse_args()
    source = options.source_root.resolve()
    output = options.output_dir.resolve() if options.output_dir else source/'exports'
    build_pdfs(source,output/'pdf')
    build_docxs(source,output/'docs')
    check_guides(source,output)


if __name__ == '__main__': main()
