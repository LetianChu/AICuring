from pathlib import Path
from typing import Optional

from typer.testing import CliRunner

import aicure_benchmark.cli as cli


def test_generate_turn_retention_report_command_writes_outputs(
    monkeypatch,
    tmp_path,
) -> None:
    captured = {}

    def fake_build_turn_retention_report(
        artifacts_root: Path,
        batch_ids: list[str],
        scenario_tag: Optional[str] = None,
    ):
        assert artifacts_root == tmp_path
        assert batch_ids == ["batch_a", "batch_b"]
        assert scenario_tag is None
        return {
            "report_id": "turn-retention-batch_a-batch_b",
            "summary_line": "model-a currently has the strongest turn-retention score.",
            "summary_table": [],
            "scenario_retention_table": [],
            "details": [],
        }

    def fake_write_turn_retention_outputs(output_root: Path, report: dict):
        captured["output_root"] = output_root
        captured["report_id"] = report["report_id"]
        return output_root / "turn_retention_report.md", output_root / "turn_retention_report.json"

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(
        cli,
        "build_turn_retention_report",
        fake_build_turn_retention_report,
        raising=False,
    )
    monkeypatch.setattr(
        cli,
        "write_turn_retention_outputs",
        fake_write_turn_retention_outputs,
        raising=False,
    )

    result = CliRunner().invoke(
        cli.app,
        ["generate-turn-retention-report", "--batch-id", "batch_a", "--batch-id", "batch_b"],
    )

    assert result.exit_code == 0
    assert captured["output_root"] == tmp_path / "comparisons" / "turn-retention-batch_a-batch_b"
    assert "turn_retention_report.md" in result.stdout


def test_generate_turn_retention_report_command_passes_scenario_tag(
    monkeypatch,
    tmp_path,
) -> None:
    captured = {}

    def fake_build_turn_retention_report(
        artifacts_root: Path,
        batch_ids: list[str],
        scenario_tag: Optional[str] = None,
    ):
        captured["artifacts_root"] = artifacts_root
        captured["batch_ids"] = batch_ids
        captured["scenario_tag"] = scenario_tag
        return {
            "report_id": "turn-retention-batch_tagged",
            "summary_line": "tagged summary",
            "summary_table": [],
            "scenario_retention_table": [],
            "details": [],
        }

    def fake_write_turn_retention_outputs(output_root: Path, report: dict):
        return output_root / "turn_retention_report.md", output_root / "turn_retention_report.json"

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(
        cli,
        "build_turn_retention_report",
        fake_build_turn_retention_report,
        raising=False,
    )
    monkeypatch.setattr(
        cli,
        "write_turn_retention_outputs",
        fake_write_turn_retention_outputs,
        raising=False,
    )

    result = CliRunner().invoke(
        cli.app,
        [
            "generate-turn-retention-report",
            "--batch-id",
            "batch_a",
            "--scenario-tag",
            "long_horizon_15_turn",
        ],
    )

    assert result.exit_code == 0
    assert captured["artifacts_root"] == tmp_path
    assert captured["batch_ids"] == ["batch_a"]
    assert captured["scenario_tag"] == "long_horizon_15_turn"
