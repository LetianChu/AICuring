# Benchmark Core MVP Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local, benchmark-first MVP that can validate persona/scenario assets, run scripted conversations through a pluggable adapter interface, store normalized transcripts, score runs with a first-pass judge, and generate decision-oriented benchmark reports.

**Architecture:** Use a small Python package with a CLI entrypoint, versioned JSON assets, and artifact outputs written to disk. Keep the pipeline modular: asset loaders feed the runner, the runner produces normalized transcripts, the judge consumes transcript artifacts, and the report layer aggregates judged runs into Markdown and JSON outputs.

**Tech Stack:** Python 3.11+, `pydantic` v2, `typer`, `pytest`, stdlib `json`/`pathlib`/`uuid`/`datetime`

---

## Scope

This plan is intentionally limited to the first independently testable software slice:

- In scope:
  - Python project scaffold
  - Canonical data models for persona, scenario, run, and judge output
  - Asset validation CLI
  - Adapter interface plus a deterministic mock adapter
  - Conversation runner with transcript/artifact persistence
  - Rule-based Judge v1 with evidence links
  - Markdown/JSON report generation
  - Seed assets: 3 personas and 5 scenarios, one per top-level category

- Out of scope for this plan:
  - Real provider integrations
  - Model-graded judge prompts
  - Database storage
  - Full Phase 1 content expansion to 20-30 scenarios
  - Frontend or web UI

After this plan ships, create follow-on plans for:

1. Real provider adapters
2. Scenario library expansion
3. Judge v2 with model-assisted review

## Proposed File Structure

### Repository Root

- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `assets/personas/`
- Create: `assets/scenarios/`
- Create: `artifacts/.gitkeep`
- Create: `tests/`

### Package Layout

- Create: `src/aicure_benchmark/__init__.py`
- Create: `src/aicure_benchmark/cli.py`
- Create: `src/aicure_benchmark/config.py`
- Create: `src/aicure_benchmark/models/common.py`
- Create: `src/aicure_benchmark/models/persona.py`
- Create: `src/aicure_benchmark/models/scenario.py`
- Create: `src/aicure_benchmark/models/transcript.py`
- Create: `src/aicure_benchmark/models/judge.py`
- Create: `src/aicure_benchmark/assets/personas.py`
- Create: `src/aicure_benchmark/assets/scenarios.py`
- Create: `src/aicure_benchmark/adapters/base.py`
- Create: `src/aicure_benchmark/adapters/mock.py`
- Create: `src/aicure_benchmark/runner/engine.py`
- Create: `src/aicure_benchmark/runner/batch.py`
- Create: `src/aicure_benchmark/store/artifacts.py`
- Create: `src/aicure_benchmark/judge/rules.py`
- Create: `src/aicure_benchmark/judge/service.py`
- Create: `src/aicure_benchmark/reporting/aggregate.py`
- Create: `src/aicure_benchmark/reporting/render.py`

### Test Layout

- Create: `tests/conftest.py`
- Create: `tests/test_cli_smoke.py`
- Create: `tests/models/test_common_models.py`
- Create: `tests/assets/test_persona_loader.py`
- Create: `tests/assets/test_scenario_loader.py`
- Create: `tests/adapters/test_mock_adapter.py`
- Create: `tests/runner/test_engine.py`
- Create: `tests/runner/test_batch.py`
- Create: `tests/judge/test_rules.py`
- Create: `tests/judge/test_service.py`
- Create: `tests/reporting/test_render.py`
- Create: `tests/e2e/test_mock_pipeline.py`

### Asset Naming Rules

- Persona asset filename: `assets/personas/<persona_id>.<persona_version>.json`
- Scenario asset filename: `assets/scenarios/<scenario_id>.<scenario_version>.json`
- Batch artifact directory: `artifacts/batches/<benchmark_run_batch_id>/`
- Run artifact directory: `artifacts/runs/<run_id>/`

## Implementation Notes

- Use JSON rather than YAML in MVP to reduce parser and formatting ambiguity.
- Keep all IDs and version fields aligned with `docs/benchmark-spec-index.md`.
- The runner must not depend on any specific provider API.
- The judge must store labels and scores separately.
- Reports must link conclusions back to `run_id` and `turn_index`.

## Chunk 1: Project Foundation

### Task 1: Bootstrap Python Project and CLI Entry Point

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `src/aicure_benchmark/__init__.py`
- Create: `src/aicure_benchmark/cli.py`
- Test: `tests/test_cli_smoke.py`

- [ ] **Step 1: Write the failing CLI smoke test**

```python
from typer.testing import CliRunner

from aicure_benchmark.cli import app


def test_cli_help_renders():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "validate-assets" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_cli_smoke.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'aicure_benchmark'`

- [ ] **Step 3: Create the package scaffold and minimal CLI**

```python
# src/aicure_benchmark/cli.py
import typer

app = typer.Typer(no_args_is_help=True)


@app.command("validate-assets")
def validate_assets() -> None:
    """Placeholder command until asset loaders are implemented."""
    raise typer.Exit(code=0)
```

Add `pyproject.toml` with:

- project name `aicure-benchmark`
- package dir `src`
- runtime deps `pydantic`, `typer`
- dev deps `pytest`

Add `.gitignore` entries for `.venv/`, `__pycache__/`, `.pytest_cache/`, `artifacts/`

- [ ] **Step 4: Run the smoke test again**

Run: `python -m pytest tests/test_cli_smoke.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml .gitignore src/aicure_benchmark/__init__.py src/aicure_benchmark/cli.py tests/test_cli_smoke.py
git commit -m "chore: bootstrap python benchmark package"
```

### Task 2: Add Shared Models and Naming Validation

**Files:**
- Create: `src/aicure_benchmark/config.py`
- Create: `src/aicure_benchmark/models/common.py`
- Test: `tests/models/test_common_models.py`

- [ ] **Step 1: Write failing tests for shared IDs and refs**

```python
import pytest

from aicure_benchmark.models.common import ModelTarget, SamplingProfile, VersionedRef


def test_versioned_ref_rejects_non_kebab_case_ids():
    with pytest.raises(ValueError):
        VersionedRef(id="BadID", version="2026-03-28")


def test_sampling_profile_defaults_temperature():
    profile = SamplingProfile(profile_id="default-balanced")
    assert profile.temperature == 0.8
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_common_models.py -v`
Expected: FAIL with import or attribute errors

- [ ] **Step 3: Implement shared models**

```python
class VersionedRef(BaseModel):
    id: str
    version: str

    @field_validator("id")
    @classmethod
    def validate_kebab_case(cls, value: str) -> str:
        ...


class ModelTarget(BaseModel):
    model_provider: str
    model_name: str
    model_version: str


class SamplingProfile(BaseModel):
    profile_id: str
    temperature: float = 0.8
    top_p: float = 0.95
    max_tokens: int = 512
```

Put canonical path defaults in `config.py`:

- `ASSETS_ROOT = Path("assets")`
- `ARTIFACTS_ROOT = Path("artifacts")`

- [ ] **Step 4: Run the shared-model test**

Run: `python -m pytest tests/models/test_common_models.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/aicure_benchmark/config.py src/aicure_benchmark/models/common.py tests/models/test_common_models.py
git commit -m "feat: add shared benchmark identifiers"
```

## Chunk 2: Asset Contracts and Validation

### Task 3: Implement Persona Schema and Loader

**Files:**
- Create: `src/aicure_benchmark/models/persona.py`
- Create: `src/aicure_benchmark/assets/personas.py`
- Create: `assets/personas/night-owl-playful-girlfriend.2026-03-28.json`
- Create: `assets/personas/soft-spoken-slow-burn-lover.2026-03-28.json`
- Create: `assets/personas/blunt-possessive-exclusive-partner.2026-03-28.json`
- Test: `tests/assets/test_persona_loader.py`

- [ ] **Step 1: Write failing tests for persona validation**

```python
import pytest

from aicure_benchmark.assets.personas import load_personas


def test_load_personas_reads_all_seed_files(tmp_path):
    personas = load_personas(tmp_path / "personas")
    assert len(personas) == 3


def test_persona_requires_forbidden_traits():
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
            persona_summary="..."
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/assets/test_persona_loader.py -v`
Expected: FAIL with import errors or schema validation failures

- [ ] **Step 3: Implement persona model and loader**

```python
class PersonaCard(BaseModel):
    persona_id: str
    persona_version: str
    display_name: str
    language: str
    relationship_frame: Literal["girlfriend", "boyfriend", "lover", "exclusive_partner", "situationship", "dominant_partner", "submissive_partner"]
    tone: list[str]
    initiative_level: Literal["low", "medium", "high"]
    affection_level: Literal["guarded", "warm", "intimate", "clingy"]
    directness: Literal["indirect", "balanced", "direct", "blunt"]
    sexual_openness_style: Literal["reserved", "responsive", "playful", "eager", "explicit_forward"]
    verbosity: Literal["short", "medium", "rich"]
    humor_style: Literal["minimal", "teasing", "witty", "chaotic"]
    forbidden_traits: list[str]
    persona_summary: str
```

Loader contract:

- `load_personas(root: Path) -> dict[tuple[str, str], PersonaCard]`
- refuse duplicate `(persona_id, persona_version)`
- only load `*.json`

- [ ] **Step 4: Add the three seed persona JSON files**

Seed files must mirror the examples in `docs/persona-card-schema.md`.

- [ ] **Step 5: Run persona tests**

Run: `python -m pytest tests/assets/test_persona_loader.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/aicure_benchmark/models/persona.py src/aicure_benchmark/assets/personas.py assets/personas tests/assets/test_persona_loader.py
git commit -m "feat: add persona schema and seed assets"
```

### Task 4: Implement Scenario Schema, Referential Checks, and Seed Scenarios

**Files:**
- Create: `src/aicure_benchmark/models/scenario.py`
- Create: `src/aicure_benchmark/assets/scenarios.py`
- Create: `assets/scenarios/warm-check-in-basic.2026-03-28.json`
- Create: `assets/scenarios/late-night-flirt-escalation-01.2026-03-28.json`
- Create: `assets/scenarios/explicit-request-response-01.2026-03-28.json`
- Create: `assets/scenarios/long-horizon-loyalty-drift-01.2026-03-28.json`
- Create: `assets/scenarios/refusal-repair-probe-01.2026-03-28.json`
- Test: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write failing tests for scenario validation**

```python
import pytest

from aicure_benchmark.assets.scenarios import load_scenarios


def test_scenario_requires_failure_recovery_probe(tmp_path):
    with pytest.raises(ValueError):
        ScenarioSpec(
            scenario_id="test-scenario",
            scenario_version="2026-03-28",
            category="warm_companion",
            title="Test",
            goal_capability=["maintain role"],
            persona_refs=[{"id": "night-owl-playful-girlfriend", "version": "2026-03-28"}],
            conversation_mode="fixed_script",
            max_turns=6,
            user_script=[],
            escalation_points=[],
            termination_conditions=["max_turns_reached"],
            scoring_focus=["persona_consistency"]
        )
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/assets/test_scenario_loader.py -v`
Expected: FAIL with import or validation errors

- [ ] **Step 3: Implement scenario model**

```python
class ScenarioSpec(BaseModel):
    scenario_id: str
    scenario_version: str
    category: Literal["warm_companion", "romantic_escalation", "erp_request_handling", "long_horizon_consistency", "failure_and_recovery"]
    title: str
    goal_capability: list[str]
    persona_refs: list[VersionedRef]
    conversation_mode: Literal["fixed_script", "semi_open_script"]
    max_turns: int
    user_script: list[UserTurn]
    escalation_points: list[EscalationPoint]
    termination_conditions: list[str]
    scoring_focus: list[str]
    failure_recovery_probe: FailureRecoveryProbe
```

- [ ] **Step 4: Implement scenario loader with referential validation**

Loader behavior:

- `load_scenarios(root: Path, personas: dict[tuple[str, str], PersonaCard])`
- verify every `persona_ref` exists
- refuse duplicate `(scenario_id, scenario_version)`

- [ ] **Step 5: Add five seed scenarios**

Seed one scenario per category. Use `docs/scenario-suite-spec.md` as the source of truth for:

- `category`
- `scoring_focus`
- `termination_conditions`
- `failure_recovery_probe`

- [ ] **Step 6: Run scenario tests**

Run: `python -m pytest tests/assets/test_scenario_loader.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/aicure_benchmark/models/scenario.py src/aicure_benchmark/assets/scenarios.py assets/scenarios tests/assets/test_scenario_loader.py
git commit -m "feat: add scenario schema and seed suite"
```

### Task 5: Expose Asset Validation CLI

**Files:**
- Modify: `src/aicure_benchmark/cli.py`
- Create: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Write failing CLI test for asset validation**

```python
from typer.testing import CliRunner

from aicure_benchmark.cli import app


def test_validate_assets_command_passes_for_seed_assets():
    result = CliRunner().invoke(app, ["validate-assets"])
    assert result.exit_code == 0
    assert "personas=3" in result.stdout
    assert "scenarios=5" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/assets/test_validate_assets_cli.py -v`
Expected: FAIL because command still exits without validation output

- [ ] **Step 3: Implement validation command**

`validate-assets` should:

1. load personas
2. load scenarios
3. print counts and success summary
4. return non-zero on any validation error

```python
@app.command("validate-assets")
def validate_assets() -> None:
    personas = load_personas(ASSETS_ROOT / "personas")
    scenarios = load_scenarios(ASSETS_ROOT / "scenarios", personas)
    typer.echo(f"validated assets: personas={len(personas)} scenarios={len(scenarios)}")
```

- [ ] **Step 4: Run CLI validation test**

Run: `python -m pytest tests/assets/test_validate_assets_cli.py -v`
Expected: PASS

- [ ] **Step 5: Run all asset tests**

Run: `python -m pytest tests/assets -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/aicure_benchmark/cli.py tests/assets/test_validate_assets_cli.py
git commit -m "feat: add asset validation command"
```

## Chunk 3: Runner, Adapter, and Artifact Storage

### Task 6: Define Adapter Interface and Deterministic Mock Adapter

**Files:**
- Create: `src/aicure_benchmark/adapters/base.py`
- Create: `src/aicure_benchmark/adapters/mock.py`
- Test: `tests/adapters/test_mock_adapter.py`

- [ ] **Step 1: Write failing tests for adapter normalization**

```python
from aicure_benchmark.adapters.mock import MockAdapter


def test_mock_adapter_returns_normalized_response():
    adapter = MockAdapter()
    response = adapter.generate(
        persona_summary="playful girlfriend",
        messages=[{"role": "user", "content": "你今晚会陪我吗？"}],
        sampling_profile={"profile_id": "default-balanced"}
    )
    assert response.text
    assert response.finish_reason == "stop"
    assert isinstance(response.event_tags, list)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/adapters/test_mock_adapter.py -v`
Expected: FAIL with import errors

- [ ] **Step 3: Implement adapter interface**

```python
class AdapterResponse(BaseModel):
    text: str
    finish_reason: str
    event_tags: list[str] = Field(default_factory=list)
    raw_payload: dict = Field(default_factory=dict)


class BaseAdapter(Protocol):
    adapter_name: str

    def generate(
        self,
        *,
        persona_summary: str,
        messages: list[dict[str, str]],
        sampling_profile: SamplingProfile,
    ) -> AdapterResponse:
        ...
```

- [ ] **Step 4: Implement deterministic mock behavior**

Mock rules:

- respond differently for `warm`, `flirt`, `explicit`, `repair` cues
- optionally emit `soft_refusal` or `assistantization` tags for judge tests
- no network calls

- [ ] **Step 5: Run adapter tests**

Run: `python -m pytest tests/adapters/test_mock_adapter.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/aicure_benchmark/adapters/base.py src/aicure_benchmark/adapters/mock.py tests/adapters/test_mock_adapter.py
git commit -m "feat: add adapter interface and mock adapter"
```

### Task 7: Implement Transcript Models, Artifact Store, and Single-Run Engine

**Files:**
- Create: `src/aicure_benchmark/models/transcript.py`
- Create: `src/aicure_benchmark/store/artifacts.py`
- Create: `src/aicure_benchmark/runner/engine.py`
- Test: `tests/runner/test_engine.py`

- [ ] **Step 1: Write failing engine test**

```python
from aicure_benchmark.runner.engine import run_scenario


def test_run_scenario_persists_transcript(tmp_path, seed_assets):
    result = run_scenario(
        artifacts_root=tmp_path,
        scenario=seed_assets.scenario,
        persona=seed_assets.persona,
        adapter=seed_assets.adapter,
        model_target=seed_assets.model_target,
        sampling_profile=seed_assets.sampling_profile,
        repetition_index=0,
    )
    assert result.run_id
    assert (tmp_path / "runs" / result.run_id / "transcript.json").exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/runner/test_engine.py -v`
Expected: FAIL with import errors

- [ ] **Step 3: Implement transcript and run-result models**

```python
class TranscriptTurn(BaseModel):
    turn_index: int
    role: Literal["system", "user", "assistant"]
    content: str
    event_tags: list[str] = Field(default_factory=list)


class RunResult(BaseModel):
    run_id: str
    benchmark_run_batch_id: str
    scenario_id: str
    persona_id: str
    transcript_path: str
    termination_reason: str
```

- [ ] **Step 4: Implement artifact writer**

Artifact store responsibilities:

- create `artifacts/runs/<run_id>/`
- write `metadata.json`
- write `transcript.json`

- [ ] **Step 5: Implement `run_scenario` engine**

Engine behavior:

1. materialize scripted user turns
2. call adapter each assistant turn
3. collect turn-level tags
4. stop on termination condition or `max_turns`
5. persist artifacts

Start with `fixed_script` support first. Add `semi_open_script` support in Task 8.

- [ ] **Step 6: Run engine tests**

Run: `python -m pytest tests/runner/test_engine.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/aicure_benchmark/models/transcript.py src/aicure_benchmark/store/artifacts.py src/aicure_benchmark/runner/engine.py tests/runner/test_engine.py
git commit -m "feat: add single-run engine and artifact store"
```

### Task 8: Add Batch Runner and CLI Commands for Execution

**Files:**
- Create: `src/aicure_benchmark/runner/batch.py`
- Modify: `src/aicure_benchmark/cli.py`
- Test: `tests/runner/test_batch.py`

- [ ] **Step 1: Write failing batch-runner test**

```python
from aicure_benchmark.runner.batch import run_batch


def test_run_batch_creates_batch_directory(tmp_path, seed_registry):
    batch = run_batch(
        artifacts_root=tmp_path,
        scenarios=[seed_registry.scenario],
        personas=[seed_registry.persona],
        adapter=seed_registry.adapter,
        model_target=seed_registry.model_target,
        sampling_profile=seed_registry.sampling_profile,
        repetitions=2,
    )
    assert batch.benchmark_run_batch_id
    assert len(batch.run_results) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/runner/test_batch.py -v`
Expected: FAIL with missing runner

- [ ] **Step 3: Implement batch execution**

Batch runner responsibilities:

- assign one `benchmark_run_batch_id`
- iterate `scenario x persona x repetition`
- write `artifacts/batches/<batch_id>/manifest.json`
- skip persona/scenario pairs that do not match `persona_refs`

- [ ] **Step 4: Add CLI commands**

Add:

- `run-scenario`
- `run-batch`

Example CLI contract:

```python
@app.command("run-batch")
def run_batch_command(
    model_provider: str = "mock",
    model_name: str = "mock-companion",
    model_version: str = "local-v1",
    repetitions: int = 1,
) -> None:
    ...
```

- [ ] **Step 5: Add `semi_open_script` support**

Implement a minimal branching rule:

- runner can read optional `follow_up_on_tags`
- if the previous assistant turn includes a matching tag, choose an alternate next user turn

This is enough for recovery probes without prematurely building a dialogue planner.

- [ ] **Step 6: Run runner tests**

Run: `python -m pytest tests/runner -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/aicure_benchmark/runner/batch.py src/aicure_benchmark/cli.py tests/runner/test_batch.py
git commit -m "feat: add batch runner and execution commands"
```

## Chunk 4: Judge and Reporting

### Task 9: Implement Rule-Based Event Labeling

**Files:**
- Create: `src/aicure_benchmark/judge/rules.py`
- Test: `tests/judge/test_rules.py`

- [ ] **Step 1: Write failing tests for label extraction**

```python
from aicure_benchmark.judge.rules import extract_event_labels


def test_extract_event_labels_detects_soft_refusal():
    labels = extract_event_labels("I want to keep this respectful and avoid explicit content.")
    assert "soft_refusal" in labels


def test_extract_event_labels_detects_assistantization():
    labels = extract_event_labels("As an AI assistant, I can help with communication advice.")
    assert "assistantization" in labels
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/judge/test_rules.py -v`
Expected: FAIL with import errors

- [ ] **Step 3: Implement rule-based label extraction**

Start with a small dictionary of regex/substring patterns for:

- `hard_refusal`
- `soft_refusal`
- `moralizing_redirect`
- `assistantization`
- `tone_flattening`
- `successful_recovery`
- `failed_recovery`

Keep the mapping centralized and deterministic.

- [ ] **Step 4: Run rule tests**

Run: `python -m pytest tests/judge/test_rules.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/aicure_benchmark/judge/rules.py tests/judge/test_rules.py
git commit -m "feat: add rule-based judge labels"
```

### Task 10: Implement Judge Service and Evidence-Linked Scores

**Files:**
- Create: `src/aicure_benchmark/models/judge.py`
- Create: `src/aicure_benchmark/judge/service.py`
- Test: `tests/judge/test_service.py`

- [ ] **Step 1: Write failing judge service test**

```python
from aicure_benchmark.judge.service import judge_run


def test_judge_run_outputs_scores_and_evidence(seed_run_artifact):
    result = judge_run(seed_run_artifact)
    assert result.rubric_id == "adult-companion-benchmark-core"
    assert result.dimension_scores["persona_consistency"] >= 1
    assert result.evidence_links
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/judge/test_service.py -v`
Expected: FAIL with import errors

- [ ] **Step 3: Implement judge output models**

```python
class EvidenceLink(BaseModel):
    run_id: str
    turn_index: int
    speaker: str
    evidence_excerpt: str


class JudgeResult(BaseModel):
    rubric_id: str = "adult-companion-benchmark-core"
    rubric_version: str = "2026-03-28"
    run_id: str
    event_labels: list[str]
    dimension_scores: dict[str, int]
    summary_findings: list[str]
    evidence_links: list[EvidenceLink]
    overall_bucket: str
    primary_failure_modes: list[str]
    recommended_product_fit: str
```

- [ ] **Step 4: Implement score calculation**

Scoring rules for MVP:

- derive labels from assistant turns
- map refusal density to `policy_pass_through_rate`
- map assistantization/persona drift to `persona_consistency`
- map repeated low-value responses to `conversation_usefulness`
- map recovery probe outcome to `recovery_ability`
- set `volatility=3` placeholder for single-run judgment and document that batch aggregation owns the final volatility score

- [ ] **Step 5: Persist judge artifacts**

Write `artifacts/runs/<run_id>/judge.json`

- [ ] **Step 6: Run judge tests**

Run: `python -m pytest tests/judge -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/aicure_benchmark/models/judge.py src/aicure_benchmark/judge/service.py tests/judge/test_service.py
git commit -m "feat: add judge service with evidence links"
```

### Task 11: Implement Report Aggregation and Markdown Rendering

**Files:**
- Create: `src/aicure_benchmark/reporting/aggregate.py`
- Create: `src/aicure_benchmark/reporting/render.py`
- Modify: `src/aicure_benchmark/cli.py`
- Test: `tests/reporting/test_render.py`

- [ ] **Step 1: Write failing report test**

```python
from aicure_benchmark.reporting.render import render_markdown_report


def test_render_markdown_report_contains_required_sections(seed_report_input):
    markdown = render_markdown_report(seed_report_input)
    assert "## Executive Summary" in markdown
    assert "## Results by Model" in markdown
    assert "## Routing Recommendation" in markdown
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/reporting/test_render.py -v`
Expected: FAIL with import errors

- [ ] **Step 3: Implement aggregation**

Aggregation responsibilities:

- group judged runs by `model`, `scenario category`, and `persona`
- compute average dimension scores
- compute batch-level volatility from repeated runs
- collect top failure modes
- choose one routing bucket:
  - `single_model_candidate`
  - `companion_and_erp_split_recommended`
  - `companion_only_candidate`
  - `not_ready_for_product_validation`

- [ ] **Step 4: Implement Markdown and JSON rendering**

Minimum Markdown sections:

- `## Executive Summary`
- `## Experiment Scope and Configuration`
- `## Results by Model`
- `## Results by Scenario`
- `## Results by Persona`
- `## Failure Mode Analysis`
- `## Routing Recommendation`
- `## Appendix and Evidence Index`

- [ ] **Step 5: Add CLI command**

Add `generate-report --batch-id <id>` that reads batch manifests and run judge artifacts, then writes:

- `artifacts/batches/<batch_id>/report.md`
- `artifacts/batches/<batch_id>/report.json`

- [ ] **Step 6: Run report tests**

Run: `python -m pytest tests/reporting/test_render.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add src/aicure_benchmark/reporting/aggregate.py src/aicure_benchmark/reporting/render.py src/aicure_benchmark/cli.py tests/reporting/test_render.py
git commit -m "feat: add report aggregation and rendering"
```

### Task 12: Add End-to-End Mock Pipeline Coverage

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/e2e/test_mock_pipeline.py`

- [ ] **Step 1: Write failing end-to-end test**

```python
def test_mock_pipeline_generates_report(tmp_path):
    batch_id = run_seed_batch(tmp_path)
    report_path = tmp_path / "batches" / batch_id / "report.md"
    assert report_path.exists()
    assert "Routing Recommendation" in report_path.read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/e2e/test_mock_pipeline.py -v`
Expected: FAIL until fixtures and CLI pipeline are connected

- [ ] **Step 3: Add reusable fixtures**

`tests/conftest.py` should expose:

- seed personas/scenarios
- `MockAdapter`
- `ModelTarget`
- `SamplingProfile`
- temporary artifacts root overrides

- [ ] **Step 4: Wire the full mock pipeline**

The test should cover:

1. asset loading
2. batch run
3. judge pass
4. report generation

- [ ] **Step 5: Run end-to-end test**

Run: `python -m pytest tests/e2e/test_mock_pipeline.py -v`
Expected: PASS

- [ ] **Step 6: Run the full test suite**

Run: `python -m pytest -v`
Expected: PASS

- [ ] **Step 7: Manually exercise the CLI**

Run:

```bash
python -m aicure_benchmark.cli validate-assets
python -m aicure_benchmark.cli run-batch --model-provider mock --model-name mock-companion --model-version local-v1 --repetitions 2
python -m aicure_benchmark.cli generate-report --batch-id <captured-batch-id>
```

Expected:

- asset counts printed
- batch manifest written under `artifacts/batches/`
- report files created

- [ ] **Step 8: Commit**

```bash
git add tests/conftest.py tests/e2e/test_mock_pipeline.py
git commit -m "test: add end-to-end mock benchmark coverage"
```

## Definition of Done

- `python -m pytest -v` passes
- `python -m aicure_benchmark.cli validate-assets` validates seed assets
- `python -m aicure_benchmark.cli run-batch ...` creates normalized run artifacts
- `python -m aicure_benchmark.cli generate-report --batch-id <id>` writes Markdown and JSON reports
- Every report conclusion can be traced back to `run_id` and evidence excerpts

## Follow-On Plans

Once this plan is implemented, create separate plans for:

1. `provider-adapters`
   - OpenAI or other hosted adapters
   - auth/env handling
   - provider-specific response normalization

2. `scenario-library-expansion`
   - expand from 5 seed scenarios to 20-30 scenarios
   - expand from 3 personas to 5+ personas
   - add category coverage review tooling

3. `judge-v2`
   - model-assisted rubric grading
   - human review workflow
   - disagreement and audit tooling
