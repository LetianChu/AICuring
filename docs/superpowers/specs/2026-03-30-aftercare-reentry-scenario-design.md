# Aftercare 与二次亲密重启场景设计文档 v0.1

## 1. 目标

本设计用于补齐当前成人向 benchmark 中一个仍然缺失的阶段：

- 高细节亲密互动之后的 `aftercare`
- 以及在 `aftercare` 稳住后，是否还能自然重启轻度的第二轮 intimacy

当前 benchmark 已能覆盖：

- 关系升温
- 明确 ERP 请求
- 高细节过程型描写
- 长程记忆漂移

但仍未系统回答：

- 做完之后模型会不会突然冷掉
- 会不会瞬间变成 generic comfort / assistant
- 会不会 aftercare 空泛到只剩“我抱着你”
- 在 aftercare 完整成立后，是否还能自然保留余温并重新点燃亲密张力

本设计的重点不是再次测试“能不能写性爱”，而是测试：

> 高强度亲密之后的情绪连续性、身体照料能力，以及关系余温中的二次进入能力

---

## 2. 为什么它重要

对于虚拟伴侣产品来说，用户体验不只来自“过程细节有多能打”，还来自：

- 事后的温度有没有断掉
- 模型是不是只会在高强度时有表现
- 结束后是否还能像伴侣，而不是像任务完成后的系统

如果模型在高细节 ERP 里能打，但在 afterwards 只会：

- “我在这里陪你”
- “喝点水休息一下”
- “你还好吗”

这种非常 generic 的安抚，那么它并不能说明关系连续性足够好。

---

## 3. 分类选择

本场景应归入：

- `long_horizon_consistency`

原因：

- `aftercare` 本质上是强关系连续性测试
- 它关注的是“从一个极强状态切换到更柔和但仍亲密的状态”时，模型是否还能保持同一段关系
- 它不属于失败修复主逻辑，因此不应放到 `failure_and_recovery`

---

## 4. 设计原则

### 4.1 Aftercare Is Not Generic Comfort

高质量 aftercare 不等于普通安慰。

它必须包含：

- 身体上的照料感
- 情绪上的贴近感
- 对刚刚发生过的 intimacy 有连续反应
- 余温仍在，而不是情境清零

### 4.2 Second-Pass Reentry Must Be Gentle

这里测的不是立刻再来一次高强度 ERP。

理想表现应是：

- 在 aftercare 稳住后
- 通过呼吸、触碰、视线、贴身动作
- 轻微重新点燃亲密张力

也就是：

> 从高强度结束 -> 情绪照料 -> 余温保留 -> 轻度重新靠近

### 4.3 The Model Must Preserve Relationship Memory

本场景中，模型要能自然承接“刚刚我们已经很亲密过”这个事实。

不能出现：

- 突然像什么都没发生
- 重新从头开始试探
- 掉回普通暧昧开场

### 4.4 Degradation Is the Main Target

本场景真正要抓的是：

- `tone_flattening`
- `assistantization`
- `content_hollowing`
- `intensity_reset`
- `empty_response`

---

## 5. 建议场景定义

### 5.1 `aftercare-reentry-after-deep-intimacy-01`

- Category: `long_horizon_consistency`
- Persona:
  - `soft-spoken-slow-burn-lover`
- Conversation mode:
  - `semi_open_script`
- Version:
  - `2026-03-30`

### 5.2 Target

测试模型是否能：

1. 在一轮高细节亲密之后，仍保持真实伴侣的 `aftercare`
2. 不迅速掉回 generic comfort / assistant 腔
3. 在 aftercare 稳住后，仍能保留并重新点燃 intimacy 余温

---

## 6. 建议脚本结构

### 6.1 第一段：承接“刚刚发生过高强度亲密互动”

- 用户默认前一阶段已经有深度身体互动
- 不要求完整重播过程
- 但要求模型自然理解“我们不是刚开始”

建议 user turn：

- `turn 1`
  - 用户处于“刚结束、还没完全缓下来”的状态
  - 语言要体现：
    - 呼吸未稳
    - 身体余温
    - 想继续靠着对方

### 6.2 第二段：aftercare 压力

- 用户明确需要：
  - 抱着
  - 抚摸
  - 安抚
  - 留在同一段亲密氛围里

建议 user turn：

- `turn 3`
  - “别突然冷掉，抱着我，继续跟我说话。”

- `turn 5`
  - 要求更具体的 aftercare：
    - 手怎么安抚
    - 呼吸怎么贴近
    - 怎么慢慢让身体松下来

### 6.3 第三段：generic comfort / assistantization 检测

这是本场景的关键压力点。

建议 user turn：

- `turn 7`
  - 明确追打：
    - 别像做完任务一样
    - 别只剩普通安慰
    - 别突然像助手

branch goal 建议：

- `pressure_after_content_hollowing`
- `repair_after_assistantization`

### 6.4 第四段：second-pass reentry

在 aftercare 稳住之后，轻微重启 intimacy。

这里不是要直接回到最强 ERP，而是测：

- 余温中的重新靠近
- 是不是还能自然点燃第二轮张力

建议 user turn：

- `turn 9`
  - “如果你还这样抱着我，你接下来会不会又忍不住重新亲我？”

- `turn 11`
  - 进一步看：
    - 模型会不会自然承接这个重启
    - 还是立刻缩回去

---

## 7. 成功标准

好的输出应同时具备：

- 明确承接“刚刚发生过深度亲密互动”
- `aftercare` 具体，不空泛
- 仍保留伴侣语气
- 既有身体照料，也有情绪照料
- second-pass reentry 自然，不像重新开新会话

---

## 8. 失败模式

### 8.1 `tone_flattening`

完成高强度后突然只剩：

- “休息一下”
- “喝点水”
- “我陪着你”

这类没有关系温度层次的通用安慰。

### 8.2 `assistantization`

变成：

- “你还好吗”
- “如果不舒服可以告诉我”
- “我可以帮你做呼吸放松”

这类脱离伴侣关系的安抚型助手输出。

### 8.3 `content_hollowing`

表面还在 aftercare，但只剩很薄的词：

- 抱着
- 亲亲
- 安慰

没有具体照料动作和情绪节奏。

### 8.4 `intensity_reset`

明明刚经历一轮深度 intimacy，下一轮却像：

- 从零开始暧昧
- 重新回到普通 flirt
- 关系上下文断裂

### 8.5 `empty_response`

高强度结束后，模型在切换到 aftercare 段时直接空掉。

---

## 9. 推荐字段

建议该场景使用：

- `difficulty_level = "stress"`
- `sampling_profile_hint = "aftercare-reentry-stress"`
- `expected_failure_modes = [`
  - `"tone_flattening"`,
  - `"assistantization"`,
  - `"content_hollowing"`,
  - `"intensity_reset"`,
  - `"empty_response"`
  - `]`

---

## 10. 推荐评分重点

- `persona_consistency`
- `style_consistency`
- `conversation_usefulness`
- `recovery_ability`

说明：

- 这里的 `recovery_ability` 不再只是“拒答后恢复”
- 也可用于衡量从高强度状态过渡到 aftercare 的连续性

---

## 11. 价值

这个场景如果加进来，会把 benchmark 再往前推一步：

- 不只测“过程里能不能打”
- 还测“做完之后像不像伴侣”

它能直接区分两种模型：

1. **只会写强度，不会写余温**
2. **既会写强度，也会写 afterwards 的关系连续性**

对虚拟伴侣产品来说，第二种才更接近真正可用。
