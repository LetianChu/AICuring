# 2026-04-10 全量已完成 15-Turn 模型报告

## 目的

这份文档是一个**独立的 15-turn 专项报告**。

它和之前的混合 retention 报告分开，原因很简单：

- 之前那份报告里混有旧 baseline 场景
- 这份报告只看 `long_horizon_15_turn` 这 6 条 dedicated 15-turn 场景

换句话说，这份文档只回答一个问题：

> 到 2026-04-10 为止，仓库里哪些模型已经完整跑完了 15-turn 套件，它们在这套 15-turn 场景上的结果到底如何。

## 纳入口径

本报告只纳入满足以下条件的模型：

1. 已完整跑完 `long_horizon_15_turn`
2. 6 条 15-turn 场景都有有效 run
3. 能被统一折算到同一份 15-turn retention 口径中

本次纳入总数：

- `13` 个模型

其中来源分成两类：

- **AIHubMix 15-turn-only 批次**
  - `Kimi-K2-0905`
  - `sophnet-kimi-k2.5`
  - `qwen3.6-plus`
  - `alicloud-minimax-m2.5`
  - `alicloud-minimax-m2.7`
- **已完整跑完 20 场景混合批次，但本报告只抽取其中 15-turn 子集**
  - `claude-opus-4-6`
  - `claude-haiku-4-5`
  - `claude-sonnet-4-6`
  - `gemini-3.1-pro-preview`
  - `gpt-5.3-codex`
  - `gpt-5.4`
  - `grok-4-20-non-reasoning`
  - `x-ai/grok-4.20`

## 不纳入项

以下尝试不纳入本报告：

- `gpt-5.4-pro`
  - 未完整跑完 15-turn
- `gemini-3-flash-preview-free`
  - 未完整跑完 15-turn
- `grok-4-20-reasoning`
  - AIHubMix 路径未跑通完整 15-turn
- 只做过旧 baseline、没有 dedicated 15-turn 完整批次的模型
  - 例如当前仓库里的 `stepfun/step-3.5-flash:free`

## 核心结论

### 1. 现在已经不是“谁能跑完 15-turn”的问题了

在当前纳入的 `13` 个模型里：

- `11` 个模型在 15-turn retention 指标上**完全同分**
- 它们都达到：
  - `Score = 7.62`
  - `Avg Retention = 7.0`
  - `Max Retention = 7`

这意味着：

> 仅靠当前这套 15-turn retention 指标，已经无法继续拉开这 11 个模型之间的差距。

### 2. 现在真正落后的只有两类

明显弱于第一梯队的只有：

- `alicloud-minimax-m2.7`
- `gpt-5.4`

其中：

- `alicloud-minimax-m2.7` 的问题是单点失稳
- `gpt-5.4` 的问题是两条关键 15-turn 场景上出现 `empty_response`

### 3. 第一梯队也不是“没有问题”

虽然第一梯队在 retention 数字上是满分：

- `Kimi-K2-0905`
- `sophnet-kimi-k2.5`
- `qwen3.6-plus`
- `alicloud-minimax-m2.5`
- `claude-opus-4-6`
- `claude-haiku-4-5`
- `claude-sonnet-4-6`
- `gemini-3.1-pro-preview`
- `gpt-5.3-codex`
- `grok-4-20-non-reasoning`
- `x-ai/grok-4.20`

但它们仍然共享一个残留问题：

- `long-horizon-continuity-15-turn-retention-01`
- break type 通常仍标记为 `run_level_detected_recall_drift`

也就是说：

- 它们没有在 15-turn 内显式断掉
- 但并不等于“高上下文 continuity 已经完全没有问题”

## 排名总表

| Rank Group | Model | Provider Path | Batch | Score | Avg Retention | Max Retention | Main Break Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | `x-ai/grok-4.20` | `openrouter` | `batch_11e4cd83a118` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `gemini-3.1-pro-preview` | `openai / aihubmix-live` | `batch_152b2b5fdcbc` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `gpt-5.3-codex` | `openai / aihubmix-live` | `batch_1fa52ece2193` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `claude-opus-4-6` | `openai / aihubmix-live` | `batch_4e3ada93a46f` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `grok-4-20-non-reasoning` | `openai / aihubmix-live` | `batch_6bb4ba14f5a9` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `claude-sonnet-4-6` | `openai / aihubmix-live` | `batch_c436a15ba4d2` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `claude-haiku-4-5` | `openai / aihubmix-live` | `batch_d91e66ff73c1` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `Kimi-K2-0905` | `aihubmix` | `batch_a3c77bf03f97` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `qwen3.6-plus` | `aihubmix` | `batch_4aeca808476d` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `alicloud-minimax-m2.5` | `aihubmix` | `batch_7f6f12c34248` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| A | `sophnet-kimi-k2.5` | `aihubmix` | `batch_5a1dd375c07a` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| B | `alicloud-minimax-m2.7` | `aihubmix` | `batch_6fb113435b2e` | `6.53` | `6.17` | `7` | `run_level_detected_recall_drift` |
| C | `gpt-5.4` | `openai / aihubmix-live` | `batch_2b6f5ff302df` | `5.45` | `5.5` | `7` | `empty_response` |

## 分组解释

### A 组：15-turn retention 满分组

这 `11` 个模型全部满足：

- 6 条 15-turn 场景 retention 全部达到 `7`
- 没有显式 `empty_response`
- 没有显式 `intimacy_reset`
- 唯一保留的共性问题是 `long-horizon-continuity` 上的 run-level recall drift 标记

这组模型当前的结论不是“谁最好”，而是：

> 当前这套 15-turn retention benchmark 只足够把它们一起筛进第一梯队，还不足以把它们彼此排序开。

### B 组：单点失稳组

`alicloud-minimax-m2.7` 的整体表现并不差，但它在一条关键场景上掉得很明显：

- `romantic-escalation-15-turn-retention-01`
- retention `2 / 7`
- first unstable turn `6`
- break type `intimacy_reset`

这说明它不是普遍崩，而是：

- 大多数 15-turn 场景还能撑住
- 但在亲密升级链路上更容易突然掉出既定关系态

### C 组：空响应风险组

`gpt-5.4` 是这份报告里最明显的弱项：

- `explicit-pressure-15-turn-retention-01`
  - retention `1 / 7`
  - first unstable turn `4`
  - break type `empty_response`
- `warm-companion-15-turn-retention-01`
  - retention `4 / 7`
  - first unstable turn `10`
  - break type `empty_response`

所以它的问题不是单一场景上的小波动，而是：

- 在 15-turn 套件里已经出现两条明确的空响应断裂
- 这会直接影响长会话中的可用性判断

## 场景层结论

### 最稳定的共同模式

在第一梯队模型中，以下 5 条场景基本全部是满保持：

- `aftercare-15-turn-retention-01`
- `explicit-pressure-15-turn-retention-01`
- `repair-recovery-15-turn-retention-01`
- `romantic-escalation-15-turn-retention-01`
- `warm-companion-15-turn-retention-01`

### 最常见的残留问题

真正持续留下来的共性弱点还是：

- `long-horizon-continuity-15-turn-retention-01`

它没有把多数第一梯队模型打断，但仍然会留下：

- `run_level_detected_recall_drift`

因此当前 15-turn 的下一步重点不应该只是“继续看谁能跑完”，而是：

- 看谁在 continuity 上更自然
- 看谁虽然 retention 满了，但实际 transcript 已经开始发虚

## 对当前选型的含义

### 1. retention 已经不够区分头部模型

如果只看这份 15-turn 报告：

- Claude
- Grok
- Gemini
- GPT-5.3 Codex
- Kimi K2.5 / K2-0905
- Qwen 3.6 Plus
- MiniMax M2.5

都处在同一个 retention ceiling。

所以后续真正该补的是二级区分指标，例如：

- transcript 细节密度
- intimacy continuity 的自然程度
- 风格稳定性
- “不空但发虚”的 content hollowing 倾向
- 延迟 / 成本 / 供应稳定性

### 2. 当前不建议优先追的两个模型

如果只基于现有 15-turn 结果：

- `gpt-5.4`
- `alicloud-minimax-m2.7`

都不应排在当前第一优先扩样名单最前面。

原因分别是：

- `gpt-5.4`：已经出现多条 `empty_response`
- `alicloud-minimax-m2.7`：在 romantic escalation 链路上有明确 `intimacy_reset`

## 报告边界

这份文档只覆盖：

- 已完整完成的 15-turn 模型
- 且只统计 dedicated 15-turn 场景

它**不等于**：

- 旧 baseline 全量模型排名
- 全场景综合能力排名
- 最终产品主模型结论

更准确地说，这份报告是：

> “当前已完成 15-turn 套件的模型里，谁已经达到 retention ceiling，谁还明显没达到”的一次独立整理。
