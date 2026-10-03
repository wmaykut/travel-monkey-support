# Rebuild the Travel Monkey guides

`quick-start.md` and `user-guide.md` remain the source of truth. Edit those files
and their screenshots in `images/`, then run this from the support repository:

```sh
bash tools/build-guides.sh
```

The command creates a local `.venv-guides`, installs the pinned dependencies,
rebuilds four files, and validates their content and navigation:

| Output | Purpose |
|---|---|
| `exports/pdf/travel-monkey-quick-start.pdf` | Designed quick start with section bookmarks |
| `exports/pdf/travel-monkey-user-guide.pdf` | Designed user guide with linked contents and bookmarks |
| `exports/docs/travel-monkey-quick-start.docx` | Editable quick start for Word or Google Docs |
| `exports/docs/travel-monkey-user-guide.docx` | Editable user guide for Word or Google Docs |

Use Python 3.10 or later and Bash (macOS, Linux, or Windows with WSL). An internet connection is needed to install dependencies
on the first run; generation itself is local. To select a particular interpreter:

```sh
GUIDES_PYTHON=/path/to/python3 bash tools/build-guides.sh
```

The fonts, their licenses, and the monkey artwork are bundled in `tools/assets`.
No neighboring app checkout, macOS font, Codex runtime, or temporary dependency
directory is required. Each guide's `Last updated:` line supplies its edition date;
change it when revising the content. Use a date like `October 2, 2026`.

## Google Docs

1. Upload a file from `exports/docs/` to Google Drive.
2. Open it with Google Docs.
3. If it opens in Office editing mode, choose **File → Save as Google Docs**.

These are editable documents with real heading styles, hyperlinks, bookmarks,
bullets, numbered lists, tables, inline screenshots, and image alt text. The user
guide's contents links point to its headings. The title is sanitized during every
build to prevent a Word title border from appearing after import.

The editable editions use standard Georgia and Arial fonts on white pages. They
carry the same source content as the designed PDFs, with a layout suited to
editing. Google Docs can reflow page breaks when importing. Treat Markdown as the
canonical source: edits made only in Google Docs do not flow back into a rebuild.

## Checks

The build fails if a source paragraph, caption, list item, or table cell is missing,
an edition date is stale, an image is missing, an internal DOCX link has no target,
a PDF section bookmark is missing, or the DOCX title audit fails.

Run the focused guard tests with:

```sh
.venv-guides/bin/python tools/test_guides.py
```

For an already-installed environment, rebuild without running pip:

```sh
.venv-guides/bin/python tools/build_guides.py
```

The Markdown converter supports the formatting used in these guides: paragraphs,
second and third level headings, bold, italic, links, images, single-level lists,
and two-column tables. Review the outputs after structural changes or new Markdown
syntax; content checks cannot prove visual quality. In particular, the quick
start's designed pagination groups steps 2–3 and 4–5.

## Visual review

After major edits, inspect both PDFs and open the DOCX editions in Word or Google
Docs. For automated local rendering, install LibreOffice and Poppler. For example:

```sh
mkdir -p /tmp/travel-monkey-docx-preview
soffice --headless --convert-to pdf --outdir /tmp/travel-monkey-docx-preview exports/docs/*.docx
pdftoppm -png exports/pdf/travel-monkey-quick-start.pdf /tmp/travel-monkey-docx-preview/quick
pdftoppm -png exports/pdf/travel-monkey-user-guide.pdf /tmp/travel-monkey-docx-preview/guide
```

Keep previews out of the repository. The `exports/` files are deliberate outputs
and can be committed or published with the source docs. The virtual environment
and Python caches are ignored.
