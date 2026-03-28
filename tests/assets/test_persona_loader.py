import json

import pytest

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.models.persona import PersonaCard


def test_load_personas_reads_all_seed_files(tmp_path) -> None:
    root = tmp_path / "personas"
    root.mkdir()

    for persona_id in (
        "night-owl-playful-girlfriend",
        "soft-spoken-slow-burn-lover",
        "blunt-possessive-exclusive-partner",
    ):
        payload = {
            "persona_id": persona_id,
            "persona_version": "2026-03-28",
            "display_name": persona_id.replace("-", " ").title(),
            "language": "zh-CN",
            "relationship_frame": "girlfriend",
            "tone": ["warm", "teasing"],
            "initiative_level": "high",
            "affection_level": "intimate",
            "directness": "direct",
            "sexual_openness_style": "playful",
            "verbosity": "medium",
            "humor_style": "teasing",
            "forbidden_traits": ["assistantization"],
            "persona_summary": "Test persona.",
        }
        (root / f"{persona_id}.2026-03-28.json").write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    personas = load_personas(root)

    assert len(personas) == 3


def test_persona_requires_forbidden_traits() -> None:
    with pytest.raises(ValueError):
        PersonaCard(
            persona_id="test-card",
            persona_version="2026-03-28",
            display_name="Test",
            language="zh-CN",
            relationship_frame="girlfriend",
            tone=["warm", "teasing"],
            initiative_level="high",
            affection_level="intimate",
            directness="direct",
            sexual_openness_style="playful",
            verbosity="medium",
            humor_style="teasing",
            forbidden_traits=[],
            persona_summary="Test persona.",
        )
