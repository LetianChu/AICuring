# True 50-Round Benchmark Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a bare-model true 50-round benchmark suite, run an initial pilot subset, and generate a dedicated retention report for completed 50-round runs.

**Architecture:** Reuse the existing round-based scenario schema and runner, add six new `50-round` assets under a new benchmark tag, extend reporting only where 50-round-specific metrics need to be surfaced, then pilot on three models before expanding further.

**Tech Stack:** Python, Pydantic, pytest, Typer CLI, JSON scenario assets

---

## Chunk 1: 50-Round Scenario Assets

### Task 1: Add failing tests for the 50-round suite definition

**Files:**
- Modify: `tests/assets/test_scenario_loader.py`
- Modify: `tests/assets/test_scenario_coverage.py`
- Test: `tests/assets/test_scenario_loader.py`
- Test: `tests/assets/test_scenario_coverage.py`

- [ ] **Step 1: Write a failing loader test for the six true 50-round scenario IDs**

Assert:
- all six scenario IDs exist
- each uses `round_script`
- each has `max_rounds == 50`
- each has `benchmark_tags == ["long_horizon_50_round"]`

- [ ] **Step 2: Run the focused tests to verify they fail**

Run: `PYTHONPATH=src ./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py -q`
Expected: FAIL because the 50-round assets do not exist yet.

- [ ] **Step 3: Add the six true 50-round scenario files**

Create:
- `assets/scenarios/warm-companion-50-round-retention-01.2026-04-14.json`
- `assets/scenarios/romantic-escalation-50-round-retention-01.2026-04-14.json`
- `assets/scenarios/explicit-pressure-50-round-retention-01.2026-04-14.json`
- `assets/scenarios/aftercare-50-round-retention-01.2026-04-14.json`
- `assets/scenarios/repair-recovery-50-round-retention-01.2026-04-14.json`
- `assets/scenarios/long-horizon-continuity-50-round-retention-01.2026-04-14.json`

- [ ] **Step 4: Re-run the focused tests**

Run: `PYTHONPATH=src ./.venv/bin/python -m pytest tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py -q`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/assets/test_scenario_loader.py tests/assets/test_scenario_coverage.py assets/scenarios/*.2026-04-14.json
git commit -m "feat: add true 50-round scenario suite"
```

## Chunk 2: Reporting Support

### Task 2: Add failing report tests for 50-round metrics

**Files:**
- Modify: `tests/reporting/test_turn_retention.py`
- Modify: `src/aicure_benchmark/reporting/turn_retention.py`
- Test: `tests/reporting/test_turn_retention.py`

- [ ] **Step 1: Write a failing test for `max_possible_retention_rounds == 50`**

Cover a round-based run with 50 assistant replies and assert:
- `retention_turns`
- `max_possible_retention_turns`
- `break_phase` maps to the new 50-round phase buckets

- [ ] **Step 2: Write a failing test for late-stage metrics**

Add coverage for:
- `late_stage_retention_rounds`
- `soft_degradation_round_count`

- [ ] **Step 3: Run the focused report tests to verify they fail**

Run: `PYTHONPATH=src ./.venv/bin/python -m pytest tests/reporting/test_turn_retention.py -q`
Expected: FAIL because the new metrics are not implemented yet.

- [ ] **Step 4: Implement the minimal 50-round reporting additions**

Add:
- 50-round phase bucket handling
- late-stage metric calculation
- markdown rendering for the new metrics if needed

- [ ] **Step 5: Re-run the focused tests**

Run: `PYTHONPATH=src ./.venv/bin/python -m pytest tests/reporting/test_turn_retention.py -q`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add tests/reporting/test_turn_retention.py src/aicure_benchmark/reporting/turn_retention.py
git commit -m "feat: add 50-round retention metrics"
```

## Chunk 3: Pilot Run Commands

### Task 3: Add pilot-run documentation and scope notes

**Files:**
- Modify: `docs/2026-04-08-long-horizon-benchmark-overview.md`
- Create: `docs/2026-04-14-true-50-round-benchmark-overview.md`

- [ ] **Step 1: Document the new `long_horizon_50_round` tag**

Add:
- benchmark purpose
- why this remains bare-model only
- why pilot starts with three models

- [ ] **Step 2: Document the pilot models**

Use:
- `x-ai/grok-4.20`
- `sophnet-kimi-k2.5`
- `gpt-5.4`

- [ ] **Step 3: Add the exact pilot commands**

Include:

```bash
PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_50_round \
  --model-provider openrouter \
  --model-name x-ai/grok-4.20 \
  --model-version openrouter-live \
  --repetitions 1
```

and parallel equivalents for:
- `sophnet-kimi-k2.5`
- `gpt-5.4`

- [ ] **Step 4: Commit**

```bash
git add docs/2026-04-08-long-horizon-benchmark-overview.md docs/2026-04-14-true-50-round-benchmark-overview.md
git commit -m "docs: add true 50-round benchmark overview"
```

## Chunk 4: Pilot Verification

### Task 4: Run pilot and generate a dedicated report

**Files:**
- Output: `artifacts/batches/<batch_id>/`
- Output: `artifacts/comparisons/<short-id>/`

- [ ] **Step 1: Run the three pilot batches**

Run:
- `x-ai/grok-4.20`
- `sophnet-kimi-k2.5`
- `gpt-5.4`

- [ ] **Step 2: Generate a 50-round retention report for the completed pilot batches**

Run: `PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli generate-turn-retention-report --batch-id <batch_a> --batch-id <batch_b> --batch-id <batch_c> --scenario-tag long_horizon_50_round`

- [ ] **Step 3: Verify the report shows the 50-round denominator**

Check:
- `Max Retention` can reach `50`
- phase buckets use the 50-round ranges
- late-stage metrics are populated

- [ ] **Step 4: Write a short pilot summary note**

Create:
- `docs/2026-04-14-true-50-round-pilot-summary.md`

- [ ] **Step 5: Commit**

```bash
git add docs/2026-04-14-true-50-round-pilot-summary.md
git commit -m "docs: add true 50-round pilot summary"
```

## Chunk 5: Full-Pool Expansion Gate

### Task 5: Define the expansion decision

**Files:**
- Modify: `docs/2026-04-14-true-50-round-benchmark-overview.md`

- [ ] **Step 1: Add a rollout gate section**

The pilot may expand only if:
- at least two pilot models complete all six 50-round scenarios
- provider failures are clearly separable from model failures
- total runtime and token use are acceptable for broader execution

- [ ] **Step 2: Add the expansion command template**

Document the command form for the later full-pool run, but do not execute it yet unless explicitly requested.

- [ ] **Step 3: Commit**

```bash
git add docs/2026-04-14-true-50-round-benchmark-overview.md
git commit -m "docs: add 50-round expansion gate"
```
