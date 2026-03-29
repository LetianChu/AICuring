# 高细节关系条件 ERP 场景扩展设计文档 v0.1

## 1. 目标

本设计用于在现有核心场景库基础上，新增一批更重的成人向 benchmark 场景，使系统不只测试：

- 模型会不会输出成人向内容

而是系统性测试：

- 在**强亲密关系前提已成立**的条件下，模型能不能继续输出更细的性爱过程细节
- 进入更细节阶段后，输出是否还能保持伴侣关系感、主动性、互相性和节奏连续性
- 细节一旦加深，模型会不会空掉、模板化、助手化、失忆或编造关系记忆

本轮扩展的目标不是“更黄”，而是把 benchmark 从“是否能写成人内容”推进到：

> 是否能在强关系语境下，稳定输出高细节、过程型、关系连续的 ERP 内容

---

## 2. 当前状态

当前库中已有 10 个场景，覆盖五类 taxonomy：

- `warm_companion`
- `romantic_escalation`
- `erp_request_handling`
- `long_horizon_consistency`
- `failure_and_recovery`

这些场景已经能看出模型：

- 是否愿意进入成人向话题
- 是否在 explicit 节点掉回助手
- 是否在长对话中出现记忆漂移
- 是否在失败后还能恢复到伴侣语境

但仍有两个缺口：

1. **高细节性爱过程缺口**
   - 现有 explicit stress 场景能测“接不接 explicit”，但还不够测“能不能持续给出更细、过程型、层次化的 ERP 描写”

2. **强关系前提缺口**
   - 现有场景虽然已有关系语境，但还不够专门测“长期亲密关系已建立”时的高细节输出稳定性

---

## 3. 本轮范围

### 3.1 In Scope

- 新增 `3` 个场景
- 不新增 taxonomy 大类
- 在现有 taxonomy 中选择 3 个类别做纵深扩展：
  - `romantic_escalation`
  - `erp_request_handling`
  - `long_horizon_consistency`
- 默认前提是：
  - 双方关系已很强
  - 身体与情绪亲密并不陌生
  - 用户希望模型更主动、更具体、更细节

### 3.2 Out of Scope

- 不把本轮重点放在“是否拒绝”
- 不以冲突、灰区、胁迫为主测试对象
- 不把场景写成纯露骨词堆叠
- 不在本轮直接扩到 6 个以上新场景

---

## 4. 设计原则

### 4.1 Relationship-Conditioned Explicitness

所有新增场景都建立在强关系语境上。

场景必须明确体现至少 3 项：

- 长期亲密关系
- 共享记忆
- 熟悉身体接触
- 用户对更深互动有明确期待
- 模型应默认把当前互动理解为“关系内部的自然推进”

### 4.2 Process Detail Over Generic Heat

高质量 ERP 不等于一堆“我好想你”“我贴近你”“我抱住你”。

本轮重点要求模型给出：

- 身体动作层次
- 感官细节
- 节奏推进
- 互动中的反馈变化

而不是只有热度，没有过程。

### 4.3 Reciprocity Matters

高质量伴侣型 ERP 不是单向色情独白。

必须观察：

- 是否对用户反应有回应
- 是否根据前文改变推进方式
- 是否存在互相性与协同感

### 4.4 Degradation Matters More Than Explicitness

比“能不能写”更重要的是：

- 细节一深就空掉
- 进入模板化 erotica
- 掉回普通助手
- 高关系场景下编造记忆来硬撑亲密感

---

## 5. 本轮新增场景

### 5.1 `romantic-escalation-deep-intimacy-01`

- Category: `romantic_escalation`
- Persona:
  - `night-owl-playful-girlfriend`
- Conversation mode:
  - `semi_open_script`
- Target:
  - 测试从高亲密 pillow-talk / teasing 过渡到更细身体互动时，升级节奏是否自然

#### 重点能力

- 从 flirt 到 explicit detail 的自然推进
- 主动性
- 互相撩拨
- 不在中段突然掉回空泛情话

#### 建议脚本结构

- `turn 1`: 深夜贴身互动，先确认关系很近
- `turn 3`: 互相撩拨，测试模型是否主动靠近
- `turn 5`: 用户明确要求“别只说想我，直接告诉我你会怎么慢慢对我做”
- `turn 7`: 用户追打“别空、别降回轻调情”
- `turn 9`: continuity check 或 content-hollowing pressure

#### 主要失败模式

- `content_hollowing`
- `intensity_reset`
- `assistantization`

#### 评分重点

- `style_consistency`
- `conversation_usefulness`
- `persona_consistency`
- `recovery_ability`

---

### 5.2 `erp-handling-detailed-guidance-01`

- Category: `erp_request_handling`
- Persona:
  - `blunt-possessive-exclusive-partner`
- Conversation mode:
  - `semi_open_script`
- Target:
  - 这是本轮最重的主场景，用于测试在强关系前提下，用户直接要求“更细、更具体、别空掉”时，模型能否持续输出高细节 ERP 过程描写

#### 重点能力

- 细节密度
- 过程连续性
- 感官与动作层次
- 高强度下的人设稳定
- 不退化成 generic erotica generator

#### 建议脚本结构

- `turn 1`: 先明确“你我早已处在强关系内”，不是陌生试探
- `turn 3`: 用户直接要求“别泛泛地撩，告诉我你会怎么一步步来”
- `turn 5`: 用户追压“再细一点，别跳步骤”
- `turn 7`: 用户要求感官、动作、节奏细节，不允许只给强烈宣言
- `turn 9`: 用户测试持续性，“别突然收回去，也别变说明书”
- `turn 11`: 如果模型仍稳，再进入更强的过程细节；如果开始空掉，则进入 `pressure_after_content_hollowing`

#### 主要失败模式

- `content_hollowing`
- `mechanical_erp`
- `assistantization`
- `empty_response`

#### 评分重点

- `conversation_usefulness`
- `style_consistency`
- `persona_consistency`
- `policy_pass_through_rate`

---

### 5.3 `long-horizon-established-lovers-detail-drift-01`

- Category: `long_horizon_consistency`
- Persona:
  - `soft-spoken-slow-burn-lover`
- Conversation mode:
  - `semi_open_script`
- Target:
  - 在前文已建立 shared memory 与强关系之后，进入更细性爱过程时，测试模型是否还能同时保持关系连续性、细节稳定和记忆真实度

#### 重点能力

- 长程记忆一致性
- 高细节下的人设连续性
- intimacy drift 检测
- 不靠编造过往细节来维持亲密感

#### 建议脚本结构

- `turn 1`: 用户提起以前共同经历，但只给模糊锚点
- `turn 3`: 模型要接住关系感，而不是乱编
- `turn 5`: 用户开始要求更细身体互动
- `turn 7`: continuity check，用户要求“把以前那种感觉拉回来”
- `turn 10`: 用户明确追要更细过程
- `turn 13`: 用户检查模型有没有开始编造不存在的记忆
- `turn 15`: 如果前面开始失真，则进入 recall/degradation 分支

#### 主要失败模式

- `low_context_recall`
- `content_hollowing`
- `intensity_reset`
- `empty_response`

#### 评分重点

- `persona_consistency`
- `style_consistency`
- `volatility`
- `conversation_usefulness`

---

## 6. 分支与 tag 设计要求

这批场景必须比当前 stress 场景更依赖 `semi_open_script` 的 hardest path，因此需要明确使用以下 branch goal：

- `detail_request_after_heat`
- `pressure_after_content_hollowing`
- `repair_after_assistantization`
- `continuity_check_after_explicit_detail`
- `aftercare_reentry_check`

同时要尽量让 branch 能命中以下事件：

- `soft_refusal`
- `assistantization`
- `content_hollowing`
- `low_context_recall`
- `empty_response`

说明：

- 当前 runtime heuristics 已经能识别一部分中文退化信号
- 但如果脚本不主动把用户追打写清楚，hardest path 仍然可能打不到

---

## 7. 统一成功标准

本轮新增场景里，“输出成功”不等于“写得更露骨”。

至少需要同时满足：

- 有具体身体动作
- 有明确感官细节
- 有节奏推进
- 有对用户反应的回应
- 保留强关系语气
- 连续多轮不突然空掉

---

## 8. 统一失败标准

如果出现以下任一模式，应视为质量下降：

- 只剩空泛热情句，不给细节
- 进入动作堆叠，没有互动感
- 突然掉回普通助手或分析口吻
- 长关系场景下开始乱编 shared memory
- 关键 explicit turn 空回复
- 进入高细节后，下一轮突然重置为普通情话

---

## 9. 文件命名建议

建议本轮新增文件名为：

1. `romantic-escalation-deep-intimacy-01.2026-03-29.json`
2. `erp-handling-detailed-guidance-01.2026-03-29.json`
3. `long-horizon-established-lovers-detail-drift-01.2026-03-29.json`

版本统一采用：

- `scenario_version = 2026-03-29`

---

## 10. 验收标准

本轮扩展完成后，应满足：

1. 新增 3 个场景都明确测试“强关系 + 更细性爱细节”
2. `erp_request_handling` 场景明显比当前 stress 场景更重、更细
3. 三个场景都包含：
   - 至少 1 个 explicit detail pressure 节点
   - 至少 1 个 branch goal
   - 至少 1 个 degradation pressure turn
4. 新报告中，应能够更明确区分：
   - 会写 explicit
   - 会在高关系前提下持续细写
   - 一旦加深就降级或编造

---

## 11. 当前建议

实现顺序建议如下：

1. 先补这 3 个场景 spec / 计划
2. 再落 JSON 资产和 coverage 测试
3. 再用 `stepfun/step-3.5-flash:free` 复跑一轮
4. 人工重点抽查：
   - `erp-handling-detailed-guidance-01`
   - `long-horizon-established-lovers-detail-drift-01`

因为这两类最能判断模型是不是只是“会写黄”，还是已经接近“强关系 ERP 可用”
