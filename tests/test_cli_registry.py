from pathlib import Path

from typer.testing import CliRunner

import aicure_benchmark.cli as cli


def test_generate_registry_command_writes_outputs(monkeypatch, tmp_path) -> None:
    captured = {}

    def fake_build_baseline_registry(artifacts_root: Path):
        assert artifacts_root == tmp_path
        return {
            "generated_at": "2026-04-01T00:00:00+00:00",
            "model_count": 1,
            "models": [
                {
                    "model_slug": "provider/model-a:free",
                    "tier": "free",
                    "status": "completed",
                    "runs_total": 12,
                    "overall_bucket": "allowed_and_stable",
                    "current_fit": "candidate_for_erp_layer",
                    "report_paths": ["comparisons/model-a-rollup/report.json"],
                    "strengths": ["Stable on short and mid-horizon explicit handling."],
                    "weaknesses": ["Long-horizon recall drifts under pressure."],
                    "evidence_summary": "Primary source comparisons/model-a-rollup/report.json.",
                }
            ],
        }

    def fake_write_registry_outputs(output_root: Path, registry: dict):
        captured["output_root"] = output_root
        captured["model_count"] = registry["model_count"]
        return output_root / "baseline_registry.md", output_root / "baseline_registry.json"

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(cli, "build_baseline_registry", fake_build_baseline_registry, raising=False)
    monkeypatch.setattr(cli, "write_registry_outputs", fake_write_registry_outputs, raising=False)

    result = CliRunner().invoke(cli.app, ["generate-registry"])

    assert result.exit_code == 0
    assert captured["output_root"] == tmp_path
    assert captured["model_count"] == 1
    assert "baseline_registry.md" in result.stdout
