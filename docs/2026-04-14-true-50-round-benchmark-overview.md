# True 50-Round Benchmark Overview

## Goal

This document defines the first rollout of the **true 50-round benchmark**.

The goal is not to solve long-term memory yet.

The goal is:

> measure how far a model can stay coherent, relational, and context-consistent across fifty full user-assistant rounds with no external memory support.

## Scope

This benchmark is:

- round-based
- fixed denominator
- bare-model only

This benchmark is not:

- legacy 15-turn
- true 15-round
- memory-assisted

## Tag

All scenarios in this suite use:

- `long_horizon_50_round`

## Scenario Families

The first version keeps the same six families as the true 15-round suite:

- `warm_companion`
- `romantic_escalation`
- `explicit_pressure`
- `aftercare`
- `repair_recovery`
- `long_horizon_continuity`

Expected asset names:

- `warm-companion-50-round-retention-01`
- `romantic-escalation-50-round-retention-01`
- `explicit-pressure-50-round-retention-01`
- `aftercare-50-round-retention-01`
- `repair-recovery-50-round-retention-01`
- `long-horizon-continuity-50-round-retention-01`

## Fixed Denominator Rule

Each run must mean:

- `50` user rounds
- `50` assistant replies
- `max_possible_retention_rounds = 50`

Branch wording may vary, but the denominator must not move.

## What 50 Rounds Is Supposed To Expose

The 50-round suite is meant to expose:

- late-stage continuity drift
- accumulated detail hollowing
- relationship-frame reset after long duration
- exhaustion-driven empty responses
- inability to recover in the last third of the session

## Key Metrics

Base metrics:

- `retention_rounds`
- `max_possible_retention_rounds`
- `first_unstable_round`
- `break_type`
- `break_phase`

50-round-specific metrics:

- `late_stage_retention_rounds`
- `soft_degradation_round_count`
- `recovery_success_count`
- `continuity_anchor_hit_rate`

## Phase Buckets

Suggested 50-round phase buckets:

- `1-10`: `early`
- `11-20`: `build`
- `21-30`: `sustain`
- `31-40`: `drift_zone`
- `41-50`: `late_endurance`

## Pilot Models

The first pilot should use three representative models:

- `x-ai/grok-4.20`
- `sophnet-kimi-k2.5`
- `gpt-5.4`

## Pilot Commands

### OpenRouter Pilot

```bash
PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_50_round \
  --model-provider openrouter \
  --model-name x-ai/grok-4.20 \
  --model-version openrouter-live \
  --repetitions 1
```

### AIHubMix Pilot

```bash
PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_50_round \
  --model-provider aihubmix \
  --model-name sophnet-kimi-k2.5 \
  --model-version aihubmix-live \
  --repetitions 1
```

### OpenAI-Compatible Pilot

```bash
OPENAI_BASE_URL=https://aihubmix.com/v1 \
OPENAI_API_KEY=$AIHUBMIX_API_KEY \
PYTHONPATH=src ./.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_50_round \
  --model-provider openai \
  --model-name gpt-5.4 \
  --model-version aihubmix-live \
  --repetitions 1
```

## Expansion Gate

Do not expand to the broader model pool until:

- at least two pilot models finish all six 50-round scenarios
- provider failures are clearly separable from model failures
- total runtime and token cost remain acceptable
