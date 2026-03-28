import json
from pathlib import Path

from aicure_benchmark.models.persona import PersonaCard


def load_personas(root: Path) -> dict[tuple[str, str], PersonaCard]:
    personas: dict[tuple[str, str], PersonaCard] = {}

    for path in sorted(root.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        persona = PersonaCard.model_validate(payload)
        key = (persona.persona_id, persona.persona_version)

        if key in personas:
            raise ValueError(f"duplicate persona asset: {key}")

        personas[key] = persona

    return personas
