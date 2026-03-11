import { defineConfig, loadEnv } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig(async ({ mode }) => {
  // Load root .env so OPENROUTER_API_KEY is available at build time
  const env = loadEnv(mode, resolve(__dirname, '..'), '')
  return {
    plugins: [svelte()],
    resolve: {
      alias: {
        $lib: resolve(__dirname, './src/lib'),
      },
    },
    define: {
      // Expose as import.meta.env.VITE_OPENROUTER_API_KEY
      'import.meta.env.VITE_OPENROUTER_API_KEY': JSON.stringify(env.OPENROUTER_API_KEY ?? ''),
    },
    // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
    //
    // 1. prevent vite from obscuring rust errors
    clearScreen: false,
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
