# Maker Manuals - Vercel publicatie

Dit is de schone publicatiemap voor de `Maker Manuals`-reeks.

## Waarom deze map bestaat

De bronlaag van de manuals zit verspreid over:

- `maker-manuals/`
- `maker-manual-01-vibecoding/`
- `maker-manual-02-ai-os/`
- `maker-manual-03-ai-bedrijf/`
- `maker-manual-04-ai-autonomie/`

Voor Vercel is een compacte, voorspelbare publicatiemap handiger. Daarom staat hier een afgeleide publicatielaag met:

- de reeks-hub als homepage
- per manual een eigen publieke route
- een centrale `downloads/`-map voor PDF en EPUB

## Werkwijze

1. Werk inhoud en sites bij in de bronmappen.
2. Draai daarna:

`python3 prepare_publish.py`

3. Publiceer vervolgens deze map als Vercel-root.

## Belangrijk

Deze map is afgeleid, niet leidend. De bron van waarheid blijft in de boekmappen zelf.
