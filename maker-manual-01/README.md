# Maker Manuals 01 - Vibecoding

Dit is de canonieke projectmap voor `Vibecoding`.

Ondertitel:
`Apps en tools bouwen zonder technische achtergrond`

Status:
`Alpha-editie 0.8 - levend boek in ontwikkeling`

Dit boek is bewust een werk in uitvoering: geen eindpunt, maar een versie die beter wordt terwijl het onderwerp beweegt.

## Structuur

- `bronnen/`
  Redactionele bouwlaag: brontriage, blueprint en hoofdstukmemo's.

- `manuscript/`
  Tekstlaag.
  - `hoofdstukken/` bevat de losse hoofdstukconcepten
  - `versies/` bevat de samengevoegde manuscriptversies
  - `2026-06-13-maker-manual-01-vibecoding-license.md` is de licentielaag
  - `2026-06-13-maker-manual-01-vibecoding-opening.md` is de opening/inhoudslaag

- `site/`
  Publieke leeslaag in neo brutalism-stijl.
  - `index.html` is de landingspagina
  - `book.html` is de online leesversie
  - `styles.css` bevat de vormgeving
  - `build_site.py` bouwt `book.html`, `index.html` en de `EPUB`

- `exports/`
  Afgeleide downloadformaten.
  - `maker-manual-01-vibecoding.epub`
  - `maker-manual-01-vibecoding.pdf`

## Bron van waarheid

De leidende tekstversie is:

- `manuscript/versies/2026-06-13-maker-manual-01-vibecoding-manuscript-final.md`

De site is de online leesversie van die bron.

## Werkwijze

1. Werk inhoudelijk eerst in markdown.
2. Gebruik daarna `site/build_site.py` om de webversie en `EPUB` opnieuw op te bouwen.
3. Render de `PDF` vanuit `site/book.html`, zodat vorm en online leesversie dicht bij elkaar blijven.
