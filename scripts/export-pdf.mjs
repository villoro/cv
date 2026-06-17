// Export every CV to PDF using headless Chromium (Playwright).
// Replaces the old `cv/do_all.py` wkhtmltopdf wrapper.
//
// Assumes `astro build` has already run (dist/ exists). It boots Astro's
// static preview server, then prints each /print/<name>.html to a PDF.
//
// Env vars (all optional):
//   CV_DATA_DIR    folder of input YAMLs   (default: sample/input)
//   CV_OUTPUT_DIR  folder for the PDFs      (default: sample/output)
import fs from "node:fs";
import path from "node:path";
import { preview } from "astro";
import { chromium } from "playwright";

const ROOT = process.cwd();
const DATA_DIR = process.env.CV_DATA_DIR
  ? path.resolve(process.env.CV_DATA_DIR)
  : path.resolve(ROOT, "sample/input");
const OUT_DIR = process.env.CV_OUTPUT_DIR
  ? path.resolve(process.env.CV_OUTPUT_DIR)
  : path.resolve(ROOT, "sample/output");

const names = fs
  .readdirSync(DATA_DIR)
  .filter((f) => /\.ya?ml$/i.test(f))
  .map((f) => f.replace(/\.ya?ml$/i, ""));

if (names.length === 0) {
  console.error(`No YAML files found in ${DATA_DIR}`);
  process.exit(1);
}

fs.mkdirSync(OUT_DIR, { recursive: true });

const server = await preview({ root: ROOT, logLevel: "error" });
const base = `http://localhost:${server.port}`;
const browser = await chromium.launch();
const page = await browser.newPage();

try {
  for (const name of names) {
    const url = `${base}/print/${name}.html`;
    await page.goto(url, { waitUntil: "networkidle" });
    // Make sure the Avenir @font-face files are loaded before printing.
    await page.evaluate(() => document.fonts.ready);

    const out = path.join(OUT_DIR, `${name}.pdf`);
    await page.pdf({
      path: out,
      printBackground: true,
      preferCSSPageSize: true, // honour each CV's @page size from its config
      margin: { top: "0", bottom: "0", left: "0", right: "0" },
    });
    console.log(`-- Created ${path.relative(ROOT, out)} --`);
  }
} finally {
  await browser.close();
  await server.stop();
}
