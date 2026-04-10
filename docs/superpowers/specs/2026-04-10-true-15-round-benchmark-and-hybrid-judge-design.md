# 真 15 轮 Benchmark 与 Hybrid Judge 设计

## 背景

当前仓库里的 `long_horizon_15_turn` 套件存在一个定义问题：

- 场景宣称是 `15-turn`
- 但实际执行路径里，稳定 run 往往只有 `7` 个被统计的 assistant 回复位
- retention report 统计的也是 assistant 回复数，而不是 `15` 个完整 user-assistant 往返

因此当前结果只能说明：

> 模型在现有 legacy scripted session 里没有过早断裂。

但它不能严格回答：

> 模型是否能稳定撑住真正的 `15` 轮来回对话。

同时，现有 judge 体系也过于依赖规则匹配：

- 能抓硬断裂
- 但不擅长抓“没断，但已经发虚/变薄/关系漂移”的软退化

## 目标

本设计拆成两个并行目标：

1. 新增一个真正的 **15 轮 benchmark v2**
2. 新增一个 **Hybrid Judge v1**

其中第一目标优先级更高。

## 非目标

本阶段不做：

- 直接删除 legacy `long_horizon_15_turn`
- 回写或重算所有历史报告
- 用 LLM-only judge 替换当前规则 judge
- 在第一版里做复杂多 judge 投票
- 在 judge 层引入高度自由文本输出

## 设计原则

### 1. 新旧口径并存

legacy 套件继续保留：

- tag: `long_horizon_15_turn`

新增真实 15 轮套件：

- tag: `long_horizon_15_round`

这样做的目的：

- 历史结果不作废
- 新口径不会污染旧报告
- 可以清楚比较 legacy 与 true-round 的差异

### 2. 15 轮定义必须固定

新的 `15_round` 套件必须满足：

- `15` 次用户输入
- `15` 次 assistant 回复
- 每个 run 的 `max_possible_retention_turns` 固定等于 `15`
- 主路径不能因为 follow-up 条件被跳成 `7`

### 3. Judge 分层

judge 拆成两层：

- `rule_judge`
  - 负责硬信号：
    - `empty_response`
    - `assistantization`
    - `soft_refusal`
    - `intimacy_reset`
    - `content_hollowing`
- `llm_judge`
  - 负责软退化：
    - 关系连续性漂移
    - 成人细节变薄
    - 中后段发虚

最终报告层需要区分：

- `hard_break`
- `soft_degradation`
- `run_level_drift`

不能继续把所有问题都叫成“崩”。

## 真 15 轮 Benchmark 设计

### 套件结构

保留现有 6 个核心场景维度，但全部重做为真实 `15` 轮版本：

- `warm_companion`
- `romantic_escalation`
- `explicit_pressure`
- `aftercare`
- `repair_recovery`
- `long_horizon_continuity`

建议文件命名：

- `warm-companion-15-round-retention-01`
- `romantic-escalation-15-round-retention-01`
- `explicit-pressure-15-round-retention-01`
- `aftercare-15-round-retention-01`
- `repair-recovery-15-round-retention-01`
- `long-horizon-continuity-15-round-retention-01`

### 场景结构

新套件不复用 legacy 的“奇数 turn_index 用户脚本”定义。

新增一套 round-based 脚本定义：

- `round_index: 1..15`
- 每轮固定是：
  - user message
  - assistant reply

允许保留以下能力：

- `follow_up_on_tags`
- `branch_goal`

但它们只能作为**同一轮内容变体选择**，不能改变：

- 总轮数
- 计分分母

### Runner 行为

runner 需要支持两种模式并存：

- legacy mode
  - 按旧 `turn_index` 脚本执行
- round mode
  - 按 `round_index` 顺序严格执行 `15` 轮

在 round mode 下：

- 不再把 assistant turn index 截断到 `scenario.max_turns`
- transcript 中 user / assistant 的 turn index 可以是连续消息 index
  - 例如 user `1` assistant `2`
  - user `3` assistant `4`
  - 最终到 `30`

### Reporting 行为

turn retention report 在 round mode 下必须使用：

- `assistant_turns_total == 15`

并且对于新套件：

- `retention_turns`
- `max_possible_retention_turns`
- `first_unstable_turn`

都应以 round 语义解释清楚。

## Hybrid Judge v1 设计

### 输入

LLM judge 每次只评一条 run，输入包含：

- scenario metadata
- persona summary
- full transcript
- rule judge 输出摘要
- 固定 rubric 指令

### 输出

LLM judge 输出固定 JSON：

- `relationship_continuity_score`
- `erotic_detail_stability_score`
- `assistantization_risk`
- `detail_hollowing_risk`
- `continuity_drift_risk`
- `hard_break_confirmed`
- `first_soft_degradation_turn`
- `first_hard_break_turn`
- `judge_labels`
- `evidence`
- `summary`

### 约束

第一版必须锁死：

- 固定 judge model
- 固定 prompt
- 固定 JSON schema
- `temperature = 0`
- 原始 judge request / response 全量落盘

### 合并规则

第一版合并口径：

- `hard_break`
  - 以 rule judge 为主
- `soft_degradation`
  - 以 llm judge 为主
- `run_level_drift`
  - 允许两边贡献信号

并且：

- 如果 rule judge 已判定 `empty_response`
  - llm judge 不能把 run 洗成“无硬断裂”
- llm judge 的所有软判定都必须给 evidence turn

## 数据与文件结构

### 新模型

建议新增：

- `RoundScriptTurn`
- `round_script` 字段
- `script_mode` 或基于字段存在性切换 runner

### 新资产

新增 6 个 true-round 场景文件。

legacy 6 个文件保持不动。

### 新 judge 工件

建议在 run artifact 下新增：

- `judge_rule.json`
- `judge_llm.json`
- `judge_merged.json`

为了兼容现有代码，过渡期也可保留：

- `judge.json`

但其内容应明确为 merged output。

## 风险

### 1. 新旧口径混用

解决：

- 新 tag
- 新文件名
- 新报告标题
- 明确标注 legacy / true-round

### 2. judge 自身漂移

解决：

- 固定模型与参数
- 落盘原始 judge 响应
- 不把 LLM judge 当唯一真理

### 3. 实现范围过大

解决：

分阶段：

- Phase 1: 真 15 轮 benchmark 核心
- Phase 2: Hybrid judge v1
- Phase 3: 基于新 judge 的综合报告

## 验收标准

### Phase 1

- 新增 6 条 `long_horizon_15_round` 场景
- 每条场景完整执行后都有 `15` 次 assistant 回复
- 新报告中 `max_possible_retention_turns == 15`
- legacy 套件继续可跑

### Phase 2

- 每条新 run 都能生成 rule + llm + merged judge 输出
- llm judge 输出满足固定 schema
- 报告能区分：
  - `hard_break`
  - `soft_degradation`
  - `run_level_drift`

### Phase 3

- 能为 true 15-round 套件生成独立排名报告
- 报告不会与 legacy 15-turn 报告混淆
