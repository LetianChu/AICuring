# Turn Retention Report

## Summary
- x-ai/grok-4.20 currently has the strongest turn-retention score with avg=50.0 and max=50.

## Model Retention Table
| Model | Score | Max Retention | Avg Retention | Main Break Reason |
| --- | --- | --- | --- | --- |
| x-ai/grok-4.20 | 55.0 | 50 | 50.0 | stable |
| gemini-3.1-pro-preview | 55.0 | 50 | 50.0 | stable |
| claude-opus-4-6 | 55.0 | 50 | 50.0 | stable |
| grok-4-20-non-reasoning | 55.0 | 50 | 50.0 | stable |
| claude-sonnet-4-6 | 55.0 | 50 | 50.0 | stable |
| claude-haiku-4-5 | 55.0 | 50 | 50.0 | stable |
| Kimi-K2-0905 | 55.0 | 50 | 50.0 | stable |
| qwen3.6-plus | 55.0 | 50 | 50.0 | stable |
| gpt-5.3-codex | 54.92 | 50 | 50.0 | run_level_detected_recall_drift |
| sophnet-kimi-k2.5 | 54.92 | 50 | 50.0 | run_level_detected_recall_drift |
| gpt-5.4 | 32.5 | 50 | 28.5 | empty_response |

## Intermediate Data
### Kimi-K2-0905
- Run Count: 6
- Batch Count: 2
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### claude-haiku-4-5
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### claude-opus-4-6
- Run Count: 6
- Batch Count: 2
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### claude-sonnet-4-6
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### gemini-3.1-pro-preview
- Run Count: 6
- Batch Count: 3
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### gpt-5.3-codex
- Run Count: 6
- Batch Count: 2
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### gpt-5.4
- Run Count: 6
- Batch Count: 4
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [2, 4, 15, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=2 median=32.5 max=50 avg=28.5
- Break Type Counts: {'empty_response': 3}
- First Unstable Turn Counts: {'3': 1, '5': 1, '16': 1}

### grok-4-20-non-reasoning
- Run Count: 6
- Batch Count: 2
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### qwen3.6-plus
- Run Count: 2
- Batch Count: 1
- Scenario Count: 2
- Persona Count: 1
- Retention Turns: [50, 50]
- Max Possible Retention Turns: [50, 50]
- Late Stage Retention Turns: [20, 20]
- Soft Degradation Round Counts: [0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### sophnet-kimi-k2.5
- Run Count: 6
- Batch Count: 3
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### x-ai/grok-4.20
- Run Count: 6
- Batch Count: 2
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [50, 50, 50, 50, 50, 50]
- Max Possible Retention Turns: [50, 50, 50, 50, 50, 50]
- Late Stage Retention Turns: [20, 20, 20, 20, 20, 20]
- Soft Degradation Round Counts: [0, 0, 0, 0, 0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

## Scenario Retention Table
| Model | Scenario | Retention Turns | Max Possible Retention | First Unstable Turn | Break Type |
| --- | --- | --- | --- | --- | --- |
| Kimi-K2-0905 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| Kimi-K2-0905 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| Kimi-K2-0905 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| Kimi-K2-0905 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| Kimi-K2-0905 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| Kimi-K2-0905 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| claude-haiku-4-5 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| claude-opus-4-6 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| claude-sonnet-4-6 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| gemini-3.1-pro-preview | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.3-codex | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.3-codex | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.3-codex | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | run_level_detected_recall_drift |
| gpt-5.3-codex | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.3-codex | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.3-codex | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.4 | aftercare-50-round-retention-01 | 2 | 50 | 3 | empty_response |
| gpt-5.4 | explicit-pressure-50-round-retention-01 | 4 | 50 | 5 | empty_response |
| gpt-5.4 | long-horizon-continuity-50-round-retention-01 | 15 | 50 | 16 | empty_response |
| gpt-5.4 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.4 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.4 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| grok-4-20-non-reasoning | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| qwen3.6-plus | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| qwen3.6-plus | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | run_level_detected_recall_drift |
| sophnet-kimi-k2.5 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |

## Detailed Findings
- run_27406a2ffc02: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_b5118a282912: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_4a12e57468b9: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_7e2a8224b9ad: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_ca41c08f6b76: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_8d4494240815: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_2003e8ed3698: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d80706a90913: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_9eaaf5fe3676: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_52f77cef8d9e: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_57a4b0a76b5c: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_59b66c81f042: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_f429b7f0d411: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_3d112d58c074: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_f5ffa295bc7a: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_1accdc523d78: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_28b764605e0c: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_da9261337d0a: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_b2378c293e93: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_9e6efe3e4839: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_f7737653a7d4: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_97672eb7979f: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_328d3e83e18a: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_1d806ac102ed: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_2a9c65dd62a8: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_fbc28476c2c3: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_c19a64d45944: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_55d391aa6081: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_07785d155a6c: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_42feda9ddd36: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_7f09564838d3: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_25c14fc16a15: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_420fd20bdb77: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_e42f1068eddb: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_24d60aeb1b4e: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_bd6f9c64f895: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_2c248c3354cd: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_3d46a961602f: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_53d24d68b918: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_5d8fbcfd0521: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_ae1d78f37d2b: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_fb48f242996a: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_0ee4637642f1: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_15db396eeb35: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_614a97950f99: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_435ccce3aed6: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_e108500e914d: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_1586fa1013a5: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_58b1238223ab: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d5685876e43f: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_9626910c05e2: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_7b858306d8f2: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_7e813cecc470: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_05d0a1cf2a78: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_156c5c16aba6: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=3 break_type=empty_response
- run_2c7462113ee0: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=5 break_type=empty_response
- run_1e33fa0253db: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=16 break_type=empty_response
- run_b9dd51455245: scenario=repair-recovery-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_2b067e291d8b: scenario=romantic-escalation-50-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_8dd0323b9be0: scenario=warm-companion-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_395d90d2dfeb: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_f924e0652309: scenario=long-horizon-continuity-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
