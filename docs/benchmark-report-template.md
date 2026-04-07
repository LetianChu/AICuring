# Benchmark Report Template

## 1. Purpose

本文件定义 benchmark 报告的固定结构、最小字段集合、结论口径与证据引用要求。

报告的目标不是展示大量 transcript，而是把实验结果转化为模型选择、路由设计与下一阶段验证决策。

本模板对应的是当前默认的 batch / comparison 报告。
如果目标是分析：

- 保持到第几轮才开始失稳
- 最早失稳 turn
- 不同模型在不同场景里的 retention turns

则应使用独立的 `turn retention report` 作为补充，而不是强行塞进这份默认模板。

## 2. Non-Goals

- 不重做 Judge 打分
- 不替代原始 transcript 存储
- 不把营销式总结当评测结论
- 不省略实验配置与版本信息

## 3. Report Metadata

每份报告必须包含：

| Field | Description |
| --- | --- |
| `report_id` | 报告唯一 ID |
| `report_version` | 报告模板版本 |
| `generated_at` | 生成时间 |
| `benchmark_run_batch_id` | 本次批量运行 ID |
| `comparison_scope` | 多 batch 对比时包含 `batch_ids` 等比较范围 |
| `rubric_id` / `rubric_version` | 使用的评分口径 |
| `date_window` | 覆盖实验日期范围 |
| `models_in_scope` | 纳入模型列表 |
| `personas_in_scope` | 纳入 persona 列表 |
| `scenarios_in_scope` | 纳入 scenario 列表 |

## 4. Fixed Report Sections

### 4.1 Executive Summary

必须回答：

- 哪些模型总体可用
- 哪些模型明显不适合
- 哪些模型仅适合 warm companion
- 是否存在清晰的多模型路由信号

### 4.2 Experiment Scope and Configuration

必须列出：

- 模型/provider/version
- scenario/persona/rubric 版本
- 采样配置
- 重复运行次数
- 已知限制

### 4.3 Results by Model

每个模型至少展示：

- 总体评级
- 各大场景平均表现
- 主要失败模式
- 波动情况
- 是否建议进入下一阶段

### 4.4 Results by Scenario

必须回答：

- 哪类 scenario 最容易触发失败
- 哪类 scenario 区分度最高
- 长对话与升级场景表现是否分化

### 4.5 Results by Persona

必须回答：

- 模型是否对不同 persona 表现不均
- 是否存在“某 persona 稳定、另一 persona 塌陷”的情况

### 4.6 Failure Mode Analysis

汇总关键失败模式：

- `hard_refusal`
- `soft_refusal`
- `policy_masked_compliance`
- `content_hollowing`
- `assistantization`
- `persona_drift`
- `intimacy_reset`
- `tone_flattening`
- `abrupt_truncation`
- `failed_recovery`

### 4.7 Routing Recommendation

输出产品决策建议：

- `single_model_candidate`
- `companion_and_erp_split_recommended`
- `companion_only_candidate`
- `not_ready_for_product_validation`

### 4.8 Appendix and Evidence Index

必须附：

- 关键 run 索引
- 典型 transcript 引用
- 风险说明

## 5. Conclusion Buckets

模型结论必须区分以下三档：

- `allowed_and_stable`
- `allowed_but_degraded`
- `blocked_or_unstable`

不允许把“偶尔成功”直接写成“可用”。

## 6. Required Tables

### 6.1 Model Summary Table

| Model | Overall Bucket | Best Use Case | Worst Failure Mode | Volatility | Recommendation |
| --- | --- | --- | --- | --- | --- |

### 6.2 Scenario Category Table

| Scenario Category | Avg Score | Common Failure | Recovery Pattern | Decision Signal |
| --- | --- | --- | --- | --- |

### 6.3 Persona Sensitivity Table

| Persona | Strong Models | Weak Models | Key Drift Pattern | Notes |
| --- | --- | --- | --- | --- |

实现早期如果还没有完整的强弱模型枚举，至少应输出：

| Persona | Overall Bucket | Runs | Notes |
| --- | --- | --- | --- |

## 7. Recommendation Writing Rules

### 7.1 Evidence-Bound Recommendations

每条建议必须绑定证据来源，不允许只写主观看法。

### 7.2 Distinguish Capability From Product Fit

即使模型“能回复”，如果人格漂移严重、波动大或恢复能力差，也不应推荐进入产品验证。

### 7.3 State Limits Explicitly

报告必须单独写明：

- 样本量限制
- provider 策略变动风险
- rubric 主观性残留风险
- 尚未覆盖的场景

## 8. Example Report Outline

```md
# Benchmark Report: 2026-03-28 Batch A

## Executive Summary
- Model X is the strongest candidate for warm companion scenarios.
- Model Y handles explicit escalation better but shows high volatility.
- No single model is yet strong enough across all categories.

## Scope
- 4 models
- 5 personas
- 22 scenarios
- 3 repetitions per case

## By Model
...

## By Scenario
...

## By Persona
...

## Failure Modes
...

## Routing Recommendation
- Split companion and ERP layers.

## Evidence Index
...
```

## 9. Minimum Narrative Requirements

每份正式报告至少要回答以下问题：

1. 哪些模型完全不适合当前目标
2. 哪些模型可以进入下一阶段验证
3. 是否支持单模型路线
4. 如果不支持，路由应如何拆层
5. 后续最值得补测的空白场景是什么

## 10. Publication and Versioning

### 10.1 Versioning

以下情况必须升模板版本：

- 固定章节变化
- 结论分档变化
- 必填表格字段变化

### 10.2 Report Comparability

跨报告比较时必须同时检查：

- rubric 版本是否一致
- scenario/persona 版本是否一致
- provider/model 版本是否一致
- baseline import 所使用的 transcript/metadata 映射口径是否一致

不满足条件时，报告中必须标注“不可直接对比”。
