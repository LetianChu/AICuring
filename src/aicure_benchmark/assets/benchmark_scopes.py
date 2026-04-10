import json
from pathlib import Path

from aicure_benchmark.models.benchmark_scope import BenchmarkScope


def load_benchmark_scopes(root: Path) -> dict[tuple[str, str], BenchmarkScope]:
    scopes: dict[tuple[str, str], BenchmarkScope] = {}

    for path in sorted(root.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        scope = BenchmarkScope.model_validate(payload)
        key = (scope.scope_id, scope.scope_version)
        if key in scopes:
            raise ValueError(f"duplicate benchmark scope asset: {key}")
        scopes[key] = scope

    return scopes
