from __future__ import annotations

from html import escape
from pathlib import Path


PUBLIEKSLAAG_ROOT = Path(__file__).resolve().parent
ROOT_CONTENT = PUBLIEKSLAAG_ROOT / "content" / "maker-manuals.md"
BOOK_DIRS = [
    "maker-manual-01",
    "maker-manual-02-ai-os",
    "maker-manual-03-ai-bedrijf",
    "maker-manual-04-ai-autonomie",
]


def text_html(text: str) -> str:
    return escape(text)


def read_lines(path: Path) -> list[str]:
    return path.read_text().splitlines()


def strip_title(lines: list[str]) -> tuple[str, list[str]]:
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    return title, lines


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    buffer: list[str] = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            if current is not None:
                sections[current] = buffer
            current = line[3:].strip()
            buffer = []
            continue
        if current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = buffer
    return sections


def join_text(lines: list[str]) -> str:
    return " ".join(line.strip() for line in lines if line.strip())


def parse_subblocks(lines: list[str]) -> dict[str, str]:
    blocks: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("### "):
            if current is not None:
                blocks[current] = join_text(buffer)
            current = line[4:].strip()
            buffer = []
            continue
        if current is not None:
            buffer.append(line)

    if current is not None:
        blocks[current] = join_text(buffer)
    return blocks


def parse_titled_blocks(lines: list[str]) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current_title: str | None = None
    current_body: list[str] = []

    def flush() -> None:
        nonlocal current_title, current_body
        if current_title is not None:
            blocks.append({"title": current_title, "body": join_text(current_body)})
        current_title = None
        current_body = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("### "):
            flush()
            current_title = line[4:].strip()
            continue
        if current_title is not None:
            current_body.append(line)

    flush()
    return blocks


def parse_tiles(lines: list[str]) -> list[dict[str, str]]:
    tiles: list[dict[str, str]] = []
    for block in parse_titled_blocks(lines):
        head = block["title"]
        tone, title = [part.strip() for part in head.split("|", 1)]
        tiles.append({"tone": tone, "title": title, "body": block["body"]})
    return tiles


def parse_sidebar(lines: list[str]) -> list[dict[str, str]]:
    return [{"label": title, "value": body} for title, body in parse_subblocks(lines).items()]


def parse_chapters(lines: list[str]) -> tuple[str, list[str]]:
    title = ""
    current: str | None = None
    title_lines: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("### "):
            current = line[4:].strip()
            continue
        if current == "Titel":
            if line.strip().startswith("- "):
                current = None
                continue
            if line.strip():
                title_lines.append(line.strip())
    title = " ".join(title_lines).strip()
    chapters = [line[2:].strip() for line in lines if line.strip().startswith("- ")]
    return title, chapters


def load_root_content() -> dict:
    title, lines = strip_title(read_lines(ROOT_CONTENT))
    sections = split_sections(lines)
    note = parse_subblocks(sections.get("Notitieblok", []))
    return {
        "title": title,
        "back_link_label": join_text(sections.get("Teruglink", [])),
        "stamp": join_text(sections.get("Stempel", [])),
        "lead": join_text(sections.get("Lead", [])),
        "hero_note_title": note.get("Titel", ""),
        "hero_note_body": note.get("Tekst", ""),
        "intro_cards": parse_titled_blocks(sections.get("Introkaarten", [])),
    }


def load_book_content(path: Path) -> dict:
    title, lines = strip_title(read_lines(path))
    sections = split_sections(lines)
    card = parse_subblocks(sections.get("Kaart op reeks-pagina", []))
    status_block = parse_subblocks(sections.get("Statusblok", []))
    chapters_title, chapters = parse_chapters(sections.get("Hoofdstukken", []))
    downloads = parse_subblocks(sections.get("Downloads", []))

    return {
        "page_title": title,
        "title": title,
        "book_label": join_text(sections.get("Boeklabel", [])),
        "overview_status": join_text(sections.get("Status kort", [])),
        "lead": join_text(sections.get("Lead", [])),
        "overview_subtitle": card.get("Ondertitel", ""),
        "overview_summary": card.get("Samenvatting", ""),
        "status_badge": status_block.get("Badge", ""),
        "status_note": status_block.get("Tekst", ""),
        "side_boxes": parse_sidebar(sections.get("Zijbalk", [])),
        "tiles": parse_tiles(sections.get("Blokken", [])),
        "chapters_title": chapters_title,
        "chapters": chapters,
        "exports": {
            "pdf": downloads.get("PDF", ""),
            "epub": downloads.get("EPUB", ""),
        },
        "theme": join_text(sections.get("Thema", [])),
    }


def render_book_page(config: dict, manuscript_html: str, license_html: str) -> str:
    side_boxes = "\n".join(
        f"""        <div class="side-box">
          <strong>{text_html(box["label"])}</strong>
          <span>{text_html(box["value"])}</span>
        </div>"""
        for box in config["side_boxes"]
    )

    return f"""<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{text_html(config["page_title"])}</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body class="book-body">
    <main class="book-shell">
      <a class="back-link" href="../../maker-manuals/index.html">Terug naar Maker Manuals</a>
      <aside class="book-side">
        <p class="eyebrow">{text_html(config["book_label"])}</p>
        <h1>{text_html(config["title"])}</h1>
        <p class="side-summary">{text_html(config["lead"])}</p>
{side_boxes}
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


def render_book_index(config: dict) -> str:
    tiles = "\n".join(
        f"""        <article class="tile {text_html(tile["tone"])}">
          <span>{index:02d}</span>
          <h2>{text_html(tile["title"])}</h2>
          <p>{text_html(tile["body"])}</p>
        </article>"""
        for index, tile in enumerate(config["tiles"], start=1)
    )
    chapter_items = "\n".join(f"          <div>{text_html(chapter)}</div>" for chapter in config["chapters"])

    return f"""<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{text_html(config["page_title"])}</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body class="landing-body">
    <main class="landing-shell">
      <section class="hero-card">
        <div class="hero-copy">
          <p class="eyebrow">{text_html(config["book_label"])}</p>
          <h1>{text_html(config["title"])}</h1>
          <p class="lead">{text_html(config["lead"])}</p>
          <div class="hero-actions">
            <a class="primary-action" href="./book.html">Lees het manual</a>
            <a class="secondary-action" href="../exports/{text_html(config["exports"]["pdf"])}">Download PDF</a>
            <a class="secondary-action" href="../exports/{text_html(config["exports"]["epub"])}">Download EPUB</a>
          </div>
        </div>
        <aside class="hero-note">
          <strong>{text_html(config["status_badge"])}</strong>
          <span>{text_html(config["status_note"])}</span>
        </aside>
      </section>

      <section class="grid">
{tiles}
      </section>

      <section class="chapter-strip">
        <div class="chapter-head">
          <p class="eyebrow">In dit manual</p>
          <h2>{text_html(config["chapters_title"])}</h2>
        </div>
        <div class="chapter-list">
{chapter_items}
        </div>
      </section>
    </main>
  </body>
</html>
"""


def load_book_configs() -> list[dict]:
    return [load_book_content(PUBLIEKSLAAG_ROOT / book_dir / "content.md") for book_dir in BOOK_DIRS]


def render_manuals_index(root_config: dict, books: list[dict]) -> str:
    first_row = root_config["intro_cards"][:2]
    second_row = root_config["intro_cards"][2:]

    first_row_html = "\n".join(
        f"""        <div class="intro-card">
          <h2>{text_html(card["title"])}</h2>
          <p>{text_html(card["body"])}</p>
        </div>"""
        for card in first_row
    )
    second_row_html = "\n".join(
        f"""        <div class="intro-card">
          <h2>{text_html(card["title"])}</h2>
          <p>{text_html(card["body"])}</p>
        </div>"""
        for card in second_row
    )
    book_cards = "\n".join(
        f"""        <article class="book-card {text_html(book["theme"])}">
          <div class="book-top">
            <p class="book-label">{text_html(book["book_label"])}</p>
            <p class="book-status">{text_html(book["overview_status"])}</p>
          </div>
          <h2>{text_html(book["title"])}</h2>
          <p class="subtitle">{text_html(book["overview_subtitle"])}</p>
          <p class="summary">{text_html(book["overview_summary"])}</p>
          <div class="actions">
            <a href="../{text_html(book["dir"])}/site/index.html">Open manual</a>
            <a href="../{text_html(book["dir"])}/site/book.html">Lees online</a>
            <a href="../{text_html(book["dir"])}/exports/{text_html(book["exports"]["pdf"])}">PDF</a>
            <a href="../{text_html(book["dir"])}/exports/{text_html(book["exports"]["epub"])}">EPUB</a>
          </div>
        </article>"""
        for book in books
    )

    return f"""<!doctype html>
<html lang="nl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{text_html(root_config["title"])}</title>
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <main class="shell">
      <a class="back-link" href="../index.html">{text_html(root_config["back_link_label"])}</a>

      <header class="hero">
        <div class="hero-copy">
          <p class="stamp">{text_html(root_config["stamp"])}</p>
          <h1>{text_html(root_config["title"])}</h1>
          <p class="lead">{text_html(root_config["lead"])}</p>
        </div>
        <aside class="hero-note">
          <strong>{text_html(root_config["hero_note_title"])}</strong>
          <span>{text_html(root_config["hero_note_body"])}</span>
        </aside>
      </header>

      <section class="intro">
{first_row_html}
      </section>

      <section class="intro trilogy">
{second_row_html}
      </section>

      <section class="books" aria-label="{text_html(root_config["title"])}">
{book_cards}
      </section>
    </main>
  </body>
</html>
"""


def write_manuals_source_index() -> Path:
    root_config = load_root_content()
    books = load_book_configs()
    for book, book_dir in zip(books, BOOK_DIRS, strict=True):
        book["dir"] = book_dir
    output_path = PUBLIEKSLAAG_ROOT / "maker-manuals" / "index.html"
    output_path.write_text(render_manuals_index(root_config, books))
    return output_path
