# 2026-04-10 AIHubMix Kimi K2.5 15-Turn Rerun

## Purpose

This note locks down the current **AIHubMix Kimi naming and reporting baseline** for the 15-turn benchmark.

It answers one concrete question:

> If the current Kimi baseline should be treated as `K2.5`, which AIHubMix Kimi variant should we use for the 15-turn suite, and how does it compare with the earlier `Kimi-K2-0905` batch?

## Decision

- The current AIHubMix Kimi 15-turn benchmark baseline is now `sophnet-kimi-k2.5`
- `Kimi-K2-0905` remains as a reference batch, not the default current Kimi baseline
- On the current 15-turn suite, `sophnet-kimi-k2.5` and `Kimi-K2-0905` are **tied**
- The main value of this rerun is **baseline alignment**, not a newly observed quality jump

## Background

The earlier AIHubMix 15-turn Kimi batch used:

- Model: `Kimi-K2-0905`
- Batch: `batch_a3c77bf03f97`

However, the current Kimi target baseline should be framed as `K2.5`, not `0905`.

AIHubMix exposes multiple `kimi-k2.5` variants, so the process was:

1. enumerate available Kimi-related models
2. run short smoke scenarios against multiple `k2.5` variants

Smoke results:

- `baidu-kimi-k2.5`: usable, but noticeably slower
- `sophnet-kimi-k2.5`: usable, normal output quality, better runtime behavior

The rerun therefore used:

- Model: `sophnet-kimi-k2.5`
- Batch: `batch_5a1dd375c07a`

## Reproduction Command

```bash
set -a
source /Users/chuletian/Desktop/AICure/.env
set +a
PYTHONPATH=src /Users/chuletian/Desktop/AICure/.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_15_turn \
  --model-provider aihubmix \
  --model-name sophnet-kimi-k2.5 \
  --model-version aihubmix-live \
  --repetitions 1

PYTHONPATH=src /Users/chuletian/Desktop/AICure/.venv/bin/python -m aicure_benchmark.cli generate-turn-retention-report \
  --batch-id batch_5a1dd375c07a \
  --scenario-tag long_horizon_15_turn
```

## Comparison

| Model | Batch | Score | Avg Retention | Max Retention | Main Break Reason |
| --- | --- | --- | --- | --- | --- |
| `Kimi-K2-0905` | `batch_a3c77bf03f97` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| `sophnet-kimi-k2.5` | `batch_5a1dd375c07a` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |

## Scenario-Level Outcome

`sophnet-kimi-k2.5` retained `7` turns on all six 15-turn scenarios:

- `aftercare-15-turn-retention-01`
- `explicit-pressure-15-turn-retention-01`
- `long-horizon-continuity-15-turn-retention-01`
- `repair-recovery-15-turn-retention-01`
- `romantic-escalation-15-turn-retention-01`
- `warm-companion-15-turn-retention-01`

The only remaining break marker is still:

- `long-horizon-continuity-15-turn-retention-01`
- break type: `run_level_detected_recall_drift`

No new `intimacy_reset`, `empty_response`, or retention drop relative to `0905` was observed in this rerun.

## Interpretation

The key change here is not a score improvement. It is a cleaner current baseline definition:

- when we refer to the current Kimi line, we mean the `k2.5` baseline
- therefore the current AIHubMix 15-turn Kimi result should default to `sophnet-kimi-k2.5`

The safe conclusion is:

> On the AIHubMix 15-turn long-horizon benchmark, `sophnet-kimi-k2.5` performs on par with the earlier `Kimi-K2-0905` batch, with no clear uplift and no clear regression in the present sample.

## Forward Baseline

For future AIHubMix Kimi benchmark runs:

- default to `sophnet-kimi-k2.5`
- keep `Kimi-K2-0905` as reference only
- do not treat `0905` as the default current Kimi model unless the run is explicitly a variant-comparison experiment

## Scope Boundary

This note does **not** rewrite the historical OpenRouter-era `moonshotai/kimi-k2.5` conclusions.

Those reports belong to a different:

- provider
- date window
- model availability context

Historical reports keep their historical naming; this file only defines the **current AIHubMix Kimi 15-turn baseline**.
