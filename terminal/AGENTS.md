# terminal/AGENTS.md — Agent Operating Manual

You are building **Covenant Terminal**: a Tauri 2.x + Svelte 5 + Vite + TypeScript desktop application. It is part of the Covenant repo — not a separate product. Agents working here have native access to section files, the glossary, build tooling, and the existing review pipeline.

---

## Before You Do Anything

Read in this order:

1. **`terminal/docs/plan.md`** — architecture, use cases, technology decisions, milestones
2. **`terminal/docs/tasks.md`** — TDD task lists per milestone (RED/GREEN/REFACTOR steps)
3. **`docs/design.md`** (repo root) — visual language, typography, palette, § motif

Do not write a line of code until you have read `plan.md`. It contains architectural decisions (platform abstraction, provider interface, council model) that are invariants — violating them creates debt that compounds.

---

## Invariants (Never Violate)

1. **Never import `@tauri-apps/*` directly in components or `src/lib/` modules.** The only exception is `platform-tauri.ts`. Everything else uses the `Platform` interface from `platform.ts`.
2. **`src/lib/` is pure TypeScript.** No Svelte components in `lib/`. No platform-specific code except `platform-tauri.ts` and `platform-web.ts`.
3. **`src/components/` imports only from `src/lib/`.** Never from `@tauri-apps/*` directly.
4. **Never edit `/dist/`.** It is generated. Use `make` from the repo root to rebuild it.
5. **All tests must pass before presenting a milestone for review.** Run `npm test` from `terminal/` and fix every failure before stopping.
6. **One milestone at a time.** Complete a milestone fully — all tasks done, all tests passing — then stop and present it for review. Do not begin the next milestone until the steward approves.
7. **Keep `tasks.md` current.** After completing each task, check off its boxes. After completing a milestone, mark it complete in the file header. Update the status in `plan.md` if the implementation diverges from the plan.

---

## Red/Green TDD Workflow

Every substantive feature follows this cycle — no exceptions:

### 1. RED — Write the test first

Before writing any implementation code:
- Open (or create) the test file in the appropriate `__tests__/` directory
- Write the test(s) described in `tasks.md` for the current task
- Run `npm test` and confirm the test **fails** (red)
- Do not proceed until you have a failing test

If the test in `tasks.md` uses an API that does not yet exist, write the test as specified and let TypeScript errors / test failures be your red state.

### 2. GREEN — Write the minimum implementation

- Write only enough code to make the failing test pass
- Do not over-engineer; do not add features not yet tested
- Run `npm test` and confirm the test **passes** (green)
- All previously passing tests must still pass

### 3. REFACTOR — Clean up without breaking

- Extract shared logic if the same pattern appears more than twice
- Rename for clarity
- Run `npm test` after every refactor step to confirm nothing broke

---

## Test Stack and Conventions

| Layer | Tool | Notes |
|---|---|---|
| Unit tests (TypeScript logic) | Vitest | Pure functions: parser, types, config, dispatch, synthesis |
| Component tests (Svelte) | `vitest-browser-svelte` | Renders in real browser via Playwright |
| Platform mocking | `vi.mock('./platform.ts')` | All platform calls mocked — no Tauri dependency in tests |
| E2E tests (M5+) | WebdriverIO + `tauri-driver` | Full app tests against a debug build |

### File layout

```
terminal/src/
├── lib/covenant/__tests__/parser.test.ts       — unit test next to module
├── lib/agents/__tests__/provider.test.ts
├── components/__tests__/SectionNav.test.ts     — component test
└── e2e/                                        — E2E tests (Milestone 5+)
```

Test files live in `__tests__/` directories adjacent to the code they test. Named `<module>.test.ts`.

### Running tests

```bash
# from terminal/
npm test              # run all tests (watch mode)
npm test -- --run     # run once and exit (for CI / pre-commit checks)
```

Always run `npm test -- --run` before presenting a milestone for review.

See `terminal/docs/footguns.md` for vitest-browser-svelte pitfalls and Svelte 5 testing gotchas.

---

## Common Tasks

### Start work on a milestone

1. Re-read the milestone's section in `terminal/docs/tasks.md`
2. Check which tasks have boxes checked vs. unchecked — start from the first unchecked task
3. Read the RED test for that task; write it; confirm it fails
4. Implement GREEN; run tests; confirm it passes
5. Repeat until all tasks in the milestone are complete
6. Run the integration verification checklist at the end of the milestone
7. Stop and present for review (see below)

### Present a milestone for review

When all tasks are complete and all tests pass:

1. Run `npm test -- --run` one final time and confirm 0 failures
2. Update `terminal/docs/tasks.md`: check off all completed boxes in the milestone
3. Stage and commit everything **except `opencode.json`**:
   ```bash
   git add terminal/
   git commit -m "feat(terminal): <milestone summary>"
   ```
4. Write a brief summary to the steward:
   - What was built
   - Test count and pass rate
   - Any deviations from `plan.md` or `tasks.md` (and why)
   - Any open questions or decisions needed before the next milestone

Do **not** begin the next milestone until the steward responds.

### Update plan.md or tasks.md

Update these documents when:
- The implementation reveals that a planned approach won't work
- A new architectural constraint emerges that wasn't in the original plan
- A task is completed and its checkboxes need marking
- A milestone is complete and its status should be updated

Always add a note in the Log section at the bottom of `tasks.md` when a significant deviation from the original plan is made.

### Add a new module

1. Create the file in the correct location (see directory structure in `plan.md`)
2. Create its `__tests__/` file in the same directory
3. Write the RED test first before any implementation
4. Add the module to the relevant milestone section in `tasks.md` if it is new

---

## Directory structure

See `README.md` for the annotated directory tree. The structural rule that matters here: if a new file's natural home is ambiguous, default to `lib/` for logic and `components/` for anything that renders Svelte markup.

---

## Commands reference

See `README.md` for setup, prerequisites, and all run/test/build commands.

The one command to remember: always run `npm test -- --run` from `terminal/` before presenting a milestone for review.

For Covenant structural validation (sections, glossary, frontmatter):
```bash
# from repo root (not terminal/)
make validate
```

### Running the app (non-blocking)

`npm run tauri -- dev` blocks the terminal. Always run it in the background with a log file:

```bash
# from terminal/
npm run tauri -- dev --no-watch > /tmp/tauri-dev.log 2>&1 &
echo "PID: $!"

# Tail the log to check for build errors or Rust panics
tail -f /tmp/tauri-dev.log

# Kill it when done
pkill -f "covenant-terminal"; pkill -f "vite"
```

The `--no-watch` flag disables Vite's file watcher inside Tauri, which is fine for a manual test run. Omit it if you want hot-reload during development.

---

## Known pitfalls

See `terminal/docs/footguns.md`.

---

## Architecture Decisions (enforced, not up for debate)

These are load-bearing. Read `plan.md` for full rationale.

**Platform abstraction:** `platform.ts` is the only crossing point between application logic and OS/environment. Every component and lib module gets its platform instance injected or imported from `platform.ts`. This is what makes the SvelteKit web migration (Milestone 6) a 1-hour task rather than a rewrite.

**Provider abstraction:** `src/lib/agents/provider.ts` defines `AgentProvider`. All AI adapters implement this interface. The council dispatches the same `ChatParams` to N providers; no council code knows which provider it is talking to.

**SSE parsing:** The OpenRouter adapter contains a reusable `parseSSE()` utility. Other providers (Copilot, direct APIs) reuse it. Do not duplicate SSE parsing logic.

**Svelte 5 reactivity:** Use `$state()`, `$derived()`, and `$effect()` — not stores, not legacy reactive declarations. Event callbacks are props (`onsubmit`, `onselect`), not `createEventDispatcher()`.

---

## Milestone status

See `README.md` for the current milestone status table.

---

*Architecture and design: `terminal/docs/plan.md`*
*TDD task lists: `terminal/docs/tasks.md`*
*Visual language: `docs/design.md` (repo root)*
*Repo-wide agent instructions: `AGENTS.md` (repo root)*
