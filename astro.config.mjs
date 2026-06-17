// @ts-check
import { defineConfig } from "astro/config";

// Static site. `format: "file"` makes pages build to `/print/<name>.html`
// (instead of `/print/<name>/index.html`), mirroring the old Flask routes that
// wkhtmltopdf used to hit.
export default defineConfig({
  build: { format: "file" },
  server: { port: 4321 },
});
