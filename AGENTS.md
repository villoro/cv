# AGENTS.md

Working notes for this repository.

## What this project is

A personal CV generator. A static **Astro** site renders CVs as HTML; those pages are
exported to **PDF via headless Chromium (Playwright)**. All content lives in YAML; all
styling is inline, millimeter-based CSS so each page maps 1:1 to a physical A4 sheet.

The PDF is the real deliverable — the website is just the rendering surface for the converter.

> Migrated from Flask + wkhtmltopdf to Astro + Playwright (branch `feat/migrate_astro`).
> See "History" at the bottom for what the old stack looked like.

## Architecture (Astro)

```
src/
  lib/
    cv.ts          # load YAML + render Markdown to HTML (ports old utilities.py/config.py)
    styles.ts      # CSS ported verbatim from the old Jinja templates, config interpolated
  components/
    ContactBlock.astro   # sidebar contact rows (address/phone/email/web/linkedin)
    SkillBars.astro      # titled bar list (languages / expertise / programming)
    PlainList.astro      # titled plain list (expertise list / key skills)
    BodySections.astro   # name + pitch + Experience/Education/... entries
    CvPage.astro         # picks CvDocument vs CoverDocument by `template`
  layouts/
    CvDocument.astro     # full doc for cv_with_bars / cv_no_bars
    CoverDocument.astro  # full doc for the standalone cover page
  pages/
    index.astro          # "/"        -> default CV (preview frame)
    v/[name].astro       # "/v/<name>"     -> named CV (preview frame)
    view/[name].astro    # "/view/<name>"  -> alias of /v
    print/[name].astro   # "/print/<name>" -> frameless, what the PDF exporter renders
public/                  # fonts/, icons/ (17 themes x 5), images/ (served from site root)
scripts/export-pdf.mjs   # boots `astro preview`, prints each /print/<name> to PDF (was do_all.py)
sample/{input,output}/   # public sample YAMLs + generated PDFs (test fixture)
cv_private/{input,output}/ # private data (git submodule): 7 language variants + sample
utilities/               # offline Python image pipeline (Pillow/rembg) — NOT part of web/PDF path
```

### Data model (YAML per CV)
Top-level keys: `template` (`cv_no_bars` | `cv_with_bars` | `cover`), `full_name`, `address`
(list), `phone`, `web`, `linkedin`, `email`, `image_uri`, `image_link`, `titles` (section
labels = the i18n mechanism), `description` (markdown pitch), `expertise`, `languages`
(name → bar width in mm), `programming` (name → mm), `keyskills` (list), `body` (ordered map of
section → entries with `start/end/title/title_link/company/company_link/description`),
and `config` (page size, theme colour, sidebar width + many mm spacing knobs).

`description` and each body `description` are Markdown → rendered to HTML in `cv.ts` and
injected with `set:html`.

### Data source selection
`src/lib/cv.ts` reads from `sample/input` by default. Override with env vars:
- `CV_DATA_DIR`   — input folder (e.g. `cv_private/input`)
- `CV_OUTPUT_DIR` — PDF output folder (e.g. `cv_private/output`)
- `CV_DEFAULT`    — name shown at `/` (default `sample_1`)

### PDF export (`scripts/export-pdf.mjs`)
Requires `astro build` first (or use `npm run build:pdf`). Boots Astro's static preview
server, loads each `/print/<name>.html`, waits for `document.fonts.ready`, then
`page.pdf({ printBackground:true, preferCSSPageSize:true, margin:0 })`. Page size comes from
each CV's own `@page` rule (built from `config.page_width/height`).

## Commands
```
npm install
npx playwright install chromium   # one-time, downloads the headless browser
npm run dev                       # dev server on :4321
npm run build                     # static build into dist/
npm run pdf                       # export PDFs from existing dist/
npm run build:pdf                 # build + export
```

## Known follow-ups / gotchas
- **Only `cv_no_bars` is exercised** by real data (all 10 input files use it). `cv_with_bars`
  and `cover` are ported and code-reviewed but have no test data — verify if they're ever used.
- **Profile images are generated artifacts.** Real CVs point `image_uri` at a processed PNG
  (e.g. `images/DSC_0136_*.png`) that does NOT live in the repo — the Python pipeline in
  `utilities/` produces it. Post-migration its `folder_out` (set per-job in the private
  `cv_private/utils_jobs/*.yaml`) should write into `public/images`, not the old `cv/static/images`.
  Until then, real CVs render a broken-image box (defaults render fine).
- **Fidelity:** Chromium packs the pitch paragraphs a touch tighter than the old wkhtmltopdf,
  so the right column sits ~5mm higher. Agreed acceptable ("visually equivalent").
- **poetry.lock was removed** (couldn't regenerate without poetry installed). Run `poetry lock`
  if you use the `utilities/` Python pipeline. `pyproject.toml` now only covers `utilities/`.

## History (old Flask stack, removed)
`cv/index.py` (Flask, 4 routes) rendered Jinja templates `cv_base.html` +
`cv_with_bars/cv_no_bars/cover`; `cv/do_all.py` shelled out to `wkhtmltopdf` against
`localhost:5000/print/<name>`. Content loaded by `cv/utilities.py`, config in `cv/config.py`.
