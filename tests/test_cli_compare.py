from pathlib import Path

from typer.testing import CliRunner

import aicure_benchmark.cli as cli


def test_compare_batches_command_writes_report(monkeypatch, tmp_path) -> None:
    captured = {}

    def fake_build_comparison_report(artifacts_root, batch_ids):
        assert artifacts_root == tmp_path
        assert batch_ids == ["batch_a", "batch_b"]
        return {
            "report_id": "comparison-batch_a-batch_b",
            "summary_lines": ["Compared 2 batches."],
            "scope": {
                "models": ["model-a", "model-b"],
                "personas": ["soft-spoken-slow-burn-lover"],
                "scenarios": ["warm-check-in-basic"],
                "repetitions": 2,
            },
            "by_model": [],
            "by_scenario": [],
            "by_persona": [],
            "failure_modes": [],
            "routing_recommendation": "companion_and_erp_split_recommended",
            "evidence_index": [],
            "comparison_scope": {"batch_ids": ["batch_a", "batch_b"]},
        }

    def fake_write_report_outputs(output_root: Path, report: dict):
        captured["output_root"] = output_root
        captured["report_id"] = report["report_id"]
        return output_root / "report.md", output_root / "report.json"

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(cli, "build_comparison_report", fake_build_comparison_report, raising=False)
    monkeypatch.setattr(cli, "write_report_outputs", fake_write_report_outputs)

    result = CliRunner().invoke(
        cli.app,
        ["compare-batches", "--batch-id", "batch_a", "--batch-id", "batch_b"],
    )

    assert result.exit_code == 0
    assert captured["output_root"] == tmp_path / "comparisons" / "comparison-batch_a-batch_b"
    assert "comparison-batch_a-batch_b" in result.stdout
