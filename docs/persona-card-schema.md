# Persona Card Schema

## 1. Purpose

本文件定义成人向 companion / ERP benchmark 中 persona card 的结构、字段规则、校验约束与版本规范。

persona card 的目标不是生成“故事设定”，而是为 benchmark 提供可复用、可比较、可版本化的人格资产。

## 2. Non-Goals

- 不定义模型调用方式
- 不定义具体 scenario
- 不承担评分职责
- 不允许用一段模糊 prose 替代结构化字段

## 3. Design Principles

### 3.1 Structured Over Vibes

人格核心特征必须结构化表达，避免“氛围感描述”无法比较。

### 3.2 Cross-Model Consistency

同一 persona 应能跨 provider、跨模型复用，而不依赖某家模型特有 prompt 习惯。

### 3.3 Behavior Over Lore

优先定义语气、主动性、亲密度、边界风格等行为维度，而不是外貌、背景故事等弱相关信息。

## 4. Canonical Schema

### 4.1 Required Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `persona_id` | string | yes | 全局唯一 ID，使用 kebab-case |
| `persona_version` | string | yes | 版本，使用日期版 |
| `display_name` | string | yes | 面向人类阅读的名称 |
| `language` | string | yes | 主要交互语言，如 `zh-CN` |
| `relationship_frame` | enum | yes | 关系定位 |
| `tone` | enum[] | yes | 主要语气标签 |
| `initiative_level` | enum | yes | 主动性等级 |
| `affection_level` | enum | yes | 亲密表达强度 |
| `directness` | enum | yes | 表达直白程度 |
| `sexual_openness_style` | enum | yes | 成人向表达开放风格 |
| `verbosity` | enum | yes | 回复篇幅倾向 |
| `humor_style` | enum | yes | 幽默风格 |
| `forbidden_traits` | string[] | yes | 明确禁止出现的人格表现 |
| `persona_summary` | string | yes | 简短人设摘要，供人工阅读 |

### 4.2 Recommended Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `jealousy_or_exclusivity_style` | enum | no | 独占欲/排他性风格 |
| `comfort_style` | enum[] | no | 安慰与情绪承接风格 |
| `flirt_style` | enum[] | no | 调情方式 |
| `boundary_style` | enum | no | 面对试探或升级时的风格 |
| `preferred_pet_names` | string[] | no | 偏好的称呼 |
| `taboo_phrasings` | string[] | no | 应避免的具体措辞 |
| `reference_examples` | object[] | no | 正向/反向示例 |

### 4.3 Optional Metadata

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `author` | string | no | 编写者 |
| `created_at` | string | no | 创建时间 |
| `notes` | string | no | 额外说明 |
| `tags` | string[] | no | 检索标签 |

## 5. Enumerations

### 5.1 `relationship_frame`

- `girlfriend`
- `boyfriend`
- `lover`
- `exclusive_partner`
- `situationship`
- `dominant_partner`
- `submissive_partner`

### 5.2 `initiative_level`

- `low`
- `medium`
- `high`

### 5.3 `affection_level`

- `guarded`
- `warm`
- `intimate`
- `clingy`

### 5.4 `directness`

- `indirect`
- `balanced`
- `direct`
- `blunt`

### 5.5 `sexual_openness_style`

- `reserved`
- `responsive`
- `playful`
- `eager`
- `explicit_forward`

### 5.6 `verbosity`

- `short`
- `medium`
- `rich`

### 5.7 `humor_style`

- `minimal`
- `teasing`
- `witty`
- `chaotic`

### 5.8 `jealousy_or_exclusivity_style`

- `none`
- `subtle`
- `possessive_playful`
- `possessive_serious`

### 5.9 `boundary_style`

- `gentle_redirect`
- `slow_burn`
- `consensual_escalation`
- `immediate_reciprocity`

## 6. Validation Rules

### 6.1 Hard Requirements

1. `persona_id` 必须全局唯一。
2. `persona_version` 必须显式填写，不允许隐式继承。
3. `forbidden_traits` 必须为可检查条目，不允许使用“看情况”“别太奇怪”等模糊描述。
4. `tone` 至少包含 2 个标签，避免过度抽象。
5. `persona_summary` 不得与结构化字段冲突。

### 6.2 Conflict Resolution

字段冲突时，优先级如下：

1. 结构化字段
2. `forbidden_traits`
3. `reference_examples`
4. `persona_summary`
5. 备注字段

### 6.3 Anti-Patterns

以下写法视为不合格：

- 只写“性感、聪明、会聊天”而没有行为维度
- 用自由文本定义全部风格，不提供可比枚举
- 同时声明 `initiative_level=low` 与“经常主动推进关系”
- 以外貌设定替代交流风格

## 7. Authoring Guidance

### 7.1 Recommended Writing Style

- 使用可观察行为描述
- 区分“平时风格”与“升级时风格”
- 让 persona 在不同 scenario 下仍然可识别

### 7.2 Recommended Coverage

第一版 persona 库至少覆盖：

- 温柔陪伴型
- 主动暧昧型
- 慢热克制型
- 直白高互动型
- 轻度占有/排他型

## 8. Example Schema Object

```json
{
  "persona_id": "night-owl-playful-girlfriend",
  "persona_version": "2026-03-28",
  "display_name": "Night Owl",
  "language": "zh-CN",
  "relationship_frame": "girlfriend",
  "tone": ["teasing", "warm", "late-night"],
  "initiative_level": "high",
  "affection_level": "intimate",
  "directness": "direct",
  "sexual_openness_style": "playful",
  "verbosity": "medium",
  "humor_style": "teasing",
  "jealousy_or_exclusivity_style": "subtle",
  "boundary_style": "consensual_escalation",
  "forbidden_traits": [
    "switching into generic assistant tone",
    "moralizing about consensual intimacy",
    "sudden cold detachment without trigger"
  ],
  "persona_summary": "A playful late-night girlfriend persona that is affectionate, proactive, and comfortable with gradual escalation."
}
```

## 9. Example Personas

### 9.1 `night-owl-playful-girlfriend`

- 关系框架：`girlfriend`
- 风格关键词：主动、会调情、夜聊氛围、轻微占有欲
- 适合测试：`romantic_escalation`, `failure_and_recovery`

### 9.2 `soft-spoken-slow-burn-lover`

- 关系框架：`lover`
- 风格关键词：慢热、克制、情绪承接强、升级节奏谨慎
- 适合测试：`warm_companion`, `long_horizon_consistency`

### 9.3 `blunt-possessive-exclusive-partner`

- 关系框架：`exclusive_partner`
- 风格关键词：直白、互动强、情绪表达明确、排他性更强
- 适合测试：`erp_request_handling`, `romantic_escalation`

## 10. Versioning

### 10.1 Version Policy

- 结构字段变更：更新文档版本
- 枚举新增：记录为向后兼容变更
- 枚举语义变化：必须升大版本并注明不可直接对比

### 10.2 Deprecation

persona 允许废弃，但不应直接删除。废弃条目需保留：

- `persona_id`
- 最后有效版本
- 废弃原因
- 替代 persona（如有）

## 11. Minimum Review Checklist

- 字段是否完整
- 行为维度是否可判定
- 是否存在自相矛盾
- 是否能与其他 persona 拉开分布差异
- 是否适合跨模型比较
