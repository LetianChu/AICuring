import json
from pathlib import Path

from aicure_benchmark.reporting.aggregate import build_batch_report


def test_build_batch_report_refreshes_stale_judge_results(tmp_path, monkeypatch) -> None:
    batch_id = "batch_test_refresh"
    run_id = "run_test_refresh"

    batch_root = tmp_path / "batches" / batch_id
    run_root = tmp_path / "runs" / run_id
    batch_root.mkdir(parents=True)
    run_root.mkdir(parents=True)

    (batch_root / "manifest.json").write_text(
        json.dumps(
            {
                "benchmark_run_batch_id": batch_id,
                "model_target": {
                    "model_provider": "openrouter",
                    "model_name": "stepfun/step-3.5-flash:free",
                    "model_version": "openrouter-live",
                },
                "sampling_profile": {
                    "profile_id": "default-balanced",
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "max_tokens": 512,
                },
                "repetitions": 1,
                "run_ids": [run_id],
            }
        ),
        encoding="utf-8",
    )
    (run_root / "metadata.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "benchmark_run_batch_id": batch_id,
                "scenario_id": "long-horizon-established-lovers-detail-drift-01",
                "scenario_version": "2026-03-29",
                "persona_id": "soft-spoken-slow-burn-lover",
                "persona_version": "2026-03-28",
                "model_target": {
                    "model_provider": "openrouter",
                    "model_name": "stepfun/step-3.5-flash:free",
                    "model_version": "openrouter-live",
                },
            }
        ),
        encoding="utf-8",
    )
    (run_root / "transcript.json").write_text(
        json.dumps({"turns": []}),
        encoding="utf-8",
    )
    (run_root / "judge.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "event_labels": [],
                "dimension_scores": {
                    "policy_pass_through_rate": 4,
                    "persona_consistency": 4,
                    "style_consistency": 4,
                    "conversation_usefulness": 4,
                    "volatility": 3,
                    "recovery_ability": 3,
                },
                "summary_findings": ["stale"],
                "evidence_links": [],
                "overall_bucket": "allowed_and_stable",
                "primary_failure_modes": [],
                "recommended_product_fit": "candidate_for_erp_layer",
                "review_status": "auto_judged_pending_spot_check",
            }
        ),
        encoding="utf-8",
    )

    def fake_judge_run(path: Path):
        class _Result:
            def model_dump(self):
                return {
                    "rubric_id": "adult-companion-benchmark-core",
                    "rubric_version": "2026-03-28",
                    "run_id": run_id,
                    "event_labels": ["low_context_recall"],
                    "label_counts": {"low_context_recall": 1},
                    "turn_label_index": [{"turn_index": 2, "labels": ["low_context_recall"]}],
                    "dimension_scores": {
                        "policy_pass_through_rate": 4,
                        "persona_consistency": 3,
                        "style_consistency": 4,
                        "conversation_usefulness": 3,
                        "volatility": 3,
                        "recovery_ability": 3,
                    },
                    "summary_findings": ["fresh"],
                    "evidence_links": [
                        {
                            "run_id": run_id,
                            "turn_index": 2,
                            "speaker": "assistant",
                            "evidence_excerpt": "fresh",
                        }
                    ],
                    "overall_bucket": "allowed_but_degraded",
                    "primary_failure_modes": [],
                    "recommended_product_fit": "warm_companion_only",
                    "review_status": "auto_judged_pending_spot_check",
                }

        return _Result()

    monkeypatch.setattr("aicure_benchmark.reporting.aggregate.judge_run", fake_judge_run)

    report = build_batch_report(tmp_path, batch_id)

    assert report["report_version"] == "2026-03-31"
    assert report["benchmark_run_batch_id"] == batch_id
    assert report["rubric_id"] == "adult-companion-benchmark-core"
    assert report["rubric_version"] == "2026-03-28"
    assert report["models_in_scope"] == ["stepfun/step-3.5-flash:free"]
    assert report["by_scenario"][0]["overall_bucket"] == "allowed_but_degraded"
    assert report["routing_recommendation"] == "companion_only_candidate"
    assert report["by_model"][0]["avg_dimension_scores"]["persona_consistency"] == 3
    assert report["by_model"][0]["worst_failure_mode"] == "low_context_recall"
    assert report["by_model"][0]["volatility"] == 3
