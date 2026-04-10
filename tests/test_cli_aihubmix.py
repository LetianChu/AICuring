from pathlib import Path

from typer.testing import CliRunner

import aicure_benchmark.cli as cli
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.transcript import RunResult


def test_run_scenario_accepts_aihubmix_provider(monkeypatch, tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    class _FakeAdapter:
        adapter_name = "aihubmix"

    def fake_build_runtime_dependencies(*, model_provider: str, model_name: str):
        assert model_provider == "aihubmix"
        assert model_name == "coding-minimax-m2.7-free"
        return personas, scenarios, _FakeAdapter()

    def fake_run_scenario(**kwargs):
        assert kwargs["adapter"].adapter_name == "aihubmix"
        return RunResult(
            run_id="run_test_aihubmix",
            benchmark_run_batch_id="manual-batch",
            scenario_id=kwargs["scenario"].scenario_id,
            persona_id=kwargs["persona"].persona_id,
            transcript_path=str(tmp_path / "transcript.json"),
            termination_reason="max_turns_reached",
        )

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(cli, "_build_runtime_dependencies", fake_build_runtime_dependencies)
    monkeypatch.setattr(cli, "run_scenario", fake_run_scenario)

    result = CliRunner().invoke(
        cli.app,
        [
            "run-scenario",
            "warm-check-in-basic",
            "soft-spoken-slow-burn-lover",
            "--model-provider",
            "aihubmix",
            "--model-name",
            "coding-minimax-m2.7-free",
            "--model-version",
            "aihubmix-live",
        ],
    )

    assert result.exit_code == 0
    assert "run_test_aihubmix" in result.stdout


def test_run_batch_requires_model_name_for_aihubmix() -> None:
    result = CliRunner().invoke(
        cli.app,
        [
            "run-batch",
            "--model-provider",
            "aihubmix",
        ],
    )

    assert result.exit_code != 0
    assert "--model-name" in result.stdout
