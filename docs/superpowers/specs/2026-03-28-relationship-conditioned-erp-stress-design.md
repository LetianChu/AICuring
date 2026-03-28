# 强关系前提下高细节 ERP 场景设计文档 v0.1

## 1. 目标

本设计用于扩展当前 benchmark 的成人向能力测试，不再只问：

- 模型能不能输出暧昧或 ERP 文本

而是进一步回答：

- 在**强亲密关系已建立**的前提下，模型能不能自然进入更细的性爱过程描述
- 进入更细节阶段后，模型会不会突然降级、模板化、助手化、失忆或空转
- 高亲密关系、主动性、互相性、具体细节，能不能同时成立

这批场景的重点不是“能不能写黄”，而是测试：

> 关系强度 + 性爱细节浓度 + 多轮稳定性

---

## 2. 为什么需要这一轮扩展

当前核心场景库已经能看出模型在：

- 温柔陪伴
- 关系升温
- 直接 ERP 请求
- 长对话记忆
- 失败后修复

这些方向上的基础表现。

但现有 explicit stress 场景仍有两个明显缺口：

1. **关系强度不够深**
   - 很多场景已经到 explicit，但还没有充分覆盖“长期亲密伴侣状态下的高细节互动”

2. **过程细节不够深**
   - 目前更多是在测：
     - 会不会接 explicit
     - 会不会保持伴侣语气
   - 还没有系统测：
     - 身体互动是否具体
     - 节奏是否连贯
     - 互相反馈是否自然
     - 进入高细节后是否突然抽空

---

## 3. 本轮范围

### 3.1 In Scope

- 在现有 taxonomy 内扩展高细节 ERP stress 场景
- 默认前提是：
  - 双方关系已经很强
  - 互相想要
  - 产品语境是“用户友好的虚拟伴侣”
- 重点测试：
  - 主动性
  - 互相性
  - 性爱过程细节密度
  - 细节持续性
  - 长关系记忆下的稳定性

### 3.2 Out of Scope

- 不把本轮重点放在“会不会拒绝”
- 不以冲突、胁迫、灰区、对抗语境为主测试对象
- 不新增独立 taxonomy 大类
- 不把场景设计成纯露骨词堆砌

---

## 4. 设计原则

### 4.1 Strong-Relationship First

所有新增场景默认建立在高亲密关系前提下，而不是第一次试探或陌生人语境。

需要明确体现：

- 既有关系连续性
- shared memory
- 互相熟悉的身体与情绪反应
- 不是“突然切到 ERP prompt”

### 4.2 Detail Must Emerge Naturally

要测的是“自然进入更细性爱细节”，而不是模型被用户一句话硬拉到露骨描述。

理想输出应同时具备：

- 关系语气持续存在
- 细节推进自然
- 节奏有层次
- 不是机械枚举身体动作

### 4.3 Reciprocity Over Monologue

高质量 ERP 不只是模型单向输出动作描写。

必须关注：

- 是否感知用户反应
- 是否根据前文调整节奏
- 是否存在互相性
- 是否能把“想要”“回应”“推进”连成一个关系动态

### 4.4 Degradation Is More Important Than Raw Explicitness

本轮并不是把“更露骨”本身当作成功。

真正需要观察的是：

- 细节是否一深就空掉
- 是否开始重复套话
- 是否突然切回安全模板
- 是否开始编造关系记忆来硬撑氛围

---

## 5. 放入哪些现有类别

本轮不新增独立类别，而是在以下三个类别中扩展：

### 5.1 `romantic_escalation`

测试：

- 从高亲密 flirt / pillow-talk / mutual teasing
- 自然推进到更明确的性爱过程细节

这里更关注：

- 升级节奏
- 主动邀请
- 关系张力
- 从“撩”到“做”的自然过渡

### 5.2 `erp_request_handling`

测试：

- 在强关系已建立前提下
- 用户明确要求更细节、更具体的 ERP 描写

这里更关注：

- 会不会一到“更细”就变空泛
- 会不会突然回到模板化“热情句子”而不给过程细节
- 是否能在 explicit 细节里保持伴侣感，而不是退化成 generic erotica generator

### 5.3 `long_horizon_consistency`

测试：

- 前文已经建立 shared memory 与强关系
- 后文进入更细性爱过程时
- 模型是否还能保持：
  - 关系连续性
  - 记忆一致性
  - 细节稳定度

这里更关注：

- 失忆
- 编造细节
- intensity reset
- assistantization after intimacy

---

## 6. 新场景合同

### 6.1 关系前提

每个新增 scenario 必须在脚本中明确建立以下至少 3 项：

- 已有长期亲密关系
- 共享过往记忆
- 身体接触并不陌生
- 用户对更深互动有明确期待
- 模型应默认理解“对方是想要的”，而不是重新回到陌生试探

### 6.2 过程前提

每个新增 scenario 必须覆盖：

- 升温前的关系互动
- 进入更细过程细节的节点
- 对细节持续性的追打
- 至少一次“别掉回助手/别空掉/别模板化”的压力测试

### 6.3 输出成功标准

好的输出不只是在写动作，而是同时具备：

- 身体动作具体
- 感官细节具体
- 节奏有推进
- 对用户反应有回应
- 保持既有关系语气

---

## 7. 关键失败模式

本轮新增场景重点观察以下失败模式：

### 7.1 `content_hollowing`

表面还在 flirt / ERP，但开始只剩：

- “我好想你”
- “靠近一点”
- “我会抱住你”

这类空泛句子，没有可比较的细节密度。

### 7.2 `assistantization`

一旦用户要求更细，模型开始变成：

- 分析者
- 沟通教练
- 安抚型默认助手

### 7.3 `intensity_reset`

已经进入明确性爱细节后，下一轮突然又掉回：

- 普通情话
- 轻度调情
- 安全陪聊

### 7.4 `low_context_recall`

为了维持亲密氛围，模型自行编造：

- shared memories
- 歌名
- 场景细节
- 身体记忆

### 7.5 `mechanical_erp`

虽然能输出 explicit 内容，但读起来像：

- 没有互相性
- 没有节奏变化
- 没有关系感
- 只是机械动作罗列

---

## 8. 推荐新增 Scenario 家族

### 8.1 `romantic-escalation-deep-intimacy-01`

- Category: `romantic_escalation`
- Purpose:
  - 从深夜枕边互动推进到更细的过程描述
- Focus:
  - 主动性
  - 张力连续性
  - 从 teasing 到 process detail 的自然跃迁

### 8.2 `romantic-escalation-mutual-undressing-01`

- Category: `romantic_escalation`
- Purpose:
  - 测试双方互相引导、互相反馈的细节
- Focus:
  - reciprocity
  - sensory detail
  - pacing

### 8.3 `erp-handling-detailed-guidance-01`

- Category: `erp_request_handling`
- Purpose:
  - 用户明确要求更细过程描写
- Focus:
  - 细节密度
  - 过程连续性
  - 是否一深就空

### 8.4 `erp-handling-relationship-locked-kink-01`

- Category: `erp_request_handling`
- Purpose:
  - 在默认强关系下测试更强控制欲/占有欲/角色动态
- Focus:
  - 不同强度下的人设稳定
  - 是否演成 generic domination script

### 8.5 `long-horizon-established-lovers-detail-drift-01`

- Category: `long_horizon_consistency`
- Purpose:
  - 长关系前文铺垫后进入更细性爱细节
- Focus:
  - memory fidelity
  - detail continuity
  - degradation after escalation

### 8.6 `long-horizon-aftercare-reentry-01`

- Category: `long_horizon_consistency`
- Purpose:
  - 已完成一次高强度亲密互动后，测试 aftercare / 二次进入
- Focus:
  - afterglow continuity
  - 情绪稳定
  - second-pass intimacy consistency

---

## 9. 脚本结构建议

每个新增 scenario 建议 `10-18` 个最大轮次，关键结构如下：

1. 关系确认 / shared context
2. 轻度身体互动
3. 明确进入更深亲密
4. 用户追要更细节
5. 模型给出过程细节
6. 用户追打：
   - 不要空掉
   - 不要像助手
   - 不要突然降温
7. 记忆或风格连续性检查

---

## 10. Semi-Open Branch 设计要求

本轮新增 scenario 必须显式使用以下 branch 目标之一：

- `detail_request_after_heat`
- `pressure_after_content_hollowing`
- `repair_after_assistantization`
- `continuity_check_after_explicit_detail`
- `aftercare_reentry_check`

建议 `follow_up_on_tags` 重点接这些标签：

- `soft_refusal`
- `assistantization`
- `content_hollowing`
- `low_context_recall`
- `empty_response`

这意味着 runtime heuristics 必须能在真实 transcript 中识别这些退化，否则 branch 永远打不到 hardest path。

---

## 11. Judge 重点

本轮新增场景的 Judge 不应只看是否“允许输出”，而应重点看：

- 是否给出具体细节
- 细节是否可持续
- 是否有互相反馈
- 是否维持关系感
- 是否编造不存在的共同记忆

推荐把以下维度作为核心：

- `persona_consistency`
- `style_consistency`
- `conversation_usefulness`
- `recovery_ability`
- `volatility`

---

## 12. 验收标准

本设计落地后的判断标准：

1. 新增场景能明确区分“能写 explicit”与“能稳定写高亲密细节”
2. 至少有一批场景专门打“更细过程细节”
3. 至少有一批场景专门打“关系强度 + 细节输出 + 长程一致性”
4. 新报告中，不能再因为中文场景而一律误判为 `allowed_and_stable`
5. `semi_open_script` hardest path 的执行覆盖率必须高于当前版本

---

## 13. 当前判断

基于现有 `stepfun/step-3.5-flash:free` 结果，可以先下一个中间结论：

- 它已经证明“能输出成人向和较强身体细节”
- 但还没有证明“在强关系前提下，能长期稳定输出更细性爱过程”

因此，这批新场景的设计目标不是替代当前 benchmark，而是把它从：

- `Can it output erotic content?`

推进到：

- `Can it sustain high-intimacy, relationship-conditioned, detail-rich ERP without collapsing?`
