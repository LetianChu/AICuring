# Benchmark Spec Index

## Overview

本索引用于串联成人向 companion / ERP benchmark 的核心设计与四份配套规格文档。

建议阅读顺序：

1. `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md`
2. `docs/superpowers/specs/2026-03-28-benchmark-spec-pack-design.md`
3. `docs/persona-card-schema.md`
4. `docs/scenario-suite-spec.md`
5. `docs/judge-rubric.md`
6. `docs/benchmark-report-template.md`

## Document Roles

### Core Architecture

- `docs/superpowers/specs/2026-03-28-adult-companion-benchmark-design.md`
  - 定义 benchmark-first 的总体目标、系统边界与阶段路线。

- `docs/superpowers/specs/2026-03-28-benchmark-spec-pack-design.md`
  - 定义规格包的职责切分、跨文档字段契约与验收标准。

### Input Contracts

- `docs/persona-card-schema.md`
  - 定义 persona 资产结构。

- `docs/scenario-suite-spec.md`
  - 定义 scenario 资产结构。

### Output Contracts

- `docs/judge-rubric.md`
  - 定义 transcript 到评分结果的转换口径。

- `docs/benchmark-report-template.md`
  - 定义评分结果到决策报告的输出结构。

## Canonical Flow

`persona card + scenario spec -> runner -> transcript -> judge rubric -> benchmark report`

## Shared IDs

全链路统一使用：

- `persona_id`, `persona_version`
- `scenario_id`, `scenario_version`
- `rubric_id`, `rubric_version`
- `run_id`
- `report_id`

## Implementation Handoff

后续进入实现计划时，应以本索引为入口，优先确保：

1. 数据模型字段名与文档一致
2. runner 输出能满足 Judge 输入合同
3. Judge 输出能直接映射到报告模板
4. 任意报告结论可追溯到 `run_id` 与 transcript 证据
