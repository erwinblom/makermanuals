from __future__ import annotations

from html import escape
from pathlib import Path
import re
import sys
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
PUBLIEKSLAAG_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PUBLIEKSLAAG_ROOT))

from site_content import load_book_content, render_book_index, render_book_page, write_manuals_source_index

MANUSCRIPT = PROJECT_ROOT / "manuscript" / "versies" / "2026-06-13-maker-manual-04-ai-autonomie-manuscript-draft-01.md"
LICENSE = PROJECT_ROOT / "manuscript" / "2026-06-13-maker-manual-04-ai-autonomie-license.md"
BOOK_HTML = ROOT / "book.html"
INDEX_HTML = ROOT / "index.html"
EPUB_PATH = PROJECT_ROOT / "exports" / "maker-manual-04-ai-autonomie.epub"
CONTENT = PROJECT_ROOT / "content.md"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def inline_html(text: str) -> str:
    text = escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    html: list[str] = []
    in_ul = False
    in_ol = False
    paragraph: list[str] = []
    last_list_item = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph if part.strip())
            if text:
                html.append(f"<p>{inline_html(text)}</p>")
            paragraph = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol, last_list_item
        if in_ul:
            html.append("</ul>")
            in_ul = False
        if in_ol:
            html.append("</ol>")
            in_ol = False
        last_list_item = False

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_lists()
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            close_lists()
            title = stripped[2:].strip()
            html.append(f'<h1 id="{slugify(title)}">{inline_html(title)}</h1>')
            last_list_item = False
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_lists()
            title = stripped[3:].strip()
            html.append(f'<h2 id="{slugify(title)}">{inline_html(title)}</h2>')
            last_list_item = False
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            close_lists()
            title = stripped[4:].strip()
            html.append(f'<h3 id="{slugify(title)}">{inline_html(title)}</h3>')
            last_list_item = False
            continue

        if re.match(r"^- ", stripped):
            flush_paragraph()
            if in_ol:
                html.append("</ol>")
                in_ol = False
            if not in_ul:
                html.append("<ul>")
                in_ul = True
            html.append(f"<li>{inline_html(stripped[2:].strip())}</li>")
            last_list_item = True
            continue

        if re.match(r"^\d+\. ", stripped):
            flush_paragraph()
            if in_ul:
                html.append("</ul>")
                in_ul = False
            if not in_ol:
                html.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+\. ", "", stripped)
            html.append(f"<li>{inline_html(item.strip())}</li>")
            last_list_item = True
            continue

        if (in_ul or in_ol) and last_list_item and html and html[-1].startswith("<li>") and html[-1].endswith("</li>"):
            html[-1] = html[-1][:-5] + " " + inline_html(stripped) + "</li>"
            continue

        if stripped.startswith("[") and "](" in stripped:
            flush_paragraph()
            close_lists()
            match = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", stripped)
            if match:
                label, url = match.groups()
                html.append(
                    f'<p><a href="{escape(url)}" target="_blank" rel="noopener noreferrer">{inline_html(label)}</a></p>'
                )
                last_list_item = False
                continue

        paragraph.append(stripped)
        last_list_item = False

    flush_paragraph()
    close_lists()
    return "\n".join(html)


def build_book() -> None:
    config = load_book_content(CONTENT)
    manuscript_html = markdown_to_html(MANUSCRIPT.read_text())
    license_html = markdown_to_html(LICENSE.read_text())
    BOOK_HTML.write_text(render_book_page(config, manuscript_html, license_html))


def build_index() -> None:
    config = load_book_content(CONTENT)
    INDEX_HTML.write_text(render_book_index(config))


def build_epub() -> None:
    manuscript_html = markdown_to_html(MANUSCRIPT.read_text())
    license_html = markdown_to_html(LICENSE.read_text())

    epub_css = """
body { font-family: Georgia, serif; line-height: 1.5; margin: 5%; color: #111; }
h1, h2, h3 { font-family: Arial, sans-serif; }
h1 { font-size: 2em; }
h2 { margin-top: 2em; font-size: 1.4em; }
h3 { margin-top: 1.5em; font-size: 1.1em; }
p, li { font-size: 1em; }
code { font-family: monospace; background: #f8e89e; padding: 0.1em 0.25em; }
"""

    book_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="nl">
  <head>
    <title>Maker Manual 04: AI-autonomie</title>
    <link rel="stylesheet" type="text/css" href="styles.css"/>
  </head>
  <body>
    {manuscript_html}
    <section>
      {license_html}
    </section>
  </body>
</html>
"""

    nav_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="nl">
  <head>
    <title>Inhoud</title>
  </head>
  <body>
    <nav epub:type="toc" id="toc">
      <h1>Inhoud</h1>
      <ol>
        <li><a href="book.xhtml">AI-autonomie</a></li>
      </ol>
    </nav>
  </body>
</html>
"""

    content_opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">maker-manual-04-ai-autonomie</dc:identifier>
    <dc:title>AI-autonomie</dc:title>
    <dc:language>nl</dc:language>
    <dc:creator>Erwin Blom</dc:creator>
    <meta property="dcterms:modified">2026-06-13T15:05:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="book" href="book.xhtml" media-type="application/xhtml+xml"/>
    <item id="css" href="styles.css" media-type="text/css"/>
  </manifest>
  <spine>
    <itemref idref="nav"/>
    <itemref idref="book"/>
  </spine>
</package>
"""

    container_xml = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

    with ZipFile(EPUB_PATH, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=ZIP_STORED)
        zf.writestr("META-INF/container.xml", container_xml, compress_type=ZIP_DEFLATED)
        zf.writestr("OEBPS/content.opf", content_opf, compress_type=ZIP_DEFLATED)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml, compress_type=ZIP_DEFLATED)
        zf.writestr("OEBPS/book.xhtml", book_xhtml, compress_type=ZIP_DEFLATED)
        zf.writestr("OEBPS/styles.css", epub_css, compress_type=ZIP_DEFLATED)


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    build_book()
    build_index()
    build_epub()
    write_manuals_source_index()
