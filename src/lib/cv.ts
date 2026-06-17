// Loads CV data from YAML files and converts the Markdown fields to HTML.
// Direct port of the old Flask `cv/utilities.py` + `cv/config.py`.
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import { marked } from "marked";

// Where the YAML inputs live. The old Flask `config.py` toggled between
// "cv_private/input" (private submodule) and "sample/input" by editing source.
// Here it is an env var so nothing in source has to change.
export const DATA_DIR = process.env.CV_DATA_DIR
  ? path.resolve(process.env.CV_DATA_DIR)
  : path.resolve("sample/input");

// Default CV shown at "/" (was FILE_DEFAULT = "sample_1").
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

// Mirrors utilities._transform_from_markdown: render the pitch and every body
// entry description from Markdown to HTML.
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
