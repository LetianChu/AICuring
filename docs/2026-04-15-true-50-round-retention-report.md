# Turn Retention Report

Coverage note: `x-ai/grok-4.20` currently includes `2/6` completed 50-round scenarios only. `sophnet-kimi-k2.5` includes `6/6`. `gpt-5.4` includes `6/6` representative runs selected from mixed provider paths already completed in this worktree.

## Summary
- x-ai/grok-4.20 currently has the strongest turn-retention score with avg=50.0 and max=50.

## Model Retention Table
| Model | Score | Max Retention | Avg Retention | Main Break Reason |
| --- | --- | --- | --- | --- |
| x-ai/grok-4.20 | 55.0 | 50 | 50.0 | stable |
| sophnet-kimi-k2.5 | 54.92 | 50 | 50.0 | run_level_detected_recall_drift |
| gpt-5.4 | 32.5 | 50 | 28.5 | empty_response |

## Intermediate Data
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
- Run Count: 2
- Batch Count: 1
- Scenario Count: 2
- Persona Count: 2
- Retention Turns: [50, 50]
- Max Possible Retention Turns: [50, 50]
- Late Stage Retention Turns: [20, 20]
- Soft Degradation Round Counts: [0, 0]
- Retention Stats: min=50 median=50.0 max=50 avg=50.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

## Scenario Retention Table
| Model | Scenario | Retention Turns | Max Possible Retention | First Unstable Turn | Break Type |
| --- | --- | --- | --- | --- | --- |
| gpt-5.4 | aftercare-50-round-retention-01 | 2 | 50 | 3 | empty_response |
| gpt-5.4 | explicit-pressure-50-round-retention-01 | 4 | 50 | 5 | empty_response |
| gpt-5.4 | long-horizon-continuity-50-round-retention-01 | 15 | 50 | 16 | empty_response |
| gpt-5.4 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.4 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| gpt-5.4 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | long-horizon-continuity-50-round-retention-01 | 50 | 50 | None | run_level_detected_recall_drift |
| sophnet-kimi-k2.5 | repair-recovery-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | romantic-escalation-50-round-retention-01 | 50 | 50 | None | stable |
| sophnet-kimi-k2.5 | warm-companion-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | aftercare-50-round-retention-01 | 50 | 50 | None | stable |
| x-ai/grok-4.20 | explicit-pressure-50-round-retention-01 | 50 | 50 | None | stable |

## Detailed Findings
- run_27406a2ffc02: scenario=aftercare-50-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_b5118a282912: scenario=explicit-pressure-50-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
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
