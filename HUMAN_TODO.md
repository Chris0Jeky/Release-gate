# HUMAN_TODO — llm-release-gate

Only actions that an agent cannot safely complete belong here (accounts, agreements,
identity, spending, or a material product choice). Agents may check an item off only when
completion is directly verified; never infer a human decision. The current release stage is
in [ORCHESTRATOR.md](ORCHESTRATOR.md).

## q-1 — Published Action reference — DECIDED 2026-08-02

Owner decision: publish the Action from the renamed public repository as
`Chris0Jeky/llm-release-gate@v0`.

- [x] Repository renamed and canonical reference selected: `Chris0Jeky/llm-release-gate@v0`.

The remaining agent-owned release work is to cut and verify the exact `v0.1.0` and initial
`v0` tags from reviewed `main`; it is tracked in the orchestration ledger, not as a human
question.

## q-2 — PyPI — DEFERRED BY OWNER 2026-08-02

Do not publish to PyPI, create a token, or add a publishing workflow until a real user asks
for `pip install`. At that point re-check name availability and use PyPI Trusted Publishing
(short-lived GitHub OIDC), not a long-lived API token. This is a dormant trigger, not an
active action item.

## q-3 — GitHub Marketplace — HUMAN ACTION AFTER INITIAL RELEASE

Owner decision: list the Action after the initial `v0.1.0` GitHub release exists. An agent
can prepare and verify the release but cannot accept GitHub's Marketplace agreement or make
owner identity/2FA attestations.

When the release is published, the owner should:

1. Open the `v0.1.0` release in this repository and choose **Publish this Action to the
   GitHub Marketplace**.
2. Accept the Marketplace Developer Agreement, complete any 2FA/identity prompt, and choose
   the appropriate category.
3. Confirm the public listing is live; an agent may then verify the listing and record it.

- [ ] Owner-only Marketplace agreement/identity and category selection completed.

## q-4 — Real provider adapter — WAIT FOR TWO REAL USER REQUESTS

Only the offline `fake` replay provider exists. Do not choose a provider, create secrets, or
add a provider matrix until `NEXT.md`'s two-user trigger is met. Then the owner chooses the
first requested provider and secret delivery path, and `.agent-harness/tier.json` receives a
fresh `sensitive_data` review. Keys remain environment-only and are never committed.

## Future owner gates

No other owner decision is active. Open a new numbered question only when live demand reaches
an existing `NEXT.md` trigger. In particular, a result store or hosted UI requires a privacy,
retention, and hosting decision before any user data is persisted.
