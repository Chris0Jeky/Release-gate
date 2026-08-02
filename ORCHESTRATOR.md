# Release-gate orchestration ledger

This is a concise, resumable coordination log. It does not override repository policy or product
documentation.

## Run header

- **Base:** `main` at `2a1e6a7` (2026-08-02 post-merge); working branch: `chore/orchestration-ledger`
- **Authority:** T2 `daily-driver` from `.agent-harness/tier.json`; push and merge are free, with
  the repository gate still required.
- **Goal:** triage live work, advance small safe slices, and leave evidence-backed checkpoints.
- **Cycle:** 1
- **Last updated:** 2026-08-02

## Source-of-truth precedence

1. Live Git state, CI/check results, and unresolved review threads at the current head.
2. `CLAUDE.md` and `AGENTS.md`, plus the strictest declared `.agent-harness/tier.json` authority.
3. `HUMAN_TODO.md` for decisions only a human can make.
4. This ledger for coordination, task status, findings, and resume state.
5. `README.md`, `NEXT.md`, and `docs/` for product and verification context.
6. `C:\Users\jekyt\Desktop\orc.txt` supplies only a generic loop shape; repository rules win.

## Lifecycle

`TRIAGE/BACKLOG -> SELECTED -> IN-PROGRESS -> IN-REVIEW -> VERIFIED -> MERGED`

Use `CHANGES-REQUESTED` when the one review finds a confirmed correctness, security, or data-loss
defect. Use `BLOCKED` or `DROPPED` with a reason. The bounded repository rule is one real review
per PR; do not copy the generic two-review rule from `orc.txt`.

## Task board

| ID | Title | Status | Priority | Dependencies | PR / branch | Review | Outcome |
|---|---|---|---|---|---|---|---|
| T-001 | Issue #1: normalize JSON input line endings before semantic hashing | MERGED | high | triage complete | [PR #3](https://github.com/Chris0Jeky/Release-gate/pull/3), merge `2a1e6a7` | post-merge reconciliation: no reviews/comments/threads present | PR #3 merged 2026-08-02 16:08:48Z; issue #1 closed/completed; local `main` and `origin/main` equal `2a1e6a7`. |
| T-002 | Close documented low-risk testing gaps: CLI/renderers `on_unavailable: skip`, all-items-errored latency fabrication guard, and baseline-side provider errors | SELECTED | low | T-001 merged; focused triage | isolated branch (next) | one bounded review per slice | Next safe queue item; triage the three documented gaps, then choose one small slice rather than batching them. |
| T-003 | Reconcile open PRs, CI, and review threads before selecting more work | VERIFIED | high | live GitHub state | none | not applicable (inventory) | Initial inventory completed before PR #3; its checks and review state are tracked under T-001. |

## Human-owned questions

- **q-1:** Choose the published Action reference (`your-org/llm-release-gate@v0` versus
  `Chris0Jeky/Release-gate@v0` / rename decision). Open in `HUMAN_TODO.md`.
- **q-2:** Decide whether to publish `llm-release-gate` to PyPI; if yes, the human creates the token.
- **q-3:** Decide whether to list the Action on GitHub Marketplace (depends on q-1).
- **q-4:** If two users request a real provider, choose the provider/secrets and re-review the
  `sensitive_data` tier flag; keys remain environment-only.

## Verification baseline

Current baseline: `PYTHONPATH=src py -3 -m pytest` (82 tests), `make demo-green`, `make demo-red`,
and `make ci` (test plus both demos). PR #3 evidence: `PYTHONPATH=src py -3 -m pytest` → **82
passed**; under Git-for-Windows Bash, `PYTHONPATH=src make ci` passed and preserved the red-demo
hash. In a linked worktree use `PYTHONPATH=src` before Python commands because editable installs
resolve the main checkout. `action.yml`'s self-test lane is CI-only. Run the narrowest seam check
for each change, then the declared gate when risk warrants it; record failures and workarounds
here. Hosted CI evidence: PR run `30291002316` succeeded; post-merge run `30755966014` succeeded
at exact head `2a1e6a7`. This documentation-only ledger update is verified with `git diff --check`.

## Findings and failures

- **F-001 (MEDIUM max, fixed in `37950c6`):** JSON inputs and fake fixtures allowed equivalent
  CRLF/lone-CR bytes to reach hashing differently, causing result-hash drift while parsed values and
  the verdict remained unchanged. The fix normalizes CRLF and lone CR to LF only in JSON-specific
  loaded-input and fake-fixture hashing; generic raw `file_sha256` and CLI behavior remain unchanged.
  Fresh-context code review found no CRITICAL, HIGH, or MEDIUM findings. LOW notes (lone-CR E2E and
  CLI raw-hash assertion) are informational/nonblocking; no fix cascade.
- **Environment workaround:** a WSL-vs-Git-for-Windows Bash command-path mismatch required running
  `PYTHONPATH=src make ci` under Git Bash; this is environment evidence, not a product failure.
- **Failures:** none in the recorded PR checks; tie any future red check to its exact head and
  record the cause before retrying.

## Checkpoint and resume

- **Current checkpoint:** PR #3 merged 2026-08-02 16:08:48Z as `2a1e6a7`; issue #1 is
  closed/completed; local `main` and `origin/main` are equal at that head. Immediate post-merge
  reconciliation found no PR #3 reviews, comments, or threads; post-merge CI `30755966014` passed.
- **Exact resume point:** focus triage of T-002's three documented coverage gaps from `2a1e6a7`,
  create/use an isolated branch, and select one small slice (do not batch the gaps). Run its focused
  checks and one bounded review, then update this ledger with the exact head and evidence.
