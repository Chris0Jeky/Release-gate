# CLAUDE.md — Release-gate

Tier: sandbox (T1) — authority: push free / merge free · single-runtime (Claude).
Harness bootstrapped 2026-07-12 per `agent-harness/BLUEPRINT.md` §1 (T1 Sandbox).

## What this is

Release-gate — an open-source CLI + GitHub Action that blocks unsafe changes to a
repo's prompts, model, retrieval, tools, or config from being merged. Given a versioned
golden/replay dataset, a baseline config, a candidate config, and quality/cost/latency
thresholds, it runs both configs, compares them, writes a report, comments on the PR,
and fails the check on a material regression. Full concept: `README.md`.

## How to run

Python ≥3.11, stdlib-only runtime (pytest for dev). Implemented 2026-07-12; the package
is `llm-release-gate` (CLI: `python -m llm_release_gate`).

- `make install` · `make test` · `make demo-green` (exit 0) · `make demo-red` (must exit 1)
- `make ci` = what `.github/workflows/ci.yml` runs (plus an action.yml self-test lane).
- Windows: run make targets under Git Bash, or use the underlying `python -m` commands.
- `examples/assistant-cheap-regression` is deliberately red — never "fix" it.
- Agent working agreements + invariants: `AGENTS.md`. Docs: `docs/`, growth: `NEXT.md`.

## Rules (T1 — keep it minimal)

- **The floor is the one guardrail.** The global PreToolUse deny hook
  (`~/.claude/hooks/dispatch.py`, floor v1.3.0) rides along and blocks only the
  irreversible: force-push, `rm -rf` outside the repo, pipe-to-shell, `sudo`, secret-file
  writes. It fires even under `bypassPermissions`. Do NOT add a repo hook copy — it would
  double-spawn against the global one.
- **Permissions are `bypassPermissions`** (gitignored `.claude/settings.local.json`) — max
  trust by design at T1. Committed `.claude/settings.json` keeps `acceptEdits` + the deny
  floor as the safe baseline for fresh clones.
- No secrets in the repo. This tool calls model APIs; keys come from the environment,
  never committed — that keeps the repo plain (no `sensitive_data` flag).
- Small diffs, commit per logical group; plain `git push` to `main` is fine (solo).
- Work inline. No subagent fan-out at T1 — it is always cheaper to stay inline here.

## Growth

Promote to T2 on durable use — a 3rd+ return session, another consumer, or the first
"wish I had a test" moment (likely soon: this ships a CLI + Action others run). Then add
SessionStart orientation, HUMAN_TODO, a BACKLOG, and a CI lane per the blueprint. Until
then add nothing speculative (second-occurrence rule). Tier/authority: `.claude/tier.json`;
estate row: `~/.claude/ESTATE.md`.
