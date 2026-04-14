# True 50-Round Benchmark Design

## Background

The repository now has a working **true 15-round** benchmark path:

- round-based scenario assets
- runner support for `round_script + max_rounds`
- retention reporting that uses the true assistant-response denominator

The next step is to extend this benchmark line to **true 50-round** evaluation.

This new phase should answer a different question from the current 15-round suite:

> when a session is stretched to 50 full user-assistant rounds with no external memory support, where does the model actually begin to degrade, drift, empty out, or break continuity?

The user explicitly wants this phase to be a **bare-model benchmark** first.

That means:

- no external long-term memory
- no md-file memory
- no retrieval layer
- no summarization layer injected into the prompt

The benchmark should measure the model and provider stack **as-is** under longer conversation pressure.

## Goal

Add a new **true 50-round** benchmark suite that:

1. preserves the true fixed-round denominator
2. reuses the existing round-based runner and reporting stack where possible
3. measures late-stage continuity and degradation without external memory assistance
4. can first be piloted on a small model subset before later expansion to the full model pool

## Non-Goals

This phase does **not** attempt to:

- replace or rewrite the existing true 15-round suite
- mix 15-round and 50-round results into a single report
- introduce any external memory layer
- add provider-specific prompt hacks just to keep sessions alive
- solve the separate problem of provider instability beyond normal retry behavior

## Design Principles

### 1. Keep the denominator fixed

Each 50-round run must always mean:

- `50` user rounds
- `50` assistant replies
- `max_possible_retention_rounds = 50`

Branching may change wording or branch_goal focus, but it must **not** reduce the denominator.

### 2. Measure late-stage behavior explicitly

The 50-round suite is only useful if it stresses the model **after** the point where 15-round runs already look strong.

So the suite must not be front-loaded with all pressure.

Important checks must be placed in:

- the middle third
- the late third
- the final stretch

### 3. Preserve comparability with the true 15-round suite

The benchmark should keep the same six scenario families as the true 15-round suite so that we can compare:

- `15-round` performance
- `50-round` performance
- drop-off between them

### 4. Separate model weakness from provider weakness

At 50 rounds, provider instability becomes more likely.

The benchmark and reports must clearly distinguish:

- model-level degradation
- transport disconnects
- provider overload or quota failures

## Suite Structure

Create six new round-based scenarios:

- `warm-companion-50-round-retention-01`
- `romantic-escalation-50-round-retention-01`
- `explicit-pressure-50-round-retention-01`
- `aftercare-50-round-retention-01`
- `repair-recovery-50-round-retention-01`
- `long-horizon-continuity-50-round-retention-01`

All six should use:

- `round_script`
- `max_rounds = 50`
- `benchmark_tags = ["long_horizon_50_round"]`

## Scenario Design

### Warm Companion

Purpose:

- test whether low-pressure intimacy collapses into assistant talk, repetitive reassurance, or generic comfort over long duration

Suggested round cadence:

- rounds `1-10`: establish warmth and relationship position
- rounds `11-20`: deepen emotional specificity
- rounds `21-35`: introduce small correction and reassurance stress
- rounds `36-50`: detect late-stage flattening or assistantization

### Romantic Escalation

Purpose:

- test whether gradual romantic build can remain natural over long duration without resetting, cooling off, or becoming formulaic

Suggested cadence:

- rounds `1-10`: light flirt and contact
- rounds `11-20`: steady escalation
- rounds `21-35`: maintain romantic pressure without jumping too hard
- rounds `36-50`: verify late-stage continuity of tension and tone

### Explicit Pressure

Purpose:

- test whether sustained erotic pressure produces refusal drift, hollowing, or repetitive heat-without-process

Suggested cadence:

- rounds `1-10`: setup and relationship continuity
- rounds `11-20`: explicit shift
- rounds `21-35`: stable process-detail pressure
- rounds `36-50`: verify whether detail density and reciprocity survive the back half

### Aftercare

Purpose:

- test whether post-intimacy warmth can be sustained for a long tail without flattening into generic comfort

Suggested cadence:

- rounds `1-15`: embodied aftercare
- rounds `16-30`: maintain physical and emotional continuity
- rounds `31-40`: gentle re-entry pressure
- rounds `41-50`: late-stage warmth and continuity check

### Repair / Recovery

Purpose:

- test whether the model can recover from small degradations and stay recovered across the rest of a very long session

Suggested cadence:

- embed several controlled repair probes
- place at least one repair probe in the final third
- verify not just one-step recovery, but durability after recovery

### Long-Horizon Continuity

Purpose:

- hardest case for 50 rounds
- stress continuity, anti-fabrication, tone consistency, and relationship persistence

Suggested cadence:

- rounds `1-15`: establish anchors
- rounds `16-30`: maintain stable continuity
- rounds `31-40`: explicit continuity probes
- rounds `41-50`: late-stage anti-drift and anti-reset checks

## Runner And Asset Model

The existing true 15-round runner already supports:

- `round_script`
- `max_rounds`
- strict one-user-one-assistant loop

So the 50-round suite should reuse the same execution architecture.

No new execution mode is required if:

- each scenario stays fully round-based
- the denominator remains fixed at 50

## Reporting

Add a dedicated **true 50-round retention report** path.

This report should not be mixed with:

- legacy 15-turn results
- true 15-round results

### Core Metrics

- `retention_rounds`
- `max_possible_retention_rounds`
- `first_unstable_round`
- `break_type`
- `break_phase`

### New 50-round-focused Metrics

- `late_stage_retention_rounds`
  how much of rounds `31-50` remain stable
- `soft_degradation_round_count`
  how many assistant rounds are degraded even if no hard break occurs
- `recovery_success_count`
  how many repair opportunities are actually recovered
- `continuity_anchor_hit_rate`
  how often required continuity anchors are preserved

### Break Phases

Suggested phase bands:

- `1-10`: `early`
- `11-20`: `build`
- `21-30`: `sustain`
- `31-40`: `drift_zone`
- `41-50`: `late_endurance`

## Provider Failure Handling

Reports must distinguish:

- `provider_transport_failure`
- `provider_overloaded`
- `provider_quota_limit`
- `model_break`

These cannot be merged into one generic "failure".

## Rollout Strategy

### Phase 1: implementation

- add the 6 scenario assets
- add tests for 50-round suite count and runner behavior
- add report support for 50-round denominator and phase buckets

### Phase 2: pilot run

Run only three representative models first:

- `x-ai/grok-4.20`
- `sophnet-kimi-k2.5`
- `gpt-5.4`

This answers:

- whether the execution path is operational
- whether provider latency is tolerable
- whether late-stage degradation is meaningfully worse than the first 30 rounds

### Phase 3: full expansion

If the pilot is stable:

- expand to the current completed-model pool
- add a `50-round` completed-model scope file after runs finish

## Expected Value

This 50-round benchmark should move the repository from:

- "can a model survive a strong medium-length session?"

to:

- "can a model remain coherent and relational across a session long enough to expose native context-limit behavior without external memory support?"

That is the right benchmark before adding any memory layer, because it gives us the clean baseline we need for later comparisons.
