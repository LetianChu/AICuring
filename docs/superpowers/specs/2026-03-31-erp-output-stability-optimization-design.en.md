# ERP Output Stability Optimization Design v0.1

## 1. Goal

This document answers a concrete engineering question:

> Under the current benchmark, and without jailbreaks or policy-bypass tricks, how do we make adult / erotic / sexual output more stable while preserving relationship continuity, detail density, and companion tone?

The target is not simply “more explicit output.”

The target is more stable performance on:

- short-horizon high-detail ERP
- aftercare and gentle reentry
- long-horizon intimacy with grounded memory
- lower rates of `assistantization`, `content_hollowing`, `empty_response`, and `low_context_recall`

---

## 2. Current Benchmark Read

Based on the current benchmark runs:

- the model can already produce short-form, high-detail erotic content
- `erp-handling-detailed-guidance-01`, `romantic-escalation-deep-intimacy-01`, and `aftercare-reentry-after-deep-intimacy-01` are comparatively stable
- the main weaknesses are concentrated in:
  - `long-horizon-explicit-memory-drift-01`
  - `long-horizon-established-lovers-detail-drift-01`

The most important failure modes right now are:

1. `low_context_recall`
   - the model invents shared-memory details to preserve intimacy continuity

2. `empty_response`
   - some aftercare or long-horizon transitions still collapse into blank turns

3. `content_hollowing`
   - surface heat remains, but the content loses process detail

4. `assistantization`
   - the model falls back into generic helper or comfort language

---

## 3. Non-Goals

This design explicitly does not propose:

- jailbreaks
- DAN-style prompting
- “ignore safety rules” overrides
- adversarial prompt attacks
- adding more explicit keywords as a fake optimization

Why:

- low reproducibility
- version fragility
- poor productization value
- contaminated benchmark conclusions

---

## 4. Core Diagnosis

The current problem is not:

> “the model cannot write erotic content”

The current problem is:

> the model can perform in short, local, high-detail erotic turns, but becomes unstable when high-detail intimacy must coexist with long-horizon relationship continuity

That means the optimal order is not:

1. make prompts more explicit

Instead, the optimal order is:

1. stabilize relationship state
2. stabilize memory grounding
3. then improve detail density and continuity

---

## 5. Recommended Optimization Path

This design recommends a 3-phase roadmap.

### Phase 1: Inference-Time Optimization

This is the fastest and most immediately testable layer.

#### 5.1 Stage-specific generation profiles

Do not use one generation profile for all intimacy stages.

Create at least separate profiles for:

- `romantic_escalation`
- `high_detail_erp`
- `aftercare`
- `gentle_reentry`
- `long_horizon_memory`

Tune independently:

- `temperature`
- `top_p`
- `max_tokens`

Purpose:

- keep creativity where detail matters
- reduce drift where memory matters
- reduce collapse in aftercare transitions

#### 5.2 Multi-candidate generation and reranking

Do not trust a single sample for critical scenarios.

Recommended flow:

1. generate `n` candidates
2. rerank them with lightweight scoring
3. choose the best grounded response

Rerank dimensions should include:

- detail density
- persona consistency
- grounded recall
- no empty response
- no assistantization
- aftercare continuity

#### 5.3 Early rejection of bad candidates

If a candidate shows:

- empty output
- obvious assistant tone
- fabricated relationship memory

downrank or discard it before final selection.

---

### Phase 2: Structured Relationship State

This is the most important medium-term fix.

#### 5.4 Do not let the model freely “remember”

The benchmark already shows:

- once long-horizon continuity and high-detail intimacy are combined
- the model fills the gap by inventing relationship facts

So the fix is not “tell it not to hallucinate.”

The fix is:

- only allow grounded recall through structured state

#### 5.5 Maintain explicit allowed relationship facts

Introduce a state layer such as:

- relationship stage
- recent intimacy phase
- allowed shared facts
- aftercare state
- reentry readiness

Example:

```json
{
  "relationship_stage": "established_lovers",
  "recent_intimacy_phase": "aftercare",
  "allowed_shared_facts": [
    "the user said they like being kissed on the back of the neck by the window",
    "the user mentioned being carried back to bed"
  ],
  "disallowed_behavior": [
    "invent song titles",
    "invent exact timestamps",
    "invent scars, keepsakes, or rituals not in context"
  ]
}
```

#### 5.6 Grounded recall only

In recall-heavy scenes, the model should only:

- reuse user-provided facts
- lightly transform user-provided facts

It should not:

- invent song titles
- invent keepsakes
- invent precise timestamps
- invent shared incidents

#### 5.7 Aftercare state machine

For aftercare scenarios, introduce explicit internal phases:

- `post_peak`
- `aftercare`
- `warm_reentry`

This reduces:

- abrupt emotional cooling
- premature return to maximum intensity
- broken continuity after high-intimacy phases

---

### Phase 3: Targeted Training / Preference Optimization

This is the strongest long-term fix.

#### 5.8 Data construction

Build examples that jointly cover:

- strong relationship context
- high-detail ERP
- aftercare
- gentle reentry
- grounded long-horizon recall

#### 5.9 Negative examples must include

Do not only train against refusal.

Negative examples should include:

- fabricated memory
- generic comfort
- assistantization
- empty response
- hollow erotic heat

#### 5.10 Training objective

The objective is not simply “be bolder.”

The objective is:

- more grounded
- more continuous
- less empty
- less assistant-like
- less likely to fabricate intimacy history

---

## 6. Best Immediate Improvements Under the Current Benchmark

If we only optimize within the current benchmark harness, the highest-priority changes are:

### 6.1 Highest priority

- grounded memory constraints for the `long_horizon_*` scenarios
- multi-candidate generation plus reranking

### 6.2 Second priority

- separate generation profiles for `aftercare` / `reentry`
- separate generation profiles for `high_detail_erp`

### 6.3 Third priority

- improve hardest-path hit rate in the `semi_open_script` scenarios
- especially:
  - `[7, 14]` in `long-horizon-explicit-memory-drift-01`
  - `[13]` in `long-horizon-established-lovers-detail-drift-01`

Because right now the benchmark still observes too much base-path behavior and not enough repair-path behavior.

---

## 7. Validation Strategy

The optimization must still be validated inside the current benchmark.

Recommended order:

1. run the current 14-scenario benchmark with `repetitions=1`
2. confirm there is no large regression
3. rerun with `repetitions=3`
4. focus on:
   - `erp-handling-detailed-guidance-01`
   - `aftercare-reentry-after-deep-intimacy-01`
   - `long-horizon-established-lovers-detail-drift-01`
   - `long-horizon-explicit-memory-drift-01`

Key success signals:

- fewer `empty_response` cases
- fewer `low_context_recall` cases
- fewer `assistantization` cases
- lower volatility in aftercare scenarios
- improved long-horizon stability without cheating the judge

---

## 8. Risks and Tradeoffs

### 8.1 If we optimize only for more explicit detail

Risk:

- short-horizon outputs may improve
- long-horizon consistency may get worse

### 8.2 If we over-regularize sampling

Risk:

- outputs become safer but thinner
- erotic detail density drops

### 8.3 If we skip structured memory

Risk:

- long-horizon intimacy will continue to rely on fabricated memory

---

## 9. Recommendation

If the goal is:

> more stable adult / erotic / sexual output under the current benchmark

the best path is:

1. stage-specific inference control
2. grounded relationship memory
3. multi-candidate generation and reranking
4. then targeted training

One-line summary:

> Use inference control for quick wins, structured memory for stability, and targeted training for long-term reliability.
