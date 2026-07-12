"""CLI exit-code contract and GitHub env integration — what CI actually sees."""

import json
import os

from llm_release_gate.cli import main
from llm_release_gate.hashing import file_sha256

from conftest import GOOD_RESPONSE, gate_argv, write_json

EXAMPLES = os.path.join(os.path.dirname(__file__), "..", "examples")


def _example_argv(name: str, out: str) -> list[str]:
    root = os.path.join(EXAMPLES, name)
    return [
        "gate",
        "--dataset", os.path.join(root, "dataset.json"),
        "--baseline", os.path.join(root, "baseline.json"),
        "--candidate", os.path.join(root, "candidate.json"),
        "--scorers", os.path.join(root, "scorers.json"),
        "--thresholds", os.path.join(root, "thresholds.json"),
        "--pricing", os.path.join(EXAMPLES, "pricing.json"),
        "--out", out,
    ]


def test_green_examples_exit_zero(tmp_path):
    assert main(_example_argv("rag-support-bot", str(tmp_path / "a"))) == 0
    assert main(_example_argv("extraction-api", str(tmp_path / "b"))) == 0


def test_red_example_exits_one_and_names_regressions(tmp_path, capsys):
    assert main(_example_argv("assistant-cheap-regression", str(tmp_path / "c"))) == 1
    out = capsys.readouterr().out
    assert "gate FAIL" in out
    assert "quality.pass_rate" in out
    assert "abstention.false_answer_rate" in out
    assert "citations.valid_rate" in out


def test_missing_input_file_exits_two(tmp_path, capsys):
    argv = _example_argv("rag-support-bot", str(tmp_path / "d"))
    argv[argv.index("--dataset") + 1] = "does-not-exist.json"
    assert main(argv) == 2
    assert "configuration error" in capsys.readouterr().err


def test_invalid_threshold_rule_exits_two(mini_gate, capsys):
    paths = mini_gate(thresholds={"rules": [{"metric": "quality.pass_rate"}]})
    assert main(gate_argv(paths)) == 2
    assert "no constraint" in capsys.readouterr().err


def test_metric_without_scorer_exits_two(mini_gate, capsys):
    # thresholds gate on schema validity but no json_schema scorer is configured
    paths = mini_gate(thresholds={"rules": [{"metric": "schema.valid_rate", "min_value": 1.0}]})
    assert main(gate_argv(paths)) == 2
    assert "schema.valid_rate" in capsys.readouterr().err


def test_github_summary_and_outputs_written(mini_gate, monkeypatch, tmp_path):
    summary = tmp_path / "summary.md"
    outputs = tmp_path / "outputs.txt"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    monkeypatch.setenv("GITHUB_OUTPUT", str(outputs))
    paths = mini_gate()
    assert main(gate_argv(paths)) == 0
    assert "llm-release-gate" in summary.read_text(encoding="utf-8")
    out_text = outputs.read_text(encoding="utf-8")
    assert "verdict=pass" in out_text
    assert "exit-code=0" in out_text
    assert "result-hash=sha256:" in out_text


def test_no_github_env_no_files(mini_gate, monkeypatch):
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    paths = mini_gate()
    assert main(gate_argv(paths)) == 0  # simply must not crash


def test_hash_command_matches_library(tmp_path, capsys):
    p = tmp_path / "f.json"
    p.write_text('{"a": 1}', encoding="utf-8")
    assert main(["hash", str(p)]) == 0
    out = capsys.readouterr().out
    assert file_sha256(str(p)) in out


def test_run_command_writes_run_json(mini_gate, tmp_path):
    paths = mini_gate()
    argv = [
        "run",
        "--dataset", paths["dataset"],
        "--config", paths["baseline"],
        "--scorers", paths["scorers"],
        "--pricing", paths["pricing"],
        "--out", str(tmp_path / "runout"),
    ]
    assert main(argv) == 0
    payload = json.loads(open(tmp_path / "runout" / "run.json", encoding="utf-8").read())
    assert payload["run"]["n_items"] == 3
    assert payload["run"]["aggregates"]["quality.pass_rate"]["value"] == 1.0


def test_internal_errors_exit_two_not_one(mini_gate, monkeypatch, capsys):
    paths = mini_gate()
    import llm_release_gate.cli as cli_mod

    def boom(*a, **k):
        raise RuntimeError("unexpected")

    monkeypatch.setattr(cli_mod, "build_report", boom)
    assert main(gate_argv(paths)) == 2
    assert "internal error" in capsys.readouterr().err
