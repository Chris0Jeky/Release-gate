# llm-release-gate orchestration ledger

This is the concise, resumable control plane for a cold agent session. It does not override
repository policy; live evidence always wins.

## Current checkpoint

- **Authority:** T2 `daily-driver` in `.agent-harness/tier.json`; push and merge are free only
  after the repository gate is met.
- **Identity:** the public repository was renamed to
  [`Chris0Jeky/llm-release-gate`](https://github.com/Chris0Jeky/llm-release-gate) on 2026-08-02.
- **Release state:** `v0.1.0` remains immutable at `0e0f480`; annotated `v0.1.1` and the
  current `v0` compatibility tag both peel to `5514019`. Marketplace validation found the
  Action description exceeded its 125-character limit, so the `v0.1.2` metadata-only patch
  must release before q-3 resumes.
- **Decisions:** q-1 is complete; q-2 is deliberately deferred; q-3 is waiting for the
  owner's Marketplace agreement after the first release; q-4 waits for two real users.
- **Known low item:** issue #7's stale proving-check count was corrected and closed by PR #9;
  it never blocked the release.
- **Release proof:** local full tests and `make ci` passed at `5514019`; hosted CI/action
  self-test and Dependency Graph both succeeded at that exact SHA. The Node 20 deprecation and
  forced-runtime warnings had zero matches in the hosted CI log. Remote tags and releases were
  verified after publication.
- **Historical audit:** merged PR evidence remains in GitHub and Git history. This file keeps
  the next decision and exact resume path, not a duplicate transaction log.

## Source-of-truth precedence

1. Current Git SHA, local changes, hosted CI/checks, review threads, and GitHub PR/issue state.
2. Applicable global working agreement and `~/.claude/ESTATE.md` for checkout identity.
3. `AGENTS.md`, `CLAUDE.md`, and the strictest `.agent-harness/tier.json` authority.
4. `HUMAN_TODO.md` for owner-only decisions.
5. This checkpoint for queue selection and evidence recording.
6. `README.md`, `NEXT.md`, and `docs/` for product and verification context.

## Cold-start autonomous loop

1. Read the global estate registry and the five local files in `AGENTS.md`'s order, then refresh
   the live state above. Reconcile any handoff against the exact current head before trusting it.
2. Finish an in-flight PR, failed exact-head check, or confirmed correctness/security/data-loss
   defect first. Otherwise choose the smallest reversible task that advances the current stage
   ladder below and has a named proving check.
3. Keep one writer per checkout and one coherent slice per PR. Run the narrowest stated check,
   complete the declared review/CI gate, and re-prove the exact head after it changes.
4. If a stage reaches an owner-only gate, record the evidence and one clear q-N in
   `HUMAN_TODO.md`, mark the stage blocked, and continue with the next safe unblocked stage.
   Never work around an agreement, identity, secret, spending, or publication choice.
5. At a stage transition or blocker, update this checkpoint with changed / verified / NOT
   verified / residual risk / open human action / exact resume point. Stop only when no useful
   unblocked work remains; `NEXT.md` triggers are not permission to invent work.

## Release and maintenance ladder

| Stage | State | Agent-owned next action | Owner-only stop condition |
|---|---|---|---|
| Repository identity | COMPLETE | Keep all canonical references on `Chris0Jeky/llm-release-gate`. | None. |
| Release readiness | COMPLETE | PR #10 merged after exact-head local/hosted checks and independent review. | None. |
| Public Action releases | IN PROGRESS | `v0.1.0` remains immutable; `v0.1.1` and `v0` resolve to reviewed `5514019`; release the Marketplace-metadata patch as `v0.1.2`. | Exact-head CI, review, and tag/release proof. |
| Marketplace | BLOCKED | After `v0.1.2` is released, verify the public listing after the owner completes q-3. | Marketplace agreement, identity/2FA, primary **Continuous integration** category, and optional **Code quality** category. |
| PyPI | DORMANT | Do nothing until a real `pip install` request; then re-open q-2 and use Trusted Publishing. | Publishing identity/account configuration. |
| Real provider | DORMANT | Do nothing until two real users request live-model runs; then implement only the requested provider. | Provider, secret path, and `sensitive_data` review. |
| Product maintenance | TRIGGER-DRIVEN | Work a verified failure, confirmed defect, or observable `NEXT.md` trigger. | Any new privacy, retention, hosting, or spending decision. |

`v0` is a compatibility alias, not an unattended automation target: move it only as part of a
reviewed, verified 0.x release after its immutable version tag is cut. A breaking CLI/schema/
metric change is a major version event and must not move `v0`.

## Runtime boundary

The local tier currently declares the Claude runtime only. This documentation makes a cold agent
session discoverable; it does **not** install or claim a Codex deny-floor adapter. Adding another
runtime or a repo safety adapter is a separate harness-reviewed change and is intentionally out
of this release slice.

## Verification baseline

- In a linked worktree, use `PYTHONPATH=src py -3 -m pytest`; the editable install can otherwise
  resolve the primary checkout.
- `PYTHONPATH=src py -3 -m pytest` exercises the full suite. `make ci` runs tests plus the green
  and deliberately red demos. Under this Windows machine, invoke `make` through Git-for-Windows
  Bash with `PYTHONPATH=src`.
- `action.yml` is proven by the hosted `action-self-test` CI lane. Release tags require green CI
  at their exact commit and remote tag/release verification.

## External reconciliation

The global estate registry still has a stale entry for the old repository name and earlier
runtime/human-todo posture. It must be corrected in its owning `claude-config` repository, not
from this repository or this session. This repo's local tier declaration is the authority here.

## Resume

**Exact resume point:** ship the reviewed `v0.1.2` Marketplace-description patch, move `v0` only
with that verified patch release, and then return the owner to q-3 from `v0.1.2`. On a cold start,
first reconcile live PR/CI/review/tag/release state. Otherwise work only a verified failure,
confirmed defect, or an observable `NEXT.md` trigger; if none exists, stop with this checkpoint
rather than inventing PyPI, provider, scheduler, hook, or hosted-platform work.
