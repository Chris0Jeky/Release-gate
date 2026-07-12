# AGENTS.md — working agreements for coding agents

Applies to any AI coding agent working in this repo (and humans who like checklists).

## Commands (run these, don't guess)

```bash
make install     # pip install -e ".[dev]"
make test        # pytest — must pass before any commit
make demo-green  # both green examples must exit 0
make demo-red    # red example must exit exactly 1
make ci          # all of the above; what GitHub Actions runs
```

On Windows without make: `python -m pytest`, `python -m llm_release_gate ...` (the
Makefile targets show the exact arguments).

## Layout

- `src/llm_release_gate/` — the package; seams are `providers/`, `adapters/`, `scorers/`
  (see `docs/architecture.md` for the module map, `docs/extending.md` for how to extend).
- `examples/` — three offline scenarios; `assistant-cheap-regression` is *deliberately*
  red. Do not "fix" it: CI asserts it fails the gate.
- `tests/` — behavior-focused; see `docs/testing.md` for the map.

## Invariants (violating these is a bug, not a style choice)

1. **Never fabricate numbers.** Unknown tokens/latency stay `None`; unknown cost is
   *unavailable + reason*. No defaults, no estimates, no partial sums presented as totals.
2. **Fail closed.** Unevaluable rules fail by default; misconfiguration is exit 2, never
   a silent pass; provider errors surface in `errors.error_rate` (implicit rule).
3. **Reproducibility.** `report.json` stays timestamp- and path-free; anything volatile
   goes in `manifest.json`. If you add report fields, they must be deterministic.
4. **Honest presentation.** Rates always ship with sample counts; heuristic scores are
   labeled heuristic (`kind: "heuristic_rate"`), never called probabilities/accuracy.
5. **Exit codes are API:** 0 pass · 1 regression · 2 could-not-run. So are the Makefile
   target names, CLI flags, input schemas, and metric keys — breaking them is a major
   version event.
6. **One owner per metric**; scorers declare direction/kind/mode and skip inapplicable
   items rather than passing them.
7. **Zero runtime dependencies.** New runtime deps need a NEXT.md-level justification.

## Workflow

- Small diffs, one logical change per commit, imperative subject lines.
- New behavior lands with the test that pins it (see `docs/testing.md` → Adding tests).
- Update docs in the same commit when you change schemas, metrics, commands or exit
  behavior. README example outputs must match what the code actually prints.
- Repo tier and agent-harness rules: `CLAUDE.md` (T1 sandbox — push to main is fine,
  keep the deny-floor untouched).
