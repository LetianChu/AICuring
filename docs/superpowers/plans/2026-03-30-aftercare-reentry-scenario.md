# Aftercare Reentry Scenario Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one `long_horizon_consistency` stress scenario that measures aftercare quality and gentle second-pass intimacy reentry after a prior deep-intimacy phase.

**Architecture:** Keep the schema, runner, and judge unchanged. Extend the scenario asset library with one new `semi_open_script` JSON asset, then update loader and coverage tests so the benchmark treats the aftercare case as part of the seed library.

**Tech Stack:** Python 3.9+, JSON assets, `pytest`, stdlib `json`/`pathlib`

---

## Chunk 1: Failing Tests

### Task 1: Add failing loader assertions for the aftercare scenario

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Test: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write failing assertions for `aftercare-reentry-after-deep-intimacy-01` metadata, branch goals, and probe turn alignment**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm the new assertions fail because the asset does not exist yet**
- [ ] **Step 3: Add the minimal JSON asset needed to satisfy the assertions**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm it passes**

### Task 2: Add failing coverage assertions for the expanded library

**Files:**
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `tests/assets/test_validate_assets_cli.py`
- Test: `tests/assets/test_scenario_coverage.py`
- Test: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Update expected scenario count from 13 to 14 and adjust `long_horizon_consistency`, `semi_open_script`, and `stress` totals**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -v` and confirm they fail**
- [ ] **Step 3: Verify the new asset satisfies the updated totals without code changes**
- [ ] **Step 4: Re-run the focused coverage tests and confirm they pass**

## Chunk 2: Asset

### Task 3: Add the aftercare reentry stress scenario

**Files:**
- Create: `assets/scenarios/aftercare-reentry-after-deep-intimacy-01.2026-03-30.json`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Create the aftercare scenario asset with `soft-spoken-slow-burn-lover` and `semi_open_script` structure**
- [ ] **Step 2: Ensure it includes aftercare pressure, anti-assistantization pressure, and a gentle second-pass reentry turn**
- [ ] **Step 3: Ensure it declares the expected failure modes from the spec and a valid probe turn**

## Chunk 3: Verification

### Task 4: Run regression checks and CLI validation

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -q`**
- [ ] **Step 2: Run the full suite with `./.venv/bin/python -m pytest -q`**
- [ ] **Step 3: Run `./.venv/bin/python -m aicure_benchmark.cli validate-assets`**
- [ ] **Step 4: Confirm the output reports `scenarios=14`**
