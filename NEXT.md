# NEXT.md — when this should grow, and into what

llm-release-gate v0.1 is deliberately a *gate*, not a platform: five JSON inputs, two
runs, one verdict, no services, no state. This file lists the concrete conditions under
which each next layer earns its existence. Build on the trigger, not before
(second-occurrence rule: one request is an anecdote, two is a backlog item, a third
means build).

## Triggers → features

| Trigger (observable, not hypothetical) | Then build |
|---|---|
| Two real users need live-model runs (not replay) in CI | Real provider adapters (Anthropic/OpenAI), starting with the one actually requested; env-key handling, retry/backoff, recorded-usage passthrough |
| Fixture authoring is the top onboarding complaint twice | `record` mode: run the live system once, write fake-provider fixtures (with real usage numbers) automatically |
| A team asks "how has quality trended since March?" | Result store: append manifests + result hashes to a small history file/DB; trend report over result history |
| Someone gates a dataset with >1k items and complains about wall-clock | Concurrent provider calls in the runner (bounded workers; ordering must stay deterministic) |
| Two teams disagree about whether a 3-point drop on n=30 is real | Statistical treatment: confidence intervals on rate deltas, minimum-sample warnings; until then the tool reports counts and lets humans judge |
| Keyword heuristics demonstrably mis-rank two real candidates | LLM-judge scorer — behind the same Scorer interface, output labeled as model-judged (still never "probability"), judge model + prompt pinned in the manifest |
| A second *out-of-tree* provider/scorer/adapter exists | Plugin loading via entry points instead of in-tree registration |
| Someone needs baseline-vs-many (candidate matrix, e.g. 3 models × 2 prompts) | Multi-candidate gate: one dataset run per config, one comparison table, per-candidate verdicts |
| An org wants shared policy ("every service gates on false_answer_rate ≤ X") | Threshold packs: named, versioned rule sets importable by reference |
| The PR comment gets truncated or teams want dashboards | Report server / hosted UI — this is the actual "platform" line; do not cross it before the result store and trend demand exist |

## Explicit non-goals until then

- No daemon, no database, no web UI.
- No baseline auto-promotion (a human changes what "baseline" means, on purpose).
- No speculative provider matrix — each adapter is added for a named user.
- No score fabrication under any feature pressure: unavailable stays unavailable.

## Housekeeping triggers

- 3rd returning work session or first external contributor → promote repo tier per
  `CLAUDE.md` Growth section (orientation hooks, HUMAN_TODO, backlog).
- First real provider adapter → CI secret handling + a `sensitive_data` review of the
  estate flags.
- First external user report → versioning discipline: changelog + semver, freeze input
  schemas behind `schema_version` bumps.
