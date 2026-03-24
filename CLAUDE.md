# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current repository state

- This repository is currently **documentation-first**. There is no application scaffold, package manifest, build pipeline, or test harness checked in yet.
- The main source of truth is `docs/depression-patient-simulator-tech-plan.md`.
- Do not assume Python/Node/Go/etc. tooling exists until the user adds it.

## Commands

There are currently **no build, lint, or test commands defined in the repository**.

That means:
- There is no supported build command yet.
- There is no supported lint command yet.
- There is no supported full-test or single-test command yet.

Until implementation code is added, the most useful repo-level commands are:

```bash
git status
git log --oneline --decorate -5
git diff
ls docs
```

When code is introduced later, update this file with the real build/lint/test commands instead of inventing stack-specific defaults.

## High-level architecture

The current project intent is defined in `docs/depression-patient-simulator-tech-plan.md`.

The planned system is a **depression patient simulator** used to train or evaluate a separate support / therapy-oriented AI. It is **not** framed as a direct-to-patient therapeutic app in the current design.

### Intended system pipeline

The design doc proposes this top-level flow:

1. **Patient Archetype / Persona**
2. **Persona Builder**
3. **Hidden State Engine**
4. **Intent Planner**
5. **Expression Retrieval**
6. **Response Generator**
7. **Safety Reviewer + Clinical Consistency Reviewer**
8. **Evaluator / Logger**

Future code should preserve these boundaries where practical instead of collapsing everything into a single prompt or one large service.

### Core design assumptions

The design doc emphasizes a few architectural rules that should shape future implementation work:

- **Structure before style**: define who the patient is and what state they are in before generating text.
- **State before text**: prefer internal state / intent representations over direct free-form roleplay.
- **Controlled risk handling**: higher-risk expressions should be constrained by tiers, templates, retrieval, and review layers rather than unrestricted generation.
- **Realism means consistency**: the target is not “more extreme” output, but stable persona, plausible symptom expression, and coherent multi-turn progression.

### Recommended implementation direction

The design doc compares several approaches and currently recommends combining:

- **Persona + hidden state**
- **Two-stage generation** (intent/semantic structure first, natural language second)
- **Expression library / retrieval augmentation**

Later phases may add:
- state-machine / course-of-illness progression
- multi-agent review modules
- distilled or fine-tuned simulator models

### Risk model

The planned simulator uses explicit risk stratification:

- **Level 0-1**: low risk, more flexible generation
- **Level 2**: medium risk, stronger control via staged generation and retrieval
- **Level 3**: high risk, tightly controlled / template-heavy generation

Future implementations should keep risk level explicit in data models and generation interfaces.

## File-level orientation

At the moment, the only substantive project artifact is:

- `docs/depression-patient-simulator-tech-plan.md` — architecture, approach comparison, and phased implementation direction

The design doc also names likely future companion documents:
- `docs/patient_schema.md`
- `docs/state_machine.md`
- `docs/expression_library_schema.md`
- `docs/evaluation_protocol.md`

If those files are added later, treat them as part of the architecture contract and update this file accordingly.

## Working guidance for future Claude instances

- Start by reading `docs/depression-patient-simulator-tech-plan.md` before proposing code structure.
- Do not fabricate runtime commands or stack assumptions that are not present in the repo.
- If scaffolding begins, keep module boundaries aligned with the planned pipeline (persona, state, intent, retrieval, generation, review, evaluation) rather than organizing purely by framework defaults.
