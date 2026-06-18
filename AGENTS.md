# AGENTS.md

Working notes for this repository.

## What this project is

A personal CV generator. A static **Astro** site renders CVs as HTML; those pages are
exported to **PDF via headless Chromium (Playwright)**. All content lives in YAML; all
styling is inline, millimeter-based CSS so each page maps 1:1 to a physical A4 sheet.

The PDF is the real deliverable — the website is just the rendering surface for the converter.

## Architecture

```
src/
  lib/
    cv.ts          # load YAML + render Markdown to HTML
    styles.ts      # inline CSS for the documents, config values interpolated
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
    index.astro          # "/"             -> default CV (preview frame)
    v/[name].astro       # "/v/<name>"      -> named CV (preview frame)
    view/[name].astro    # "/view/<name>"   -> alias of /v
    print/[name].astro   # "/print/<name>"  -> frameless, what the PDF exporter renders
public/                  # fonts/, icons/ (17 themes x 5), images/ (served from site root)
scripts/
  export-pdf.mjs   # boots `astro preview`, prints each /print/<name> to PDF
  process.py + image_transformations.py  # offline Python image pipeline (Pillow/rembg)
  pyproject.toml + uv.lock               # uv project for the Python pipeline (NOT the web/PDF path)
sample/{input,output}/   # public sample YAMLs + generated PDFs (test fixture)
cv_private/{input,output}/ # private data (git submodule): 7 language variants + sample
```

### Data model (YAML per CV)
Top-level keys: `template` (`cv_no_bars` | `cv_with_bars` | `cover`), `full_name`, `address`
(list), `phone`, `web`, `linkedin`, `email`, `image_uri`, `image_link`, `titles` (section
labels = the i18n mechanism), `description` (markdown pitch), `expertise`, `languages`
(name → bar width in mm), `programming` (name → mm), `keyskills` (list), `body` (ordered map of
section → entries with `start/end/title/title_link/company/company_link/description`),
and `config` (page size, theme colour, sidebar width + many mm spacing knobs).

`description` and each body `description` are Markdown, rendered to HTML in `cv.ts` and
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

## Tooling
- **Hooks:** run with **prek** (config in `.pre-commit-config.yaml`). CI uses `j178/prek-action@v2`.
- **Python lint+format:** **ruff**; `ruff.toml` sets `line-length = 100`.
- **Python deps:** **uv** — `scripts/pyproject.toml` + `scripts/uv.lock`; run with
  `uv sync` / `uv run python process.py` from `scripts/`.
- **Versioning:** [villoro/vhooks](https://github.com/villoro/vhooks) reads `package.json` →
  `version`. `check_version.yaml` (PR) enforces a bump; `tag_version.yaml` (push to `main`) tags.
  Repo version is **`3.0.0`**.

## Known gotchas
- All current input YAMLs use the `cv_no_bars` template. `cv_with_bars` and `cover` are
  implemented but have no test data — verify if they're ever used.
- **Profile images are generated artifacts.** Real CVs point `image_uri` at a processed PNG
  (e.g. `images/DSC_0136_*.png`) that is not stored in the repo — the `scripts/` Python pipeline
  produces it. Set that pipeline's `folder_out` (per-job in `cv_private/utils_jobs/*.yaml`) to
  `public/images`; until then real CVs render a broken-image box (defaults render fine).
