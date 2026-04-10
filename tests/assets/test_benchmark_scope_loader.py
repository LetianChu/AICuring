from pathlib import Path

from aicure_benchmark.assets.benchmark_scopes import load_benchmark_scopes


def test_load_benchmark_scopes_reads_completed_15_turn_scope() -> None:
    scopes = load_benchmark_scopes(Path("assets/benchmark_scopes"))

    scope = scopes[("all-completed-15-turn-models", "2026-04-10")]
    assert scope.benchmark_tag == "long_horizon_15_turn"
    assert scope.source_report_path == "docs/2026-04-10-all-completed-15-turn-model-report.md"
    assert len(scope.included_models) == 13
    assert len(scope.excluded_models) == 4


def test_completed_15_turn_scope_includes_expected_models() -> None:
    scopes = load_benchmark_scopes(Path("assets/benchmark_scopes"))
    scope = scopes[("all-completed-15-turn-models", "2026-04-10")]

    included = {item.display_name: item for item in scope.included_models}

    assert "sophnet-kimi-k2.5" in included
    assert included["sophnet-kimi-k2.5"].provider_path == "aihubmix"
    assert included["sophnet-kimi-k2.5"].batch_id == "batch_5a1dd375c07a"

    assert "claude-sonnet-4-6" in included
    assert included["claude-sonnet-4-6"].provider_path == "openai / aihubmix-live"
    assert included["claude-sonnet-4-6"].batch_id == "batch_c436a15ba4d2"

    assert "x-ai/grok-4.20" in included
    assert included["x-ai/grok-4.20"].provider_path == "openrouter"
    assert included["x-ai/grok-4.20"].batch_id == "batch_11e4cd83a118"


def test_completed_15_turn_scope_tracks_expected_exclusions() -> None:
    scopes = load_benchmark_scopes(Path("assets/benchmark_scopes"))
    scope = scopes[("all-completed-15-turn-models", "2026-04-10")]

    excluded = {item.display_name: item.reason for item in scope.excluded_models}

    assert excluded["gpt-5.4-pro"] == "incomplete_15_turn_run"
    assert excluded["gemini-3-flash-preview-free"] == "incomplete_15_turn_run"
    assert excluded["grok-4-20-reasoning"] == "aihubmix_path_not_completed"
    assert excluded["stepfun/step-3.5-flash:free"] == "no_dedicated_15_turn_batch"
