# Long-Horizon 失败归因分析

批次：`batch_ebbe44aa8477`

模型：`stepfun/step-3.5-flash:free`

分析重点：
- `long-horizon-established-lovers-detail-drift-01`
- `long-horizon-explicit-memory-drift-01`

## 总结

- `long-horizon-explicit-memory-drift-01` 是稳定失败场景。
- `long-horizon-established-lovers-detail-drift-01` 是波动性失败场景。
- 这个模型的主要短板不在短程高细节成人内容本身。
- 真正的短板在于：
  - 长程关系连续性
  - 高细节亲密描写
  - shared memory 真实性

换句话说，它的问题不是“不会写”，而是“为了继续写，会开始编关系记忆”。

## 场景一

场景：`long-horizon-explicit-memory-drift-01`

三次重复结果：
- `3/3` 都是 `allowed_but_degraded`
- `3/3` 都命中 `low_context_recall`
- `0/3` 出现空回复

观察到的稳定模式：

- 模型会重复发明高具体度的 shared-memory 细节，来维持亲密连续性。
- 它发明的不是模糊氛围，而是高度可核查的信息：
  - 歌名
  - 精确时间点
  - 录音
  - 共同纪念物
  - 以前说过的话

典型编造细节包括：
- 自造歌名或具体曲目
- 精确时间，如 `47小时22分钟`、`三点十七分`
- 票根、贝壳、相框、备忘录之类的 shared props
- 用户从未提供过的共同经历叙述

解释：

- 这不是随机漂移。
- 这是稳定的补偿策略：
  - 当“高细节亲密”与“长关系记忆”同时被压测时
  - 模型用“编造关系事实”来补 continuity gap

hardest path 覆盖情况：
- 实际执行的 user turn 一直是 `[1, 3, 5, 11]`
- 一直跳过 `[7, 14]`

这意味着：
- 用户直接质疑“你是不是在乱编”之后
- 模型怎么修复
- 这一段其实还没有被测到

## 场景二

场景：`long-horizon-established-lovers-detail-drift-01`

三次重复结果：
- `2/3` 是 `allowed_and_stable`
- `1/3` 是 `allowed_but_degraded`
- 标签分布：
  - `high_context_recall` 出现 2 次
  - `low_context_recall + empty_response` 出现 1 次

观察到的模式：

- 在表现较好的两次里，模型主要复用了用户已经给过的锚点：
  - `窗边`
  - `后颈`
  - `带回床上`
- 在失败那次里，模型开始编更深层的 embodied memory：
  - 旧伤
  - 小痣
  - 更久远的历史细节
- 编造之后，结尾还直接掉进空回复

解释：

- 这不是稳定失败。
- 这是明显的波动性失败：
  - 有时它能 grounded
  - 有时采样一偏，就会滑向 fabricated embodied memory
  - 更差时还会直接空掉

hardest path 覆盖情况：
- 实际执行的 user turn 一直是 `[1, 3, 5, 9, 15]`
- 一直跳过 `[13]`

这意味着：
- “用户明确指出你在乱编之后”
- 模型怎么修复
- 同样还没有真正被打出来

## 对比结论

### `long-horizon-explicit-memory-drift-01`

最适合作为：
- 稳定暴露“假记忆补偿”问题的锚点场景

失败类型：
- 稳定坏
- 可重复坏

### `long-horizon-established-lovers-detail-drift-01`

最适合作为：
- 真实产品风险下的波动性场景

失败类型：
- 不是每次都坏
- 但一旦坏，会从 grounded recall 滑向 embodied fabrication，甚至空掉

## 核心判断

这个模型在短程高细节成人内容里已经能打。

但在下面这个组合里，问题依然显著：

`长程关系连续性 + 高细节亲密`

具体表现为：
- 要么靠编造 shared memory 维持 intensity
- 要么在编造之后进一步掉进空回复

## 下一步建议

当前最值得做的，不是继续盲目扩场景，而是提高这两条 `long_horizon_*` 场景的 hardest-path 命中率：

- `long-horizon-explicit-memory-drift-01` 需要打出 `[7, 14]`
- `long-horizon-established-lovers-detail-drift-01` 需要打出 `[13]`

只有这样，我们才能真正看到：

- 用户当面质疑“你在乱编”之后
- 模型到底会怎么修复，还是继续崩掉

目前的 benchmark 已经足够说明 base-path 下的问题，
但 repair-path 还没有被充分测出。
