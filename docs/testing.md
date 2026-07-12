# Testing

## Commands

```bash
make install      # pip install -e ".[dev]"
make test         # pytest (75 tests)
make demo-green   # both green examples; target fails unless both exit 0
make demo-red     # red example; target fails unless the gate exits exactly 1
make ci           # test + demo-green + demo-red (what CI runs)
```

Windows note: run under Git Bash (GNU make + sh), or call the underlying
`python -m pytest` / `python -m llm_release_gate ...` commands directly.

## What the suite covers (and deliberately not)

Tests target the behaviors CI depends on — verdict logic, reproducibility, hashing, cost
math, provider failure, report honesty, exit codes — not line-coverage maximization.

| File | Guards |
|---|---|
| `test_verdicts.py` | every constraint type incl. boundaries and zero-baseline percentages; warn vs fail; `on_unavailable` fail/warn/skip; candidate-only constraints ignoring baseline availability; the implicit `errors.error_rate` rule (added, replaced, fails); unknown metric → config error; direction-mismatched constraints rejected; nearest-rank percentile math pinned |
| `test_hashing.py` | canonical-JSON invariance (key order), sensitivity (values, list order), unicode, NaN rejection, digest format, file hashing |
| `test_cost.py` | exact token×price math; missing tokens / missing model / no table → unavailable with reason; partial token data poisons totals instead of understating them; gating on unavailable cost fails closed |
| `test_provider_failure.py` | missing fixture and simulated `error` entries raise `ProviderError`; the run continues; failures land on items and in `errors.error_rate`; a candidate that only looks good on surviving items is blocked; all-items-failed yields unavailable score metrics, not zeros; malformed fixture entries (negative/string tokens, non-dict) are clean config errors |
| `test_reproducibility.py` | identical inputs → byte-identical report/md/html and equal `result_hash`; report is timestamp- and path-free; manifest pins hashes + verdict; changed input changes the hash |
| `test_scorers.py` | adapter parsing (citations, abstention regex, JSON fence stripping); all four abstention quadrants; hedged-fabrication answers (hedge + citation) counted as answers with citations validated; citation validity incl. fabricated citations on should-abstain items; keyword/field-match pass/fail/applicability; JSON-schema subset violations; unenforceable schemas rejected at construction; JSON-strict bool≠int semantics |
| `test_reports.py` | rates rendered with sample counts; heuristic footnote present; unavailable cost labeled with its reason (and no fabricated `$0`); HTML escapes model output; failing items carry actionable detail |
| `test_cli.py` | exit 0 (both green examples), exit 1 (red example, naming the regressions), exit 2 (missing file, bad rule, metric without scorer, missing/typo'd prompt template, malformed dataset, internal error); breached warn-level rule annotates but exits 0; `GITHUB_STEP_SUMMARY` / `GITHUB_OUTPUT` writing; `hash` and `run` subcommands |

The shared fixture (`conftest.mini_gate`) builds a tiny 3-item grounded gate on disk;
tests break exactly one thing per case.

**Not covered (known, intentional):** real provider calls (no real adapter exists yet —
see NEXT.md); the Action's PR-comment step (needs a live PR; the rest of action.yml is
self-tested in CI on both examples and the step logic was exercised locally, below).

**Known coverage gaps, pickup-ready** (from the 2026-07-12 adversarial review; all
low-risk, current behavior verified correct by trace):

- `on_unavailable: "skip"` end-to-end through CLI + renderers (unit-tested only; a
  renderer regression on the `skipped` verdict icon would surface as exit 2, not a
  wrong verdict).
- Latency partial-availability note (`runner.py` — some-but-not-all items report
  latency) and fabrication-guard assertions on the all-items-errored latency branch.
- Baseline-side provider errors end-to-end (the "baseline run had N/M provider errors"
  notice; `mini_gate` already accepts `baseline_responses` for this).

## Verified runs (2026-07-12, Windows 10, Python 3.14.3; CI mirrors on ubuntu 3.11/3.13)

`python -m pytest` →

```
75 passed in 0.46s
```

`make demo-green` → both gates PASS, exit 0. RAG example (prompt improvement):
quality 7/8 → 8/8, cost +11.8% (≤ 25% cap), all citations valid. Extraction example
(safe cheap swap): 6/6 fields, 6/6 schema-valid, cost −95.5%.

`make demo-red` → gate FAIL, exit 1, blocked on exactly the injected regressions:

```
llm-release-gate: gate FAIL
  rules: 7 evaluated, 3 failed, 0 warned
  [FAIL] quality.pass_rate: drop 0.375 vs allowed 0.1
  [FAIL] abstention.false_answer_rate: candidate 1 vs allowed maximum 0
  [FAIL] citations.valid_rate: drop 0.3 vs allowed 0.05
  result hash: sha256:76c8494b3553423bececfad4a653e1497f63fdcf0cc5804d535e2c3216dddd8e
OK: regression correctly blocked (exit 1)
```

(cost.total_usd fell 96.4% — and the gate still failed; that asymmetry is the product.)

Reproducibility spot-check: two consecutive red-example runs produced byte-identical
`report.json` and the same `result_hash` shown above.

Action logic local simulation (bash, `GITHUB_OUTPUT`/`GITHUB_STEP_SUMMARY` pointed at
temp files, same commands as action.yml): outputs file received `verdict=fail`,
`exit-code=1`, `result-hash=…`, report paths, `cli-exit=1`; summary file received the
Markdown report; the enforce step maps `cli-exit=1` to a failed check.

## Adding tests

Break one behavior per test. Prefer driving through `cli.main([...])` (in-process, fast,
exercises loading + wiring) with `mini_gate` overrides; drop to unit level for pure logic
(verdicts, hashing, schema validation). If you add a metric or scorer, test its
*ownership* (no metric collisions), its applicability rules, and how it renders when
unavailable.
