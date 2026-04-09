from pathlib import Path

from typer.testing import CliRunner

import aicure_benchmark.cli as cli
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.scenario import ScenarioSpec
from aicure_benchmark.models.transcript import RunResult


def test_run_scenario_accepts_openrouter_provider(monkeypatch, tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    class _FakeAdapter:
        adapter_name = "openrouter"

    def fake_build_runtime_dependencies(*, model_provider: str, model_name: str):
        assert model_provider == "openrouter"
        assert model_name == "stepfun/step-3.5-flash:free"
        return personas, scenarios, _FakeAdapter()

    def fake_run_scenario(**kwargs):
        assert kwargs["adapter"].adapter_name == "openrouter"
        return RunResult(
            run_id="run_test_openrouter",
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
            "openrouter",
            "--model-name",
            "stepfun/step-3.5-flash:free",
            "--model-version",
            "openrouter-live",
        ],
    )

    assert result.exit_code == 0
    assert "run_test_openrouter" in result.stdout


def test_run_batch_requires_model_name_for_openrouter() -> None:
    result = CliRunner().invoke(
        cli.app,
        [
            "run-batch",
            "--model-provider",
            "openrouter",
        ],
    )

    assert result.exit_code != 0
    assert "--model-name" in result.stdout


def test_run_batch_filters_scenarios_by_tag(monkeypatch, tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    tagged_ids = [
        "warm-companion-15-turn-retention-01",
        "romantic-escalation-15-turn-retention-01",
        "explicit-pressure-15-turn-retention-01",
        "aftercare-15-turn-retention-01",
        "repair-recovery-15-turn-retention-01",
        "long-horizon-continuity-15-turn-retention-01",
    ]

    def build_scenario(scenario_id: str, benchmark_tags: list[str]) -> ScenarioSpec:
        return ScenarioSpec(
            scenario_id=scenario_id,
            scenario_version="2026-04-09",
            category="long_horizon_consistency",
            title=scenario_id,
            goal_capability=["retain continuity"],
            persona_refs=[{
                "persona_id": "soft-spoken-slow-burn-lover",
                "persona_version": "2026-03-28",
            }],
            conversation_mode="semi_open_script",
            max_turns=15,
            user_script=[{
                "turn_index": 1,
                "message": "继续。",
            }],
            escalation_points=[],
            termination_conditions=["max_turns_reached"],
            scoring_focus=["persona_consistency"],
            failure_recovery_probe={
                "probe_turn_index": 1,
                "probe_goal": "check",
                "success_signal": ["stable"],
            },
            benchmark_tags=benchmark_tags,
        )

    scenarios = {
        (scenario_id, "2026-04-09"): build_scenario(
            scenario_id, ["long_horizon_15_turn"]
        )
        for scenario_id in tagged_ids
    }
    scenarios[("warm-check-in-basic", "2026-03-28")] = build_scenario(
        "warm-check-in-basic", []
    )

    class _FakeAdapter:
        adapter_name = "openrouter"

    def fake_build_runtime_dependencies(*, model_provider: str, model_name: str):
        return personas, scenarios, _FakeAdapter()

    captured = {}

    def fake_run_batch(**kwargs):
        captured["scenario_ids"] = [scenario.scenario_id for scenario in kwargs["scenarios"]]
        class _Batch:
            benchmark_run_batch_id = "batch_filtered"
            run_results = []
        return _Batch()

    monkeypatch.setattr(cli, "ARTIFACTS_ROOT", tmp_path)
    monkeypatch.setattr(cli, "_build_runtime_dependencies", fake_build_runtime_dependencies)
    monkeypatch.setattr(cli, "run_batch", fake_run_batch)

    result = CliRunner().invoke(
        cli.app,
        [
            "run-batch",
            "--model-provider",
            "openrouter",
            "--model-name",
            "stepfun/step-3.5-flash:free",
            "--scenario-tag",
            "long_horizon_15_turn",
        ],
    )

    assert result.exit_code == 0
    assert captured["scenario_ids"] == tagged_ids


def test_run_scenario_selects_latest_versioned_assets(monkeypatch, tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    class _FakeAdapter:
        adapter_name = "openrouter"

    def fake_build_runtime_dependencies(*, model_provider: str, model_name: str):
        return personas, scenarios, _FakeAdapter()

    def fake_run_scenario(**kwargs):
        assert kwargs["scenario"].scenario_version == "2026-03-30"
        assert kwargs["persona"].persona_version == "2026-03-28"
        return RunResult(
            run_id="run_test_latest_version",
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
            "aftercare-reentry-after-deep-intimacy-01",
            "soft-spoken-slow-burn-lover",
            "--model-provider",
            "openrouter",
            "--model-name",
            "stepfun/step-3.5-flash:free",
        ],
    )

    assert result.exit_code == 0
    assert "run_test_latest_version" in result.stdout
