import { defineConfig, loadEnv } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { resolve } from 'path'
import fs from 'fs'
import type { Connect } from 'vite'

const REPO_ROOT = resolve(__dirname, '..')

// Middleware that serves /sections/** and /docs/** directly from the repo root.
// Only active in dev (browser mode). Tauri uses TauriPlatform and never hits this.
function repoStaticMiddleware(): Connect.NextHandleFunction {
  return (req, res, next) => {
    const url = req.url ?? ''
    const match = url.match(/^\/(sections|docs)(\/.*)?$/)
    if (!match) return next()
    const filePath = resolve(REPO_ROOT, match[1] + (match[2] ?? ''))
    if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) return next()
    const ext = filePath.split('.').pop()
    const mime = ext === 'md' ? 'text/plain; charset=utf-8' : 'application/octet-stream'
    res.setHeader('Content-Type', mime)
    res.end(fs.readFileSync(filePath))
  }
}

// Build a section manifest at dev-server startup so WebPlatform.listSections() works.
function buildSectionManifest(): { path: string; category: string }[] {
  const sectionsDir = resolve(REPO_ROOT, 'sections')
  const manifest: { path: string; category: string }[] = []
  if (!fs.existsSync(sectionsDir)) return manifest
  for (const cat of fs.readdirSync(sectionsDir)) {
    const catPath = resolve(sectionsDir, cat)
    if (!fs.statSync(catPath).isDirectory() || cat.startsWith('.')) continue
    for (const file of fs.readdirSync(catPath)) {
      if (file.endsWith('.md')) {
        manifest.push({ path: `sections/${cat}/${file}`, category: cat })
      }
    }
  }
  return manifest
}

// https://vitejs.dev/config/
export default defineConfig(async ({ mode }) => {
  // Load root .env so OPENROUTER_API_KEY is available at build time
  const env = loadEnv(mode, resolve(__dirname, '..'), '')
  const sectionManifest = buildSectionManifest()
  return {
    plugins: [
      svelte(),
      {
        name: 'repo-static',
        configureServer(server) {
          server.middlewares.use(repoStaticMiddleware())
        },
      },
    ],
    resolve: {
      alias: {
        $lib: resolve(__dirname, './src/lib'),
      },
    },
    define: {
      // Expose as import.meta.env.VITE_OPENROUTER_API_KEY
      'import.meta.env.VITE_OPENROUTER_API_KEY': JSON.stringify(env.OPENROUTER_API_KEY ?? ''),
      // Baked-in section manifest for WebPlatform.listSections()
      '__SECTION_MANIFEST__': JSON.stringify(sectionManifest),
    },
    // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
    //
    // 1. prevent vite from obscuring rust errors
    clearScreen: false,
    // Serve terminal/static/ as the public root (fonts, etc.)
    publicDir: resolve(__dirname, 'static'),
    // 2. tauri expects a fixed port, fail if that port is not available
    server: {
      port: 1420,
      strictPort: true,
      watch: {
        // 3. tell vite to ignore watching `src-tauri`
        ignored: ['**/src-tauri/**'],
      },
    },
  }
})
