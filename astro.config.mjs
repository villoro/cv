// @ts-check
import { defineConfig } from "astro/config";

// Static site. `format: "file"` makes pages build to `/print/<name>.html`
// (instead of `/print/<name>/index.html`).
export default defineConfig({
  build: { format: "file" },
  server: { port: 4321 },
});
