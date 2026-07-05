// Downscale oversized images under public/ so the PDF (which embeds them at
// full resolution) stays small. Profile photos are shown at ~36mm, so a few
// hundred pixels is plenty for print. Idempotent: images already within the
// cap are skipped, and re-running does nothing.
import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

const ROOT = path.resolve("public");
const MAX = Number(process.env.CV_IMAGE_MAX_PX ?? 600); // max width/height in px
const EXT = new Set([".png", ".jpg", ".jpeg"]);

let changed = 0;
let saved = 0;

async function optimize(file) {
  const ext = path.extname(file).toLowerCase();
  if (!EXT.has(ext)) return;

  // Read into a buffer first so sharp doesn't hold the file open while we
  // overwrite it (that lock fails on Windows).
  const input = fs.readFileSync(file);
  const before = input.length;
  const meta = await sharp(input).metadata();
  if (Math.max(meta.width ?? 0, meta.height ?? 0) <= MAX) return;

  let pipe = sharp(input).resize(MAX, MAX, { fit: "inside", withoutEnlargement: true });
  pipe = ext === ".png" ? pipe.png({ compressionLevel: 9 }) : pipe.jpeg({ quality: 85, mozjpeg: true });
  const buf = await pipe.toBuffer();
  fs.writeFileSync(file, buf);

  changed++;
  saved += before - buf.length;
}

async function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) await walk(full);
    else await optimize(full);
  }
}

if (fs.existsSync(ROOT)) await walk(ROOT);
if (changed) {
  console.log(`optimize-public-images: shrank ${changed} image(s), saved ${(saved / 1048576).toFixed(1)} MB`);
}
