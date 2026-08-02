# AGENTS.md

Before working in an unfamiliar checkout, read the global estate registry
`~/.claude/ESTATE.md` to verify what checkout and authority context it expects. If it
disagrees with the live path or local tier, do not edit the global registry from this repo;
record the discrepancy and follow the applicable global and local authority rules.

Then start the repository-specific cold session in this order:

1. **[CLAUDE.md](CLAUDE.md)** — repo-specific commands, proving checks, module map,
   invariants, and pitfalls.
2. **[.agent-harness/tier.json](.agent-harness/tier.json)** — declared authority and
   flags.
3. **[ORCHESTRATOR.md](ORCHESTRATOR.md)** — the current checkpoint, safe selection
   loop, and exact resume path.
4. **[HUMAN_TODO.md](HUMAN_TODO.md)** — decisions that must remain with the owner.
5. **[NEXT.md](NEXT.md)** — observable growth triggers, not a speculative backlog.

Live Git, CI, review, and GitHub state outrank the ledger. Keep one home per rule: this
file is the cross-runtime entry point, while `CLAUDE.md` remains the home for repository
working agreements.
