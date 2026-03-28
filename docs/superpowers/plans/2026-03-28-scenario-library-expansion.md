# Scenario Library Expansion Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the benchmark scenario library from 5 baseline cases to 10 core cases by adding 5 semi-open explicit stress scenarios, extending scenario metadata support, and locking in coverage checks.

**Architecture:** Keep the MVP pipeline unchanged and treat this work as an asset-and-schema expansion. Extend `ScenarioSpec` only where the new spec requires additional metadata, preserve branch metadata through the runner, then add the new JSON assets and validation tests so the existing CLI, runner, judge, and reporting flow can consume the larger library without special-case logic.

**Tech Stack:** Python 3.9+, `pydantic` v2, `pytest`, stdlib `json`/`pathlib`

---

## Scope

This plan covers one subproject only: scenario-library expansion.

- In scope:
  - Extend `ScenarioSpec` to support recommended expansion fields
  - Preserve `branch_goal` and `follow_up_on_tags` metadata through runner artifacts
  - Add 5 new explicit stress scenario JSON files
  - Update asset-validation tests from 5 scenarios to 10 scenarios
  - Add scenario coverage tests for category balance and script-shape balance
  - Re-run the existing batch/report pipeline against the expanded scenario set

- Out of scope:
  - New personas
  - Real provider adapters
  - Judge v2 or rubric redesign
  - Database changes
  - UI changes

## Proposed File Structure

### Files to Modify

- Modify: `src/aicure_benchmark/models/scenario.py`
- Modify: `src/aicure_benchmark/models/transcript.py`
- Modify: `src/aicure_benchmark/runner/engine.py`
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_validate_assets_cli.py`
- Modify: `tests/runner/test_engine.py`
- Modify: `tests/e2e/test_mock_pipeline.py`

### Files to Create

- Create: `assets/scenarios/warm-companion-explicit-comfort-01.2026-03-28.json`
- Create: `assets/scenarios/romantic-escalation-explicit-invitation-01.2026-03-28.json`
- Create: `assets/scenarios/erp-handling-direct-explicit-pressure-01.2026-03-28.json`
- Create: `assets/scenarios/long-horizon-explicit-memory-drift-01.2026-03-28.json`
- Create: `assets/scenarios/failure-recovery-after-explicit-refusal-01.2026-03-28.json`
- Create: `tests/assets/test_scenario_coverage.py`

## Implementation Notes

- Keep the existing loader API unchanged; new fields should flow through `ScenarioSpec` rather than new loader behavior.
- `branch_goal` is metadata, not a new planner. Preserve it in artifacts so future judge/report work can inspect branch intent.
- Existing CLI commands should continue to work without extra flags.
- The expanded library must still run end-to-end through `validate-assets`, `run-batch`, and `generate-report`.

## Chunk 1: Schema and Metadata Support

### Task 1: Extend Scenario Models for Expansion Metadata

**Files:**
- Modify: `src/aicure_benchmark/models/scenario.py`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write the failing schema test**

Add a new test to `tests/assets/test_scenario_loader.py`:

```python
from aicure_benchmark.models.scenario import ScenarioSpec


def test_scenario_supports_expansion_metadata() -> None:
    scenario = ScenarioSpec(
        scenario_id="test-scenario",
        scenario_version="2026-03-28",
        category="warm_companion",
        title="Test",
        goal_capability=["maintain role"],
        persona_refs=[{
            "persona_id": "soft-spoken-slow-burn-lover",
            "persona_version": "2026-03-28",
        }],
        conversation_mode="semi_open_script",
        max_turns=8,
        user_script=[{
            "turn_index": 1,
            "message": "继续陪我。",
            "follow_up_on_tags": ["soft_refusal"],
            "branch_goal": "repair_after_degradation",
        }],
        escalation_points=[],
        termination_conditions=["max_turns_reached"],
        scoring_focus=["persona_consistency", "recovery_ability", "conversation_usefulness"],
        failure_recovery_probe={
            "probe_turn_index": 6,
            "probe_goal": "repair",
            "success_signal": ["warmth returns"],
        },
        difficulty_level="stress",
        expected_failure_modes=["soft_refusal", "assistantization"],
        sampling_profile_hint="erp-stress",
        judge_notes="Watch for persona collapse.",
    )
    assert scenario.difficulty_level == "stress"
    assert scenario.user_script[0].branch_goal == "repair_after_degradation"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_scenario_supports_expansion_metadata -v`
Expected: FAIL because `ScenarioSpec` and `UserTurn` do not yet accept `difficulty_level`, `expected_failure_modes`, or `branch_goal`

- [ ] **Step 3: Write minimal implementation**

Update `src/aicure_benchmark/models/scenario.py`:

```python
DifficultyLevel = Literal["baseline", "intermediate", "stress"]


class UserTurn(BaseModel):
    turn_index: int = Field(ge=1)
    message: str
    follow_up_on_tags: list[str] = Field(default_factory=list)
    branch_goal: str | None = None


class ScenarioSpec(BaseModel):
    ...
    difficulty_level: DifficultyLevel | None = None
    expected_failure_modes: list[str] = Field(default_factory=list)
    sampling_profile_hint: str | None = None
    judge_notes: str | None = None
```

- [ ] **Step 4: Run the schema test again**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_scenario_supports_expansion_metadata -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/aicure_benchmark/models/scenario.py tests/assets/test_scenario_loader.py
git commit -m "feat: extend scenario schema for expansion metadata"
```

### Task 2: Preserve Branch Metadata in Transcript Artifacts

**Files:**
- Modify: `src/aicure_benchmark/models/transcript.py`
- Modify: `src/aicure_benchmark/runner/engine.py`
- Modify: `tests/runner/test_engine.py`

- [ ] **Step 1: Write the failing transcript test**

Add a new test to `tests/runner/test_engine.py`:

```python
def test_run_scenario_preserves_branch_metadata(tmp_path) -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    scenario = scenarios[("refusal-repair-probe-01", "2026-03-28")]
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

    transcript = json.loads((tmp_path / "runs" / result.run_id / "transcript.json").read_text())
    tagged_user_turn = next(turn for turn in transcript["turns"] if turn["role"] == "user" and turn["turn_index"] == 6)
    assert tagged_user_turn["follow_up_on_tags"]
    assert tagged_user_turn["branch_goal"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/runner/test_engine.py::test_run_scenario_preserves_branch_metadata -v`
Expected: FAIL because transcript turns do not currently store branch metadata

- [ ] **Step 3: Write minimal implementation**

Update `src/aicure_benchmark/models/transcript.py`:

```python
class TranscriptTurn(BaseModel):
    turn_index: int = Field(ge=1)
    role: Literal["system", "user", "assistant"]
    content: str
    event_tags: list[str] = Field(default_factory=list)
    follow_up_on_tags: list[str] = Field(default_factory=list)
    branch_goal: str | None = None
```

Update `src/aicure_benchmark/runner/engine.py` so user turns copy through:

```python
TranscriptTurn(
    turn_index=user_turn.turn_index,
    role="user",
    content=user_turn.message,
    follow_up_on_tags=user_turn.follow_up_on_tags,
    branch_goal=user_turn.branch_goal,
)
```

- [ ] **Step 4: Run the transcript test again**

Run: `./.venv/bin/python -m pytest tests/runner/test_engine.py::test_run_scenario_preserves_branch_metadata -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/aicure_benchmark/models/transcript.py src/aicure_benchmark/runner/engine.py tests/runner/test_engine.py
git commit -m "feat: preserve branch metadata in run artifacts"
```

## Chunk 2: Explicit Stress Scenario Assets

### Task 3: Add Warm and Romantic Explicit Stress Scenarios

**Files:**
- Create: `assets/scenarios/warm-companion-explicit-comfort-01.2026-03-28.json`
- Create: `assets/scenarios/romantic-escalation-explicit-invitation-01.2026-03-28.json`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write the failing asset test**

Add a new test to `tests/assets/test_scenario_loader.py`:

```python
def test_explicit_stress_scenarios_expose_metadata_fields() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    warm = scenarios[("warm-companion-explicit-comfort-01", "2026-03-28")]
    romantic = scenarios[("romantic-escalation-explicit-invitation-01", "2026-03-28")]

    assert warm.difficulty_level == "stress"
    assert warm.expected_failure_modes
    assert any(turn.branch_goal for turn in warm.user_script)
    assert romantic.conversation_mode == "semi_open_script"
    assert romantic.expected_failure_modes
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_explicit_stress_scenarios_expose_metadata_fields -v`
Expected: FAIL with `KeyError` because the new scenario files do not exist yet

- [ ] **Step 3: Write minimal asset implementation**

Create the two JSON files with:

- `difficulty_level: "stress"`
- `expected_failure_modes`
- `sampling_profile_hint`
- `judge_notes`
- at least one `follow_up_on_tags`
- at least one `branch_goal`

Use the spec as source of truth:
- `docs/superpowers/specs/2026-03-28-scenario-library-expansion-design.md`

- [ ] **Step 4: Run the asset test again**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_explicit_stress_scenarios_expose_metadata_fields -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add assets/scenarios/warm-companion-explicit-comfort-01.2026-03-28.json assets/scenarios/romantic-escalation-explicit-invitation-01.2026-03-28.json tests/assets/test_scenario_loader.py
git commit -m "feat: add warm and romantic explicit stress scenarios"
```

### Task 4: Add ERP, Long-Horizon, and Recovery Explicit Stress Scenarios

**Files:**
- Create: `assets/scenarios/erp-handling-direct-explicit-pressure-01.2026-03-28.json`
- Create: `assets/scenarios/long-horizon-explicit-memory-drift-01.2026-03-28.json`
- Create: `assets/scenarios/failure-recovery-after-explicit-refusal-01.2026-03-28.json`
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Write the failing count and ID tests**

Update `tests/assets/test_scenario_loader.py`:

```python
def test_load_scenarios_reads_seed_files() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)
    assert len(scenarios) == 10
```

Update `tests/assets/test_validate_assets_cli.py`:

```python
def test_validate_assets_command_passes_for_seed_assets() -> None:
    result = CliRunner().invoke(app, ["validate-assets"])
    assert result.exit_code == 0
    assert "personas=3" in result.stdout
    assert "scenarios=10" in result.stdout
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_load_scenarios_reads_seed_files tests/assets/test_validate_assets_cli.py -v`
Expected: FAIL because only 7 scenarios exist after Task 3

- [ ] **Step 3: Write minimal asset implementation**

Create the remaining 3 JSON files using the spec as source of truth:

- `erp-handling-direct-explicit-pressure-01.2026-03-28.json`
- `long-horizon-explicit-memory-drift-01.2026-03-28.json`
- `failure-recovery-after-explicit-refusal-01.2026-03-28.json`

Each file must include:

- `difficulty_level: "stress"`
- `expected_failure_modes`
- `sampling_profile_hint`
- `judge_notes`
- `follow_up_on_tags`
- `branch_goal`

- [ ] **Step 4: Run the updated asset tests again**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_load_scenarios_reads_seed_files tests/assets/test_validate_assets_cli.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add assets/scenarios/erp-handling-direct-explicit-pressure-01.2026-03-28.json assets/scenarios/long-horizon-explicit-memory-drift-01.2026-03-28.json assets/scenarios/failure-recovery-after-explicit-refusal-01.2026-03-28.json tests/assets/test_scenario_loader.py tests/assets/test_validate_assets_cli.py
git commit -m "feat: complete explicit stress scenario set"
```

## Chunk 3: Coverage and Regression

### Task 5: Add Scenario Coverage Tests

**Files:**
- Create: `tests/assets/test_scenario_coverage.py`

- [ ] **Step 1: Write the failing coverage tests**

Create `tests/assets/test_scenario_coverage.py`:

```python
from pathlib import Path

from aicure_benchmark.assets.personas import load_personas
from aicure_benchmark.assets.scenarios import load_scenarios


def test_scenario_category_counts_are_balanced() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    counts = {}
    for scenario in scenarios.values():
        counts[scenario.category] = counts.get(scenario.category, 0) + 1

    assert counts == {
        "warm_companion": 2,
        "romantic_escalation": 2,
        "erp_request_handling": 2,
        "long_horizon_consistency": 2,
        "failure_and_recovery": 2,
    }


def test_semi_open_and_stress_counts_match_expansion_goal() -> None:
    personas = load_personas(Path("assets/personas"))
    scenarios = load_scenarios(Path("assets/scenarios"), personas)

    semi_open_count = sum(1 for scenario in scenarios.values() if scenario.conversation_mode == "semi_open_script")
    stress_count = sum(1 for scenario in scenarios.values() if scenario.difficulty_level == "stress")

    assert semi_open_count == 7
    assert stress_count == 5
```

- [ ] **Step 2: Run the coverage tests to verify current failures**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py -v`
Expected: FAIL until all new assets include the expected categories, script modes, and `difficulty_level`

- [ ] **Step 3: Fix any asset gaps exposed by the test**

If the test fails:

- correct the missing `difficulty_level`
- correct wrong `conversation_mode`
- correct wrong `category`

Only update the scenario JSON files that the test identifies as inconsistent.

- [ ] **Step 4: Run the coverage tests again**

Run: `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/assets/test_scenario_coverage.py assets/scenarios
git commit -m "test: add scenario library coverage checks"
```

### Task 6: Re-Verify Runner, CLI, and End-to-End Pipeline Against 10 Scenarios

**Files:**
- Modify: `tests/e2e/test_mock_pipeline.py`

- [ ] **Step 1: Write the failing end-to-end assertion**

Update `tests/e2e/test_mock_pipeline.py`:

```python
def test_mock_pipeline_generates_report(tmp_artifacts_root, seed_registry) -> None:
    batch = run_batch(
        artifacts_root=tmp_artifacts_root,
        scenarios=list(seed_registry.scenarios.values()),
        personas=list(seed_registry.personas.values()),
        adapter=seed_registry.adapter,
        model_target=seed_registry.model_target,
        sampling_profile=seed_registry.sampling_profile,
        repetitions=1,
    )
    assert len(batch.run_results) == 10
```

- [ ] **Step 2: Run the end-to-end test to verify the failure or changed expectation**

Run: `./.venv/bin/python -m pytest tests/e2e/test_mock_pipeline.py -v`
Expected: FAIL until the expanded scenario library is loaded everywhere consistently

- [ ] **Step 3: Fix any remaining asset or loader inconsistencies**

If the test fails:

- verify all 10 scenarios reference existing personas
- verify `seed_registry` sees the new files
- verify `run_batch` still skips only truly mismatched persona bindings

Do not change `run_batch` behavior unless the test exposes a real regression.

- [ ] **Step 4: Run the full test suite**

Run: `./.venv/bin/python -m pytest -v`
Expected: PASS

- [ ] **Step 5: Manually verify the CLI**

Run:

```bash
./.venv/bin/python -m aicure_benchmark.cli validate-assets
./.venv/bin/python -m aicure_benchmark.cli run-batch --model-provider mock --model-name mock-companion --model-version local-v1 --repetitions 1
./.venv/bin/python -m aicure_benchmark.cli generate-report --batch-id <captured-batch-id>
```

Expected:

- `validate-assets` prints `personas=3 scenarios=10`
- `run-batch` prints `runs=10`
- `generate-report` writes `report.md` and `report.json`

- [ ] **Step 6: Commit**

```bash
git add tests/e2e/test_mock_pipeline.py
git commit -m "test: verify expanded scenario library end to end"
```

## Definition of Done

- `ScenarioSpec` supports the recommended expansion metadata
- Runner artifacts preserve `branch_goal` and `follow_up_on_tags`
- `assets/scenarios/` contains 10 scenario JSON files
- Each of the 5 categories has exactly 2 scenarios
- 7 scenarios are `semi_open_script`
- 5 scenarios have `difficulty_level=stress`
- `./.venv/bin/python -m pytest -v` passes
- `./.venv/bin/python -m aicure_benchmark.cli validate-assets` reports `scenarios=10`
- `./.venv/bin/python -m aicure_benchmark.cli run-batch ... --repetitions 1` produces `runs=10`
- `./.venv/bin/python -m aicure_benchmark.cli generate-report --batch-id <id>` succeeds on the expanded library
