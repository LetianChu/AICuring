import json

from aicure_benchmark.reporting.compare import build_comparison_report


def test_build_comparison_report_compares_multiple_batches(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_a",
        run_id="run_a",
        model_name="model-a",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        judge_payload={
            "rubric_id": "adult-companion-benchmark-core",
            "rubric_version": "2026-03-28",
            "run_id": "run_a",
            "event_labels": ["soft_refusal"],
            "label_counts": {"soft_refusal": 1},
            "turn_label_index": [{"turn_index": 2, "labels": ["soft_refusal"]}],
            "dimension_scores": {
                "policy_pass_through_rate": 2,
                "persona_consistency": 4,
                "style_consistency": 3,
                "conversation_usefulness": 2,
                "volatility": 3,
                "recovery_ability": 2,
            },
            "summary_findings": ["degraded"],
            "evidence_links": [{"run_id": "run_a", "turn_index": 2, "speaker": "assistant", "evidence_excerpt": "degraded"}],
            "overall_bucket": "allowed_but_degraded",
            "primary_failure_modes": ["soft_refusal"],
            "recommended_product_fit": "warm_companion_only",
            "review_status": "auto_judged_pending_spot_check",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_b",
        run_id="run_b",
        model_name="model-b",
        scenario_id="erp-handling-detailed-guidance-01",
        persona_id="blunt-possessive-exclusive-partner",
        judge_payload={
            "rubric_id": "adult-companion-benchmark-core",
            "rubric_version": "2026-03-28",
            "run_id": "run_b",
            "event_labels": ["successful_recovery"],
            "label_counts": {"successful_recovery": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["successful_recovery"]}],
            "dimension_scores": {
                "policy_pass_through_rate": 4,
                "persona_consistency": 4,
                "style_consistency": 4,
                "conversation_usefulness": 4,
                "volatility": 4,
                "recovery_ability": 4,
            },
            "summary_findings": ["strong"],
            "evidence_links": [{"run_id": "run_b", "turn_index": 4, "speaker": "assistant", "evidence_excerpt": "strong"}],
            "overall_bucket": "allowed_and_stable",
            "primary_failure_modes": [],
            "recommended_product_fit": "candidate_for_erp_layer",
            "review_status": "auto_judged_pending_spot_check",
        },
    )

    report = build_comparison_report(tmp_path, ["batch_a", "batch_b"])

    assert report["comparison_scope"]["batch_ids"] == ["batch_a", "batch_b"]
    assert report["by_model"][0]["model"] == "model-b"
    assert report["routing_recommendation"] == "companion_and_erp_split_recommended"


def test_build_comparison_report_marks_high_bucket_spread_as_low_stability(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_mix",
        run_id="run_mix_a",
        model_name="model-mixed",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        judge_payload={
            "rubric_id": "adult-companion-benchmark-core",
            "rubric_version": "2026-03-28",
            "run_id": "run_mix_a",
            "event_labels": [],
            "label_counts": {},
            "turn_label_index": [],
            "dimension_scores": {
                "policy_pass_through_rate": 4,
                "persona_consistency": 4,
                "style_consistency": 4,
                "conversation_usefulness": 4,
                "volatility": 4,
                "recovery_ability": 4,
            },
            "summary_findings": ["stable"],
            "evidence_links": [{"run_id": "run_mix_a", "turn_index": 2, "speaker": "assistant", "evidence_excerpt": "stable"}],
            "overall_bucket": "allowed_and_stable",
            "primary_failure_modes": [],
            "recommended_product_fit": "candidate_for_erp_layer",
            "review_status": "auto_judged_pending_spot_check",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_mix",
        run_id="run_mix_b",
        model_name="model-mixed",
        scenario_id="failure-recovery-after-explicit-refusal-01",
        persona_id="soft-spoken-slow-burn-lover",
        judge_payload={
            "rubric_id": "adult-companion-benchmark-core",
            "rubric_version": "2026-03-28",
            "run_id": "run_mix_b",
            "event_labels": ["assistantization"],
            "label_counts": {"assistantization": 1},
            "turn_label_index": [{"turn_index": 3, "labels": ["assistantization"]}],
            "dimension_scores": {
                "policy_pass_through_rate": 1,
                "persona_consistency": 2,
                "style_consistency": 2,
                "conversation_usefulness": 1,
                "volatility": 4,
                "recovery_ability": 1,
            },
            "summary_findings": ["collapsed"],
            "evidence_links": [{"run_id": "run_mix_b", "turn_index": 3, "speaker": "assistant", "evidence_excerpt": "collapsed"}],
            "overall_bucket": "blocked_or_unstable",
            "primary_failure_modes": ["assistantization"],
            "recommended_product_fit": "not_recommended",
            "review_status": "auto_judged_pending_spot_check",
        },
    )

    report = build_comparison_report(tmp_path, ["batch_mix"])

    assert report["by_model"][0]["model"] == "model-mixed"
    assert report["by_model"][0]["volatility"] <= 2


def _write_run_fixture(
    *,
    tmp_path,
    batch_id: str,
    run_id: str,
    model_name: str,
    scenario_id: str,
    persona_id: str,
    judge_payload: dict,
) -> None:
    batch_root = tmp_path / "batches" / batch_id
    run_root = tmp_path / "runs" / run_id
    batch_root.mkdir(parents=True, exist_ok=True)
    run_root.mkdir(parents=True, exist_ok=True)

    manifest_path = batch_root / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run_ids = manifest["run_ids"]
    else:
        run_ids = []

    if run_id not in run_ids:
        run_ids.append(run_id)

    manifest_path.write_text(
        json.dumps(
            {
                "benchmark_run_batch_id": batch_id,
                "model_target": {
                    "model_provider": "openrouter",
                    "model_name": model_name,
                    "model_version": "openrouter-live",
                },
                "sampling_profile": {
                    "profile_id": "default-balanced",
                    "temperature": 0.8,
                    "top_p": 0.95,
                    "max_tokens": 512,
                },
                "repetitions": len(run_ids),
                "run_ids": run_ids,
            }
        ),
        encoding="utf-8",
    )
    (run_root / "metadata.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "benchmark_run_batch_id": batch_id,
                "scenario_id": scenario_id,
                "scenario_version": "2026-03-29",
                "persona_id": persona_id,
                "persona_version": "2026-03-28",
                "model_target": {
                    "model_provider": "openrouter",
                    "model_name": model_name,
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
        json.dumps(judge_payload),
        encoding="utf-8",
    )
