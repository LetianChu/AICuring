# Turn Retention Report

## Summary
- x-ai/grok-4.20 currently has the strongest turn-retention score with avg=15.0 and max=15.

## Model Retention Table
| Model | Score | Max Retention | Avg Retention | Main Break Reason |
| --- | --- | --- | --- | --- |
| x-ai/grok-4.20 | 16.5 | 15 | 15.0 | stable |
| grok-4-20-non-reasoning | 16.5 | 15 | 15.0 | stable |
| Kimi-K2-0905 | 16.5 | 15 | 15.0 | stable |
| sophnet-kimi-k2.5 | 16.5 | 15 | 15.0 | stable |
| gemini-3.1-pro-preview | 16.42 | 15 | 15.0 | run_level_detected_recall_drift |
| gpt-5.3-codex | 16.42 | 15 | 15.0 | run_level_detected_recall_drift |
| claude-opus-4-6 | 16.42 | 15 | 15.0 | run_level_detected_recall_drift |
| claude-sonnet-4-6 | 16.42 | 15 | 15.0 | run_level_detected_recall_drift |
| alicloud-minimax-m2.5 | 14.83 | 15 | 13.67 | empty_response |
| claude-haiku-4-5 | 13.75 | 15 | 12.5 | assistantization |
| alicloud-minimax-m2.7 | 8.0 | 15 | 7.5 | empty_response |
| gpt-5.4 | 5.1 | 11 | 6.0 | empty_response |

## Intermediate Data
### Kimi-K2-0905
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### alicloud-minimax-m2.5
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 7, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=7 median=15.0 max=15 avg=13.67
- Break Type Counts: {'empty_response': 1}
- First Unstable Turn Counts: {'8': 1}

### alicloud-minimax-m2.7
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [0, 0, 15, 0, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=0 median=7.5 max=15 avg=7.5
- Break Type Counts: {'empty_response': 3}
- First Unstable Turn Counts: {'1': 3}

### claude-haiku-4-5
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 0, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=0 median=15.0 max=15 avg=12.5
- Break Type Counts: {'assistantization': 1}
- First Unstable Turn Counts: {'1': 1}

### claude-opus-4-6
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### claude-sonnet-4-6
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### gemini-3.1-pro-preview
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### gpt-5.3-codex
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {}

### gpt-5.4
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [2, 1, 11, 8, 6, 8]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=1 median=7.0 max=11 avg=6.0
- Break Type Counts: {'empty_response': 6}
- First Unstable Turn Counts: {'3': 1, '2': 1, '12': 1, '9': 2, '7': 1}

### grok-4-20-non-reasoning
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### sophnet-kimi-k2.5
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

### x-ai/grok-4.20
- Run Count: 6
- Batch Count: 1
- Scenario Count: 6
- Persona Count: 3
- Retention Turns: [15, 15, 15, 15, 15, 15]
- Max Possible Retention Turns: [15, 15, 15, 15, 15, 15]
- Retention Stats: min=15 median=15.0 max=15 avg=15.0
- Break Type Counts: {}
- First Unstable Turn Counts: {}

## Scenario Retention Table
| Model | Scenario | Retention Turns | Max Possible Retention | First Unstable Turn | Break Type |
| --- | --- | --- | --- | --- | --- |
| Kimi-K2-0905 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| Kimi-K2-0905 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| Kimi-K2-0905 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| Kimi-K2-0905 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| Kimi-K2-0905 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| Kimi-K2-0905 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.5 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.5 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.5 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.5 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.5 | romantic-escalation-15-round-retention-01 | 7 | 15 | 8 | empty_response |
| alicloud-minimax-m2.5 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.7 | aftercare-15-round-retention-01 | 0 | 15 | 1 | empty_response |
| alicloud-minimax-m2.7 | explicit-pressure-15-round-retention-01 | 0 | 15 | 1 | empty_response |
| alicloud-minimax-m2.7 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.7 | repair-recovery-15-round-retention-01 | 0 | 15 | 1 | empty_response |
| alicloud-minimax-m2.7 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| alicloud-minimax-m2.7 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| claude-haiku-4-5 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| claude-haiku-4-5 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| claude-haiku-4-5 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| claude-haiku-4-5 | repair-recovery-15-round-retention-01 | 0 | 15 | 1 | assistantization |
| claude-haiku-4-5 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| claude-haiku-4-5 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| claude-opus-4-6 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| claude-opus-4-6 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| claude-opus-4-6 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | run_level_detected_recall_drift |
| claude-opus-4-6 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| claude-opus-4-6 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| claude-opus-4-6 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| claude-sonnet-4-6 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| claude-sonnet-4-6 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| claude-sonnet-4-6 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | run_level_detected_recall_drift |
| claude-sonnet-4-6 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| claude-sonnet-4-6 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| claude-sonnet-4-6 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| gemini-3.1-pro-preview | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| gemini-3.1-pro-preview | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| gemini-3.1-pro-preview | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | run_level_detected_recall_drift |
| gemini-3.1-pro-preview | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| gemini-3.1-pro-preview | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| gemini-3.1-pro-preview | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.3-codex | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.3-codex | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.3-codex | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | run_level_detected_recall_drift |
| gpt-5.3-codex | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.3-codex | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.3-codex | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| gpt-5.4 | aftercare-15-round-retention-01 | 2 | 15 | 3 | empty_response |
| gpt-5.4 | explicit-pressure-15-round-retention-01 | 1 | 15 | 2 | empty_response |
| gpt-5.4 | long-horizon-continuity-15-round-retention-01 | 11 | 15 | 12 | empty_response |
| gpt-5.4 | repair-recovery-15-round-retention-01 | 8 | 15 | 9 | empty_response |
| gpt-5.4 | romantic-escalation-15-round-retention-01 | 6 | 15 | 7 | empty_response |
| gpt-5.4 | warm-companion-15-round-retention-01 | 8 | 15 | 9 | empty_response |
| grok-4-20-non-reasoning | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| grok-4-20-non-reasoning | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| grok-4-20-non-reasoning | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| grok-4-20-non-reasoning | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| grok-4-20-non-reasoning | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| grok-4-20-non-reasoning | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| sophnet-kimi-k2.5 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | aftercare-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | explicit-pressure-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | long-horizon-continuity-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | repair-recovery-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | romantic-escalation-15-round-retention-01 | 15 | 15 | None | stable |
| x-ai/grok-4.20 | warm-companion-15-round-retention-01 | 15 | 15 | None | stable |

## Detailed Findings
- run_c195c3a68c39: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_98194b832a18: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_edf4dcc33e56: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_75b65e07510e: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_8d481c4bab76: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_988c13869720: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_deabd9a0daba: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_ed5753a0c0a8: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_b312971d8804: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_1f98bb5e4eed: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_c9053682459f: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_708183a1cf13: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d626566dcfa0: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_07fffc6f5399: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_9841c087a95c: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_f892f7b6f543: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_cbda734dd88d: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_9c78ae3f5100: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_0cf55794a4d1: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_3567548a46c7: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_41f145766b64: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_1c8e6f87fce6: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_f006de825539: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_d3e72e124a14: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_dbe6b3d5b6cc: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_6ea4ed080284: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_c0180efa1ccc: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_ec003e2e1eb7: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_7e5fa91dccdb: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_5d987cfae7bf: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_aabb3cc6273b: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_7f44cce43c8f: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_8fdc6bf60d8a: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_cb4f4dade5a6: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_d3ad7b880df6: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_a6e840708c49: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_98ad639ed7dc: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_1a0d370e2035: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_a5f16209e6b3: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_feb88f8a76fc: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=1 break_type=assistantization
- run_bc76c2002fa0: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_e71fd7ef3c98: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_e865a63d6acb: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_e27d26316e11: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_655725ce3215: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_cc5c12ca0e59: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_26748e80a6fa: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_eb65566af361: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_0537c1c9fb56: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_50af2eff8c86: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_66994857cb56: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_bfea09956813: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_7961346ca25e: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=8 break_type=empty_response
- run_358b9b698d8c: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_466d49feeff6: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_1b4df87adacf: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_3bb4168d9105: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_6b4fe2acacfe: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_b402c49e0fb9: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_4c1c889e4c79: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_6402cd8f117a: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=1 break_type=empty_response
- run_47389442b5cc: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=1 break_type=empty_response
- run_4527dc8e7f09: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d55e4c6ae76b: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=1 break_type=empty_response
- run_0572f6d3cc60: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_057e86607f9e: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_2928888bfc36: scenario=aftercare-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=3 break_type=empty_response
- run_5de5ba6b5f6d: scenario=explicit-pressure-15-round-retention-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=2 break_type=empty_response
- run_bb189f6099f9: scenario=long-horizon-continuity-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=12 break_type=empty_response
- run_41740287170a: scenario=repair-recovery-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=9 break_type=empty_response
- run_7942413d3101: scenario=romantic-escalation-15-round-retention-01 persona=night-owl-playful-girlfriend first_unstable_turn=7 break_type=empty_response
- run_70e81f29376d: scenario=warm-companion-15-round-retention-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=9 break_type=empty_response
