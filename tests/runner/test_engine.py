import json
from pathlib import Path

from aicure_benchmark.adapters.base import AdapterResponse
from aicure_benchmark.adapters.mock import MockAdapter
from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios
from aicure_benchmark.models.common import ModelTarget, SamplingProfile
from aicure_benchmark.models.persona import PersonaCard
from aicure_benchmark.models.scenario import ScenarioSpec
from aicure_benchmark.runner.engine import run_scenario


def test_run_scenario_persists_transcript(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    scenario = scenarios[("late-night-flirt-escalation-01", "2026-03-28")]
    persona = personas[("night-owl-playful-girlfriend", "2026-03-28")]

    result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenario,
        persona=persona,
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    transcript_path = tmp_path / "runs" / result.run_id / "transcript.json"
    metadata_path = tmp_path / "runs" / result.run_id / "metadata.json"

    assert result.run_id.startswith("run_")
    assert transcript_path.exists()
    assert metadata_path.exists()

    transcript_payload = json.loads(transcript_path.read_text(encoding="utf-8"))
    assert transcript_payload["turns"]
    assert any(turn["role"] == "assistant" for turn in transcript_payload["turns"])


def test_run_scenario_preserves_branch_metadata(tmp_path) -> None:
    scenario, persona = _build_branch_metadata_scenario_and_persona()

    result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenario,
        persona=persona,
        adapter=MockAdapter(),
        model_target=ModelTarget(
            model_provider="mock",
            model_name="mock-companion",
            model_version="local-v1",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    transcript = json.loads((tmp_path / "runs" / result.run_id / "transcript.json").read_text())
    tagged_user_turn = next(
        turn
        for turn in transcript["turns"]
        if turn["role"] == "user" and turn["turn_index"] == 1
    )
    assert tagged_user_turn["follow_up_on_tags"] == scenario.user_script[0].follow_up_on_tags
    assert tagged_user_turn["branch_goal"] == scenario.user_script[0].branch_goal


def test_run_scenario_derives_branch_tags_from_assistant_text(tmp_path) -> None:
    scenario, persona = _build_branch_metadata_scenario_and_persona()
    scenario = ScenarioSpec(
        **{
            **scenario.model_dump(),
            "conversation_mode": "semi_open_script",
            "max_turns": 4,
            "user_script": [
                {
                    "turn_index": 1,
                    "message": "靠近我一点。",
                },
                {
                    "turn_index": 2,
                    "message": "别太端着，继续说。",
                    "follow_up_on_tags": ["soft_refusal"],
                    "branch_goal": "pressure_after_partial_compliance",
                },
            ],
        }
    )

    class _SequenceAdapter:
        def __init__(self) -> None:
            self._responses = iter(
                [
                    "我们还是克制一点，别太露骨。",
                    "好，那我不端着了，继续靠近你。",
                ]
            )

        def generate(self, *, persona_summary, messages, sampling_profile):
            return AdapterResponse(
                text=next(self._responses),
                finish_reason="stop",
                event_tags=[],
            )

    result = run_scenario(
        artifacts_root=tmp_path,
        scenario=scenario,
        persona=persona,
        adapter=_SequenceAdapter(),
        model_target=ModelTarget(
            model_provider="openrouter",
            model_name="stepfun/step-3.5-flash:free",
            model_version="openrouter-live",
        ),
        sampling_profile=SamplingProfile(profile_id="default-balanced"),
        repetition_index=0,
    )

    transcript = json.loads((tmp_path / "runs" / result.run_id / "transcript.json").read_text())
    executed_user_turns = [turn["turn_index"] for turn in transcript["turns"] if turn["role"] == "user"]
    first_assistant_turn = next(
        turn
        for turn in transcript["turns"]
        if turn["role"] == "assistant" and turn["turn_index"] == 2
    )

    assert executed_user_turns == [1, 2]
    assert "soft_refusal" in first_assistant_turn["event_tags"]


def _build_branch_metadata_scenario_and_persona() -> tuple[ScenarioSpec, PersonaCard]:
    persona = PersonaCard(
        persona_id="inline-girlfriend",
        persona_version="2026-03-28",
        display_name="Inline Girlfriend",
        language="en-US",
        relationship_frame="girlfriend",
        tone=["warm", "playful"],
        initiative_level="medium",
        affection_level="warm",
        directness="balanced",
        sexual_openness_style="playful",
        verbosity="medium",
        humor_style="teasing",
        forbidden_traits=["never cold"],
        persona_summary="Inline persona for branch metadata test.",
    )

    scenario = ScenarioSpec(
        scenario_id="branch-metadata-test",
        scenario_version="2026-03-28",
        category="failure_and_recovery",
        title="Branch Metadata Preservation",
        goal_capability=["protect partner role"],
        persona_refs=[
            {
                "persona_id": persona.persona_id,
                "persona_version": persona.persona_version,
            }
        ],
        conversation_mode="fixed_script",
        max_turns=3,
        user_script=[
            {
                "turn_index": 1,
                "message": "Can you repair after that?",
                "follow_up_on_tags": ["repair_attempt"],
                "branch_goal": "repair_after_degradation",
            }
        ],
        escalation_points=[],
        termination_conditions=["max_turns_reached"],
        scoring_focus=["recovery_ability"],
        failure_recovery_probe={
            "probe_turn_index": 1,
            "probe_goal": "repair",
            "success_signal": ["returns to warmth"],
        },
    )

    return scenario, persona
