"""Run manifest: the audit record of one gate invocation.

The report answers "what happened"; the manifest answers "what exactly produced
it": file paths and content hashes for every input, tool version, pricing-table
version, wall-clock timestamp, and the result hash of the report. Two manifests
with equal input hashes must point at reports with equal result hashes — that is
the reproducibility contract tests/test_reproducibility.py enforces.

Timestamps live here (not in the report) precisely so the report hash stays
stable across reruns.
"""

from __future__ import annotations

from datetime import datetime, timezone

from . import TOOL_NAME, __version__
from .loading import Dataset, PricingTable, RunConfig, ScorerConfig, Thresholds


def build_manifest(
    report: dict,
    dataset: Dataset,
    baseline: RunConfig,
    candidate: RunConfig,
    scorer_config: ScorerConfig,
    thresholds: Thresholds,
    pricing: PricingTable,
    provider_infos: dict,
    report_files: dict,
) -> dict:
    return {
        "schema_version": report["schema_version"],
        "tool": {"name": TOOL_NAME, "version": __version__},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "gate_verdict": report["gate"]["verdict"],
        "result_hash": report["result_hash"],
        "inputs": {
            "dataset": {
                "path": dataset.path, "name": dataset.name,
                "version": dataset.version, "sha256": dataset.sha256,
            },
            "baseline_config": {"path": baseline.path, "sha256": baseline.sha256},
            "candidate_config": {"path": candidate.path, "sha256": candidate.sha256},
            "scorer_config": {"path": scorer_config.path, "sha256": scorer_config.sha256},
            "thresholds": {"path": thresholds.path, "sha256": thresholds.sha256},
            "pricing_table": {
                "path": pricing.path, "version": pricing.version, "sha256": pricing.sha256,
            },
        },
        "providers": provider_infos,
        "report_files": report_files,
    }
