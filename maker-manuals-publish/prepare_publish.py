from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = ROOT.parent

HUB_SOURCE = SOURCE_ROOT / "maker-manuals"

BOOKS = [
    {
        "slug": "vibecoding",
        "source": SOURCE_ROOT / "maker-manual-01",
        "pdf": "maker-manual-01-vibecoding.pdf",
        "epub": "maker-manual-01-vibecoding.epub",
    },
    {
        "slug": "ai-os",
        "source": SOURCE_ROOT / "maker-manual-02-ai-os",
        "pdf": "maker-manual-02-ai-os.pdf",
        "epub": "maker-manual-02-ai-os.epub",
    },
    {
        "slug": "het-ai-bedrijf",
        "source": SOURCE_ROOT / "maker-manual-03-ai-bedrijf",
        "pdf": "maker-manual-03-ai-bedrijf.pdf",
        "epub": "maker-manual-03-ai-bedrijf.epub",
    },
    {
        "slug": "ai-autonomie",
        "source": SOURCE_ROOT / "maker-manual-04-ai-autonomie",
        "pdf": "maker-manual-04-ai-autonomie.pdf",
        "epub": "maker-manual-04-ai-autonomie.epub",
    },
]


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)


def build_hub() -> None:
    copy_file(HUB_SOURCE / "index.html", ROOT / "index.html")
    copy_file(HUB_SOURCE / "styles.css", ROOT / "styles.css")

    html = (ROOT / "index.html").read_text()
    replacements = {
        "../index.html": "./index.html",
        "../maker-manual-01/site/index.html": "./vibecoding/",
        "../maker-manual-01/site/book.html": "./vibecoding/book/",
        "../maker-manual-01/exports/maker-manual-01-vibecoding.pdf": "./downloads/maker-manual-01-vibecoding.pdf",
        "../maker-manual-01/exports/maker-manual-01-vibecoding.epub": "./downloads/maker-manual-01-vibecoding.epub",
        "../maker-manual-02-ai-os/site/index.html": "./ai-os/",
        "../maker-manual-02-ai-os/site/book.html": "./ai-os/book/",
        "../maker-manual-02-ai-os/exports/maker-manual-02-ai-os.pdf": "./downloads/maker-manual-02-ai-os.pdf",
        "../maker-manual-02-ai-os/exports/maker-manual-02-ai-os.epub": "./downloads/maker-manual-02-ai-os.epub",
        "../maker-manual-03-ai-bedrijf/site/index.html": "./het-ai-bedrijf/",
        "../maker-manual-03-ai-bedrijf/site/book.html": "./het-ai-bedrijf/book/",
        "../maker-manual-03-ai-bedrijf/exports/maker-manual-03-ai-bedrijf.pdf": "./downloads/maker-manual-03-ai-bedrijf.pdf",
        "../maker-manual-03-ai-bedrijf/exports/maker-manual-03-ai-bedrijf.epub": "./downloads/maker-manual-03-ai-bedrijf.epub",
        "../maker-manual-04-ai-autonomie/site/index.html": "./ai-autonomie/",
        "../maker-manual-04-ai-autonomie/site/book.html": "./ai-autonomie/book/",
        "../maker-manual-04-ai-autonomie/exports/maker-manual-04-ai-autonomie.pdf": "./downloads/maker-manual-04-ai-autonomie.pdf",
        "../maker-manual-04-ai-autonomie/exports/maker-manual-04-ai-autonomie.epub": "./downloads/maker-manual-04-ai-autonomie.epub",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    (ROOT / "index.html").write_text(html)


def build_books() -> None:
    downloads = ROOT / "downloads"
    downloads.mkdir(parents=True, exist_ok=True)

    for book in BOOKS:
        slug = book["slug"]
        source = book["source"]
        landing_dir = ROOT / slug
        book_dir = landing_dir / "book"

        landing_dir.mkdir(parents=True, exist_ok=True)
        book_dir.mkdir(parents=True, exist_ok=True)

        copy_file(source / "site" / "styles.css", landing_dir / "styles.css")
        copy_file(source / "site" / "styles.css", book_dir / "styles.css")
        copy_file(source / "site" / "index.html", landing_dir / "index.html")
        copy_file(source / "site" / "book.html", book_dir / "index.html")

        landing_html = (landing_dir / "index.html").read_text()
        landing_html = landing_html.replace('./styles.css', './styles.css')
        landing_html = landing_html.replace('./book.html', './book/')
        landing_html = landing_html.replace(f'../exports/{book["pdf"]}', f'../downloads/{book["pdf"]}')
        landing_html = landing_html.replace(f'../exports/{book["epub"]}', f'../downloads/{book["epub"]}')
        (landing_dir / "index.html").write_text(landing_html)

        book_html = (book_dir / "index.html").read_text()
        book_html = book_html.replace('./styles.css', './styles.css')
        book_html = book_html.replace('../../maker-manuals/index.html', '../../')
        book_html = book_html.replace('./index.html', '../')
        (book_dir / "index.html").write_text(book_html)

        copy_file(source / "exports" / book["pdf"], downloads / book["pdf"])
        copy_file(source / "exports" / book["epub"], downloads / book["epub"])


def main() -> None:
    keep = {"prepare_publish.py", "README.md", "vercel.json"}
    for item in ROOT.iterdir():
        if item.name in keep:
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    build_hub()
    build_books()


if __name__ == "__main__":
    main()
