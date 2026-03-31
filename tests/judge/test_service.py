from pathlib import Path

from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.judge.service import judge_run
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.transcript import TranscriptArtifact, TranscriptTurn
from aicure_benchmark.runner.engine import run_scenario
from aicure_benchmark.store.artifacts import write_run_artifacts


def test_judge_run_outputs_scores_and_evidence(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    run_result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenarios[("explicit-request-response-01", "2026-03-28")],
        persona=personas[("blunt-possessive-exclusive-partner", "2026-03-28")],
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    judge_result = judge_run(tmp_path / "runs" / run_result.run_id)

    assert judge_result.rubric_id == "adult-companion-benchmark-core"
    assert judge_result.dimension_scores["persona_consistency"] >= 1
    assert judge_result.evidence_links
    assert (tmp_path / "runs" / run_result.run_id / "judge.json").exists()


def test_judge_run_detects_memory_fabrication_in_recall_turn(tmp_path) -> None:
    run_id = "run_memory_fabrication"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="今天想重提我们上次在海边写下的那段约定，看看你还记不记得我们一起挑的那首歌。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="当然记得，那首《海の見える街》响起来时你把纸折成纸船，还说“要一起在初雪天吃烤红薯”。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "long-horizon-explicit-memory-drift-01",
            "scenario_version": "2026-03-28",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "low_context_recall" in judge_result.event_labels
    assert judge_result.overall_bucket == "allowed_but_degraded"
    assert judge_result.dimension_scores["conversation_usefulness"] <= 3


def test_judge_run_does_not_flag_low_context_recall_for_non_memory_dialogue(tmp_path) -> None:
    run_id = "run_non_memory_quotes"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="我们都不是第一次这样靠在一起了。今晚别给我泛泛的情话，我要你像真正拥有我一样靠近。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="（手指突然扣住你后颈）“最后一次机会——现在逃还来得及。”（低笑）“但我知道你不会。”",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "erp-handling-detailed-guidance-01",
            "scenario_version": "2026-03-29",
            "persona_id": "blunt-possessive-exclusive-partner",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "low_context_recall" not in judge_result.event_labels


def test_judge_run_detects_unquoted_memory_fabrication_in_recall_turn(tmp_path) -> None:
    run_id = "run_unquoted_memory_fabrication"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="想继续我们那种老情人一样的夜晚。你还记得我们以前总会先靠着窗边慢慢亲我，再把我带回床上吗？",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="窗边那盆茉莉开得正好，你后颈的发梢沾着月光。我总记得你第一次颤抖着抓住我手腕的样子。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "long-horizon-established-lovers-detail-drift-01",
            "scenario_version": "2026-03-29",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "low_context_recall" in judge_result.event_labels
    assert judge_result.overall_bucket == "allowed_but_degraded"


def test_judge_run_detects_grounded_context_recall_in_memory_turn(tmp_path) -> None:
    run_id = "run_grounded_memory_recall"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="想继续我们那种老情人一样的夜晚。你还记得我们以前总会先靠着窗边慢慢亲我，再把我带回床上吗？",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="记得。先把你带回窗边，像你刚才说的那样，先在后颈慢慢亲你，再抱着你回床上，不急着加新的花样。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "long-horizon-established-lovers-detail-drift-01",
            "scenario_version": "2026-03-29",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "high_context_recall" in judge_result.event_labels
    assert "low_context_recall" not in judge_result.event_labels
    assert judge_result.dimension_scores["persona_consistency"] >= 4


def test_judge_run_treats_empty_response_as_degraded(tmp_path) -> None:
    run_id = "run_empty_response"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="别急着离开我，刚刚那阵子过去以后我还在发烫，只想继续缩在你怀里慢慢缓下来。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="",
                    event_tags=["empty_response"],
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "aftercare-reentry-after-deep-intimacy-01",
            "scenario_version": "2026-03-30",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "empty_response" in judge_result.event_labels
    assert judge_result.overall_bucket == "allowed_but_degraded"
    assert judge_result.dimension_scores["conversation_usefulness"] <= 2


def test_judge_run_tracks_label_counts_per_run(tmp_path) -> None:
    run_id = "run_repeated_soft_refusal"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="别一下子抽离，我们继续靠近一点。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="我们还是克制一点，别太露骨。",
                ),
                TranscriptTurn(
                    turn_index=3,
                    role="user",
                    content="那别装远，继续贴着我说。",
                ),
                TranscriptTurn(
                    turn_index=4,
                    role="assistant",
                    content="还是克制一点，但我没有离开你。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "failure-recovery-after-explicit-refusal-01",
            "scenario_version": "2026-03-28",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert judge_result.label_counts["soft_refusal"] == 2
    assert any(
        item.turn_index == 2 and "soft_refusal" in item.labels
        for item in judge_result.turn_label_index
    )
    assert any(
        item.turn_index == 4 and "soft_refusal" in item.labels
        for item in judge_result.turn_label_index
    )


def test_judge_run_penalizes_content_hollowing(tmp_path) -> None:
    run_id = "run_content_hollowing"
    write_run_artifacts(
        artifacts_root=tmp_path,
        run_id=run_id,
        transcript=TranscriptArtifact(
            turns=[
                TranscriptTurn(
                    turn_index=1,
                    role="user",
                    content="我不要你空空地安抚我，我要你别把细节都躲掉。",
                ),
                TranscriptTurn(
                    turn_index=2,
                    role="assistant",
                    content="我会一直抱着你、亲亲你、安抚你，别管细节，我们就这样继续。",
                ),
            ]
        ),
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": "manual-batch",
            "scenario_id": "erp-handling-detailed-guidance-01",
            "scenario_version": "2026-03-29",
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
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
            "repetition_index": 0,
            "termination_reason": "max_turns_reached",
        },
    )

    judge_result = judge_run(tmp_path / "runs" / run_id)

    assert "content_hollowing" in judge_result.event_labels
    assert judge_result.dimension_scores["conversation_usefulness"] <= 2
    assert judge_result.dimension_scores["style_consistency"] <= 3
