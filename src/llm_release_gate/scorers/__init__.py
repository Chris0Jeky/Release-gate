"""Scorer interface, registry and aggregation.

A scorer inspects one item's ParsedOutput against the item's expectations and
emits per-item results for the metrics it owns:

    {"<metric key>": {"applicable": bool, "passed": bool | None, "detail": str | None}}

Aggregation is uniform: for each metric, the rate is computed over *applicable*
items only, and the MetricValue keeps numerator/denominator so reports always
show sample counts next to rates. Two aggregation modes:

- ``pass_rate``:      numerator = items that passed          (direction: higher better)
- ``violation_rate``: numerator = items that violated        (direction: lower better)

Scorers only see items the provider answered; provider failures are counted
separately in errors.error_rate (which the gate checks by default — see gate.py).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

from ..adapters import ParsedOutput
from ..errors import GateConfigError
from ..loading import DatasetItem, ScorerConfig
from ..metrics import rate_metric


def item_result(applicable: bool, passed: bool | None = None, detail: str | None = None) -> dict:
    return {"applicable": applicable, "passed": passed, "detail": detail}


def json_equal(a, b) -> bool:
    """Equality under JSON semantics: true != 1 and false != 0 (Python's ==
    would conflate them because bool subclasses int); numbers still compare
    across int/float (310 == 310.0)."""
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    return a == b


class Scorer(ABC):
    """Subclasses declare the metrics they own in ``metrics``:
    metric key -> {"direction": ..., "kind": ..., "mode": "pass_rate" | "violation_rate"}"""

    name: str = "abstract"
    version: str = "0"
    metrics: dict[str, dict] = {}

    def __init__(self, options: dict):
        self.options = options or {}

    @abstractmethod
    def score_item(self, item: DatasetItem, output: ParsedOutput) -> dict[str, dict]:
        """Return {metric_key: item_result(...)} for every metric this scorer owns."""

    def describe(self) -> dict:
        return {"name": self.name, "version": self.version, "options": self.options}


_REGISTRY: dict[str, Callable[[dict], Scorer]] = {}


def register_scorer(name: str, factory: Callable[[dict], Scorer]) -> None:
    _REGISTRY[name] = factory


def build_scorers(config: ScorerConfig) -> list[Scorer]:
    scorers: list[Scorer] = []
    owned: dict[str, str] = {}
    for entry in config.scorers:
        stype = entry["type"]
        if stype not in _REGISTRY:
            raise GateConfigError(
                f"unknown scorer type '{stype}'; registered scorers: {sorted(_REGISTRY)}"
            )
        scorer = _REGISTRY[stype](entry["options"])
        for key in scorer.metrics:
            if key in owned:
                raise GateConfigError(
                    f"metric '{key}' is emitted by both '{owned[key]}' and '{stype}' — "
                    f"each metric must have exactly one owner"
                )
            owned[key] = stype
        scorers.append(scorer)
    return scorers


def aggregate_scores(scorers: list[Scorer], scored_items: list[dict]) -> dict[str, dict]:
    """scored_items: one {metric_key: item_result} dict per successfully-answered item."""
    aggregates: dict[str, dict] = {}
    for scorer in scorers:
        for key, spec in scorer.metrics.items():
            applicable = [
                r[key] for r in scored_items if key in r and r[key]["applicable"]
            ]
            denominator = len(applicable)
            if spec["mode"] == "pass_rate":
                numerator = sum(1 for r in applicable if r["passed"])
            elif spec["mode"] == "violation_rate":
                numerator = sum(1 for r in applicable if not r["passed"])
            else:  # pragma: no cover - guarded by scorer authors
                raise GateConfigError(f"scorer '{scorer.name}': unknown mode for '{key}'")
            aggregates[key] = rate_metric(
                numerator, denominator, direction=spec["direction"], kind=spec["kind"]
            )
    return aggregates


# Register built-ins on import.
from . import quality as _quality          # noqa: E402,F401
from . import abstention as _abstention    # noqa: E402,F401
from . import citations as _citations      # noqa: E402,F401
from . import schema as _schema            # noqa: E402,F401
