# Release-gate

**Stop unsafe prompt, model, retrieval, tool, or configuration changes from being merged.**

Release-gate is an open-source CLI and GitHub Action that runs your **baseline** and
**candidate** AI configurations against a versioned **golden / replay dataset**, compares
them on **quality, cost, and latency**, and fails the pull-request check when the candidate
introduces a material regression.

> ⚠️ **Early scaffold — no product code yet.** This README describes the intended design;
> the agent harness is in place and implementation starts next.

## The problem

A one-line change to a prompt, a model swap, a new retrieval setting, or a tool-config
tweak can quietly wreck answer quality while looking harmless in a diff. Release-gate makes
those changes *measurable* and *blockable* at review time — not discovered in production.

## How it works

A repository supplies:

1. A **versioned golden / replay dataset** — the inputs to evaluate against.
2. A **baseline configuration** — what's live today.
3. A **candidate configuration** — the change under review.
4. **Quality, cost, and latency thresholds** — what counts as a material regression.

Release-gate then:

- executes both the baseline and the candidate over the dataset,
- compares them across the metrics,
- generates a human-readable report,
- comments the summary on the pull request, and
- fails the GitHub check when the candidate crosses a threshold.

## Example

> Candidate reduced cost by **41%**, but citation coverage fell from **28/30 → 21/30** and
> unsupported answers rose from **1/30 → 6/30**. **Release blocked.**

Cheaper is not the same as safe. Release-gate makes the trade-off explicit and refuses to
let a silent quality regression merge.

## Status

Pre-implementation. The agent harness (tiering, deny floor, permissions) is set up. The
CLI, evaluators, comparison engine, report renderer, and GitHub Action are the next work —
along with the choice of implementation language and dataset/config/threshold schemas.

## License

TBD (intended: open source).
