# HUMAN_TODO — llm-release-gate

Only actions that an agent cannot safely complete belong here (accounts, agreements,
identity, spending, or a material product choice). Agents may check an item off only when
completion is directly verified; never infer a human decision. The current release stage is
in [ORCHESTRATOR.md](ORCHESTRATOR.md).

## q-1 — Published Action reference — DECIDED 2026-08-02

Owner decision: publish the Action from the renamed public repository as
`Chris0Jeky/llm-release-gate@v0`.

- [x] Repository renamed and canonical reference selected: `Chris0Jeky/llm-release-gate@v0`.
- [x] Annotated `v0.1.0` and initial `v0` tags both verified at `0e0f480`; the public
  [v0.1.0 GitHub release](https://github.com/Chris0Jeky/llm-release-gate/releases/tag/v0.1.0)
  is published.
- [x] Annotated `v0.1.1` remains immutable at `5514019`; the public
  [v0.1.1 GitHub release](https://github.com/Chris0Jeky/llm-release-gate/releases/tag/v0.1.1)
  is published.
- [x] Annotated `v0.1.2` and the current `v0` compatibility tag both verified at `5c36235`;
  the public [v0.1.2 GitHub release](https://github.com/Chris0Jeky/llm-release-gate/releases/tag/v0.1.2)
  is published.

The agent-owned initial release is complete. `v0` may move only with a later reviewed,
verified 0.x release; it is never an unattended automation target.

## q-2 — PyPI — DEFERRED BY OWNER 2026-08-02

Do not publish to PyPI, create a token, or add a publishing workflow until a real user asks
for `pip install`. At that point re-check name availability and use PyPI Trusted Publishing
(short-lived GitHub OIDC), not a long-lived API token. This is a dormant trigger, not an
active action item.

## q-3 — GitHub Marketplace — COMPLETED 2026-08-02

The owner completed the Marketplace workflow. The public
[llm-release-gate Marketplace listing](https://github.com/marketplace/actions/llm-release-gate)
is live at `v0.1.2` with **Continuous integration** and **Code quality** categories.

- [x] Owner-only Marketplace agreement/identity and category selection completed; public
  listing directly verified 2026-08-02.

## q-4 — Real provider adapter — WAIT FOR TWO REAL USER REQUESTS

Only the offline `fake` replay provider exists. Do not choose a provider, create secrets, or
add a provider matrix until `NEXT.md`'s two-user trigger is met. Then the owner chooses the
first requested provider and secret delivery path, and `.agent-harness/tier.json` receives a
fresh `sensitive_data` review. Keys remain environment-only and are never committed.

## Future owner gates

No other owner decision is active. Open a new numbered question only when live demand reaches
an existing `NEXT.md` trigger. In particular, a result store or hosted UI requires a privacy,
retention, and hosting decision before any user data is persisted.
