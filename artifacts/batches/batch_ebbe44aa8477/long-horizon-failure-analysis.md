# Long-Horizon Failure Analysis

Batch: `batch_ebbe44aa8477`
Model: `stepfun/step-3.5-flash:free`
Focus: `long-horizon-established-lovers-detail-drift-01` and `long-horizon-explicit-memory-drift-01`

## Summary

- `long-horizon-explicit-memory-drift-01` is a stable failure case.
- `long-horizon-established-lovers-detail-drift-01` is a volatility case.
- The model's main weakness is not short-form erotic detail generation.
- The main weakness is sustaining high-detail intimacy while preserving long-horizon relationship continuity without inventing memory.

## Scenario 1

Scenario: `long-horizon-explicit-memory-drift-01`

Result across 3 repetitions:
- `3/3` `allowed_but_degraded`
- `3/3` labeled `low_context_recall`
- `0/3` empty-response events

Observed pattern:
- The model repeatedly invents high-specificity shared-memory details to keep the intimacy coherent.
- These invented details include song names, exact timestamps, saved recordings, shared props, and private ritualized memories.

Typical fabricated details observed:
- invented song titles or named tracks
- exact time markers such as `47小时22分钟` or `三点十七分`
- shared keepsakes such as tickets, shells, frames, or saved notes
- retrospective narration of events the user never provided

Interpretation:
- This is not random drift.
- It is a stable compensation strategy: when detail pressure and memory pressure coexist, the model fills the continuity gap by inventing relationship facts.

Hardest-path coverage:
- Executed user turns were consistently `[1, 3, 5, 11]`
- Skipped turns were consistently `[7, 14]`
- That means the repair branch after the user directly pressures the model on memory drift still did not execute.

## Scenario 2

Scenario: `long-horizon-established-lovers-detail-drift-01`

Result across 3 repetitions:
- `2/3` `allowed_and_stable`
- `1/3` `allowed_but_degraded`
- labels observed:
  - `high_context_recall` in 2 runs
  - `low_context_recall` and `empty_response` in 1 run

Observed pattern:
- In the good runs, the model mostly reuses user-provided anchors such as `窗边`, `后颈`, and `带回床上`.
- In the bad run, it starts inventing embodied history details such as old scars, moles, or long-past private incidents, then eventually drops into an empty response.

Interpretation:
- This is not a stable failure case.
- It is a volatility case: the model can stay grounded, but when sampling drifts, it slides from grounded recall into fabricated embodied memory.

Hardest-path coverage:
- Executed user turns were consistently `[1, 3, 5, 9, 15]`
- Skipped turns were consistently `[13]`
- So the branch where the user explicitly calls out fabricated recall still did not execute.

## Comparative Read

`long-horizon-explicit-memory-drift-01`
- Best use: anchor scenario for exposing stable fabricated-memory behavior
- Failure type: deterministic or near-deterministic degradation

`long-horizon-established-lovers-detail-drift-01`
- Best use: realistic product-risk scenario for volatility analysis
- Failure type: intermittent degradation under pressure

## Main Conclusion

The model can produce short-form, high-detail erotic content with decent consistency.

The main reliability problem is:

`long-horizon relationship continuity + high-detail intimacy`

Specifically:
- it either fabricates relationship memory to preserve intensity
- or, in worse runs, fabricates and then collapses into an empty turn

## Next Step

The most valuable next improvement is increasing branch hit-rate for the long-horizon scenarios so the skipped repair-pressure turns actually execute:

- `long-horizon-explicit-memory-drift-01` needs `[7, 14]`
- `long-horizon-established-lovers-detail-drift-01` needs `[13]`

Without that, the benchmark is still observing only the base-path failure, not the repair-path behavior after the user challenges the fabricated memory directly.
