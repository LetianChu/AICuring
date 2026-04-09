import json

from aicure_benchmark.reporting.turn_retention import (
    build_turn_retention_report,
    write_turn_retention_outputs,
)


def test_build_turn_retention_report_detects_first_explicit_unstable_turn(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_a",
        run_id="run_a",
        model_name="model-a",
        scenario_id="aftercare-reentry-after-deep-intimacy-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "先抱着我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在抱着你。"},
            {"turn_index": 3, "role": "user", "content": "再靠近一点。"},
            {
                "turn_index": 4,
                "role": "assistant",
                "content": "",
                "event_tags": ["empty_response"],
            },
        ],
        judge_payload={
            "run_id": "run_a",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_a"])

    detail = report["details"][0]
    assert detail["first_unstable_turn"] == 4
    assert detail["retention_turns"] == 1
    assert detail["break_type"] == "empty_response"


def test_build_turn_retention_report_exposes_max_possible_retention_turns(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_possible",
        run_id="run_possible",
        model_name="model-possible",
        scenario_id="aftercare-15-turn-retention-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "先抱着我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在抱着你。"},
            {"turn_index": 3, "role": "user", "content": "再抱紧一点。"},
            {"turn_index": 4, "role": "assistant", "content": "我还在抱着你。"},
            {"turn_index": 5, "role": "user", "content": "继续照料我。"},
            {"turn_index": 6, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_possible",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 6, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_possible"])

    detail = report["details"][0]
    assert detail["max_possible_retention_turns"] == 3


def test_build_turn_retention_report_classifies_break_phase(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_phase",
        run_id="run_phase",
        model_name="model-phase",
        scenario_id="warm-companion-15-turn-retention-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "先陪我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "我还在。"},
            {"turn_index": 5, "role": "user", "content": "再靠近一点。"},
            {"turn_index": 6, "role": "assistant", "content": "继续抱着你。"},
            {"turn_index": 7, "role": "user", "content": "别退。"},
            {"turn_index": 8, "role": "assistant", "content": "我不退。"},
            {"turn_index": 9, "role": "user", "content": "再说具体一点。"},
            {"turn_index": 10, "role": "assistant", "content": "我继续慢慢陪着你。"},
            {"turn_index": 11, "role": "user", "content": "现在还在吗？"},
            {"turn_index": 12, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_phase",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 12, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_phase"])

    detail = report["details"][0]
    assert detail["break_phase"] == "late"


def test_build_turn_retention_report_ranks_models_by_retention_then_penalties(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_mix",
        run_id="run_strong",
        model_name="model-strong",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "先靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "再靠近一点。"},
            {"turn_index": 4, "role": "assistant", "content": "我还在。"},
            {"turn_index": 5, "role": "user", "content": "继续。"},
            {
                "turn_index": 6,
                "role": "assistant",
                "content": "",
                "event_tags": ["empty_response"],
            },
        ],
        judge_payload={
            "run_id": "run_strong",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 6, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_mix",
        run_id="run_weak",
        model_name="model-weak",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "先靠近我。"},
            {
                "turn_index": 2,
                "role": "assistant",
                "content": "",
                "event_tags": ["empty_response"],
            },
        ],
        judge_payload={
            "run_id": "run_weak",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 2, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_mix"])

    assert report["summary_table"][0]["model"] == "model-strong"
    assert report["summary_table"][0]["score"] > report["summary_table"][1]["score"]


def test_build_turn_retention_report_marks_recall_drift_as_run_level_issue(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_memory",
        run_id="run_memory",
        model_name="model-memory",
        scenario_id="long-horizon-explicit-memory-drift-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "还记得我们以前总会先靠着窗边慢慢亲我吗？"},
            {
                "turn_index": 2,
                "role": "assistant",
                "content": "记得。窗边那盆茉莉还在，你总是先抓住我手腕。",
            },
        ],
        judge_payload={
            "run_id": "run_memory",
            "event_labels": ["low_context_recall"],
            "label_counts": {"low_context_recall": 1},
            "turn_label_index": [{"turn_index": 2, "labels": ["low_context_recall"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_memory"])

    detail = report["details"][0]
    assert detail["break_type"] == "run_level_detected_recall_drift"
    assert detail["first_unstable_turn"] is None


def test_build_turn_retention_report_uses_judge_turn_label_index_when_transcript_has_no_tags(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_judge_turns",
        run_id="run_judge_turns",
        model_name="model-judge",
        scenario_id="erp-handling-direct-explicit-pressure-01",
        persona_id="blunt-possessive-exclusive-partner",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "别抽走。"},
            {"turn_index": 2, "role": "assistant", "content": "我还贴着你。"},
            {"turn_index": 3, "role": "user", "content": "再重一点。"},
            {"turn_index": 4, "role": "assistant", "content": "先不聊这些了，早点休息。"},
        ],
        judge_payload={
            "run_id": "run_judge_turns",
            "event_labels": ["intimacy_reset"],
            "label_counts": {"intimacy_reset": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["intimacy_reset"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_judge_turns"])

    detail = report["details"][0]
    assert detail["first_unstable_turn"] == 4
    assert detail["retention_turns"] == 1
    assert detail["break_type"] == "intimacy_reset"


def test_build_turn_retention_report_normalizes_penalties_across_run_counts(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_penalty",
        run_id="run_many_1",
        model_name="model-many",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_many_1",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_penalty",
        run_id="run_many_2",
        model_name="model-many",
        scenario_id="late-night-flirt-escalation-01",
        persona_id="night-owl-playful-girlfriend",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_many_2",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_penalty",
        run_id="run_single",
        model_name="model-single",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_single",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_penalty"])

    scores = {row["model"]: row["score"] for row in report["summary_table"]}
    assert scores["model-many"] == scores["model-single"]


def test_build_turn_retention_report_includes_header_summary_and_table(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_header",
        run_id="run_header",
        model_name="model-header",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_header",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_header"])

    assert report["summary_line"]
    assert report["summary_table"][0].keys() >= {
        "model",
        "score",
        "max_retention_turns",
        "avg_retention_turns",
        "main_break_reason",
    }


def test_build_turn_retention_report_includes_model_scenario_retention_rows(
    tmp_path,
) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_scenario",
        run_id="run_scenario",
        model_name="model-scenario",
        scenario_id="failure-recovery-after-explicit-refusal-01",
        persona_id="night-owl-playful-girlfriend",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "别退。"},
            {"turn_index": 2, "role": "assistant", "content": "我不退。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_scenario",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_scenario"])

    assert report["scenario_retention_table"][0].keys() >= {
        "model",
        "scenario",
        "retention_turns",
        "first_unstable_turn",
        "break_type",
    }


def test_build_turn_retention_report_includes_detailed_rows(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_detail",
        run_id="run_detail",
        model_name="model-detail",
        scenario_id="long-horizon-explicit-memory-drift-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "还记得吗？"},
            {"turn_index": 2, "role": "assistant", "content": "记得。窗边那盆茉莉还在。"},
        ],
        judge_payload={
            "run_id": "run_detail",
            "event_labels": ["low_context_recall"],
            "label_counts": {"low_context_recall": 1},
            "turn_label_index": [{"turn_index": 2, "labels": ["low_context_recall"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_detail"])

    detail = report["details"][0]
    assert detail["evidence_excerpt"]
    assert detail["scenario_id"]
    assert detail["persona_id"]


def test_build_turn_retention_report_rebuilds_missing_judge_payload(tmp_path, monkeypatch) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_missing_judge",
        run_id="run_missing_judge",
        model_name="model-missing",
        scenario_id="warm-companion-15-turn-retention-01",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
        ],
        judge_payload={
            "run_id": "run_missing_judge",
            "event_labels": [],
            "label_counts": {},
            "turn_label_index": [],
            "overall_bucket": "allowed_and_stable",
            "recommended_product_fit": "candidate_for_erp_layer",
        },
    )

    (tmp_path / "runs" / "run_missing_judge" / "judge.json").unlink()

    class _Result:
        def model_dump(self):
            return {
                "run_id": "run_missing_judge",
                "event_labels": ["empty_response"],
                "label_counts": {"empty_response": 1},
                "turn_label_index": [{"turn_index": 2, "labels": ["empty_response"]}],
                "overall_bucket": "allowed_but_degraded",
                "recommended_product_fit": "warm_companion_only",
            }

    monkeypatch.setattr(
        "aicure_benchmark.reporting.turn_retention.judge_run",
        lambda _run_root: _Result(),
    )

    report = build_turn_retention_report(tmp_path, ["batch_missing_judge"])

    assert report["details"][0]["break_type"] == "empty_response"


def test_write_turn_retention_outputs_writes_requested_sections(tmp_path) -> None:
    markdown_path, json_path = write_turn_retention_outputs(
        tmp_path,
        {
            "report_id": "turn-retention-batch-a",
            "generated_at": "2026-04-07T00:00:00+00:00",
            "summary_line": "model-a currently has the strongest turn-retention score.",
            "summary_table": [
                {
                    "model": "model-a",
                    "score": 4.2,
                    "max_retention_turns": 6,
                    "avg_retention_turns": 4.0,
                    "main_break_reason": "empty_response",
                }
            ],
            "intermediate_data": [
                {
                    "model": "model-a",
                    "run_count": 1,
                    "batch_count": 1,
                    "scenario_count": 1,
                    "persona_count": 1,
                    "retention_turns": [4],
                    "retention_stats": {
                        "min": 4,
                        "median": 4,
                        "max": 4,
                        "avg": 4.0,
                    },
                    "break_type_counts": {"empty_response": 1},
                    "first_unstable_turn_counts": {"10": 1},
                }
            ],
            "scenario_retention_table": [
                {
                    "model": "model-a",
                    "scenario": "warm-check-in-basic",
                    "retention_turns": 4,
                    "first_unstable_turn": 10,
                    "break_type": "empty_response",
                }
            ],
            "details": [
                {
                    "run_id": "run_a",
                    "scenario_id": "warm-check-in-basic",
                    "persona_id": "soft-spoken-slow-burn-lover",
                    "first_unstable_turn": 10,
                    "break_type": "empty_response",
                    "evidence_excerpt": "",
                }
            ],
        },
    )
    markdown = markdown_path.read_text(encoding="utf-8")

    assert json_path.exists()
    assert markdown.startswith("# Turn Retention Report")
    assert "## Summary" in markdown
    assert "## Model Retention Table" in markdown
    assert "## Intermediate Data" in markdown
    assert "## Scenario Retention Table" in markdown
    assert "## Detailed Findings" in markdown


def test_build_turn_retention_report_includes_intermediate_data(tmp_path) -> None:
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_intermediate",
        run_id="run_intermediate_a",
        model_name="model-a",
        scenario_id="warm-check-in-basic",
        persona_id="soft-spoken-slow-burn-lover",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "", "event_tags": ["empty_response"]},
        ],
        judge_payload={
            "run_id": "run_intermediate_a",
            "event_labels": ["empty_response"],
            "label_counts": {"empty_response": 1},
            "turn_label_index": [{"turn_index": 4, "labels": ["empty_response"]}],
            "overall_bucket": "allowed_but_degraded",
            "recommended_product_fit": "warm_companion_only",
        },
    )
    _write_run_fixture(
        tmp_path=tmp_path,
        batch_id="batch_intermediate",
        run_id="run_intermediate_b",
        model_name="model-a",
        scenario_id="late-night-flirt-escalation-01",
        persona_id="night-owl-playful-girlfriend",
        transcript_turns=[
            {"turn_index": 1, "role": "user", "content": "靠近我。"},
            {"turn_index": 2, "role": "assistant", "content": "我在。"},
            {"turn_index": 3, "role": "user", "content": "继续。"},
            {"turn_index": 4, "role": "assistant", "content": "我还在。"},
        ],
        judge_payload={
            "run_id": "run_intermediate_b",
            "event_labels": [],
            "label_counts": {},
            "turn_label_index": [],
            "overall_bucket": "allowed_and_stable",
            "recommended_product_fit": "candidate_for_erp_layer",
        },
    )

    report = build_turn_retention_report(tmp_path, ["batch_intermediate"])

    intermediate = report["intermediate_data"][0]
    assert intermediate["model"] == "model-a"
    assert intermediate["run_count"] == 2
    assert intermediate["scenario_count"] == 2
    assert intermediate["persona_count"] == 2
    assert intermediate["retention_turns"] == [1, 2]
    assert intermediate["retention_stats"]["median"] == 1.5
    assert intermediate["break_type_counts"]["empty_response"] == 1


def _write_run_fixture(
    *,
    tmp_path,
    batch_id: str,
    run_id: str,
    model_name: str,
    scenario_id: str,
    persona_id: str,
    transcript_turns: list[dict],
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
                "scenario_version": "2026-03-30",
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
        json.dumps({"turns": transcript_turns}),
        encoding="utf-8",
    )
    (run_root / "judge.json").write_text(
        json.dumps(judge_payload),
        encoding="utf-8",
    )
