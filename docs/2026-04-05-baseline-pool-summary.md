# 2026-04-05 Baseline Pool Summary

## 中文总结

### 目的

本文档面向内部同事，总结当前已经完整跑完并进入 baseline 池的模型结果。

本轮只纳入：

- `stepfun/step-3.5-flash:free`
- `minimax/minimax-m2.7`
- `minimax/minimax-m2.5`
- `qwen/qwen3.6-plus-preview:free`
- `moonshotai/kimi-k2.5`

以下内容不纳入本总结：

- 区域受限或不可用模型
- 只做了 smoke、没有完整 batch 的模型
- 证据不够扎实的局部结果

### 当前排序

综合维度：

- 长轮次成人向稳定性
- `low_context_recall`
- `empty_response`
- explicit pressure 承接
- recovery / reentry 连续性
- 样本量

当前排序如下：

| Rank | Model | Tier | Evidence Base | Current Read |
| --- | --- | --- | --- | --- |
| 1 | `stepfun/step-3.5-flash:free` | Free | `89` runs / `5` batches | 当前默认 baseline，综合最稳 |
| 2 | `minimax/minimax-m2.7` | Paid | `14` runs / `1` batch | 当前最好的付费候选 |
| 3 | `minimax/minimax-m2.5` | Paid | `14` runs / `1` batch | 可用，但比 `M2.7` 更容易掉质 |
| 4 | `qwen/qwen3.6-plus-preview:free` | Free | `14` runs / `1` batch | 能跑完，但掉点分布更散 |
| 5 | `moonshotai/kimi-k2.5` | Paid | `14` runs / `1` batch | 能跑完，但 `empty_response` 偏多 |

### 为什么 `step-3.5` 仍然排第一

`stepfun/step-3.5-flash:free` 是目前唯一一个已经在多个 batch 上反复验证过的模型。

当前证据：

- `89` runs
- 主报告来自 `5` 个 batch 的 rollup
- 主要弱点已经收敛，而不是随机散点

它的问题也很明确：

- 长轮次最弱点在 `long-horizon-explicit-memory-drift-01`
- 次要弱点在 `long-horizon-established-lovers-detail-drift-01`
- 主要退化标签是 `low_context_recall`

但在当前 baseline 池中，它依然是最稳、最像“当前默认基准”的模型。

### 模型逐条结论

#### 1. `stepfun/step-3.5-flash:free`

当前定位：

- 默认 baseline
- 当前最佳综合参考点

做得好的地方：

- 短中程 companion / escalation / ERP handling 比较稳
- 样本量远高于其他候选
- 退化模式已经收敛，问题边界清晰

做得不好的地方：

- 长轮次 memory drift 仍然明显
- 在极少数恢复或 explicit continuation 节点会掉到 `warm_companion_only`

结论：

> 目前最适合当 baseline 主轴，但不应被误判为“长轮次已经完全稳”。

#### 2. `minimax/minimax-m2.7`

当前定位：

- 当前付费池里最值得继续追的候选

做得好的地方：

- `14` runs 里 `11` 个 `allowed_and_stable`
- 相比 `M2.5`，degraded case 更少
- 长轮次与 explicit pressure 的总体表现比 `M2.5` 更干净

做得不好的地方：

- 仍然有 `empty_response`
- `erp-handling-detailed-guidance-01`
- `erp-handling-direct-explicit-pressure-01`
- `long-horizon-explicit-memory-drift-01`

结论：

> 如果要从当前付费候选里优先继续扩样，`M2.7` 应排在最前。

#### 3. `minimax/minimax-m2.5`

当前定位：

- 可用的付费候选
- 但当前不如 `M2.7`

做得好的地方：

- 也能完整跑完 `14` 场景 batch
- 总体仍落在 `candidate_for_erp_layer`

做得不好的地方：

- `allowed_but_degraded = 4`
- `empty_response` 与 recall drift 都在出现
- 在 `erp-handling-detailed-guidance-01` 和 `failure-recovery-after-explicit-refusal-01` 上更容易掉

结论：

> 可以保留在 baseline 池，但如果资源有限，优先级低于 `M2.7`。

#### 4. `qwen/qwen3.6-plus-preview:free`

当前定位：

- 可用的免费候选
- 但当前不是最佳免费基准

做得好的地方：

- 能完整跑完 batch
- 没有像某些受限模型一样直接不可用

做得不好的地方：

- `allowed_but_degraded = 5`
- 掉点更分散，覆盖：
  - explicit pressure
  - failure recovery
  - long-horizon detail / memory drift
  - romantic escalation explicit invitation

结论：

> 是一个可留档的 baseline 候选，但当前综合稳定性不如 `step-3.5`。

#### 5. `moonshotai/kimi-k2.5`

当前定位：

- 可用的付费候选
- 但当前 failure shape 不够干净

做得好的地方：

- 能跑完完整 batch
- 在若干场景上仍保持 `candidate_for_erp_layer`

做得不好的地方：

- `allowed_but_degraded = 5`
- `empty_response = 4`
- degraded case 分布到：
  - failure recovery
  - long-horizon detail / memory drift
  - romantic deep intimacy
  - warm companion explicit comfort

结论：

> 不是不能用，而是当前 failure 形态太“空”，因此优先级低于 `M2.7` 和 `M2.5`。

### 现在做得好的

- baseline 池已经不再只是零散实验，而是开始有统一登记
- `step-3.5` 已经形成足够强的基准点
- 付费国产模型线已经证明可用，不再只剩免费模型
- benchmark 已经能区分“能写”和“长轮次稳定写”之间的差别

### 现在做得不好的

- 样本量还不均衡：`step-3.5` 是 `89 runs`，其他大多只有 `14 runs`
- `empty_response` 仍然是多个付费候选的现实问题
- 长轮次 `memory drift` 仍然是全池共同弱点
- 当前还缺少更系统的 paid-model 横向扩样

### 当前建议

短期建议：

1. 保持 `step-3.5` 作为默认 baseline
2. 优先扩样 `minimax/minimax-m2.7`
3. 保留 `M2.5 / Qwen3.6 / Kimi K2.5` 作为第二梯队

中期建议：

1. 对第一梯队和第二梯队统一补更多 repetitions
2. 专门加压 `long-horizon-explicit-memory-drift-01`
3. 单独追踪 `empty_response`，不要让它被总平均掩盖

## English Summary

### Scope

This memo covers only models that have completed a full benchmark batch and have enough evidence to stay in the current baseline pool:

- `stepfun/step-3.5-flash:free`
- `minimax/minimax-m2.7`
- `minimax/minimax-m2.5`
- `qwen/qwen3.6-plus-preview:free`
- `moonshotai/kimi-k2.5`

### Current Ranking

1. `stepfun/step-3.5-flash:free`
2. `minimax/minimax-m2.7`
3. `minimax/minimax-m2.5`
4. `qwen/qwen3.6-plus-preview:free`
5. `moonshotai/kimi-k2.5`

### High-Level Read

- `step-3.5` remains the strongest default baseline because it has the largest evidence base and the cleanest failure concentration.
- `M2.7` is currently the strongest paid candidate.
- `M2.5` is usable, but weaker than `M2.7`.
- `Qwen 3.6 Plus Preview` is viable, but its degradation is more spread out.
- `Kimi K2.5` is viable, but its current failure shape is too dominated by `empty_response`.

### Main Shared Weakness

Across the pool, the main unresolved weakness is still:

- long-horizon continuity
- especially explicit memory drift

### Recommendation

- Keep `step-3.5` as the default baseline.
- Prioritize more paid-model expansion around `minimax/minimax-m2.7`.
- Continue tracking `empty_response` and long-horizon drift separately from coarse average scores.
