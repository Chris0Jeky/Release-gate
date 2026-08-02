# Release-gate orchestration ledger

This is a concise, resumable coordination log. It does not override repository policy or product
documentation.

## Run header

- **Base:** `main` at `69b5c73` (2026-08-02 post-merge); working branch: `chore/orchestration-ledger`
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
| T-002 | Close documented low-risk testing gaps (current slice: baseline-side provider-error notice) | MERGED | low | T-001 merged; focused triage | [PR #4](https://github.com/Chris0Jeky/Release-gate/pull/4), merge `566c002b` | post-merge reconciliation: no reviews/comments/threads present | PR #4 merged 2026-08-02 16:19:44Z; post-merge CI run `30756377935` succeeded at exact head `566c002b`; fresh-review LOW observation remains informational/nonblocking. |
| T-003 | Reconcile open PRs, CI, and review threads before selecting more work | VERIFIED | high | live GitHub state | none | not applicable (inventory) | Initial inventory completed before PR #3; its checks and review state are tracked under T-001. |
| T-004 | Add all-items-errored latency no-fabrication guard | MERGED | low | T-002 merged; existing provider-failure test | [PR #5](https://github.com/Chris0Jeky/Release-gate/pull/5), head `ebc8737`, merge `e0b22a5` | independent narrow review: no findings; post-merge no reviews/comments/threads | PR #5 merged 2026-08-02 16:28:55Z; latency metrics are unavailable with value `None` and note `provider reported no latency`. |
| T-005 | Exercise `on_unavailable: skip` through CLI and renderers | MERGED | low | T-004 merged | [PR #6](https://github.com/Chris0Jeky/Release-gate/pull/6), head `2ecb64b`, merge `69b5c73` | independent narrow review: no findings; post-merge no reviews/comments/threads | PR #6 merged 2026-08-02 16:39:50Z; the candidate unavailable cost rule is skipped and renders through JSON, Markdown, and HTML. |

## Human-owned questions

- **q-1:** Choose the published Action reference (`your-org/llm-release-gate@v0` versus
  `Chris0Jeky/Release-gate@v0` / rename decision). Open in `HUMAN_TODO.md`.
- **q-2:** Decide whether to publish `llm-release-gate` to PyPI; if yes, the human creates the token.
- **q-3:** Decide whether to list the Action on GitHub Marketplace (depends on q-1).
- **q-4:** If two users request a real provider, choose the provider/secrets and re-review the
  `sensitive_data` tier flag; keys remain environment-only.

## Verification baseline

Current baseline: `PYTHONPATH=src py -3 -m pytest` (84 tests), `make demo-green`, `make demo-red`,
and `make ci` (test plus both demos). PR #3 evidence: `PYTHONPATH=src py -3 -m pytest` → **82
passed**; under Git-for-Windows Bash, `PYTHONPATH=src make ci` passed and preserved the red-demo
hash. In a linked worktree use `PYTHONPATH=src` before Python commands because editable installs
resolve the main checkout. `action.yml`'s self-test lane is CI-only. Run the narrowest seam check
for each change, then the declared gate when risk warrants it; record failures and workarounds
here. PR #4 evidence: provider suite 9 passed, full suite 83 passed, and Git-Bash `make ci` passed.
Hosted CI evidence: PR run `30291002316` succeeded; post-merge run `30755966014` succeeded at
exact head `2a1e6a7`; PR #4 post-merge run `30756377935` succeeded at exact head `566c002b`; PR #5
pre-merge run `30756695591` had all three jobs succeed at `ebc8737`; post-merge run `30756726049`
succeeded at exact head `e0b22a5`; PR #6 pre-merge run `30757007282` had all three jobs succeed at
`2ecb64b`; post-merge run `30757135915` succeeded at exact head `69b5c73`. The full-suite baseline is
now 84 tests. This operational-ledger update is verified with `git diff --check`.

## Findings and failures

- **F-001 (MEDIUM max, fixed in `37950c6`):** JSON inputs and fake fixtures allowed equivalent
  CRLF/lone-CR bytes to reach hashing differently, causing result-hash drift while parsed values and
  the verdict remained unchanged. The fix normalizes CRLF and lone CR to LF only in JSON-specific
  loaded-input and fake-fixture hashing; generic raw `file_sha256` and CLI behavior remain unchanged.
  Fresh-context code review found no CRITICAL, HIGH, or MEDIUM findings. LOW notes (lone-CR E2E and
  CLI raw-hash assertion) are informational/nonblocking; no fix cascade.
- **F-002 (PR #4 review):** Fresh-context review found no blocking defects. The LOW observation
  that tests do not separately assert baseline run/item accounting is informational/nonblocking; no
  fix cascade.
- **F-003 (PR #5 review):** Independent narrow review found no findings; immediate post-merge
  reconciliation found no PR #5 reviews, comments, or threads.
- **F-004 (PR #6 review):** Independent narrow review found no findings; immediate post-merge
  reconciliation found no PR #6 reviews, comments, or threads. The candidate unavailable cost rule
  is skipped and rendered through JSON, Markdown, and HTML as intended.
- **Environment workaround:** a WSL-vs-Git-for-Windows Bash command-path mismatch required running
  `PYTHONPATH=src make ci` under Git Bash; this is environment evidence, not a product failure.
- **Failures:** none in the recorded PR checks; tie any future red check to its exact head and
  record the cause before retrying.

## Checkpoint and resume

- **Prior checkpoint:** PR #3 merged 2026-08-02 16:08:48Z as `2a1e6a7`; issue #1 is
  closed/completed; local `main` and `origin/main` are equal at that head. Immediate post-merge
  reconciliation found no PR #3 reviews, comments, or threads; post-merge CI `30755966014` passed.
- **Current checkpoint:** PR #4 merged 2026-08-02 16:19:44Z as `566c002b`; immediate post-merge
  reconciliation found no PR #4 reviews, comments, or threads; post-merge CI `30756377935` passed
  at that exact head.
- **Prior checkpoint:** PR #5 merged 2026-08-02 16:28:55Z as `e0b22a5`; pre-merge CI
  `30756695591` had all three jobs succeed at `ebc8737`; post-merge CI `30756726049` succeeded at
  that exact head. Independent narrow review found no findings, and immediate post-merge
  reconciliation found no PR #5 reviews, comments, or threads. Local `main` and `origin/main` match
  `e0b22a5`.
- **Current checkpoint:** PR #6 merged 2026-08-02 16:39:50Z as `69b5c73`; pre-merge CI
  `30757007282` had all three jobs succeed at `2ecb64b`; post-merge CI `30757135915` succeeded at
  that exact head. Independent narrow review found no findings, and immediate post-merge
  reconciliation found no PR #6 reviews, comments, or threads. Local `main` and `origin/main` match
  `69b5c73`; the full-suite baseline is 84 tests.
- **Exact resume point:** No unblocked product work remains after T-005 merged. HUMAN_TODO q-1
  through q-4 remain open (published Action reference, PyPI, Marketplace, and real-provider/secrets
  decisions); resume only when a human resolves one or new scoped work is authorized. Do not invent
  additional product tasks.
