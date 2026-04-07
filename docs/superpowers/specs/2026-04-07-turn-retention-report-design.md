# 轮次保持报告设计文档 v0.1

## 1. 目标

本文档定义一份新的 benchmark 报告形态，用于回答：

> 不同模型在成人向长轮次对话中，能稳定保持到第几轮，何时开始失稳，以及失稳的主要原因是什么。

这份报告的目标不是替代现有 batch report，而是补上一层更贴近“长轮次稳定性”的结论视图。

---

## 2. 适用范围

当前版本只覆盖已经完整跑完 full batch 的模型。

第一批纳入：

- `stepfun/step-3.5-flash:free`
- `qwen/qwen3.6-plus-preview:free`
- `moonshotai/kimi-k2.5`
- `minimax/minimax-m2.5`
- `minimax/minimax-m2.7`

不纳入：

- 区域受限模型
- 只做过 smoke 的模型
- 证据不足的 partial batch

---

## 3. 核心定义

### 3.1 保持轮次

`保持轮次 = 从对话开始，到首次出现明确失稳信号之前的 assistant turn 数`

例如：

- 如果模型在 assistant `turn 2` 就空回复，则保持轮次为 `0`
- 如果模型直到 assistant `turn 10` 才首次出现失稳，则保持轮次按前面已稳定承接的 assistant turn 数计算

### 3.2 明确失稳信号

优先纳入：

- `empty_response`
- `intimacy_reset`
- `soft_refusal`
- `assistantization`
- `content_hollowing`

这些标签优先作为 `first explicit unstable turn` 的判断依据。

### 3.3 Run-level 失稳

对于以下问题，不总是能精确定位到唯一 turn：

- `low_context_recall`
- `high_context_recall`

当前版本的口径是：

- 如果 run 被这些问题判定 degraded，但没有更早的显式失稳信号
- 则报告中仍保留该 run 为失稳 case
- 但原因标为：
  - `run-level detected recall drift`
  - 或 `run-level detected continuity issue`

换句话说：

> 当前版本允许“失稳已确认，但首个失稳 turn 只可近似定位”。

---

## 4. 总分规则

### 4.1 设计原则

总分采用：

> 保持轮次优先，失稳类型只做扣分

原因：

- 用户当前最关心的是“能稳定保持到多少轮”
- 失稳类型的重要性应该体现在扣分，而不是压过主轴

### 4.2 建议公式

建议总分由两部分构成：

1. `average_retention_turns`
2. `max_retention_turns_bonus`

并辅以失稳扣分：

- `empty_response` 扣分最高
- `assistantization / soft_refusal / intimacy_reset` 次高
- `content_hollowing` 次之
- `low_context_recall` 扣分较轻，但仍保留

当前版本不要求把公式做成严格学术分制，但必须保持：

- 可解释
- 可比较
- 同一版本下可复现

### 4.3 排序原则

模型排序按以下优先级：

1. 总分
2. 平均保持轮次
3. 最大保持轮次
4. 失稳严重度

---

## 5. 报告结构

### 5.1 一句话总结

报告头部必须先给一句话总结，例如：

> `step-3.5` 目前仍是综合最稳的 baseline，而 `M2.7` 是当前最值得继续扩样的付费候选。

### 5.2 头部总表

报告开头必须给总表，至少包含：

| Model | Score | Max Retention | Avg Retention | Main Break Reason |
| --- | --- | --- | --- | --- |

这部分必须一眼能看出：

- 当前排名
- 谁保持得最久
- 谁平均最稳
- 谁最容易怎么坏

### 5.3 模型 x 场景保持表

第二部分必须展示：

> 不同模型在不同场景上的保持轮次

建议字段：

| Model | Scenario | Retention Turns | First Break Turn | Break Type |
| --- | --- | --- | --- | --- |

### 5.4 详细测试报告

第三部分进入明细，至少包括：

- 模型名
- batch id
- scenario id
- persona id
- overall bucket
- recommended fit
- first explicit unstable turn
- unstable label
- evidence excerpt

这部分用于支持“为什么开始不稳定”的结论。

---

## 6. 结论写法

每个模型需要明确回答：

1. 最早大概从第几轮开始坏
2. 最常见是在前段、中段还是后段开始坏
3. 主要是怎么坏
4. 当前是否适合继续留在 baseline 池

例如：

- `step-3.5`：主要是后段 long-horizon drift
- `qwen3.6`：中段 explicit pressure 提前降温
- `kimi-k2.5`：关键节点空掉
- `m2.5`：早段空掉与后段 drift 并存
- `m2.7`：总体更干净，但 explicit handling 仍有早段失败

---

## 7. 非目标

当前版本不做：

- 精确学术打分校准
- turn-level causal attribution 自动化建模
- 替代原始 transcript
- 覆盖不可用或只做 smoke 的模型

---

## 8. 实现建议

建议新增一份专门的 turn-retention report 生成逻辑，而不是把现有 batch report 强行改成这个结构。

原因：

- 现有 report 更适合总体比较
- 新报告更适合“轮次保持”和“失稳起点”分析
- 两者并存更清晰

建议产物：

- `artifacts/comparisons/<report-id>/turn_retention_report.md`
- `artifacts/comparisons/<report-id>/turn_retention_report.json`

---

## 9. 当前推荐

当前最推荐的第一版实现方式：

1. 先生成一份人可读 markdown 报告
2. 配套生成一份机器可读 json
3. 基于现有已完成 batch 先做第一版静态分析
4. 后续再逐步把 `first_unstable_turn`、`break_phase`、`break_type` 系统化
