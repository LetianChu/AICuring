# 15-Turn Long-Horizon Benchmark Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing 15-turn benchmark overview into a runnable workflow with tagged 15-turn scenario assets, scenario-selection support, and retention reporting that surfaces break phase, break type, and max-possible retention.

**Architecture:** Reuse the current asset loader, runner, judge, and turn-retention report rather than creating a parallel benchmark stack. Add one light schema extension to mark scenarios as part of the 15-turn suite, create six 15-turn scenario assets aligned to the overview layers, then extend the CLI and reporting modules so a user can run only the 15-turn suite and get a dedicated retention-first report.

**Tech Stack:** Python 3.9+, JSON scenario assets, Typer CLI, Pydantic v2, stdlib `json`/`pathlib`/`statistics`, `pytest`

---

## File Map

- `src/aicure_benchmark/models/scenario.py`
  Responsibility: add lightweight scenario tagging for benchmark-suite selection without changing existing core fields.
- `src/aicure_benchmark/cli.py`
  Responsibility: support selecting scenarios by benchmark tag or expose a dedicated 15-turn benchmark command.
- `src/aicure_benchmark/reporting/turn_retention.py`
  Responsibility: compute 15-turn-specific metrics such as `max_possible_retention_turns` and `break_phase`, then render them into the existing retention report output.
- `tests/assets/test_scenario_loader.py`
  Responsibility: lock down the new 15-turn scenario assets and their benchmark tags.
- `tests/assets/test_scenario_coverage.py`
  Responsibility: assert the 15-turn suite composition and counts.
- `tests/test_cli_openrouter.py`
  Responsibility: if scenario-tag filtering lands in the main CLI, prove batch selection respects the requested benchmark tag.
- `tests/test_cli_turn_retention.py`
  Responsibility: verify retention report CLI behavior for the 15-turn suite.
- `tests/reporting/test_turn_retention.py`
  Responsibility: lock down the new retention metrics and phase classification.
- `assets/scenarios/warm-companion-15-turn-retention-01.2026-04-09.json`
  Responsibility: low-pressure, long-horizon warm companion retention case.
- `assets/scenarios/romantic-escalation-15-turn-retention-01.2026-04-09.json`
  Responsibility: gradual escalation retention case.
- `assets/scenarios/explicit-pressure-15-turn-retention-01.2026-04-09.json`
  Responsibility: explicit pressure retention case.
- `assets/scenarios/aftercare-15-turn-retention-01.2026-04-09.json`
  Responsibility: post-intimacy aftercare retention case.
- `assets/scenarios/repair-recovery-15-turn-retention-01.2026-04-09.json`
  Responsibility: degradation and repair retention case.
- `assets/scenarios/long-horizon-continuity-15-turn-retention-01.2026-04-09.json`
  Responsibility: strongest memory/continuity retention case.
- `docs/2026-04-08-long-horizon-benchmark-overview.md`
  Responsibility: source design reference; no implementation details should drift away from it.
- `CLAUDE.md`
  Responsibility: document the actual CLI command for running the 15-turn suite once implemented.

## Chunk 1: Scenario Selection Contract

### Task 1: Add a failing schema test for benchmark tags

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `src/aicure_benchmark/models/scenario.py`
- Test: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write a failing test proving `ScenarioSpec` accepts a `benchmark_tags` list**

```python
def test_scenario_supports_benchmark_tags() -> None:
    scenario = ScenarioSpec(
        ...,
        benchmark_tags=["long_horizon_15_turn"],
    )
    assert scenario.benchmark_tags == ["long_horizon_15_turn"]
```

- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py::test_scenario_supports_benchmark_tags -v` and confirm it fails**

- [ ] **Step 3: Add `benchmark_tags: list[str] = Field(default_factory=list)` to `src/aicure_benchmark/models/scenario.py`**

- [ ] **Step 4: Re-run the targeted test and confirm it passes**

### Task 2: Add a failing CLI test for scenario-tag batch filtering

**Files:**
- Modify: `tests/test_cli_openrouter.py`
- Modify: `src/aicure_benchmark/cli.py`
- Test: `tests/test_cli_openrouter.py`

- [ ] **Step 1: Write a failing CLI test that passes `--scenario-tag long_horizon_15_turn` and asserts only tagged scenarios are sent to `run_batch(...)`**

```python
def test_run_batch_filters_scenarios_by_tag(monkeypatch, tmp_path) -> None:
    ...
    assert [scenario.scenario_id for scenario in kwargs["scenarios"]] == [
        "warm-companion-15-turn-retention-01",
        ...
    ]
```

- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/test_cli_openrouter.py::test_run_batch_filters_scenarios_by_tag -v` and confirm it fails**

- [ ] **Step 3: Add a minimal optional `scenario_tag: Optional[str]` CLI parameter and filter scenarios before calling `run_batch(...)`**

- [ ] **Step 4: Re-run the targeted test and confirm it passes**

## Chunk 2: 15-Turn Scenario Assets

### Task 3: Add failing loader assertions for the six 15-turn assets

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Test: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Add failing assertions for the six new scenario IDs, `max_turns == 15`, and `benchmark_tags == [\"long_horizon_15_turn\"]`**

- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm those assertions fail because the assets do not exist yet**

- [ ] **Step 3: Create the six JSON assets with the required personas, branch goals, and failure recovery probes**

- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm it passes**

### Task 4: Update coverage expectations for the 15-turn suite

**Files:**
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `tests/assets/test_validate_assets_cli.py`
- Test: `tests/assets/test_scenario_coverage.py`
- Test: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Add a failing test that counts `benchmark_tags` and asserts six scenarios belong to `long_horizon_15_turn`**

```python
def test_long_horizon_15_turn_suite_count() -> None:
    ...
    assert tagged_count == 6
```

- [ ] **Step 2: Update total scenario counts to include the six new assets**

- [ ] **Step 3: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -v` and confirm the new expectations fail**

- [ ] **Step 4: Re-run the same focused tests after asset creation and confirm they pass**

## Chunk 3: Turn Retention Report Hardening

### Task 5: Add failing tests for 15-turn-specific retention metrics

**Files:**
- Modify: `tests/reporting/test_turn_retention.py`
- Modify: `src/aicure_benchmark/reporting/turn_retention.py`
- Test: `tests/reporting/test_turn_retention.py`

- [ ] **Step 1: Add a failing test for `max_possible_retention_turns`**

```python
def test_build_turn_retention_report_exposes_max_possible_retention_turns(tmp_path) -> None:
    ...
    detail = report["details"][0]
    assert detail["max_possible_retention_turns"] == 7
```

- [ ] **Step 2: Add a failing test for `break_phase` classification**

```python
def test_build_turn_retention_report_classifies_break_phase(tmp_path) -> None:
    ...
    assert detail["break_phase"] == "late"
```

- [ ] **Step 3: Add a failing test for run-level recall drift on 15-turn scenarios that never hit an explicit tagged break**

- [ ] **Step 4: Run `./.venv/bin/python -m pytest tests/reporting/test_turn_retention.py -v` and confirm the new assertions fail**

- [ ] **Step 5: Extend `src/aicure_benchmark/reporting/turn_retention.py` so each run detail includes:
  - `max_possible_retention_turns`
  - `break_phase`
  - retention ratios derived from actual assistant turns vs possible assistant turns**

- [ ] **Step 6: Re-run `./.venv/bin/python -m pytest tests/reporting/test_turn_retention.py -v` and confirm it passes**

### Task 6: Add failing CLI tests for 15-turn retention report generation

**Files:**
- Modify: `tests/test_cli_turn_retention.py`
- Modify: `tests/test_cli_smoke.py`
- Modify: `src/aicure_benchmark/cli.py`
- Test: `tests/test_cli_turn_retention.py`
- Test: `tests/test_cli_smoke.py`

- [ ] **Step 1: Add a failing CLI test that generates a retention report for a specific `--batch-id` and `--scenario-tag long_horizon_15_turn` selection**
- [ ] **Step 2: Extend the CLI help expectations if a dedicated `run-15-turn-benchmark` command is introduced**
- [ ] **Step 3: Run the focused CLI tests and confirm they fail**
- [ ] **Step 4: Implement the minimal CLI wiring so retention reporting works cleanly for the 15-turn suite**
- [ ] **Step 5: Re-run the focused CLI tests and confirm they pass**

## Chunk 4: Verification

### Task 7: Run the full verification set and document the workflow

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Run `./.venv/bin/python -m pytest -q`**
- [ ] **Step 2: Run `./.venv/bin/python -m aicure_benchmark.cli validate-assets` and confirm the new total scenario count**
- [ ] **Step 3: Run one tagged 15-turn batch with:

```bash
./.venv/bin/python -m aicure_benchmark.cli run-batch \
  --model-provider openrouter \
  --model-name stepfun/step-3.5-flash:free \
  --model-version openrouter-live \
  --scenario-tag long_horizon_15_turn
```
**
- [ ] **Step 4: Run `generate-turn-retention-report` for that batch and confirm the markdown/json outputs are written**
- [ ] **Step 5: Update `CLAUDE.md` with the actual 15-turn benchmark command once the implementation is real**
