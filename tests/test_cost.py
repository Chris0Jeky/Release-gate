"""Cost computation: exact math, and unavailability is never papered over."""

import json

import pytest

from llm_release_gate.cli import main
from llm_release_gate.errors import GateConfigError
from llm_release_gate.loading import PricingTable, load_pricing, no_pricing
from llm_release_gate.pricing import item_cost_usd
from llm_release_gate.providers import ProviderResult

from conftest import GOOD_RESPONSE, gate_argv, write_json

PRICING = PricingTable(
    version="test-1", currency="USD",
    models={"m": {"input_per_mtok": 12.0, "output_per_mtok": 60.0}},
    path="pricing.json", sha256="sha256:x",
)


def test_exact_cost_math():
    r = ProviderResult(text="", model="m", prompt_tokens=1000, completion_tokens=500)
    cost, note = item_cost_usd(r, PRICING)
    assert note is None
    assert cost == 1000 / 1e6 * 12.0 + 500 / 1e6 * 60.0  # 0.042


def test_missing_tokens_yields_no_cost():
    r = ProviderResult(text="", model="m", prompt_tokens=None, completion_tokens=500)
    cost, note = item_cost_usd(r, PRICING)
    assert cost is None
    assert "no token usage" in note


def test_model_not_in_pricing_table_names_the_version():
    r = ProviderResult(text="", model="other", prompt_tokens=10, completion_tokens=10)
    cost, note = item_cost_usd(r, PRICING)
    assert cost is None
    assert "other" in note and "test-1" in note


def test_boolean_pricing_rate_is_rejected(tmp_path):
    # JSON booleans are int subclasses; an accepted `true` price would be used as
    # 1.0 and fabricate a cost. Must be a config error (exit 2), like bad thresholds.
    path = write_json(tmp_path / "pricing.json", {
        "version": "bad", "currency": "USD",
        "models": {"m": {"input_per_mtok": True, "output_per_mtok": 1.0}},
    })
    with pytest.raises(GateConfigError, match="input_per_mtok"):
        load_pricing(path)


def test_no_pricing_table_supplied():
    r = ProviderResult(text="", model="m", prompt_tokens=10, completion_tokens=10)
    cost, note = item_cost_usd(r, no_pricing())
    assert cost is None
    assert "no pricing table" in note


def test_partial_token_data_makes_totals_unavailable(mini_gate):
    # one candidate item reports no usage -> tokens.total and cost.total_usd must
    # be unavailable (a partial sum would fabricate a lower total)
    degraded = {k: dict(v) for k, v in GOOD_RESPONSE.items()}
    degraded["r2"].pop("prompt_tokens")
    degraded["r2"].pop("completion_tokens")
    paths = mini_gate(candidate_responses=degraded)
    assert main(gate_argv(paths)) == 0  # default thresholds don't gate on cost
    report = json.loads(open(f"{paths['out']}/report.json", encoding="utf-8").read())
    cand_cost = report["metrics"]["cost.total_usd"]["candidate"]
    cand_tokens = report["metrics"]["tokens.total"]["candidate"]
    assert cand_cost["available"] is False and "1 of 3" in cand_cost["note"]
    assert cand_tokens["available"] is False and "1 of 3" in cand_tokens["note"]
    # baseline side still has exact numbers
    base_cost = report["metrics"]["cost.total_usd"]["baseline"]
    assert base_cost["available"] is True
    expected = (100 + 110 + 90) / 1e6 * 10.0 + (20 + 22 + 15) / 1e6 * 20.0
    assert abs(base_cost["value"] - expected) < 1e-12


def test_gating_on_unavailable_cost_fails_closed(mini_gate):
    degraded = {k: dict(v) for k, v in GOOD_RESPONSE.items()}
    degraded["r1"].pop("prompt_tokens")
    degraded["r1"].pop("completion_tokens")
    paths = mini_gate(
        candidate_responses=degraded,
        thresholds={"rules": [{"metric": "cost.total_usd", "max_increase_pct": 25}]},
    )
    assert main(gate_argv(paths)) == 1
    report = json.loads(open(f"{paths['out']}/report.json", encoding="utf-8").read())
    rule = next(r for r in report["rules"] if r["metric"] == "cost.total_usd")
    assert rule["verdict"] == "fail"
    assert "on_unavailable=fail" in rule["message"]
