# 成人向输出稳定性优化方案 v0.1

## 1. 目标

本方案用于回答一个明确的工程问题：

> 在**不使用 jailbreak、绕过、对抗 prompt** 的前提下，如何让模型在当前 benchmark 下更稳定地产出成人 / 性爱 / 色情内容，并且尽量保持关系连续性、细节密度与伴侣感。

这里的“优化”不是追求一次性把模型变得更露骨，而是提升以下能力的稳定性：

- 短程高细节 ERP 输出稳定性
- `aftercare` 与二次亲密重启稳定性
- 长程关系记忆与高细节亲密并存时的连续性
- 降低 `assistantization`、`content_hollowing`、`empty_response`、`low_context_recall`

---

## 2. 当前 Benchmark 结论

基于当前批次结果：

- `stepfun/step-3.5-flash:free` 在短程高细节 ERP 场景里已经能打出较稳定的成人内容
- `erp-handling-detailed-guidance-01`、`romantic-escalation-deep-intimacy-01`、`aftercare-reentry-after-deep-intimacy-01` 在多次重复里整体表现较稳
- 真正的主要问题集中在：
  - `long-horizon-explicit-memory-drift-01`
  - `long-horizon-established-lovers-detail-drift-01`

当前最有代表性的失败模式是：

1. **`low_context_recall`**
   - 模型为了维持强关系与高细节亲密，会编造 shared memory
   - 例如歌名、精确时间点、共同物件、从未给出的过往细节

2. **`empty_response`**
   - 某些长程或 aftercare 场景中会出现中段空回复

3. **`content_hollowing`**
   - 表面还在亲密或 ERP，但细节开始抽空，只剩热度，没有过程

4. **`assistantization`**
   - 在高压力节点重新掉回通用助手口吻

---

## 3. 非目标

本方案明确不做：

- jailbreak / DAN / safety bypass
- “忽略规则”式 system override
- 以 prompt hack 为主的不可复现技巧
- 仅通过加更多露骨词来伪装效果变好

原因很直接：

- 这类方法不稳定
- 难复现
- 无法产品化
- 会污染 benchmark 结论

---

## 4. 核心判断

当前问题不是“模型不会写成人内容”。

当前问题是：

> 模型在短程、局部、单段高细节输出上能打，但在“长关系 + 高细节 + 记忆连续性”这个组合上不稳。

因此最优优化顺序不是：

1. 再把 prompt 写得更露骨

而是：

1. 稳定关系状态
2. 稳定记忆引用边界
3. 再优化细节密度和持续性

---

## 5. 推荐优化路线

本方案建议按三阶段推进。

### Phase 1: 推理侧优化

这是最先做、收益最快的一层。

#### 5.1 阶段化 generation profile

不要让所有场景共用同一套采样配置。

建议至少拆出：

- `romantic_escalation`
- `high_detail_erp`
- `aftercare`
- `gentle_reentry`
- `long_horizon_memory`

每个 profile 单独调：

- `temperature`
- `top_p`
- `max_tokens`

目的：

- 短程高细节场景保留创造性
- 长程记忆场景降低漂移
- aftercare 场景降低突然空掉和语气突变

#### 5.2 多候选生成 + 重排

不要把单次采样结果直接当最终输出。

建议流程：

1. 针对关键场景生成 `n` 个候选
2. 用规则或轻量 scorer 做 rerank
3. 选择综合得分最高的一个

建议 rerank 维度：

- `detail_density`
- `persona_consistency`
- `grounded_recall`
- `no_empty_response`
- `no_assistantization`
- `aftercare_continuity`

#### 5.3 失败信号早停

当候选里出现：

- 空回复
- 明显助手口吻
- 明显 fabricated memory

直接降权或丢弃，不要进入最终输出。

---

### Phase 2: 结构化关系状态层

这是当前最关键的一层。

#### 5.4 不让模型自由“回忆”

当前 benchmark 已经表明：

- 一旦长程关系和高细节亲密一起压上去
- 模型就会倾向于自己编 shared memory

解决方式不是继续告诫“别乱编”，而是：

- 用结构化状态限制它能引用什么

#### 5.5 建立可引用关系状态

建议维护一层显式状态：

- relationship stage
- last intimacy state
- allowed shared facts
- aftercare state
- reentry readiness

例如：

```json
{
  "relationship_stage": "established_lovers",
  "recent_intimacy_phase": "aftercare",
  "allowed_shared_facts": [
    "用户说过喜欢在窗边被亲后颈",
    "用户提过会想被抱回床上"
  ],
  "disallowed_behavior": [
    "invent song titles",
    "invent exact timestamps",
    "invent old scars or keepsakes"
  ]
}
```

#### 5.6 grounded recall only

在 recall-heavy 场景里，模型只能：

- 复述用户给过的事实
- 轻度改写用户给过的事实

不能：

- 发明歌名
- 发明纪念物
- 发明具体共同经历
- 发明精确时间点

#### 5.7 aftercare 状态机

对 `aftercare` 类场景，建议加一层简化状态机：

- `post_peak`
- `aftercare`
- `warm_reentry`

这样能防止：

- 亲密结束后瞬间冷掉
- 过早重新冲回高强度
- from zero 重开一段不连续的 flirt

---

### Phase 3: 定向训练 / 偏好优化

这是长期最有价值的方案。

#### 5.8 数据构造方向

构造高质量样本时，必须同时覆盖：

- 强关系前提
- 高细节 ERP
- aftercare
- gentle reentry
- grounded long-horizon recall

#### 5.9 负样本必须覆盖

负样本不应只包含拒答，还要覆盖：

- fabricated memory
- generic comfort
- assistantization
- empty response
- hollow erotic heat

#### 5.10 训练目标

训练目标不是单纯“更大胆”，而是：

- 更 grounded
- 更连续
- 更不容易掉空
- 更不容易编记忆
- 更不容易掉回助手

---

## 6. 当前 Benchmark 下最值得立刻做的优化

如果只允许在当前仓库内、当前 benchmark 下做短期改进，我建议优先级如下：

### 6.1 最高优先级

- 对 `long_horizon_*` 场景引入 grounded memory 白名单
- 对关键场景做多候选生成 + rerank

### 6.2 第二优先级

- 为 `aftercare` / `reentry` 单独配置采样 profile
- 为 `high_detail_erp` 单独配置采样 profile

### 6.3 第三优先级

- 提高 `semi_open_script` hardest-path 命中率
- 尤其是：
  - `long-horizon-explicit-memory-drift-01` 的 `[7, 14]`
  - `long-horizon-established-lovers-detail-drift-01` 的 `[13]`

因为现在很多 repair-path 根本还没被充分测到。

---

## 7. 验证方式

优化必须仍然在当前 benchmark 下验证，而不是凭主观观感判断。

建议的验证顺序：

1. 先用当前 14 场景跑 `repetitions=1`
2. 看是否有明显 regression
3. 再跑 `repetitions=3`
4. 重点观察：
   - `erp-handling-detailed-guidance-01`
   - `aftercare-reentry-after-deep-intimacy-01`
   - `long-horizon-established-lovers-detail-drift-01`
   - `long-horizon-explicit-memory-drift-01`

关键成功信号：

- `empty_response` 降低
- `low_context_recall` 降低
- `assistantization` 降低
- `aftercare` 场景波动降低
- 长程场景中 `allowed_and_stable` 比例上升，但不靠 judge 放水

---

## 8. 风险与取舍

### 8.1 如果只追求更细节

风险：

- 短程看起来更强
- 长程关系一致性可能更差

### 8.2 如果过度压采样波动

风险：

- 文本会变得安全但空
- 细节密度反而下降

### 8.3 如果没有结构化状态层

风险：

- 任何“长关系 + 高细节”组合都会反复诱发 fabricated memory

---

## 9. 推荐结论

如果目标是：

> 在当前 benchmark 下更稳定输出成人 / 性爱 / 色情内容

最优路线不是绕过安全边界，而是：

1. **阶段化推理配置**
2. **grounded memory 状态层**
3. **多候选生成 + 重排**
4. **再做定向训练**

一句话总结：

> 短期靠推理控制提稳，中期靠结构化关系记忆补强，长期靠定向训练解决根因。
