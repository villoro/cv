// Loads CV data from YAML files and converts the Markdown fields to HTML.
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import { marked } from "marked";

// Where the YAML inputs live. Set CV_DATA_DIR to point elsewhere (e.g.
// "cv_private/input"); defaults to the sample folder.
export const DATA_DIR = process.env.CV_DATA_DIR
  ? path.resolve(process.env.CV_DATA_DIR)
  : path.resolve("sample/input");

// Default CV shown at "/".
export const DEFAULT_NAME = process.env.CV_DEFAULT ?? "sample_1";

export interface CvEntry {
  start?: string;
  end?: string;
  title?: string;
  title_link?: string;
  company?: string;
  company_link?: string;
  description?: string;
}

export interface CvData {
  template: "cv_with_bars" | "cv_no_bars" | "cover" | string;
  full_name: string;
  address?: string[];
  phone?: string;
  web?: string;
  linkedin?: string;
  email?: string;
  image_uri?: string;
  image_link?: string;
  titles?: Record<string, string>;
  description?: string;
  // `expertise` is a list (cv_no_bars) or a name->mm map (cv_with_bars).
  expertise?: string[] | Record<string, number>;
  languages?: Record<string, number>;
  programming?: Record<string, number>;
  keyskills?: string[];
  body?: Record<string, CvEntry[]>;
  config: Record<string, number | string>;
}

marked.setOptions({ async: false });

function md(text: string): string {
  return marked.parse(text) as string;
}

// Render the pitch and every body entry description from Markdown to HTML.
function transformMarkdown(data: CvData): void {
  if (data.description) data.description = md(data.description);
  if (data.body) {
    for (const block of Object.values(data.body)) {
      for (const entry of block) {
        if (entry.description) entry.description = md(entry.description);
      }
    }
  }
}

// Characters that don't survive the static server (e.g. '#', spaces) are
// replaced with '_'. scripts/sanitize-public-images.mjs renames the files on
// disk with the same rule, so a sanitized image_uri always points at a real file.
const UNSAFE_ASSET_CHARS = /[^A-Za-z0-9._/-]/g;

/** Web-safe version of an asset path (slashes preserved). */
export function sanitizeAssetPath(relPath: string): string {
  return relPath.replace(UNSAFE_ASSET_CHARS, "_");
}

/** Root-relative URL for a file served from public/. */
export function assetUrl(relPath: string): string {
  return "/" + sanitizeAssetPath(relPath);
}

/** Names of every CV available (file stems, without extension). */
export function listNames(): string[] {
  return fs
    .readdirSync(DATA_DIR)
    .filter((f) => /\.ya?ml$/i.test(f))
    .map((f) => f.replace(/\.ya?ml$/i, ""));
}

/** Load and prepare a single CV by name. */
export function getContent(name?: string): CvData {
  const stem = (name ?? DEFAULT_NAME).split(".")[0];
  const file = path.join(DATA_DIR, `${stem}.yaml`);
  const data = yaml.load(fs.readFileSync(file, "utf-8")) as CvData;
  transformMarkdown(data);
  return data;
}
