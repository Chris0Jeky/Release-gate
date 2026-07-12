"""The reproducibility contract: identical inputs -> identical report bytes and
result hash; volatile data (timestamps, paths) lives only in the manifest."""

import json

from llm_release_gate.cli import main

from conftest import gate_argv


def test_same_inputs_same_result_hash_and_report_bytes(mini_gate, tmp_path):
    paths = mini_gate()
    out_a = str(tmp_path / "out_a")
    out_b = str(tmp_path / "out_b")
    assert main(gate_argv({**paths, "out": out_a})) == 0
    assert main(gate_argv({**paths, "out": out_b})) == 0
    report_a = open(f"{out_a}/report.json", encoding="utf-8").read()
    report_b = open(f"{out_b}/report.json", encoding="utf-8").read()
    assert report_a == report_b
    assert json.loads(report_a)["result_hash"] == json.loads(report_b)["result_hash"]
    # Markdown and HTML renderings are pure functions of the report
    assert (
        open(f"{out_a}/report.md", encoding="utf-8").read()
        == open(f"{out_b}/report.md", encoding="utf-8").read()
    )
    assert (
        open(f"{out_a}/report.html", encoding="utf-8").read()
        == open(f"{out_b}/report.html", encoding="utf-8").read()
    )


def test_report_carries_no_timestamps_or_paths(mini_gate):
    paths = mini_gate()
    assert main(gate_argv(paths)) == 0
    report = json.loads(open(f"{paths['out']}/report.json", encoding="utf-8").read())
    text = json.dumps(report)
    assert "created_at" not in text
    # input identity is by hash, not by filesystem location
    assert paths["dataset"].replace("\\", "/") not in text.replace("\\\\", "/")


def test_manifest_pins_inputs_and_result(mini_gate):
    paths = mini_gate()
    assert main(gate_argv(paths)) == 0
    report = json.loads(open(f"{paths['out']}/report.json", encoding="utf-8").read())
    manifest = json.loads(open(f"{paths['out']}/manifest.json", encoding="utf-8").read())
    assert manifest["result_hash"] == report["result_hash"]
    assert manifest["gate_verdict"] == report["gate"]["verdict"]
    assert "created_at" in manifest
    for key in ("dataset", "baseline_config", "candidate_config", "scorer_config", "thresholds"):
        assert manifest["inputs"][key]["sha256"].startswith("sha256:")
    assert manifest["inputs"]["dataset"]["sha256"] == report["inputs"]["dataset"]["sha256"]
    # fixture identity of the fake provider is pinned too
    assert manifest["providers"]["baseline"]["fixtures_sha256"].startswith("sha256:")


def test_changed_input_changes_result_hash(mini_gate, tmp_path):
    paths = mini_gate()
    assert main(gate_argv(paths)) == 0
    hash_a = json.loads(open(f"{paths['out']}/report.json", encoding="utf-8").read())["result_hash"]
    # tighten a threshold -> different verdict inputs -> different result identity
    paths2 = mini_gate(thresholds={
        "rules": [{"metric": "quality.pass_rate", "max_drop_abs": 0.0},
                  {"metric": "latency.p95_ms", "max_increase_pct": 1, "level": "warn"}]
    })
    out2 = str(tmp_path / "out2")
    assert main(gate_argv({**paths2, "out": out2})) == 0
    hash_b = json.loads(open(f"{out2}/report.json", encoding="utf-8").read())["result_hash"]
    assert hash_a != hash_b
