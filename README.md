# Maker Manuals

Maker Manuals is een reeks praktische gidsen van Erwin Blom voor makers, zelfstandigen en kleine teams die AI slim willen inzetten zonder eerst technisch te hoeven worden.

Deze repository is de publieke laag van die reeks: de plek waar de websites, publieksingangen en publicatiebestanden samenkomen.

## Waar begin je?

Wil je de reeks verkennen of gewoon lezen? Begin dan hier:

- [maker-manuals.vercel.app](https://maker-manuals.vercel.app/)

## Wat je hier vindt

- `maker-manuals/` - de centrale publieksingang van de reeks
- `maker-manual-01-vibecoding/` - `Vibecoding`
- `maker-manual-02-ai-os/` - `AI-OS`
- `maker-manual-03-ai-bedrijf/` - `Het AI-bedrijf`
- `maker-manual-04-ai-autonomie/` - `AI-autonomie`
- `maker-manuals-vercel/` - de Vercel-publicatielaag
- `index.html` en `home.css` - de bovenliggende publieksingang

## Voor wie dit is

Deze reeks is bedoeld voor mensen die wel met AI willen werken, maar geen behoefte hebben aan technisch gedoe, toolhype of abstracte toekomstpraat.

## Voor beheerders

Dit deel is voor wie aan de inhoud of publicatielaag werkt.

### Waar pas je teksten aan

- Overkoepelende reeks-pagina: `reeks-content/maker-manuals.md`
- Boek-overzichtspagina per manual: `maker-manual-01-vibecoding/content.md` tot en met `maker-manual-04-ai-autonomie/content.md`
- Lopende boektekst zelf: het markdownbestand in `manuscript/`

### Naamregel voor bestanden

Gebruik voor bestandsnamen binnen de `Maker Manuals`-reeks voortaan de korte familiecode:

- `MM` = hele reeks
- `MM-01` = `Vibecoding`
- `MM-02` = `AI-OS`
- `MM-03` = `Het AI-bedrijf`
- `MM-04` = `AI-autonomie`

Praktische regel:

- mapnamen mogen beschrijvend blijven
- bestandsnamen binnen de boekmappen worden bij voorkeur kort en scanbaar met `YYYY-MM-DD-MM-..-...`

Voorbeelden:

- `2026-06-13-MM-04-manuscript-draft-01.md`
- `2026-06-13-MM-04-positionering-en-inhoudsopgave.md`
- `2026-06-13-MM-04-bronnenrichtingen.md`
- `2026-06-13-MM-04-greg-isenberg-lokale-modellen-als-verzekering.md`

De markdownbestanden zijn nu expres menselijk opgezet, met gewone secties als:

- `Lead`
- `Kaart op reeks-pagina`
- `Statusblok`
- `Zijbalk`
- `Blokken`
- `Hoofdstukken`

### Opnieuw opbouwen

- Alleen de reeks-pagina: `python3 maker-manuals/build_page.py`
- Een boekpagina en de gekoppelde reeks-kaart: draai het bestaande `site/build_site.py` in die boekmap
- Publicatielaag verversen: `python3 maker-manuals-vercel/prepare_publish.py`

### Werkwijze

1. Werk inhoudelijk in de juiste boekmap.
2. Werk bij betekenisvolle wijzigingen ook het juiste `CHANGELOG.md` bij.
3. Gebruik in Vercel voortaan alleen het project `maker-manuals-vercel` als canonieke publicatielaag voor `maker-manuals.vercel.app`.

Oud Vercel-project:

- `maker-manuals-publish-archief` is alleen nog archief en niet meer de leidende live-publicatie.
4. Gebruik voor commits dit format:

`[Boektitel]: [inhoud|site|export|structuur] - [wijziging]`

Voorbeelden:

- `Vibecoding: inhoud - openingshoofdstuk aangescherpt`
- `AI-OS: site - landingspagina versimpeld`
- `Het AI-bedrijf: export - PDF en EPUB vernieuwd`
- `AI-autonomie: structuur - bronlaag uitgebreid`

### Wat hier niet in hoort

Losse conceptnotities, screenshots en andere publiekslaag-experimenten die niet direct onderdeel zijn van de `Maker Manuals`-reeks.

### GitHub Desktop

Open deze map als repository:

`/Users/eb-air/Desktop/Blom-OS/00_Algemeen/mijn-os/publiekslaag`

Dan zie je wijzigingen aan de boeken, sites, changelogs en publicatielaag direct terug in GitHub Desktop.
