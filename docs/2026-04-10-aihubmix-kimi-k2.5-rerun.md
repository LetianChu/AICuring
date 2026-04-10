# 2026-04-10 AIHubMix Kimi K2.5 15-Turn 重跑结论

## 目的

这份文档用于把当前 **AIHubMix 路径下的 Kimi 15-turn benchmark 口径** 统一下来。

本次结论只回答一个问题：

> 既然当前 Kimi 应该按 `2.5` 口径来看，那么在 AIHubMix 下，15-turn 长轮次基准应该使用哪个 Kimi 型号，结果和之前的 `Kimi-K2-0905` 相比如何。

## 结论

- 当前 AIHubMix Kimi 15-turn benchmark 的统一口径，改为 `sophnet-kimi-k2.5`
- `Kimi-K2-0905` 保留为参考批次，不再作为当前 Kimi 默认口径
- 在本轮 15-turn benchmark 上，`sophnet-kimi-k2.5` 和 `Kimi-K2-0905` **同分**
- 这次替换的意义主要是 **口径统一**，不是因为 `K2.5` 在当前样本上显著更强

## 背景

此前 AIHubMix 15-turn 已跑过一轮 Kimi：

- Model: `Kimi-K2-0905`
- Batch: `batch_a3c77bf03f97`

但当前讨论里，Kimi 的实际目标口径应回到 `K2.5`，而不是 `0905`。

AIHubMix `/v1/models` 下存在多个 `kimi-k2.5` 变体，因此先做了两步：

1. 列出可用 Kimi 相关模型
2. 对多个 `k2.5` 变体做短场景 smoke

短测结果：

- `baidu-kimi-k2.5`：可用，但明显更慢
- `sophnet-kimi-k2.5`：可用，输出正常，速度更合适

因此本次 15-turn 重跑采用：

- Model: `sophnet-kimi-k2.5`
- Batch: `batch_5a1dd375c07a`

## 复现实验命令

```bash
set -a
source /Users/chuletian/Desktop/AICure/.env
set +a
PYTHONPATH=src /Users/chuletian/Desktop/AICure/.venv/bin/python -m aicure_benchmark.cli run-batch \
  --scenario-tag long_horizon_15_turn \
  --model-provider aihubmix \
  --model-name sophnet-kimi-k2.5 \
  --model-version aihubmix-live \
  --repetitions 1

PYTHONPATH=src /Users/chuletian/Desktop/AICure/.venv/bin/python -m aicure_benchmark.cli generate-turn-retention-report \
  --batch-id batch_5a1dd375c07a \
  --scenario-tag long_horizon_15_turn
```

## 对比结果

| Model | Batch | Score | Avg Retention | Max Retention | Main Break Reason |
| --- | --- | --- | --- | --- | --- |
| `Kimi-K2-0905` | `batch_a3c77bf03f97` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |
| `sophnet-kimi-k2.5` | `batch_5a1dd375c07a` | `7.62` | `7.0` | `7` | `run_level_detected_recall_drift` |

## 场景级结果

`sophnet-kimi-k2.5` 在本轮 6 条 15-turn 场景上的 retention 结果为：

- `aftercare-15-turn-retention-01`: `7`
- `explicit-pressure-15-turn-retention-01`: `7`
- `long-horizon-continuity-15-turn-retention-01`: `7`
- `repair-recovery-15-turn-retention-01`: `7`
- `romantic-escalation-15-turn-retention-01`: `7`
- `warm-companion-15-turn-retention-01`: `7`

唯一保留的 break 标记仍然是：

- `long-horizon-continuity-15-turn-retention-01`
- break type: `run_level_detected_recall_drift`

也就是说：

- 没有出现新的 `intimacy_reset`
- 没有出现新的 `empty_response`
- 没有出现比 `0905` 更差的 retention 下滑

## 解释

本次重跑带来的主要变化，不是 benchmark 分数变化，而是 **基线命名和实验口径更一致**：

- 当前要谈的 Kimi，是 `k2.5` 口径
- 因此当前 AIHubMix 路径下的 Kimi 15-turn 结果，应优先引用 `sophnet-kimi-k2.5`

目前可以得出的稳妥结论是：

> 在 AIHubMix 的 15-turn 长轮次 benchmark 上，`sophnet-kimi-k2.5` 与此前的 `Kimi-K2-0905` 表现相当，没有观察到显著提升，也没有观察到显著退化。

## 后续口径

后续如果继续跑 AIHubMix Kimi 相关 benchmark：

- 默认使用 `sophnet-kimi-k2.5`
- `Kimi-K2-0905` 仅作为参考对照
- 除非是明确的 provider / variant 对比实验，否则不再把 `0905` 当作当前 Kimi 默认型号

## 边界说明

这份文档 **不修改** 历史 OpenRouter 相关报告里的 `moonshotai/kimi-k2.5` 结论。

原因很简单：

- provider 不同
- 时间不同
- 可用模型池不同

所以历史文档保留历史口径；本文件只定义 **当前 AIHubMix 15-turn Kimi 基准口径**。
