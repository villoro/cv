# AGENTS.md

Working notes for this repository. Goal: **migrate from Flask to Astro** while preserving exact PDF output.

## What this project is

A personal CV generator. A small Flask webapp renders CVs as HTML pages; those pages are
then exported to PDF with **wkhtmltopdf**. All content lives in YAML; all styling is inline,
millimeter-based CSS templated with Jinja2 variables so the page maps 1:1 to a physical A4 sheet.

The PDF is the real deliverable — the website is just the rendering surface for the converter.

## Current architecture (Flask)

```
cv/
  index.py        # Flask app, 4 routes
  config.py       # paths, wkhtmltopdf exe path, default file, print URL
  utilities.py    # loads YAML, converts markdown -> HTML
  do_all.py       # loops input YAMLs, calls wkhtmltopdf per file
  static/
    fonts/        # Avenir LT Std OTFs (35/Light, 45/Book, 55/Roman used; Medium/Oblique present)
    icons/        # 17 color themes x 5 contact icons (address/email/linkedin/phone/web).jpg
    images/       # profile pictures
  templates/
    cv_base.html      # ALL CSS lives here (inline <style>), layout = sidebar + body
    cv_with_bars.html # extends base: languages/expertise/programming as bars
    cv_no_bars.html   # extends base: languages as bars, expertise+keyskills as lists
    cover.html        # extends base: full-width name + description only
sample/{input,output}/    # public sample YAMLs + generated PDFs
cv_private/{input,output}/ # private data (git submodule), 7 language variants + sample
utilities/                 # offline image processing (Pillow/rembg/pydantic) — NOT part of web/PDF path
```

### Routes (`cv/index.py`)
- `/` → default sample (preview, with frame)
- `/v/<name>` and `/view/<name>` → named CV, preview (frame shown)
- `/print/<name>` → named CV, **no frame** (this is what wkhtmltopdf hits)
- `/print.html` → default sample, no frame

`preview=True` wraps the page in a grey `.frame` div for on-screen viewing; the PDF route sets
`preview=False` so no frame is rendered.

### Data model (YAML per CV)
Top-level keys: `template` (which of the 3 templates), `full_name`, `address` (list), `phone`,
`web`, `linkedin`, `email`, `image_uri`, `image_link`, `titles` (section labels = the i18n mechanism),
`description` (markdown pitch), `expertise`, `languages` (name → bar width in mm), `programming`
(name → mm), `keyskills` (list), `body` (ordered dict of sections → list of entries with
`start/end/title/title_link/company/company_link/description`), and `config` (per-CV overrides).

Markdown → HTML conversion happens in `utilities._transform_from_markdown` for `description`
and each body entry's `description`. Templates render that HTML with `{% autoescape false %}`.

### Styling — the critical part
- `cv_base.html` holds the entire stylesheet inline, with Jinja interpolating values from each
  YAML's `config` block: `page_width`, `page_height`, `sidebar_width`, `padding`, `theme_color`,
  `sidebar_color`, `bar_background_color`, `date2_color`, and many mm padding/width knobs.
- Layout is **float-based** and sized in **mm** to match A4 (210×297mm). Bar widths are literal mm.
- Fonts loaded via `@font-face` from `static/fonts`.
- Contact icons are chosen at render time by `config.theme_color_name` (a folder under `icons/`).

### PDF export (`do_all.py`)
Calls `wkhtmltopdf` per input YAML against `localhost:5000/print/<name>.html`. Options:
`--javascript-delay 3000`, `--dpi 300`, margins `-T/-B/-L/-R 0`, `--disable-smart-shrinking`,
`--print-media-type`. Requires the Flask server running. Windows exe path hardcoded in `config.py`.

### Tooling
- Poetry (`pyproject.toml`), Python 3.10–3.11. Deps: flask, markdown, oyaml.
- Pre-commit: black, check-yaml/json/toml, poetry-check.
- GitHub Actions: CI (pre-commit), version bump, tag-on-main.

## Migration decisions (agreed)
- **PDF engine:** switch to Playwright/Puppeteer (headless Chromium). Expect to re-tune mm/float CSS.
- **Fidelity bar:** visually equivalent (same content & look; minor spacing differences OK). CSS may be modernized.
- **Scope:** migrate web + PDF, remove Flask entirely. Keep `utilities/` Python image pipeline as-is, out of scope.
- **Workflow:** produce a detailed plan for approval before building.

## Migration notes / risks (Flask → Astro)

- **Layout fidelity is the #1 risk.** wkhtmltopdf is an old WebKit. Moving to a modern Chromium-based
  converter (Playwright/Puppeteer) can shift float/mm rendering. Output must be diffed page-by-page.
  Decision pending: keep wkhtmltopdf, or switch converters.
- Astro is static → Flask backend disappears. YAML → Astro Content Collections; the 3 templates →
  Astro layouts selected by a frontmatter/`template` field; dynamic `config` → CSS custom properties
  or inline style bindings.
- Markdown is built into Astro (drop the Python `markdown` lib).
- The `utilities/` image pipeline is independent of the web/PDF path — likely stays in Python, out of scope.
- Private data is a git submodule; sample data is the public test fixture for the migration.

## Useful commands (current)
```
poetry install
poetry run python cv/index.py     # dev server on :5000
poetry run python cv/do_all.py    # export all PDFs (server must be running)
./create_sample.sh                # export the sample PDF
```
