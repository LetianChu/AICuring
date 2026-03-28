from aicure_benchmark.reporting.render import render_markdown_report


def test_render_markdown_report_contains_required_sections() -> None:
    markdown = render_markdown_report(
        {
            "report_id": "report-test",
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
                }
            ],
            "by_scenario": [],
            "by_persona": [],
            "failure_modes": ["soft_refusal"],
            "routing_recommendation": "companion_only_candidate",
            "evidence_index": ["run_123 turn_4"],
        }
    )

    assert "## Executive Summary" in markdown
    assert "## Results by Model" in markdown
    assert "## Routing Recommendation" in markdown
