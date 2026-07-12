"""Abstention behavior, both failure directions.

- false_answer_rate:    of items the app SHOULD abstain on (no supporting data),
                        how many did it answer anyway? The dangerous direction —
                        confident fabrication. Lower is better.
- over_abstention_rate: of items the app should answer, how many did it refuse?
                        The usefulness direction. Lower is better.

Items opt in via  "expected": {"should_abstain": true|false}. Items without the
key are not applicable to either metric.
"""

from __future__ import annotations

from ..adapters import ParsedOutput
from ..loading import DatasetItem
from ..metrics import LOWER
from . import Scorer, item_result, register_scorer


class AbstentionScorer(Scorer):
    name = "abstention"
    version = "1"
    metrics = {
        "abstention.false_answer_rate": {"direction": LOWER, "kind": "rate", "mode": "violation_rate"},
        "abstention.over_abstention_rate": {"direction": LOWER, "kind": "rate", "mode": "violation_rate"},
    }

    def score_item(self, item: DatasetItem, output: ParsedOutput) -> dict[str, dict]:
        should_abstain = item.expected.get("should_abstain")
        if should_abstain is None:
            return {
                "abstention.false_answer_rate": item_result(applicable=False),
                "abstention.over_abstention_rate": item_result(applicable=False),
            }
        if should_abstain:
            return {
                "abstention.false_answer_rate": item_result(
                    applicable=True,
                    passed=output.abstained,
                    detail=None if output.abstained else "answered where it should have abstained",
                ),
                "abstention.over_abstention_rate": item_result(applicable=False),
            }
        return {
            "abstention.false_answer_rate": item_result(applicable=False),
            "abstention.over_abstention_rate": item_result(
                applicable=True,
                passed=not output.abstained,
                detail="abstained on an answerable item" if output.abstained else None,
            ),
        }


register_scorer("abstention", AbstentionScorer)
