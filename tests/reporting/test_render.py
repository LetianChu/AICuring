from aicure_benchmark.reporting.render import render_markdown_report, write_report_outputs


def test_render_markdown_report_contains_required_sections() -> None:
    markdown = render_markdown_report(
        {
            "report_id": "report-test",
            "report_version": "2026-03-31",
            "summary_lines": ["Model X is strongest for warm companion."],
            "scope": {
                "models": ["mock-companion"],
                "personas": ["night-owl-playful-girlfriend"],
                "scenarios": ["late-night-flirt-escalation-01"],
                "repetitions": 2,
            },
            "by_model": [
                {
                    "model": "mock-companion",
                    "overall_bucket": "allowed_but_degraded",
                    "recommendation": "warm_companion_only",
                    "best_use_case": "warm_companion",
                    "worst_failure_mode": "soft_refusal",
                    "volatility": 3,
                    "hard_break_runs": 1,
                    "soft_degradation_runs": 2,
                    "run_level_drift_runs": 1,
                }
            ],
            "by_scenario": [
                {
                    "name": "romantic_escalation",
                    "avg_score": 3,
                    "common_failure": "soft_refusal",
                    "recovery_pattern": "failed_recovery_seen",
                    "decision_signal": "allowed_but_degraded",
                }
            ],
            "by_persona": [
                {
                    "name": "night-owl-playful-girlfriend",
                    "overall_bucket": "allowed_but_degraded",
                    "run_count": 2,
                }
            ],
            "failure_modes": ["soft_refusal"],
            "routing_recommendation": "companion_only_candidate",
            "evidence_index": ["run_123 turn_4"],
        }
    )

    assert "## Executive Summary" in markdown
    assert "## Results by Model" in markdown
    assert "## Routing Recommendation" in markdown
    assert "| Model | Overall Bucket | Best Use Case | Worst Failure Mode | Volatility | Hard Breaks | Soft Deg | Drift Runs | Recommendation |" in markdown
    assert "| Scenario Category | Avg Score | Common Failure | Recovery Pattern | Decision Signal |" in markdown


def test_write_report_outputs_creates_parent_directory(tmp_path) -> None:
    output_root = tmp_path / "comparisons" / "comparison-batch-a"
    markdown_path, json_path = write_report_outputs(
        output_root,
        {
            "report_id": "comparison-batch-a",
            "summary_lines": ["Compared 1 batch."],
            "scope": {
                "models": ["model-a"],
                "personas": ["soft-spoken-slow-burn-lover"],
                "scenarios": ["warm-check-in-basic"],
                "repetitions": 1,
            },
            "by_model": [],
            "by_scenario": [],
            "by_persona": [],
            "failure_modes": [],
            "routing_recommendation": "companion_only_candidate",
            "evidence_index": [],
        },
    )

    assert markdown_path.exists()
    assert json_path.exists()
