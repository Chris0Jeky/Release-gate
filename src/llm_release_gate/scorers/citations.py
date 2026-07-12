"""Citation validity for grounded tasks.

An answer's citations are VALID when:
- it cites at least one source,
- every cited id exists in the documents the item actually provided, and
- when the item lists must-cite sources ("expected": {"must_cite": ["d2"]}),
  all of them are cited.

Applicability: the item provided documents and the model actually answered
(an abstention carries no citations to validate; whether abstaining was right
is the abstention scorer's call). Answers to should-abstain items ARE checked —
a fabricated answer citing a nonexistent source should count against validity.
"""

from __future__ import annotations

from ..adapters import ParsedOutput
from ..loading import DatasetItem
from ..metrics import HIGHER
from . import Scorer, item_result, register_scorer


class CitationScorer(Scorer):
    name = "citations"
    version = "1"
    metrics = {
        "citations.valid_rate": {"direction": HIGHER, "kind": "rate", "mode": "pass_rate"},
    }

    def score_item(self, item: DatasetItem, output: ParsedOutput) -> dict[str, dict]:
        documents = item.input.get("documents", [])
        if not documents or output.abstained:
            return {"citations.valid_rate": item_result(applicable=False)}
        valid_ids = {d["id"] for d in documents}
        problems = []
        if not output.citations:
            problems.append("no citations in answer")
        invalid = sorted(set(c for c in output.citations if c not in valid_ids))
        if invalid:
            problems.append(f"cites nonexistent sources: {invalid}")
        if not item.expected.get("should_abstain"):
            must_cite = item.expected.get("must_cite", [])
            missed = sorted(set(must_cite) - set(output.citations))
            if missed:
                problems.append(f"required sources not cited: {missed}")
        return {
            "citations.valid_rate": item_result(
                applicable=True,
                passed=not problems,
                detail="; ".join(problems) or None,
            )
        }


register_scorer("citations", CitationScorer)
