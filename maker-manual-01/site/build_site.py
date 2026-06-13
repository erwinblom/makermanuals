from __future__ import annotations

from html import escape
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
MANUSCRIPT = PROJECT_ROOT / "manuscript" / "versies" / "2026-06-13-maker-manual-01-vibecoding-manuscript-final.md"
LICENSE = PROJECT_ROOT / "manuscript" / "2026-06-13-maker-manual-01-vibecoding-license.md"
BOOK_HTML = ROOT / "book.html"
INDEX_HTML = ROOT / "index.html"
EPUB_PATH = PROJECT_ROOT / "exports" / "maker-manual-01-vibecoding.epub"


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
    manuscript_html = markdown_to_html(MANUSCRIPT.read_text())
    license_html = markdown_to_html(LICENSE.read_text())

    book = f"""<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Vibecoding</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body class="book-body">
    <main class="book-shell">
      <a class="back-link" href="../../maker-manuals/index.html">Terug naar Maker Manuals</a>
      <aside class="book-side">
        <p class="eyebrow">Maker Manuals 01</p>
        <h1>Vibecoding</h1>
        <p class="side-summary">Apps en tools bouwen zonder technische achtergrond.</p>
        <div class="side-box">
          <strong>Formaat</strong>
          <span>Webeditie in neo brutalism-stijl</span>
        </div>
        <div class="side-box">
          <strong>Licentie</strong>
          <span>CC BY-SA 4.0</span>
        </div>
        <div class="side-box">
          <strong>Status</strong>
          <span>Alpha-editie 0.8</span>
        </div>
      </aside>
      <article class="book-article">
        {manuscript_html}
      </article>
    </main>
    <section class="license-strip">
      {license_html}
    </section>
  </body>
</html>
"""
    BOOK_HTML.write_text(book)


def build_index() -> None:
    index = """<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Vibecoding</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body class="landing-body">
    <main class="landing-shell">
      <section class="hero-card">
        <div class="hero-copy">
          <p class="eyebrow">Maker Manuals 01</p>
          <h1>Vibecoding</h1>
          <p class="lead">Apps en tools bouwen zonder technische achtergrond.</p>
          <div class="hero-actions">
            <a class="primary-action" href="./book.html">Lees het manual</a>
            <a class="secondary-action" href="../exports/maker-manual-01-vibecoding.pdf">Download PDF</a>
            <a class="secondary-action" href="../exports/maker-manual-01-vibecoding.epub">Download EPUB</a>
          </div>
        </div>
        <aside class="hero-note">
          <strong>Alpha-editie 0.8</strong>
          <span>Levend boek in ontwikkeling. Deze uitgave wordt doorlopend aangescherpt en geactualiseerd. Bewust werk in uitvoering dus, geen eindpunt.</span>
        </aside>
      </section>

      <section class="grid">
        <article class="tile yellow">
          <span>01</span>
          <h2>Waarom dit werkt</h2>
          <p>Het boek zit niet vast aan toolhype, maar aan een blijvende verschuiving: meer makers kunnen dichter op software gaan zitten.</p>
        </article>

        <article class="tile mint">
          <span>02</span>
          <h2>Hoe je het leest</h2>
          <p>Als webeditie, als EPUB, als PDF en als markdown-bronbestand. De webversie is de hoofdversie.</p>
        </article>

        <article class="tile red">
          <span>03</span>
          <h2>Wat je ermee mag</h2>
          <p>CC BY-SA 4.0: delen, hergebruiken en bewerken mag, zolang je Erwin Blom noemt en afgeleiden onder dezelfde licentie deelt.</p>
        </article>
      </section>

      <section class="chapter-strip">
        <div class="chapter-head">
          <p class="eyebrow">In dit manual</p>
          <h2>Acht hoofdstukken</h2>
        </div>
        <div class="chapter-list">
          <div>Waarom vibecoding ertoe doet</div>
          <div>Wat vibecoding wel en niet is</div>
          <div>Begin kleiner dan je denkt</div>
          <div>Werk vanuit taken, niet vanuit tools</div>
          <div>Van idee naar eerste bruikbare versie</div>
          <div>Smaak, oordeel en productgevoel</div>
          <div>Het speelveld verandert snel</div>
          <div>Wat blijft als de hype weg is</div>
        </div>
      </section>
    </main>
  </body>
</html>
"""
    INDEX_HTML.write_text(index)


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
code { font-family: monospace; background: #f3e7a5; padding: 0.1em 0.25em; }
"""

    book_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="nl">
  <head>
    <title>Maker Manual 01: Vibecoding</title>
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
        <li><a href="book.xhtml">Vibecoding</a></li>
      </ol>
    </nav>
  </body>
</html>
"""

    content_opf = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">maker-manual-01-vibecoding</dc:identifier>
    <dc:title>Vibecoding</dc:title>
    <dc:language>nl</dc:language>
    <dc:creator>Erwin Blom</dc:creator>
    <meta property="dcterms:modified">2026-06-13T12:50:00Z</meta>
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
