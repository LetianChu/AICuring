# Step Batch Quality Hardening Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make benchmark runs against `stepfun/step-3.5-flash:free` more trustworthy by deriving branch tags from assistant text, expanding judge rules for Chinese degradation patterns, and detecting memory fabrication during recall scenarios.

**Architecture:** Keep the existing adapter and CLI unchanged. Add lightweight runtime heuristics in the runner by merging text-derived labels into `event_tags`, then strengthen the judge in two layers: extend phrase-based label extraction for Chinese outputs and add transcript-aware context checks for memory recall turns so fabricated specifics degrade the final assessment.

**Tech Stack:** Python 3.9+, stdlib `json`/`re`/`pathlib`, `pytest`

---

## Chunk 1: Runner Branch Tags

### Task 1: Derive branch tags from assistant text during scenario execution

**Files:**
- Modify: `src/aicure_benchmark/runner/engine.py`
- Modify: `tests/runner/test_engine.py`

- [ ] **Step 1: Write a failing runner test showing a semi-open follow-up turn executes when the assistant text implies `soft_refusal`**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/runner/test_engine.py::test_run_scenario_derives_branch_tags_from_assistant_text -v` and confirm it fails**
- [ ] **Step 3: Implement minimal runtime tag derivation by merging adapter tags with text-derived labels**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/runner/test_engine.py::test_run_scenario_derives_branch_tags_from_assistant_text -v` and confirm it passes**

## Chunk 2: Judge Hardening

### Task 2: Expand phrase rules for Chinese degradation and recovery labels

**Files:**
- Modify: `src/aicure_benchmark/judge/rules.py`
- Modify: `tests/judge/test_rules.py`

- [ ] **Step 1: Write failing rule tests for Chinese `soft_refusal` and `assistantization` detection**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/judge/test_rules.py -v` and confirm they fail**
- [ ] **Step 3: Implement the minimal Chinese pattern expansion**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/judge/test_rules.py -v` and confirm they pass**

### Task 3: Detect memory fabrication in recall scenarios

**Files:**
- Modify: `src/aicure_benchmark/judge/service.py`
- Modify: `tests/judge/test_service.py`

- [ ] **Step 1: Write a failing judge test for a recall transcript that invents quoted or titled details absent from user history**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/judge/test_service.py::test_judge_run_detects_memory_fabrication_in_recall_turn -v` and confirm it fails**
- [ ] **Step 3: Implement the minimal transcript-aware context check and scoring downgrade**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/judge/test_service.py -v` and confirm all judge service tests pass**

## Chunk 3: Full Verification

### Task 4: Re-run regression tests and a fresh Step batch

**Files:**
- Modify: `src/aicure_benchmark/runner/engine.py`
- Modify: `src/aicure_benchmark/judge/rules.py`
- Modify: `src/aicure_benchmark/judge/service.py`

- [ ] **Step 1: Run the full suite with `./.venv/bin/python -m pytest -q`**
- [ ] **Step 2: Run `./.venv/bin/python -m aicure_benchmark.cli run-batch --model-provider openrouter --model-name stepfun/step-3.5-flash:free --model-version openrouter-live`**
- [ ] **Step 3: Run `./.venv/bin/python -m aicure_benchmark.cli generate-report --batch-id <new-batch-id>`**
- [ ] **Step 4: Inspect the new report and transcripts for branch coverage and memory-fabrication labels**
