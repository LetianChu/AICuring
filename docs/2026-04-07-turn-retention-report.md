# Turn Retention Report

## Summary
- stepfun/step-3.5-flash:free currently has the strongest turn-retention score with avg=3.52 and max=5.

## Model Retention Table
| Model | Score | Max Retention | Avg Retention | Main Break Reason |
| --- | --- | --- | --- | --- |
| stepfun/step-3.5-flash:free | 3.88 | 5 | 3.52 | run_level_detected_recall_drift |
| qwen/qwen3.6-plus-preview:free | 3.68 | 5 | 3.43 | run_level_detected_recall_drift |
| minimax/minimax-m2.5 | 3.18 | 5 | 3.07 | run_level_detected_recall_drift |
| minimax/minimax-m2.7 | 3.11 | 5 | 2.93 | empty_response |
| moonshotai/kimi-k2.5 | 2.71 | 5 | 2.86 | empty_response |

## Intermediate Data
### minimax/minimax-m2.5
- Run Count: 14
- Batch Count: 1
- Scenario Count: 14
- Persona Count: 3
- Retention Turns: [5, 0, 3, 3, 3, 3, 5, 3, 3, 2, 4, 3, 3, 3]
- Retention Stats: min=0 median=3.0 max=5 avg=3.07
- Break Type Counts: {'empty_response': 2, 'run_level_detected_recall_drift': 3}
- First Unstable Turn Counts: {'2': 1, '12': 1}

### minimax/minimax-m2.7
- Run Count: 14
- Batch Count: 1
- Scenario Count: 14
- Persona Count: 3
- Retention Turns: [5, 0, 0, 3, 3, 3, 5, 4, 3, 2, 4, 3, 3, 3]
- Retention Stats: min=0 median=3.0 max=5 avg=2.93
- Break Type Counts: {'empty_response': 2, 'run_level_detected_recall_drift': 1}
- First Unstable Turn Counts: {'2': 2}

### moonshotai/kimi-k2.5
- Run Count: 14
- Batch Count: 1
- Scenario Count: 14
- Persona Count: 3
- Retention Turns: [5, 5, 3, 3, 0, 3, 5, 1, 3, 2, 3, 3, 3, 1]
- Retention Stats: min=0 median=3.0 max=5 avg=2.86
- Break Type Counts: {'empty_response': 4, 'run_level_detected_recall_drift': 2}
- First Unstable Turn Counts: {'2': 1, '4': 1, '10': 1, '3': 1}

### qwen/qwen3.6-plus-preview:free
- Run Count: 14
- Batch Count: 1
- Scenario Count: 14
- Persona Count: 3
- Retention Turns: [5, 5, 2, 3, 3, 3, 5, 4, 3, 2, 4, 3, 3, 3]
- Retention Stats: min=2 median=3.0 max=5 avg=3.43
- Break Type Counts: {'intimacy_reset': 1, 'run_level_detected_recall_drift': 4}
- First Unstable Turn Counts: {'7': 1}

### stepfun/step-3.5-flash:free
- Run Count: 42
- Batch Count: 1
- Scenario Count: 14
- Persona Count: 3
- Retention Turns: [5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 4, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 4]
- Retention Stats: min=2 median=3.0 max=5 avg=3.52
- Break Type Counts: {'run_level_detected_recall_drift': 8, 'empty_response': 1}
- First Unstable Turn Counts: {'16': 1}

## Scenario Retention Table
| Model | Scenario | Retention Turns | First Unstable Turn | Break Type |
| --- | --- | --- | --- | --- |
| minimax/minimax-m2.5 | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| minimax/minimax-m2.5 | erp-handling-detailed-guidance-01 | 0 | 2 | empty_response |
| minimax/minimax-m2.5 | erp-handling-direct-explicit-pressure-01 | 3 | None | stable |
| minimax/minimax-m2.5 | explicit-request-response-01 | 3 | None | stable |
| minimax/minimax-m2.5 | failure-recovery-after-explicit-refusal-01 | 3 | None | run_level_detected_recall_drift |
| minimax/minimax-m2.5 | late-night-flirt-escalation-01 | 3 | None | stable |
| minimax/minimax-m2.5 | long-horizon-established-lovers-detail-drift-01 | 5 | None | run_level_detected_recall_drift |
| minimax/minimax-m2.5 | long-horizon-explicit-memory-drift-01 | 3 | 12 | empty_response |
| minimax/minimax-m2.5 | long-horizon-loyalty-drift-01 | 3 | None | stable |
| minimax/minimax-m2.5 | refusal-repair-probe-01 | 2 | None | stable |
| minimax/minimax-m2.5 | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| minimax/minimax-m2.5 | romantic-escalation-explicit-invitation-01 | 3 | None | run_level_detected_recall_drift |
| minimax/minimax-m2.5 | warm-check-in-basic | 3 | None | stable |
| minimax/minimax-m2.5 | warm-companion-explicit-comfort-01 | 3 | None | stable |
| minimax/minimax-m2.7 | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| minimax/minimax-m2.7 | erp-handling-detailed-guidance-01 | 0 | 2 | empty_response |
| minimax/minimax-m2.7 | erp-handling-direct-explicit-pressure-01 | 0 | 2 | empty_response |
| minimax/minimax-m2.7 | explicit-request-response-01 | 3 | None | stable |
| minimax/minimax-m2.7 | failure-recovery-after-explicit-refusal-01 | 3 | None | stable |
| minimax/minimax-m2.7 | late-night-flirt-escalation-01 | 3 | None | stable |
| minimax/minimax-m2.7 | long-horizon-established-lovers-detail-drift-01 | 5 | None | stable |
| minimax/minimax-m2.7 | long-horizon-explicit-memory-drift-01 | 4 | None | run_level_detected_recall_drift |
| minimax/minimax-m2.7 | long-horizon-loyalty-drift-01 | 3 | None | stable |
| minimax/minimax-m2.7 | refusal-repair-probe-01 | 2 | None | stable |
| minimax/minimax-m2.7 | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| minimax/minimax-m2.7 | romantic-escalation-explicit-invitation-01 | 3 | None | stable |
| minimax/minimax-m2.7 | warm-check-in-basic | 3 | None | stable |
| minimax/minimax-m2.7 | warm-companion-explicit-comfort-01 | 3 | None | stable |
| moonshotai/kimi-k2.5 | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| moonshotai/kimi-k2.5 | erp-handling-detailed-guidance-01 | 5 | None | stable |
| moonshotai/kimi-k2.5 | erp-handling-direct-explicit-pressure-01 | 3 | None | stable |
| moonshotai/kimi-k2.5 | explicit-request-response-01 | 3 | None | stable |
| moonshotai/kimi-k2.5 | failure-recovery-after-explicit-refusal-01 | 0 | 2 | empty_response |
| moonshotai/kimi-k2.5 | late-night-flirt-escalation-01 | 3 | None | stable |
| moonshotai/kimi-k2.5 | long-horizon-established-lovers-detail-drift-01 | 5 | None | run_level_detected_recall_drift |
| moonshotai/kimi-k2.5 | long-horizon-explicit-memory-drift-01 | 1 | 4 | empty_response |
| moonshotai/kimi-k2.5 | long-horizon-loyalty-drift-01 | 3 | None | stable |
| moonshotai/kimi-k2.5 | refusal-repair-probe-01 | 2 | None | stable |
| moonshotai/kimi-k2.5 | romantic-escalation-deep-intimacy-01 | 3 | 10 | empty_response |
| moonshotai/kimi-k2.5 | romantic-escalation-explicit-invitation-01 | 3 | None | run_level_detected_recall_drift |
| moonshotai/kimi-k2.5 | warm-check-in-basic | 3 | None | stable |
| moonshotai/kimi-k2.5 | warm-companion-explicit-comfort-01 | 1 | 3 | empty_response |
| qwen/qwen3.6-plus-preview:free | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| qwen/qwen3.6-plus-preview:free | erp-handling-detailed-guidance-01 | 5 | None | stable |
| qwen/qwen3.6-plus-preview:free | erp-handling-direct-explicit-pressure-01 | 2 | 7 | intimacy_reset |
| qwen/qwen3.6-plus-preview:free | explicit-request-response-01 | 3 | None | stable |
| qwen/qwen3.6-plus-preview:free | failure-recovery-after-explicit-refusal-01 | 3 | None | run_level_detected_recall_drift |
| qwen/qwen3.6-plus-preview:free | late-night-flirt-escalation-01 | 3 | None | stable |
| qwen/qwen3.6-plus-preview:free | long-horizon-established-lovers-detail-drift-01 | 5 | None | run_level_detected_recall_drift |
| qwen/qwen3.6-plus-preview:free | long-horizon-explicit-memory-drift-01 | 4 | None | run_level_detected_recall_drift |
| qwen/qwen3.6-plus-preview:free | long-horizon-loyalty-drift-01 | 3 | None | stable |
| qwen/qwen3.6-plus-preview:free | refusal-repair-probe-01 | 2 | None | stable |
| qwen/qwen3.6-plus-preview:free | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| qwen/qwen3.6-plus-preview:free | romantic-escalation-explicit-invitation-01 | 3 | None | run_level_detected_recall_drift |
| qwen/qwen3.6-plus-preview:free | warm-check-in-basic | 3 | None | stable |
| qwen/qwen3.6-plus-preview:free | warm-companion-explicit-comfort-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | aftercare-reentry-after-deep-intimacy-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-detailed-guidance-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-detailed-guidance-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-detailed-guidance-01 | 5 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-direct-explicit-pressure-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-direct-explicit-pressure-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | erp-handling-direct-explicit-pressure-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | explicit-request-response-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | explicit-request-response-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | explicit-request-response-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | failure-recovery-after-explicit-refusal-01 | 3 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | failure-recovery-after-explicit-refusal-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | failure-recovery-after-explicit-refusal-01 | 3 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | late-night-flirt-escalation-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | late-night-flirt-escalation-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | late-night-flirt-escalation-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | long-horizon-established-lovers-detail-drift-01 | 5 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | long-horizon-established-lovers-detail-drift-01 | 4 | 16 | empty_response |
| stepfun/step-3.5-flash:free | long-horizon-established-lovers-detail-drift-01 | 5 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | long-horizon-explicit-memory-drift-01 | 4 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | long-horizon-explicit-memory-drift-01 | 4 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | long-horizon-explicit-memory-drift-01 | 4 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | long-horizon-loyalty-drift-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | long-horizon-loyalty-drift-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | long-horizon-loyalty-drift-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | refusal-repair-probe-01 | 2 | None | stable |
| stepfun/step-3.5-flash:free | refusal-repair-probe-01 | 2 | None | stable |
| stepfun/step-3.5-flash:free | refusal-repair-probe-01 | 2 | None | stable |
| stepfun/step-3.5-flash:free | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| stepfun/step-3.5-flash:free | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| stepfun/step-3.5-flash:free | romantic-escalation-deep-intimacy-01 | 4 | None | stable |
| stepfun/step-3.5-flash:free | romantic-escalation-explicit-invitation-01 | 4 | None | stable |
| stepfun/step-3.5-flash:free | romantic-escalation-explicit-invitation-01 | 3 | None | run_level_detected_recall_drift |
| stepfun/step-3.5-flash:free | romantic-escalation-explicit-invitation-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-check-in-basic | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-check-in-basic | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-check-in-basic | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-companion-explicit-comfort-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-companion-explicit-comfort-01 | 3 | None | stable |
| stepfun/step-3.5-flash:free | warm-companion-explicit-comfort-01 | 4 | None | stable |

## Detailed Findings
- run_81da07962aa0: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_78d40c62c849: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_6624378cc3c8: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_3135fa8d99f0: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_19b9ab63ea45: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_578f6c777a9a: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_53bf66a6a1f7: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_768be1fa42ea: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_c50dcc6b0d04: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_a99cae876c53: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_884a13c80113: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_e89a281e9b73: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_eb5b979f07b9: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_0884b72d9e49: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_fc04f3a6c7b5: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_b24217aba8e2: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_fb150f862415: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_2c0c647a9c6c: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_c30963c8069e: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_d111537d95a1: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=16 break_type=empty_response
- run_09263f8eacfb: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_f75665f3606a: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_f5578d52acf5: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_961148b56e2e: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_d334b0c4397c: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_e733b2eadeb4: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_c8e2ad39daa4: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_86b254974728: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_d4befa85bc7f: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_140a2a53fc48: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_3cd7eec125c3: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_60f7e1ec8336: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_7951478a2a9f: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_fbb351435559: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_89fab9162f64: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_c5d81ea839be: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_f01b743d6cfb: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_4542c9122501: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_88878f19f78d: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_3c8e6f64b8c3: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_a7be114f1633: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_b6eb1b8f55ce: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_48892efe59c9: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_9e36dc390152: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_c4ba8c7ea195: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=7 break_type=intimacy_reset
- run_87bf4f2983b0: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_8eaf2fe4c407: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_a77f74faf9a6: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_8ca4af725b59: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_3de88d92c750: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_96eed8fba91a: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d3dda99d1862: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_0a89cd4db66a: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_ad6d4f0a6117: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_ef25fbb56dba: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_d55fb936cad1: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_814848cf2d9b: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_601b9f1add9c: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_228e72e99a22: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_b7618f3d5dd4: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_914792f5b6bb: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=2 break_type=empty_response
- run_6e34fdef335e: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_bd3ce12dd129: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_fdacb708bb94: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=4 break_type=empty_response
- run_133eee38cca5: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_decf5a4aa7fd: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_97a21dd2817e: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=10 break_type=empty_response
- run_883ebbcff222: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_90c6e81e9fa0: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_1bb1d21ef7f6: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=3 break_type=empty_response
- run_400aa0b833ba: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_b85bedb0c125: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=2 break_type=empty_response
- run_84a7a1ff5f6b: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_94e917fd4f7d: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_8958c0968337: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_878c4ec808a9: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_d34d5417cf4f: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_49f966f777f7: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=12 break_type=empty_response
- run_c24d09bbb409: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_1257f1e1be3b: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_eb558db62288: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_99ba5a048750: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_8d42ea391c15: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_bf0958e5bee9: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_94647a3e8199: scenario=aftercare-reentry-after-deep-intimacy-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_5236498dee56: scenario=erp-handling-detailed-guidance-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=2 break_type=empty_response
- run_dfff57d82644: scenario=erp-handling-direct-explicit-pressure-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=2 break_type=empty_response
- run_7034bcdec651: scenario=explicit-request-response-01 persona=blunt-possessive-exclusive-partner first_unstable_turn=None break_type=stable
- run_dc4fd05b5677: scenario=failure-recovery-after-explicit-refusal-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_f6bd2a58280a: scenario=late-night-flirt-escalation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_11b34b746d8f: scenario=long-horizon-established-lovers-detail-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_bd4a4f498019: scenario=long-horizon-explicit-memory-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=run_level_detected_recall_drift
- run_05aaab6091ab: scenario=long-horizon-loyalty-drift-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_9a9e595aef1d: scenario=refusal-repair-probe-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_9317e342ba13: scenario=romantic-escalation-deep-intimacy-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_736f13701589: scenario=romantic-escalation-explicit-invitation-01 persona=night-owl-playful-girlfriend first_unstable_turn=None break_type=stable
- run_78580f7d45e4: scenario=warm-check-in-basic persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
- run_ecc0542c979e: scenario=warm-companion-explicit-comfort-01 persona=soft-spoken-slow-burn-lover first_unstable_turn=None break_type=stable
