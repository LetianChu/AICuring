# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current repository state

- This repository is currently **documentation-first**. There is no application scaffold, package manifest, build pipeline, or test harness checked in yet.
- The current design source of truth is `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md`.
- Earlier depression-simulator documents remain in the repo as historical background and reference material.
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

The current project intent is defined in `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md`.

The planned system is an **adult companion / ERP model benchmarking platform**. The current phase is explicitly benchmark-first rather than a direct-to-user product build.

### Intended system pipeline

The design doc proposes this top-level flow:

1. **Persona Cards**
2. **Scenario Specs**
3. **Benchmark Registry**
4. **Conversation Runner**
5. **Model Adapters**
6. **Transcript + Metadata Store**
7. **Judge / Scoring Layer**
8. **Reports**
9. **Product Routing Decision**

Future code should preserve these boundaries where practical instead of collapsing everything into a single prompt or one large service.

### Core design assumptions

The design doc emphasizes a few architectural rules that should shape future implementation work:

- **Evidence before model choice**: do benchmark work before committing to a product stack.
- **Multi-turn before single-turn**: prioritize long-horizon conversation behavior over isolated prompt wins.
- **Scenario isolation**: keep persona, scenario, runner, adapters, judging, and reporting modular.
- **Reproducibility first**: record provider, model version, parameters, persona version, scenario version, and transcripts for every run.

### Recommended implementation direction

The design doc recommends combining:

- **Standardized scenario suites**
- **Reusable persona cards**
- **Provider-agnostic model adapters**
- **Transcript capture plus structured scoring**
- **Benchmark reports that directly inform routing / architecture decisions**

Later phases may add:
- long-horizon conversation evaluation
- hybrid routing experiments
- product prototype validation based on benchmark results

## File-level orientation

At the moment, the main substantive project artifacts are:

- `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md` — current architecture, benchmark scope, and phased direction
- `docs/depression-patient-simulator-tech-plan.md` — prior project direction kept for historical reference
- `docs/model-alignment-expression-strategies.md` — prior notes on alignment constraints that may still inform evaluation design

The new design doc names likely future companion documents:
- `docs/persona-card-schema.md`
- `docs/scenario-suite-spec.md`
- `docs/judge-rubric.md`
- `docs/benchmark-report-template.md`

These documents now exist, along with:
- `docs/benchmark-spec-index.md`
- `docs/superpowers/specs/2026-03-28-benchmark-spec-pack-design.md`

If those files are added later, treat them as part of the architecture contract and update this file accordingly.

## Working guidance for future Claude instances

- Start by reading `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md` before proposing code structure.
- Treat the earlier depression-simulator documents as background, not current product direction, unless the user explicitly reopens that line of work.
- Do not fabricate runtime commands or stack assumptions that are not present in the repo.
- If scaffolding begins, keep module boundaries aligned with the benchmark pipeline (persona, scenario, runner, adapters, scoring, reporting) rather than organizing purely by framework defaults.
