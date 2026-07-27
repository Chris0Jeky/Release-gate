# HUMAN_TODO — Release-gate

Actions only a human can take (accounts, names, publishing identity, spending). Agents
may check an item off only when completion is directly verified; never infer a decision.

## q-1 — Decide the published Action reference (blocks any outside consumer)

`README.md` documents `uses: your-org/llm-release-gate@v0`, but the repo is
`Chris0Jeky/Release-gate` and **no git tags exist** (verified 2026-07-27, `git tag -l`
empty). As written, nobody can consume the Action.

Decide one: (a) rename the repo to `llm-release-gate` and keep the docs as-is, or
(b) keep `Release-gate` and document `Chris0Jeky/Release-gate@v0`. Then say so here — an
agent can do the doc edit and cut the `v0` / `v0.1.0` tags once the name is settled.

- [ ] Name chosen: __________

## q-2 — Decide whether `llm-release-gate` gets published to PyPI

`pyproject.toml` declares `name = "llm-release-gate"`, `version = "0.1.0"`. Publishing
needs a PyPI account and an API token, which an agent must never hold. Also decides
whether the name is claimed before someone else takes it.

- [ ] Publish / don't publish (and if publishing, create the token as a repo secret)

## q-3 — Decide on a GitHub Marketplace listing for the Action

`action.yml` already carries `branding` (shield / red), so it is Marketplace-ready.
Listing requires the repo owner to accept the Marketplace terms in the GitHub UI —
human-only, and it depends on q-1's name.

- [ ] Listed / deliberately not listed

## q-4 — When a real provider adapter is requested, decide the provider and the secrets

Only the offline `fake` replay provider exists. `NEXT.md` gates real adapters on two real
users asking. When that fires, a human picks the provider, supplies the CI secret, and the
estate `sensitive_data` flag plus `.agent-harness/tier.json` get re-reviewed. Keys are read
from the environment only — never committed, never in a config file.

- [ ] Not yet triggered (no action needed until two users ask)
