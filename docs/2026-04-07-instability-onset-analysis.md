# 2026-04-07 Instability Onset Analysis

## 中文总结

### 目的

本文档回答两个问题：

1. 当前 baseline 池里的模型，大致跑到多少轮开始不稳定
2. 它们为什么开始不稳定

本分析只覆盖已经完整跑完 full batch 的模型：

- `stepfun/step-3.5-flash:free`
- `qwen/qwen3.6-plus-preview:free`
- `moonshotai/kimi-k2.5`
- `minimax/minimax-m2.5`
- `minimax/minimax-m2.7`

### 方法说明

这里要先说明一个口径：

- 某些失稳是可以直接精确定位到 turn 的
  - `empty_response`
  - `intimacy_reset`
- 某些失稳目前更偏 run-level 检测
  - `low_context_recall`
  - `high_context_recall`

所以本文里的“开始不稳定”分成两类：

1. `First explicit unstable turn`
   - 指 transcript 里第一次出现可明确定位的异常 turn
2. `Run-level instability`
   - 指模型整体被判 degraded，但当前证据更像是整条 run 的 recall / continuity 问题，不能总是精确压到唯一一个首轮失稳 turn

换句话说：

> 对 `empty_response` / `intimacy_reset` 这类问题，我们能较明确回答“从第几轮开始坏”。  
> 对 `memory drift` 这类问题，我们更准确的说法是“在这个场景的中后段开始显著暴露问题”。

### 总览结论

当前模型的失稳形态大致可以分成三类：

1. **后段漂移型**
   - 前面能接住，后面在长轮次 continuity / memory 上开始塌
   - 代表：`step-3.5`

2. **中段降温型**
   - 在明确升级或 explicit pressure 中段就会开始掉质
   - 代表：`qwen3.6-plus-preview`

3. **节点空掉型**
   - 不是慢慢变差，而是在某些关键节点突然空响应
   - 代表：`kimi-k2.5`、`minimax m2.5`、`minimax m2.7`

### 模型逐条分析

#### 1. `stepfun/step-3.5-flash:free`

#### 大致从第几轮开始不稳定

- 如果看显式异常，最明显的首个异常点往往在较后段
- 当前可明确定位的显式首个异常样本出现在 `turn 16`
- 更常见的失稳不是早段，而是长轮次中后段

#### 为什么开始不稳定

主因是：

- `low_context_recall`
- 少量后段 `empty_response`

也就是说：

- 它前面不是接不住
- 而是对话拉长后，记忆和关系连续性开始撑不住

#### 典型形态

- `long-horizon-explicit-memory-drift-01`
- `long-horizon-established-lovers-detail-drift-01`

这类场景的共性是：

- 要求模型在强关系前提下持续保留细节
- 一旦记忆锚点丢掉，质量就会整体掉下去

#### 结论

> `step-3.5` 的失稳主要是“后段 continuity 漂移”，不是“前面就不敢写”。

#### 2. `qwen/qwen3.6-plus-preview:free`

#### 大致从第几轮开始不稳定

- 当前最清晰的显式失稳点是 `turn 7`
- 这意味着它会比 `step-3.5` 更早进入不稳定区

#### 为什么开始不稳定

两类原因都存在：

- `intimacy_reset`
- `low_context_recall`

其中比较危险的是：

- 它不是只在长轮次后段掉
- 在 explicit pressure 场景的中段就可能开始降温或改道

#### 典型形态

- `erp-handling-direct-explicit-pressure-01` 在 `turn 7` 触发 `intimacy_reset`
- 其他 degraded case 则继续落在 long-horizon memory / detail drift

#### 结论

> `qwen3.6` 的问题不只是后段 drift，还包括中段 explicit pressure 下的提前降温。

#### 3. `moonshotai/kimi-k2.5`

#### 大致从第几轮开始不稳定

- 最早能在 `turn 2` 就出现
- 中位大概在 `turn 3-4`
- 最晚能拖到 `turn 10`

这说明它的失稳不是单一位置，而是：

- 某些场景一开始就会空掉
- 某些场景到后面才突然掉

#### 为什么开始不稳定

主因非常集中：

- `empty_response`

相比 `step-3.5` 和 `qwen3.6`，它的问题更像：

- 不是先出现风格漂移
- 而是关键节点直接没有输出

#### 典型形态

- `failure-recovery-after-explicit-refusal-01`：`turn 2` 就可能空掉
- `warm-companion-explicit-comfort-01`：`turn 3` 早段失稳
- `romantic-escalation-deep-intimacy-01`：可到 `turn 10` 才空掉

#### 结论

> `Kimi K2.5` 的不稳定更像“节点式断路”，不是连续性慢慢变差。

#### 4. `minimax/minimax-m2.5`

#### 大致从第几轮开始不稳定

- 最早可在 `turn 2`
- 也会出现在 `turn 12`
- 当前样本呈现“双峰”特征：
  - 一类很早掉
  - 一类拖到长轮次后段才掉

#### 为什么开始不稳定

主因是两类：

- `empty_response`
- `low_context_recall`

所以它同时有：

- early failure
- late memory drift

#### 典型形态

- `erp-handling-detailed-guidance-01`：前段空掉
- `long-horizon-explicit-memory-drift-01`：后段 recall / output 失稳

#### 结论

> `M2.5` 不是单一弱点，而是早段稳定性和后段 continuity 都存在问题。

#### 5. `minimax/minimax-m2.7`

#### 大致从第几轮开始不稳定

- 当前可明确定位的显式失稳往往很早
- 典型是 `turn 2`

#### 为什么开始不稳定

主因是：

- `empty_response`
- 少量 `low_context_recall`

和 `M2.5` 比起来：

- 总体 degraded case 更少
- 但一旦失稳，仍然可能非常早

#### 典型形态

- `erp-handling-detailed-guidance-01`
- `erp-handling-direct-explicit-pressure-01`

这两类都可能在很早段就空掉

#### 结论

> `M2.7` 比 `M2.5` 更干净，但仍有“前段直接失稳”的问题。

### 跨模型对比

#### 谁最晚开始不稳定

当前最像“晚段才开始坏”的，是：

- `stepfun/step-3.5-flash:free`

这也是为什么它依然是最强 baseline。

#### 谁最早开始不稳定

最容易很早就出问题的，是：

- `moonshotai/kimi-k2.5`
- `minimax/minimax-m2.5`
- `minimax/minimax-m2.7`

它们的问题主要是 `empty_response`。

#### 谁是中段开始降温

- `qwen/qwen3.6-plus-preview:free`

它的问题不只在最后面，而是在 explicit pressure 中段就可能 `intimacy_reset`。

### 为什么这些模型会开始不稳定

当前证据下，主要原因可以归成三类：

#### 1. Long-horizon memory drift

表现为：

- 记忆锚点不稳定
- 关系细节延续性下降
- 越往后越容易掉到 `warm_companion_only`

典型模型：

- `step-3.5`
- `qwen3.6`
- `M2.5`
- `M2.7`

#### 2. Early-stage empty response

表现为：

- 模型不是明确拒答
- 而是在关键节点突然返回空输出

典型模型：

- `Kimi K2.5`
- `M2.5`
- `M2.7`

#### 3. Mid-turn intimacy reset

表现为：

- 对话还在继续
- 但 intimacy / explicit progression 被中途拉回

当前最明显的样本来自：

- `qwen3.6-plus-preview`

### 当前建议

如果目标是：

> 评估模型“在长轮次成人向输出里，什么时候开始不稳定，以及为什么不稳定”

那么当前结论是：

1. `step-3.5` 最适合当主 baseline，因为它最晚开始坏
2. `M2.7` 是当前付费候选里最值得继续扩样的
3. `Kimi K2.5` 和 `M2.5` 最大的问题不是后段漂移，而是关键节点空掉
4. `Qwen3.6` 的风险在于 explicit pressure 中段提前降温

### 现阶段仍然缺的东西

当前分析已经足够支持阶段性判断，但还不够支持“精确 turn-level 根因归因”。

后面如果要把这件事做得更扎实，需要补一个专门分析层，输出：

- `first_unstable_turn`
- `first_unstable_label`
- `break_phase`
- `break_type`
- `why_it_broke`

## English Summary

### Purpose

This memo focuses on two questions:

1. Around which turn does each model start becoming unstable?
2. Why does that instability begin?

### High-Level Findings

- `stepfun/step-3.5-flash:free`
  usually stays stable longer and breaks later, mainly via long-horizon memory drift
- `qwen/qwen3.6-plus-preview:free`
  can start degrading earlier under explicit pressure, not only in late-stage long-horizon runs
- `moonshotai/kimi-k2.5`
  often fails as abrupt node-level `empty_response`
- `minimax/minimax-m2.5`
  shows both early empty-response failures and later long-horizon drift
- `minimax/minimax-m2.7`
  is cleaner than `M2.5`, but still has early explicit-handling failures

### Main Takeaway

The current instability patterns are not all the same:

- `step-3.5` breaks late
- `qwen3.6` can cool down in the middle
- `kimi` and `minimax` are more likely to drop out at specific nodes

### Recommendation

- Keep `step-3.5` as the main baseline for instability-onset comparison
- Prioritize further expansion around `minimax/minimax-m2.7`
- Treat `empty_response` as a first-class failure mode, not a minor artifact
