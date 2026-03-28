# OpenRouter CLI Integration Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a generic OpenRouter adapter to the benchmark CLI so `run-scenario` and `run-batch` can execute against an explicit OpenRouter model such as `stepfun/step-3.5-flash:free`.

**Architecture:** Keep the existing runner and judge unchanged. Add one focused adapter module responsible for loading the API key, calling OpenRouter chat completions, and normalizing responses; then update the CLI to choose between `mock` and `openrouter` providers without embedding provider-specific request logic in command handlers.

**Tech Stack:** Python 3.9+, stdlib `json`/`urllib`/`os`/`time`, `pytest`, `typer`

---

## Chunk 1: Adapter and CLI Routing

### Task 1: Add failing tests for OpenRouter adapter behavior

**Files:**
- Create: `tests/adapters/test_openrouter_adapter.py`
- Test: `tests/adapters/test_openrouter_adapter.py`

- [ ] **Step 1: Write the failing adapter tests**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/adapters/test_openrouter_adapter.py -v` and confirm they fail**
- [ ] **Step 3: Implement the minimal `OpenRouterAdapter` and API key loader**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/adapters/test_openrouter_adapter.py -v` and confirm they pass**

### Task 2: Add failing CLI tests for provider selection

**Files:**
- Create: `tests/test_cli_openrouter.py`
- Modify: `src/aicure_benchmark/cli.py`
- Test: `tests/test_cli_openrouter.py`

- [ ] **Step 1: Write the failing CLI tests**
- [ ] **Step 2: Run `./.venv/bin/python -m pytest tests/test_cli_openrouter.py -v` and confirm they fail**
- [ ] **Step 3: Add CLI provider routing for `mock` and `openrouter`**
- [ ] **Step 4: Re-run `./.venv/bin/python -m pytest tests/test_cli_openrouter.py -v` and confirm they pass**

## Chunk 2: Verification

### Task 3: Verify regression safety and live smoke

**Files:**
- Modify: `src/aicure_benchmark/adapters/openrouter.py`
- Modify: `src/aicure_benchmark/cli.py`

- [ ] **Step 1: Run focused regression tests**
- [ ] **Step 2: Run full suite with `./.venv/bin/python -m pytest -q`**
- [ ] **Step 3: Run a live smoke command with `stepfun/step-3.5-flash:free`**
- [ ] **Step 4: Inspect the generated transcript to confirm non-empty assistant output**
