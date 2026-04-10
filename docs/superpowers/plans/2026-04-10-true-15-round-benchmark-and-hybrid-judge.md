# True 15-Round Benchmark And Hybrid Judge Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real 15-round benchmark suite with a fixed 15-response denominator while preserving the legacy 15-turn suite, then layer in a hybrid rule-plus-LLM judge for soft degradation detection.

**Architecture:** Extend the scenario model and runner to support round-based scripts without breaking legacy turn-index scripts. Keep reporting compatible with both suites, then add a separate LLM judge path that augments the current rule judge instead of replacing it.

**Tech Stack:** Python, Pydantic, pytest, Typer CLI, JSON scenario assets

---

## Chunk 1: True 15-Round Benchmark Core

### Task 1: Add failing model tests for round-based scenario support

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_scenario_coverage.py`
- Modify: `src/aicure_benchmark/models/scenario.py`

- [ ] **Step 1: Write a failing loader test for round-based scripts**

Add a test that loads a scenario using `round_script` and asserts:
- `round_index` values are preserved
- `max_rounds == 15`
- legacy `user_script` scenarios still load

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/assets/test_scenario_loader.py -v`
Expected: FAIL because the schema does not support round-based scripts yet.

- [ ] **Step 3: Add minimal schema support**

Implement:
- `RoundScriptTurn`
- optional `round_script`
- optional `max_rounds`
- validation that scenarios use either legacy turn scripting or round scripting

- [ ] **Step 4: Run focused tests to verify they pass**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py src/aicure_benchmark/models/scenario.py
git commit -m "Add round-based scenario schema support"
```

### Task 2: Add failing runner tests for strict 15-round execution

**Files:**
- Modify: `tests/runner/test_engine.py`
- Modify: `src/aicure_benchmark/runner/engine.py`

- [ ] **Step 1: Write a failing runner test for 15 round execution**

Add a test that:
- builds a round-based scenario with `15` rounds
- runs it with a mock adapter
- asserts transcript contains `15` user turns and `15` assistant turns
- asserts message indices stay sequential through the full transcript

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/runner/test_engine.py -v`
Expected: FAIL because runner only knows legacy `user_script`.

- [ ] **Step 3: Implement minimal round-mode runner support**

Update `run_scenario` so that:
- legacy scenarios keep current behavior
- round-based scenarios iterate `round_script`
- each round always produces one assistant reply
- transcript message indices stay sequential

- [ ] **Step 4: Run focused runner tests to verify they pass**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/runner/test_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/runner/test_engine.py src/aicure_benchmark/runner/engine.py
git commit -m "Add strict round-based benchmark execution"
```

### Task 3: Add the six true 15-round scenario assets

**Files:**
- Create: `assets/scenarios/warm-companion-15-round-retention-01.2026-04-10.json`
- Create: `assets/scenarios/romantic-escalation-15-round-retention-01.2026-04-10.json`
- Create: `assets/scenarios/explicit-pressure-15-round-retention-01.2026-04-10.json`
- Create: `assets/scenarios/aftercare-15-round-retention-01.2026-04-10.json`
- Create: `assets/scenarios/repair-recovery-15-round-retention-01.2026-04-10.json`
- Create: `assets/scenarios/long-horizon-continuity-15-round-retention-01.2026-04-10.json`
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_scenario_coverage.py`

- [ ] **Step 1: Write failing asset coverage tests for the new suite**

Add tests that assert:
- `long_horizon_15_round` suite count is `6`
- each new file uses round-based scripting
- each new file declares `max_rounds == 15`

- [ ] **Step 2: Run focused asset coverage tests to verify failure**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py -v`
Expected: FAIL because the files do not exist yet.

- [ ] **Step 3: Add the six scenario files**

Use deterministic scripts with:
- `15` explicit user rounds each
- no branch path that changes denominator
- the same six scenario categories as the legacy suite

- [ ] **Step 4: Re-run asset tests**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add assets/scenarios/*.2026-04-10.json tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py
git commit -m "Add true 15-round scenario suite"
```

### Task 4: Add failing reporting tests for fixed denominator 15

**Files:**
- Modify: `tests/reporting/test_turn_retention.py`
- Modify: `tests/test_cli_turn_retention.py`
- Modify: `src/aicure_benchmark/reporting/turn_retention.py`

- [ ] **Step 1: Write failing report tests for true-round scenarios**

Add tests that assert:
- `max_possible_retention_turns == 15` for a full true-round run
- report output clearly carries the 15-round denominator
- scenario tag filtering with `long_horizon_15_round` works

- [ ] **Step 2: Run the focused report tests to verify failure**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/reporting/test_turn_retention.py tests/test_cli_turn_retention.py -v`
Expected: FAIL because report logic is still written around legacy semantics.

- [ ] **Step 3: Implement minimal report compatibility**

Update reporting so that:
- round-based runs always expose `15` as max possible retention
- break phase logic works against 15 assistant replies
- CLI can generate `long_horizon_15_round` reports cleanly

- [ ] **Step 4: Re-run focused report tests**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/reporting/test_turn_retention.py tests/test_cli_turn_retention.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/reporting/test_turn_retention.py tests/test_cli_turn_retention.py src/aicure_benchmark/reporting/turn_retention.py
git commit -m "Support true 15-round retention reporting"
```

## Chunk 2: Hybrid Judge v1

### Task 5: Add failing tests for LLM judge payload and schema

**Files:**
- Create: `tests/judge/test_llm_service.py`
- Create: `src/aicure_benchmark/models/judge_llm.py`
- Create: `src/aicure_benchmark/judge/llm_service.py`

- [ ] **Step 1: Write failing tests for fixed-schema LLM judge output**

Cover:
- request payload contains scenario metadata, persona summary, transcript, and rule summary
- JSON response parsing into a strict model
- failure on malformed judge payload

- [ ] **Step 2: Run focused tests to verify failure**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/judge/test_llm_service.py -v`
Expected: FAIL because the module does not exist.

- [ ] **Step 3: Implement minimal LLM judge service and schema**

Implement:
- strict Pydantic schema for judge output
- helper to build judge request payload
- deterministic request settings

- [ ] **Step 4: Re-run focused tests**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/judge/test_llm_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/judge/test_llm_service.py src/aicure_benchmark/models/judge_llm.py src/aicure_benchmark/judge/llm_service.py
git commit -m "Add strict schema LLM judge service"
```

### Task 6: Add failing tests for merged judge output

**Files:**
- Modify: `tests/judge/test_service.py`
- Modify: `src/aicure_benchmark/judge/service.py`

- [ ] **Step 1: Write failing tests for merged judge categorization**

Cover:
- hard break remains owned by rule judge
- soft degradation can be added by llm judge
- run-level drift can aggregate both layers

- [ ] **Step 2: Run focused tests to verify failure**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/judge/test_service.py -v`
Expected: FAIL because the service has no hybrid merge behavior.

- [ ] **Step 3: Implement merged judge output**

Add:
- `judge_rule.json`
- `judge_llm.json`
- merged output fields in `judge.json`

- [ ] **Step 4: Re-run focused tests**

Run: `PYTHONPATH=src ./.venv/bin/pytest tests/judge/test_service.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/judge/test_service.py src/aicure_benchmark/judge/service.py
git commit -m "Merge rule and LLM judge outputs"
```

## Chunk 3: Docs, Verification, And Rollout

### Task 7: Add benchmark documentation for legacy vs true-round split

**Files:**
- Modify: `docs/2026-04-08-long-horizon-benchmark-overview.md`
- Create: `docs/2026-04-10-true-15-round-benchmark-overview.md`

- [ ] **Step 1: Document the new benchmark split**

Explain:
- why legacy `15_turn` is preserved
- what true `15_round` means
- which report should be used for forward comparisons

- [ ] **Step 2: Commit**

```bash
git add docs/2026-04-08-long-horizon-benchmark-overview.md docs/2026-04-10-true-15-round-benchmark-overview.md
git commit -m "Document true 15-round benchmark rollout"
```

### Task 8: Run full verification and capture example commands

**Files:**
- Modify: `docs/2026-04-10-true-15-round-benchmark-overview.md`

- [ ] **Step 1: Run the full test suite**

Run: `PYTHONPATH=src ./.venv/bin/pytest`
Expected: PASS

- [ ] **Step 2: Run one smoke true-round scenario**

Run a single `run-scenario` command against a stable provider and verify:
- transcript contains `15` user turns
- transcript contains `15` assistant turns

- [ ] **Step 3: Generate one true-round retention report**

Run:

```bash
PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli generate-turn-retention-report --batch-id <batch_id> --scenario-tag long_horizon_15_round
```

Expected:
- report writes successfully
- max possible retention shows `15`

- [ ] **Step 4: Write the exact working commands into docs**

- [ ] **Step 5: Commit**

```bash
git add docs/2026-04-10-true-15-round-benchmark-overview.md
git commit -m "Add true 15-round verification commands"
```

Plan complete and saved to `docs/superpowers/plans/2026-04-10-true-15-round-benchmark-and-hybrid-judge.md`. Ready to execute.
