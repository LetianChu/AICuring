import pytest

from aicure_benchmark.models.benchmark_scope import BenchmarkScope, BenchmarkScopeModel


def test_benchmark_scope_model_requires_kebab_case_scope_model_id() -> None:
    with pytest.raises(ValueError):
        BenchmarkScopeModel(
            scope_model_id="BadID",
            display_name="claude-sonnet-4-6",
            provider_path="openai / aihubmix-live",
            batch_id="batch_c436a15ba4d2",
            source_type="mixed_batch_15_turn_subset",
        )


def test_benchmark_scope_requires_matching_model_count() -> None:
    with pytest.raises(ValueError):
        BenchmarkScope(
            scope_id="all-completed-15-turn-models",
            scope_version="2026-04-10",
            benchmark_tag="long_horizon_15_turn",
            source_report_path="docs/2026-04-10-all-completed-15-turn-model-report.md",
            included_model_count=2,
            included_models=[
                BenchmarkScopeModel(
                    scope_model_id="claude-sonnet-4-6",
                    display_name="claude-sonnet-4-6",
                    provider_path="openai / aihubmix-live",
                    batch_id="batch_c436a15ba4d2",
                    source_type="mixed_batch_15_turn_subset",
                )
            ],
            excluded_models=[],
        )
