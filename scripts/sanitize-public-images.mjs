// Rename files under public/ to web-safe names (e.g. replace '#' with '_').
// The static dev/preview server cannot serve files whose names contain '#'
// (it is the URL fragment delimiter), so names are normalized here. The loader
// (src/lib/cv.ts) applies the same rule to image_uri values, keeping them in sync.
// Idempotent — safe to run on every dev/build.
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve("public");
const UNSAFE = /[^A-Za-z0-9._-]/g;

let renamed = 0;

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
    } else {
      const safe = entry.name.replace(UNSAFE, "_");
      if (safe !== entry.name) {
        fs.renameSync(full, path.join(dir, safe));
        renamed++;
      }
    }
  }
}

if (fs.existsSync(ROOT)) walk(ROOT);
if (renamed) console.log(`sanitize-public-images: renamed ${renamed} file(s)`);
