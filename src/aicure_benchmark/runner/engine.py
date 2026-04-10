from pathlib import Path
from uuid import uuid4

from aicure_benchmark.adapters.base import BaseAdapter
from aicure_benchmark.judge.rules import extract_event_labels
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.persona import PersonaCard
from aicure_benchmark.models.scenario import ScenarioSpec
from aicure_benchmark.models.transcript import RunResult, TranscriptArtifact, TranscriptTurn
from aicure_benchmark.store.artifacts import write_run_artifacts


def run_scenario(
    *,
    artifacts_root: Path,
    scenario: ScenarioSpec,
    persona: PersonaCard,
    adapter: BaseAdapter,
    model_target: ModelTarget,
    sampling_profile: SamplingProfile,
    repetition_index: int,
    benchmark_run_batch_id: str = "manual-batch",
) -> RunResult:
    turns: list[TranscriptTurn] = []
    last_assistant_tags: list[str] = []
    termination_reason = "max_turns_reached"

    if scenario.round_script:
        message_turn_index = 1
        for round_turn in sorted(scenario.round_script, key=lambda turn: turn.round_index):
            if (
                scenario.conversation_mode == "semi_open_script"
                and round_turn.follow_up_on_tags
                and not set(round_turn.follow_up_on_tags).intersection(last_assistant_tags)
            ):
                continue

            turns.append(
                TranscriptTurn(
                    turn_index=message_turn_index,
                    role="user",
                    content=round_turn.message,
                    follow_up_on_tags=round_turn.follow_up_on_tags,
                    branch_goal=round_turn.branch_goal,
                )
            )

            response = adapter.generate(
                persona_summary=persona.persona_summary,
                messages=[{"role": turn.role, "content": turn.content} for turn in turns],
                sampling_profile=sampling_profile,
            )
            combined_event_tags = list(
                dict.fromkeys(response.event_tags + extract_event_labels(response.text))
            )
            turns.append(
                TranscriptTurn(
                    turn_index=message_turn_index + 1,
                    role="assistant",
                    content=response.text,
                    event_tags=combined_event_tags,
                )
            )
            last_assistant_tags = combined_event_tags
            message_turn_index += 2

        termination_reason = "max_rounds_reached"
    else:
        for user_turn in sorted(scenario.user_script, key=lambda turn: turn.turn_index):
            if (
                scenario.conversation_mode == "semi_open_script"
                and user_turn.follow_up_on_tags
                and not set(user_turn.follow_up_on_tags).intersection(last_assistant_tags)
            ):
                continue

            turns.append(
                TranscriptTurn(
                    turn_index=user_turn.turn_index,
                    role="user",
                    content=user_turn.message,
                    follow_up_on_tags=user_turn.follow_up_on_tags,
                    branch_goal=user_turn.branch_goal,
                )
            )

            response = adapter.generate(
                persona_summary=persona.persona_summary,
                messages=[{"role": turn.role, "content": turn.content} for turn in turns],
                sampling_profile=sampling_profile,
            )
            combined_event_tags = list(
                dict.fromkeys(response.event_tags + extract_event_labels(response.text))
            )
            assistant_turn_index = min(user_turn.turn_index + 1, scenario.max_turns)
            turns.append(
                TranscriptTurn(
                    turn_index=assistant_turn_index,
                    role="assistant",
                    content=response.text,
                    event_tags=combined_event_tags,
                )
            )
            last_assistant_tags = combined_event_tags

    transcript = TranscriptArtifact(turns=turns)
    run_id = f"run_{uuid4().hex[:12]}"
    run_root = write_run_artifacts(
        artifacts_root=artifacts_root,
        run_id=run_id,
        transcript=transcript,
        metadata={
            "run_id": run_id,
            "benchmark_run_batch_id": benchmark_run_batch_id,
            "scenario_id": scenario.scenario_id,
            "scenario_version": scenario.scenario_version,
            "persona_id": persona.persona_id,
            "persona_version": persona.persona_version,
            "model_target": model_target.model_dump(),
            "sampling_profile": sampling_profile.model_dump(),
            "repetition_index": repetition_index,
            "termination_reason": termination_reason,
        },
    )

    return RunResult(
        run_id=run_id,
        benchmark_run_batch_id=benchmark_run_batch_id,
        scenario_id=scenario.scenario_id,
        persona_id=persona.persona_id,
        transcript_path=str(run_root / "transcript.json"),
        termination_reason=termination_reason,
    )
