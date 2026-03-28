# 成人向 Companion / ERP Benchmark 规格包设计文档 v0.1

## 1. 目标

在 `2026-03-28-adult-companion-benchmark-design.md` 的总体架构基础上，补齐一套可直接驱动后续实现与评测执行的“规格包”。

本规格包包含 4 份主文档：

1. `docs/persona-card-schema.md`
2. `docs/scenario-suite-spec.md`
3. `docs/judge-rubric.md`
4. `docs/benchmark-report-template.md`

外加 1 份索引文档：

- `docs/benchmark-spec-index.md`

## 2. 设计原则

### 2.1 混合型规格

每份文档同时覆盖两层内容：

- 概念层：目标、边界、术语、决策用途
- 执行层：字段定义、必填约束、标签口径、输出模板、版本规则

### 2.2 单一职责

每份文档只承担一层“合同职责”，避免互相写入实现细节：

- Persona 文档只定义角色资产
- Scenario 文档只定义测试资产
- Judge 文档只定义评分资产
- Report 文档只定义决策输出资产

### 2.3 可回溯与可复现

文档需支持从“报告结论”回溯至：

- run 元数据
- transcript 证据片段
- scenario/persona/rubric 的具体版本

## 3. 文档边界与衔接

统一流程：

`persona card + scenario spec -> conversation runner -> transcript -> judge rubric -> benchmark report`

边界要求：

- Scenario 通过 `persona_id/persona_version` 引用 persona，不复制人格文本
- Judge 基于 runner 输出评分，不直接依赖 provider 私有字段
- Report 聚合 Judge 结果，不重新定义评分口径

## 4. 跨文档主键与命名规则

### 4.1 全局主键

- `persona_id`, `persona_version`
- `scenario_id`, `scenario_version`
- `rubric_id`, `rubric_version`
- `report_id`, `benchmark_run_batch_id`
- `run_id`

### 4.2 实验元数据主键

- `model_provider`
- `model_name`
- `model_version`
- `sampling_profile_id`
- `executed_at`

### 4.3 命名约束

- ID：`kebab-case`，例如 `warm-companion-basic-v1`
- 标签枚举：`snake_case`，例如 `soft_refusal`
- 版本：日期版 `YYYY-MM-DD`（与当前仓库规范一致）

## 5. 交付内容

### 5.1 Persona Card Schema

必须覆盖：

- 字段定义（类型、必填、默认值、约束）
- 可枚举维度（主动性、亲密度、表达风格等）
- 冲突规则（结构化字段优先于自由文本）
- 至少 3 个示例 persona

### 5.2 Scenario Suite Spec

必须覆盖：

- 5 大场景分类
- 场景模板（目标、轮次、升级点、终止条件、评分重点）
- 固定脚本/半开放脚本执行规则
- 覆盖矩阵与最小样本要求

### 5.3 Judge Rubric

必须覆盖：

- 规则化标签定义（拒答、降级、漂移、截断等）
- Rubric 维度与分档标准
- 证据引用规则
- 抽检与复核流程

### 5.4 Benchmark Report Template

必须覆盖：

- 固定章节模板
- 三种聚合视角（按模型、按场景、按 persona）
- 路由建议输出口径
- 证据索引与风险披露要求

## 6. 非目标

- 不定义任何 provider SDK 或调用代码
- 不绑定数据库实现细节
- 不在本阶段定义产品 UI/前端交互
- 不把“绕过策略”作为正式能力要求

## 7. 验收标准

规格包完成后应满足：

1. 任意实现者仅依据文档即可构建 runner 输入输出模型
2. 任意 reviewer 可依据 rubric 对同一 transcript 得到可比结论
3. 任意报告读者可从结论追溯到 run 与证据
4. 文档间字段命名一致，无重复定义与口径冲突

## 8. 后续衔接

规格包落地后，下一步应基于这些文档编写实现计划，覆盖：

- 目录结构与模块边界
- 数据模型与序列化格式
- runner 执行流程
- judge 管线
- 报告生成流程
