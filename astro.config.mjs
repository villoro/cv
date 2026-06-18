// @ts-check
import { defineConfig } from "astro/config";
import path from "node:path";

const dataDir = process.env.CV_DATA_DIR
  ? path.resolve(process.env.CV_DATA_DIR)
  : path.resolve("sample/input");

// The CV YAMLs are read via fs (not imported), so Vite doesn't watch them.
// Trigger a full browser reload when a YAML in the data folder changes.
function watchCvData() {
  return {
    name: "watch-cv-data",
    configureServer(server) {
      server.watcher.add(dataDir);
      const reload = (file) => {
        if (/\.ya?ml$/i.test(file) && path.resolve(file).startsWith(dataDir)) {
          server.ws.send({ type: "full-reload" });
        }
      };
      server.watcher.on("change", reload);
      server.watcher.on("add", reload);
      server.watcher.on("unlink", reload);
    },
  };
}

// Static site. `format: "file"` makes pages build to `/print/<name>.html`
// (instead of `/print/<name>/index.html`).
export default defineConfig({
  build: { format: "file" },
  server: { port: 4321 },
  vite: { plugins: [watchCvData()] },
});
