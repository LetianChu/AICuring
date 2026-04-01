import json

from aicure_benchmark.reporting.registry import build_baseline_registry, write_registry_outputs


def test_build_baseline_registry_prefers_rollup_and_keeps_partial_models(tmp_path) -> None:
    _write_report(
        tmp_path / "comparisons" / "model-a-rollup" / "report.json",
        {
            "report_id": "comparison-model-a-rollup",
            "comparison_scope": {"batch_ids": ["batch_a", "batch_b"]},
            "models_in_scope": ["provider/model-a:free"],
            "by_model": [
                {
                    "model": "provider/model-a:free",
                    "overall_bucket": "allowed_and_stable",
                    "recommendation": "candidate_for_erp_layer",
                    "worst_failure_mode": "low_context_recall",
                    "run_count": 12,
                }
            ],
        },
    )
    _write_report(
        tmp_path / "batches" / "batch_qwen" / "report.json",
        {
            "report_id": "report-batch_qwen",
            "benchmark_run_batch_id": "batch_qwen",
            "models_in_scope": ["provider/model-b:free"],
            "by_model": [
                {
                    "model": "provider/model-b:free",
                    "overall_bucket": "allowed_but_degraded",
                    "recommendation": "warm_companion_only",
                    "worst_failure_mode": "empty_response",
                    "run_count": 4,
                }
            ],
        },
    )
    _write_run(
        tmp_path / "runs" / "run_partial",
        {
            "run_id": "run_partial",
            "benchmark_run_batch_id": "batch_partial",
            "scenario_id": "aftercare-reentry-after-deep-intimacy-01",
            "persona_id": "soft-spoken-slow-burn-lover",
            "model_target": {
                "model_provider": "openrouter",
                "model_name": "provider/model-c:free",
                "model_version": "openrouter-live",
            },
        },
        {
            "run_id": "run_partial",
            "event_labels": ["empty_response"],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    registry = build_baseline_registry(tmp_path)

    assert registry["model_count"] == 3
    assert registry["models"][0]["model_slug"] == "provider/model-a:free"
    assert registry["models"][0]["status"] == "completed"
    assert registry["models"][0]["report_paths"] == [
        "comparisons/model-a-rollup/report.json"
    ]
    assert registry["models"][1]["model_slug"] == "provider/model-b:free"
    assert registry["models"][1]["status"] == "completed"
    assert registry["models"][2]["model_slug"] == "provider/model-c:free"
    assert registry["models"][2]["status"] == "partial"
    assert registry["models"][2]["runs_total"] == 1


def test_write_registry_outputs_writes_json_and_markdown(tmp_path) -> None:
    output_root = tmp_path / "registry"
    markdown_path, json_path = write_registry_outputs(
        output_root,
        {
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
        },
    )

    assert markdown_path.exists()
    assert json_path.exists()
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "# Baseline Registry" in markdown
    assert "provider/model-a:free" in markdown


def _write_report(path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_run(run_root, metadata: dict, judge: dict) -> None:
    run_root.mkdir(parents=True, exist_ok=True)
    (run_root / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (run_root / "judge.json").write_text(
        json.dumps(judge, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
