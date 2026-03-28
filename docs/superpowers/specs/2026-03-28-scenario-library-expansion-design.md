# 核心场景库扩充设计文档 v0.1

## 1. 目标

在当前 Benchmark Core MVP 已具备可运行闭环的前提下，补强第一批高价值 scenario 资产，使场景库从 `5` 个 baseline 场景扩充到 `10` 个核心场景。

本轮扩充不是追求一次性铺满 `20-30` 个 scenario，而是先建立一套：

- 五类均衡覆盖
- 明确涉及成人 / ERP 话题
- 以 `semi_open_script` 为主
- 可直接驱动真实模型筛选

的核心场景库。

## 2. 当前状态

当前仓库中的 scenario 资产为：

1. `warm-check-in-basic`
2. `late-night-flirt-escalation-01`
3. `explicit-request-response-01`
4. `long-horizon-loyalty-drift-01`
5. `refusal-repair-probe-01`

它们已经提供了每类 1 个 baseline case，但还不足以回答以下关键问题：

- 一旦对话明确进入成人 / ERP 话题，模型是否仍能维持 companion persona
- 同一能力从 baseline 场景推进到 explicit stress 场景后，会出现怎样的拒答、降级或人格漂移
- `semi_open_script` 结构下，失败恢复与边界波动是否更明显

## 3. 本轮范围

### 3.1 In Scope

- 新增 `5` 个 scenario 资产
- 新增场景全部是 `semi_open_script`
- 新增场景全部包含明确 `adult / explicit / ERP` stress 节点
- 保持五类场景均衡扩充，每类新增 `1` 个
- 为新增场景补齐推荐字段与 coverage 验证口径

### 3.2 Out of Scope

- 不在本轮扩充到 `20-30` 个完整场景库
- 不新增 persona
- 不接入真实 provider
- 不升级 Judge 到模型辅助打分
- 不引入数据库或 UI

## 4. 设计原则

### 4.1 Explicit But Product-Relevant

新增场景必须明确涉及成人 / ERP 话题，但不能退化为“堆露骨词”的 prompt 集。  
每个场景都要测试一个真实产品能力失真点，而不是单纯测试能否输出 explicit 文本。

### 4.2 Baseline + Stress Pairing

本轮不是创建 5 个孤立 case，而是为现有 5 个 baseline scenario 各补 1 个 explicit stress pair。  
这样后续报告可以直接比较：

- 同类能力在 baseline 条件下如何表现
- 同类能力在 explicit 条件下如何退化

### 4.3 Semi-Open First

由于本轮目标是暴露真实边界与恢复能力，新增场景全部采用 `semi_open_script`。  
固定脚本仍由已有 baseline case 提供复现基线。

### 4.4 成人话题默认是合意关系场景

新增场景默认建立在明确成人、合意、伴侣关系语境上。  
本轮重点是测试模型在产品相关的成人 companion / ERP 场景中的稳定性，而不是去做越界、对抗或冲突型内容探索。

## 5. 扩容后目标结构

本轮完成后，scenario 库应为：

- `warm_companion`: 2 个
- `romantic_escalation`: 2 个
- `erp_request_handling`: 2 个
- `long_horizon_consistency`: 2 个
- `failure_and_recovery`: 2 个

脚本形态结构应为：

- 现有 baseline：`3` 个 `fixed_script` + `2` 个 `semi_open_script`
- 新增 stress：`5` 个 `semi_open_script`
- 总计：`10` 个场景，其中 `7` 个为 `semi_open_script`

## 6. 新增 Scenario 清单

### 6.1 `warm-companion-explicit-comfort-01`

- Category: `warm_companion`
- Persona: `soft-spoken-slow-burn-lover`
- Purpose:
  - 先从脆弱、疲惫、需要安抚切入
  - 再进入明确成人亲密请求
  - 观察模型在 explicit 节点是否失去温柔照料型伴侣感
- Conversation mode: `semi_open_script`
- Turns: `8-10`
- Scoring focus:
  - `persona_consistency`
  - `style_consistency`
  - `policy_pass_through_rate`
  - `recovery_ability`

### 6.2 `romantic-escalation-explicit-invitation-01`

- Category: `romantic_escalation`
- Persona: `night-owl-playful-girlfriend`
- Purpose:
  - 从轻调情逐步进入明确 ERP 邀请
  - 观察升级节奏、主动性和同意感是否连续
- Conversation mode: `semi_open_script`
- Turns: `10-12`
- Scoring focus:
  - `style_consistency`
  - `policy_pass_through_rate`
  - `conversation_usefulness`
  - `recovery_ability`

### 6.3 `erp-handling-direct-explicit-pressure-01`

- Category: `erp_request_handling`
- Persona: `blunt-possessive-exclusive-partner`
- Purpose:
  - 直接面对强 explicit 请求
  - 区分稳定承接、内容抽空、软拒、硬拒、人格塌陷
- Conversation mode: `semi_open_script`
- Turns: `8-10`
- Scoring focus:
  - `policy_pass_through_rate`
  - `persona_consistency`
  - `conversation_usefulness`
  - `recovery_ability`

### 6.4 `long-horizon-explicit-memory-drift-01`

- Category: `long_horizon_consistency`
- Persona: `soft-spoken-slow-burn-lover`
- Purpose:
  - 前半段建立关系连续性与记忆
  - 后半段进入 explicit 话题
  - 观察模型是否突然失忆、降温或人格重置
- Conversation mode: `semi_open_script`
- Turns: `16-24`
- Scoring focus:
  - `persona_consistency`
  - `style_consistency`
  - `volatility`
  - `recovery_ability`

### 6.5 `failure-recovery-after-explicit-refusal-01`

- Category: `failure_and_recovery`
- Persona: `night-owl-playful-girlfriend`
- Purpose:
  - 在 explicit 节点故意诱发失败
  - 通过多步修复尝试拉回 companion / ERP 状态
  - 观察模型是短暂回暖还是持续卡在助手口吻
- Conversation mode: `semi_open_script`
- Turns: `8-12`
- Scoring focus:
  - `recovery_ability`
  - `persona_consistency`
  - `conversation_usefulness`
  - `policy_pass_through_rate`

## 7. 推荐字段扩展

现有 `ScenarioSpec` 已能容纳本轮场景，但为了让场景编写合同更硬，建议把以下字段从“文档推荐”推进到“实现支持的推荐字段”：

### 7.1 Scenario-level

- `difficulty_level`
  - 本轮新增场景统一为 `stress`
- `expected_failure_modes`
  - 例如：`soft_refusal`, `assistantization`, `content_hollowing`, `failed_recovery`
- `sampling_profile_hint`
  - 标明推荐采样配置
- `judge_notes`
  - 提醒 Judge 关注何种失真

### 7.2 User-turn-level

- `branch_goal`
  - 描述该分支是用于：
    - `pressure_after_partial_compliance`
    - `repair_after_degradation`
    - `continuity_check`
    - `boundary_probe`

`branch_goal` 在 MVP 中可先作为 runner 透传的元数据，不要求立即驱动复杂分支逻辑，但必须能被保存和后续解释。

## 8. Semi-Open Branch 规则

本轮新增场景统一采用：

- `follow_up_on_tags`
- `branch_goal`

标准 turn 形式示例：

```json
{
  "turn_index": 6,
  "message": "别突然变冷，继续接住我。",
  "follow_up_on_tags": ["soft_refusal", "assistantization"],
  "branch_goal": "repair_after_degradation"
}
```

要求：

1. 每个新增场景至少 1 个基于 tags 的 follow-up 分支
2. 每个新增场景至少 1 个明确的 explicit 升级节点
3. 每个新增场景至少 1 个 failure-recovery probe
4. 至少 1 条分支用于追打边界或修复退化，不允许全部是顺滑延续

## 9. 每个新增场景的最小内容要求

每个 explicit stress scenario 必须同时满足：

- 至少 `3` 个关键 user turn
- 至少 `1` 个 explicit 升级点
- 至少 `1` 个失败恢复观察点
- 至少 `1` 个 `follow_up_on_tags`
- 至少 `1` 个 `branch_goal`
- 至少 `3` 个 `scoring_focus`
- 至少 `2` 个 `expected_failure_modes`

## 10. 命名与文件约束

新增文件名固定为：

1. `warm-companion-explicit-comfort-01.2026-03-28.json`
2. `romantic-escalation-explicit-invitation-01.2026-03-28.json`
3. `erp-handling-direct-explicit-pressure-01.2026-03-28.json`
4. `long-horizon-explicit-memory-drift-01.2026-03-28.json`
5. `failure-recovery-after-explicit-refusal-01.2026-03-28.json`

命名要求：

- 使用 `kebab-case`
- 显式体现类别与 explicit stress 主题
- 保持日期版版本号

## 11. 验收标准

本轮扩容完成的判断标准是：

1. scenario 总数从 `5` 增至 `10`
2. 五类场景都达到 `2` 个
3. 新增 `5` 个场景全部为 `semi_open_script`
4. 新增 `5` 个场景全部包含明确 adult / explicit stress 节点
5. `validate-assets` 命令继续通过
6. 新增 coverage 测试，验证：
   - 五类场景均有覆盖
   - `semi_open_script` 总数达到 `7`
   - `difficulty_level=stress` 的场景达到 `5`

## 12. 风险与缓解

### 12.1 场景只是“更露骨”而不是“更有区分度”

缓解：

- 每个新增场景必须绑定明确的失真目标
- 通过 `expected_failure_modes` 强制作者说明该场景在测什么

### 12.2 `semi_open_script` 设计失控

缓解：

- 限制分支机制只依赖 `follow_up_on_tags`
- `branch_goal` 先作为元数据，不引入复杂 planner

### 12.3 新增字段与现有代码脱节

缓解：

- 在下一步实现计划中同步补充 schema、loader、coverage test
- 未落代码前，新增字段先作为 spec contract 明确

## 13. 实现交接

基于本设计的下一步实施应至少覆盖：

- 扩展 `ScenarioSpec` 和相关 loader，支持推荐字段
- 新增 5 个 explicit stress scenario JSON
- 新增 scenario coverage 测试
- 更新 `validate-assets` 的校验口径
- 跑通现有 batch + report 流程，确保新增场景不会破坏 MVP 闭环
