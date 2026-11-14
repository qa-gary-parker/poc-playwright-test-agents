# poc-playwright-test-agents

**The question:** can Playwright's official Test Agents (planner → generator → healer)
produce a test suite you'd actually keep — and does the healer fix real breakage
or just paper over it?

**The answer:** the generated suite is genuinely good — role-first locators, higher
assertion density than the human baseline, and it discovered a real UI gotcha the
baseline sidestepped. The cost is wall-clock time: ~46 minutes of unattended agent
time for 7 tests. The healer is fast and accurate but conservative — it restores
broken locators in the style it finds them, it does not improve them.

> Exploratory PoC, throwaway by default. Written up in
> [Hands-on with Playwright Test Agents](https://garyparker.dev/blog/hands-on-with-playwright-test-agents).
> Two-minute video: [youtu.be/eWpzpwyMTkk](https://youtu.be/eWpzpwyMTkk).

## Method

Target app: [the-internet.herokuapp.com](https://the-internet.herokuapp.com) (public demo app).
Playwright **1.62.0**, agents initialised with `npx playwright init-agents --loop=claude`,
run through headless Claude Code (`claude -p`), which executes the planner/generator/healer
agent definitions with the bundled `playwright-test` MCP server.

Three experiments:

1. **Baseline** — a 6-test suite covering login (success/failure), dynamic controls
   (checkbox, input), and dynamic loading (examples 1 and 2), written in one pass
   without live browser verification (`tests/baseline/`). This is the "experienced
   engineer writing from knowledge of the app" comparison point, authored by the
   orchestrating model, not a human — treat the authoring-time comparison accordingly.
2. **Plan → generate** — the planner explored the app and wrote
   [`specs/the-internet-test-plan.md`](specs/the-internet-test-plan.md); the generator
   turned it into `tests/form-authentication/`, `tests/dynamic-controls/`,
   `tests/dynamic-loading/`, live-verifying every locator as it wrote.
3. **Heal** — [`tests/healer/stale-login.spec.ts`](tests/healer/stale-login.spec.ts)
   simulates app drift: six deliberately stale locators (wrong ids, wrong button
   label, wrong flash selector, wrong heading). The healer repaired it against the
   live page.

## Results

| | Baseline (one-pass) | Agent-generated |
|---|---|---|
| Scenarios | 6 | 7 (planner added invalid-username case — and disclosed it) |
| Wall time to produce | minutes (one pass, no verification) | planner 2m 44s + generator **43m 22s** |
| Lines of test code | 80 | 223 |
| Assertion lines | 15 (~2.5/test) | 64 (~9/test) |
| Locators | 10 `getByRole`, 4 `getByLabel`, 6 CSS ids | 29 `getByRole`, 7 `getByText`, 3 CSS ids |
| Suite runtime | 10.1s (6 tests) | 8.8s (7 tests) |
| Pass rate | 6/6 | 7/7 |

Healer experiment: **1m 55s**, 6/6 stale locators repaired, 2/2 tests passing after.

## What impressed

- **Live verification catches what knowledge misses.** The generator found that
  `/dynamic_controls` keeps stale hidden `#loading` elements in the DOM and filtered
  for the visible one — a flake trap the baseline only avoided by accident of
  targeting different elements.
- **Guardrail judgment.** The plan said "attempt to fill the disabled input"; the
  generator recognised that Playwright's actionability checks would hang forever on
  that step and replaced it with `toBeDisabled()` + `toHaveValue('')` assertions.
  Same intent, no flake.
- **The healer doesn't guess.** It cross-referenced the known-good login test in the
  repo before patching the stale one, and repaired all six corruptions correctly.

## What to watch

- **The agentic tax is real**: 43 minutes to generate 7 tests, because every locator
  and assertion is verified in a live browser. Unattended time, but not free time —
  and it scales with suite size.
- **Assertion density cuts both ways.** ~9 assertions per test documents the UI
  thoroughly, but every intermediate assertion is a maintenance liability when the
  UI legitimately changes.
- **The healer repairs, it does not refactor.** Stale CSS ids came back as correct
  CSS ids, not semantic locators. It also matched a button's accessible name
  literally — `{ name: ' Login' }`, leading space included. Healed code preserves
  the quality level of the code that broke.

## Verdict

Use the planner/generator to scaffold coverage on apps you don't know — the live
verification produces better selectors than humans writing from memory. Budget the
wall time. Treat the healer as a PR assistant that proposes fixes for review, not as
a silent auto-repair step in CI: it will faithfully restore your worst locators
exactly as they were.

## Reproduce

```bash
npm ci && npx playwright install chromium
npx playwright test tests/baseline          # handwritten comparison suite
npx playwright test tests/form-authentication tests/dynamic-controls tests/dynamic-loading
npx playwright test tests/healer            # post-heal state
```

Agent runs require Claude Code: `npx playwright init-agents --loop=claude`, then ask
for the `playwright-test-planner` / `-generator` / `-healer` agents.

MIT. No affiliation with the Playwright team — independent evaluation.
