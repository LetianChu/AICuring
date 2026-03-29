# High-Detail ERP Scenario Expansion Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three new relationship-conditioned, high-detail ERP stress scenarios so the benchmark can measure finer-grained erotic process detail under strong intimacy and long-horizon continuity.

**Architecture:** Keep the existing scenario schema and runner unchanged. Extend the asset library with three new `semi_open_script` stress scenarios, then update loader and coverage tests so the benchmark treats them as first-class seed assets without special-case logic.

**Tech Stack:** Python 3.9+, JSON assets, `pytest`, stdlib `json`/`pathlib`

---

## Chunk 1: Scenario Tests

### Task 1: Add failing loader assertions for the new high-detail scenarios

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Test: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Write failing assertions for the three new scenarios**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm the new assertions fail because the assets do not exist yet**
- [ ] **Step 3: Add the minimal JSON assets needed to satisfy the assertions**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py -v` and confirm it passes**

### Task 2: Add failing coverage assertions for the expanded library

**Files:**
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `tests/assets/test_validate_assets_cli.py`
- Test: `tests/assets/test_scenario_coverage.py`
- Test: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Update the expected counts from 10 scenarios to 13 scenarios and adjust category / semi-open / stress totals**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -v` and confirm they fail**
- [ ] **Step 3: Verify the new assets satisfy the coverage changes without additional code changes**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -v` and confirm they pass**

## Chunk 2: Scenario Assets

### Task 3: Add the romantic deep-intimacy stress scenario

**Files:**
- Create: `assets/scenarios/romantic-escalation-deep-intimacy-01.2026-03-29.json`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Add the minimal romantic deep-intimacy asset matching the spec**
- [ ] **Step 2: Confirm it includes high-detail escalation, a degradation pressure turn, and a valid failure recovery probe**

### Task 4: Add the ERP detailed-guidance stress scenario

**Files:**
- Create: `assets/scenarios/erp-handling-detailed-guidance-01.2026-03-29.json`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Add the heaviest ERP asset with stronger process-detail pressure**
- [ ] **Step 2: Confirm it includes `detail_request_after_heat` / `pressure_after_content_hollowing` style branch goals and explicit scoring focus**

### Task 5: Add the long-horizon detail-drift stress scenario

**Files:**
- Create: `assets/scenarios/long-horizon-established-lovers-detail-drift-01.2026-03-29.json`
- Modify: `tests/assets/test_scenario_loader.py`

- [ ] **Step 1: Add the long-horizon asset with shared-memory pressure and detail drift checks**
- [ ] **Step 2: Confirm it includes recall pressure plus at least one branch tied to context or continuity degradation**

## Chunk 3: Verification

### Task 6: Run regression tests and a smoke asset validation

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `tests/assets/test_validate_assets_cli.py`

- [ ] **Step 1: Run `./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py tests/assets/test_validate_assets_cli.py -q`**
- [ ] **Step 2: Run the full suite with `./.venv/bin/python -m pytest -q`**
- [ ] **Step 3: Run `./.venv/bin/python -m aicure_benchmark.cli validate-assets`**
- [ ] **Step 4: Inspect the output to confirm `scenarios=13`**
