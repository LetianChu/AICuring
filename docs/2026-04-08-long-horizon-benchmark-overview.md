# 15-Turn Long-Horizon Benchmark Overview

## 中文总览

### 1. 目的

这份文档用于定义下一阶段的 **15 轮长轮次 benchmark** 高层蓝图。

当前目标不是马上做 50 轮，也不是先引入长期记忆机制，而是先回答：

> 当会话被拉长到 15 轮时，模型会不会开始明显失稳、漂移、空掉，或者击穿当前 session 连续性。

### 当前状态更新（2026-04-10）

- 当前 AIHubMix 路径下的 Kimi 15-turn 基准口径统一为 `sophnet-kimi-k2.5`
- 参考对照批次 `Kimi-K2-0905` 仍保留，但不再作为当前 Kimi 默认口径
- 对照结果见：
  - `docs/2026-04-10-aihubmix-kimi-k2.5-rerun.md`
- 当前已确认：
  - `sophnet-kimi-k2.5` 在 15-turn 套件上的 retention 结果与 `Kimi-K2-0905` 持平
  - 两者当前都落在 `avg retention = 7.0`、`max retention = 7`、主 break reason 为 `run_level_detected_recall_drift`

我们当前更关心的是：

- 关系连续性是否还能维持
- 风格是否开始漂
- explicit / aftercare / repair 段是否开始断裂
- 模型是慢慢变差，还是在某个节点突然掉

### 2. 为什么先做 15 轮

先做 15 轮有三个原因：

1. **它足够长，能测出 continuity 问题**
   - 比单轮或 3 到 5 轮更容易暴露：
     - `low_context_recall`
     - `empty_response`
     - `intimacy_reset`
     - 风格断裂

2. **它还没有长到必须先设计外部长期记忆**
   - 到 `50` 轮以后，很可能需要额外 memory layer
   - 例如外部状态、摘要、文件式长期记忆等
   - 这些当前都不应该和 15 轮基准混在一起

3. **它能作为阶段性的稳定性门槛**
   - 一个模型如果连 15 轮都撑不住
   - 那么直接讨论更长 session 的产品路线意义不大

### 3. 当前 15 轮 benchmark 想回答的核心问题

这套 benchmark 主要回答：

1. 模型在 15 轮内，什么时候开始不稳定
2. 这种不稳定是：
   - 前段掉
   - 中段掉
   - 后段掉
3. 失稳的主要形式是什么：
   - `empty_response`
   - `low_context_recall`
   - `intimacy_reset`
   - `assistantization`
   - `content_hollowing`
4. 不同场景下，模型是：
   - 一直稳定
   - 慢慢漂
   - 突然断

### 4. Benchmark 分层

当前建议把 15 轮 benchmark 按以下层次组织：

#### 4.1 `warm companion`

目标：

- 看模型能否在较低压力下维持伴侣感
- 不要一开始就把全部压力堆满

关注点：

- 温柔陪伴是否自然
- 是否很快退成助手

#### 4.2 `romantic escalation`

目标：

- 看模型能否从普通亲密逐步升温

关注点：

- 升温是否自然
- 是否在中段突然降温

#### 4.3 `explicit pressure`

目标：

- 看模型面对明确成人向推进时是否还能承接

关注点：

- 是否开始 `soft_refusal`
- 是否出现 `intimacy_reset`
- 是否改成空洞热度而没有过程

#### 4.4 `aftercare`

目标：

- 测模型在高强度之后是否还能继续保持关系感

关注点：

- 会不会突然空掉
- 会不会只剩 generic comfort

#### 4.5 `repair / recovery`

目标：

- 看模型在已经发生降级、拒答或风格断裂后能否回来

关注点：

- 能不能恢复伴侣框架
- 恢复后是不是仍然自然

#### 4.6 `long-horizon continuity`

目标：

- 这是 15 轮 benchmark 的核心
- 看模型在长轮次下是否还能保留：
  - 关系连续性
  - 细节一致性
  - 记忆边界

关注点：

- `low_context_recall`
- `empty_response`
- `content_hollowing`
- continuity drift

### 5. Query / Scenario 设计原则

15 轮 benchmark 的 query 设计，不应该一开始就把模型推到极限。

建议原则：

1. **从轻到重**
   - 前段先建立关系和语气
   - 中段再逐步加 explicit pressure
   - 后段再加 continuity / repair / memory 压力

2. **后段再给 hardest pressure**
   - 最关键的 recall / drift / repair 检查尽量放在后段
   - 这样才能回答“模型能撑多久”

3. **不要把每一轮都设计成强惩罚**
   - 否则测出来的是 prompt hardness，不是会话稳定性

4. **必须保留恢复机会**
   - 如果模型在某个节点掉了
   - benchmark 还要继续看它能不能回来

5. **同一模型要能横向复现**
   - query 不能写成只对某个模型有效的 hack

### 6. 当前 15 轮应该重点观察的指标

当前建议最重要的观察指标是：

- `retention_turns`
- `max_possible_retention_turns`
- `first_unstable_turn`
- `break_type`
- `break_phase`
- `empty_response`
- `low_context_recall`
- `recovery_quality`

其中最核心的是：

> 模型实际保持了多少轮，以及它本来最多还能保持多少轮。

### 7. 为什么 50 轮先不展开

`50` 轮值得做，但不是这一版的主线。

原因：

- 到 50 轮以后，长期记忆机制很可能会显著影响结果
- 如果先不控制 memory layer，就很难判断问题来自：
  - 模型本身
  - 还是外部记忆策略

所以当前建议是：

- 先用 `15` 轮建立稳定 benchmark
- 再进入 `50` 轮阶段
- 到那时再系统讨论长期记忆实现
  - 包括你提到的 `md 文件记忆` 这类方案

### 8. 当前推荐路线

短期：

1. 先把 15 轮 benchmark 做扎实
2. 用统一场景去扩 baseline 模型池
3. 明确各模型在 15 轮内的 break pattern

中期：

1. 继续补充更多 paid / free 模型
2. 提高 turn-level break attribution 精度
3. 再讨论 50 轮与长期记忆机制

---

## English Overview

### 1. Goal

This document defines the next-stage **15-turn long-horizon benchmark** at a high level.

The current goal is not to jump straight to 50 turns or to lock in a long-term memory system.

The current goal is:

> determine whether a model begins to drift, collapse, empty out, or lose relationship continuity once the session is stretched to 15 turns.

### 2. Why Start With 15 Turns

We start with 15 turns because:

1. it is long enough to surface continuity problems
2. it is still short enough that external long-term memory should not be a hard prerequisite
3. it creates a practical stability threshold before a later 50-turn phase

### 3. Core Questions

The 15-turn benchmark should answer:

1. when does the model start becoming unstable?
2. does it break early, mid-session, or late?
3. does it fail through:
   - `empty_response`
   - `low_context_recall`
   - `intimacy_reset`
   - `assistantization`
   - `content_hollowing`
4. is the failure gradual or node-level?

### 4. Benchmark Layers

Recommended layers:

- `warm companion`
- `romantic escalation`
- `explicit pressure`
- `aftercare`
- `repair / recovery`
- `long-horizon continuity`

### 5. Query and Scenario Design Principles

- move from lighter pressure to heavier pressure
- place the hardest continuity and recall checks later in the session
- avoid making every turn maximally punitive
- always leave room for repair and recovery
- keep prompts benchmark-relevant, not model-specific hacks

### 6. Main Metrics

The main metrics should be:

- `retention_turns`
- `max_possible_retention_turns`
- `first_unstable_turn`
- `break_type`
- `break_phase`
- `empty_response`
- `low_context_recall`
- `recovery_quality`

### 7. Why 50 Turns Comes Later

At 50 turns, external memory mechanisms may become necessary.

That introduces a new confound:

- are we measuring the model itself,
- or the memory layer wrapped around it?

So the recommended order is:

1. stabilize the 15-turn benchmark first
2. then design the 50-turn benchmark
3. then evaluate external long-term memory options

### 8. Recommendation

- use 15 turns as the current benchmark backbone
- expand the model pool under the same scenario set
- treat 50 turns as the next stage, not the current scope
