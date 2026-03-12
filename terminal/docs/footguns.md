# Footguns — Known Pitfalls

Hard-won lessons from building Covenant Terminal. Read this when something is mysteriously broken.

---

## Svelte 5

**Mount API:** Use `mount(App, { target })` from `svelte`, not `new App({ target })`. The `new` syntax is Svelte 4 and throws `component_api_invalid_new` at runtime with no build-time warning.

**Reactivity:** Use `$state()`, `$derived()`, and `$effect()` — not stores, not legacy reactive declarations. Event callbacks are props (`onsubmit`, `onselect`), not `createEventDispatcher()`.

**State seeded from props:** If a component initialises `$state()` from a prop value, wrap it in `untrack()` to avoid `state_referenced_locally` warnings:
```ts
import { untrack } from 'svelte'
let value = $state(untrack(() => props.initialValue))
```

---

## Tauri

**Environment detection:** Use `isTauri()` from `@tauri-apps/api/core` — do not check `window.__TAURI_INTERNALS__` manually. The correct global is `globalThis.isTauri`, and the SDK function is the stable API.

**Filesystem permissions:** `fs:read-all` is a shorthand that only covers reads within the app's sandboxed directories — it does **not** grant access to arbitrary absolute paths (e.g. the repo root). To read files outside the sandbox you must use `fs:allow-read-text-file` + `fs:allow-read-dir` with an explicit `fs:scope` entry:

```json
"fs:allow-read-text-file",
"fs:allow-read-dir",
{
  "identifier": "fs:scope",
  "allow": [
    "/absolute/path/to/repo/**",
    "$APPCONFIG/**"
  ]
}
```

Config writes (`saveConfig`) additionally require `fs:allow-appconfig-write-recursive`. Any capability change triggers a Rust recompile (~10–30s). Missing-permission errors surface as `forbidden path` or `not allowed on the scope for allow-read-text-file`.

**Non-fatal startup operations:** Wrap any `onMount` operation that is not required for section loading in its own `try/catch`. An unhandled error before `loading = false` leaves the app stuck on the loading spinner with no visible error.

**Static assets (fonts) in dev mode:** Vite only serves `public/` as static assets by default. The project uses `static/` instead — set `publicDir: resolve(__dirname, 'static')` in `vite.config.ts`. Without this, font requests in the browser return `text/html` (the index fallback) and the browser sanitizer rejects them with "rejected by sanitizer".

**Webview debugging:** The Tauri webview gives no console output to the terminal. To see JavaScript errors, open `http://localhost:1420` in a regular browser while `tauri dev` is running and check the Console tab. The browser runs `WebPlatform` (no `isTauri()`), so file reads will fail — but JS errors, import failures, and component crashes are visible.

---

## vitest-browser-svelte

**Global query scope:** `screen.getByText()` queries the whole page, not just the render container. If multiple renders share a common label (e.g. "Claude"), add `cleanup()` in `afterEach` to prevent strict-mode violations, or scope queries to `container.querySelector()`.

**Assertion API:** Use `await expect.element(...).toBeVisible()` (Playwright assertions), not `expect(...).toBeInTheDocument()` (Testing Library). The APIs are not interchangeable.

---

## App integration tests

Unit and component tests pass even when the app renders blank, because they test components in isolation with mock data. `src/components/__tests__/App.test.ts` must exist and must include:

- A test that waits for a section heading to appear (guards against blank/loading-forever)
- A test that all-files-fail produces an error message (guards against silent failures)
