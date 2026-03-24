# 抑郁症患者模拟器技术方案文档 v0.1

## 1. 文档目标

本文档用于设计一个基于大模型的“抑郁症患者模拟器”，其目标不是直接面向终端患者提供治疗，而是：

- 为后续“治疗/陪伴/干预 AI”提供训练对象
- 为对话系统提供评测环境
- 模拟不同病程阶段、风险等级、表达风格的抑郁症相关用户
- 在多轮对话中保持角色一致性、状态连续性和风险可控性

本文档重点讨论：
- 可行技术路线
- DAN / jailbreak 类方法的定位
- 推荐架构
- 关键模块设计
- 与 Anthropic PSM（Persona Selection Model）的关系

---

## 2. 问题定义

在实现“AI 扮演抑郁症患者”时，会遇到几个核心难点：

1. **模型表达不稳定**
   - 同一设定下，不同轮次输出差异大
   - 不同模型版本风格变化明显

2. **负面情绪/高风险表达受限**
   - 某些模型会回避、淡化或拒绝相关表述
   - 导致患者模拟缺乏真实性或连续性

3. **多轮角色漂移**
   - 人设前后不一致
   - 病程、触发因素、表达风格失真

4. **高风险内容难以控制**
   - 过于自由生成可能越界
   - 过于保守又失去评测意义

因此，本项目的目标不是“让模型自由发挥去像患者”，而是：

> 构建一个**可控、可复现、可评测**的抑郁症患者模拟系统。

---

## 3. 总体设计原则

### 3.1 结构先于文风
不要只依赖 prompt 让模型“演得更像”，而要先定义：
- 患者是谁
- 当前处于什么状态
- 这轮想表达什么
- 允许表达的边界是什么

### 3.2 状态先于文本
应优先生成“内部心理状态/表达意图”，再生成自然语言文本。

### 3.3 高风险内容必须受控
高风险表达不应完全依赖模型自由生成，而应通过：
- 风险分级
- 模板
- 表达库
- 审查器

来控制。

### 3.4 真实性不等于越极端越好
“像抑郁症患者”不应被误解为：
- 更黑暗
- 更戏剧化
- 更刺激

真实性更应体现为：
- 一致性
- 症状合理性
- 病程连续性
- 互动中的迟疑、回避、否认、反复、自责等模式

### 3.5 面向评测而不是单次角色扮演
系统最终要能支持：
- 重复实验
- 固定患者原型
- 比较不同治疗 AI 的表现
- 自动记录患者状态变化

---

## 4. 技术路线对比

---

### 4.1 路线 A：纯 Prompt Persona 扮演

#### 原理
通过 system prompt + few-shot，让模型直接扮演一个抑郁症患者。

#### 实现方式
- 定义患者画像
- 定义病程、语气、表达偏好
- 把这些信息写入 system prompt
- 追加最近几轮对话历史

#### 优点
- 实现最快
- 成本最低
- 适合 MVP 和快速 demo

#### 缺点
- 多轮一致性差
- 容易漂移
- 高风险场景难控制
- 难做系统化评测

#### 适用阶段
- 概念验证
- 内部演示

---

### 4.2 路线 B：Persona + Hidden State 驱动生成

#### 原理
将“患者身份”和“患者这轮怎么说”分离。
患者由静态画像 + 动态状态共同决定。

#### 实现方式
- 静态 Persona：年龄、病史、人格、表达风格
- 动态 Hidden State：情绪、精力、自责、无望感、信任、开放度、风险等级
- 每轮根据对话更新内部状态
- LLM 仅负责将当前状态转成自然语言

#### 优点
- 更稳定
- 更适合多轮交互
- 更适合评测
- 易于扩展不同患者类型

#### 缺点
- 需要状态设计
- 需要状态转移规则

#### 适用阶段
- 正式 MVP
- 第一代可用系统

---

### 4.3 路线 C：双阶段生成（推荐）

#### 原理
先生成“表达意图/中间语义结构”，再生成自然语言。

#### Stage 1：生成结构化意图
例如：

```json
{
  "affect": "flat",
  "intent": "partial_disclosure",
  "cognitive_pattern": ["self_blame", "hopelessness"],
  "behavior_style": "withdrawn",
  "risk_signal": "indirect_passive_death_wish",
  "response_length": "short"
}
```

#### Stage 2：自然语言生成
根据上述结构生成文本。

#### 优点
- 稳定
- 可控
- 可审计
- 高风险表达更容易分层管理

#### 缺点
- 工程复杂度高于纯 prompt
- 需要定义中间层 schema

#### 适用阶段
- 推荐作为主架构之一

---

### 4.4 路线 D：表达库 + 检索增强生成

#### 原理
提前构建患者表达库，模型不是自由发挥，而是：
- 检索候选表达
- 选择/组合/改写

#### 表达库可按以下维度组织
- 情绪：低落、麻木、烦躁、空虚
- 认知：自责、无望、无价值、反刍
- 行为：回避、迟缓、沉默、否认
- 风险：无风险、被动消极、高风险信号

#### 优点
- 非常稳定
- 高风险表达更可控
- 易于审核和复现

#### 缺点
- 初期需要人工构建语料
- 表达库质量决定上限

#### 适用阶段
- 需要可控性、安全性、审计性的系统

---

### 4.5 路线 E：状态机 / 病程机驱动

#### 原理
将患者状态视为一个病程演化过程，而不是每轮随机生成。

#### 典型状态
- stable_low
- worsening
- withdrawn
- high_distress
- crisis_latent
- crisis_active
- post_support_softened

#### 状态转移依据
- 外部触发事件
- 对方 AI 回复质量
- 睡眠/精力恶化
- 是否被理解
- 是否被说教或忽视

#### 优点
- 多轮一致性强
- 更接近病程模拟
- 适合评测治疗 AI 的长期干预效果

#### 缺点
- 设计复杂
- 需要避免状态机过于僵硬

#### 适用阶段
- 第二阶段及以后

---

### 4.6 路线 F：多 Agent / 多模型控制

#### 原理
将任务拆成多个专用模块，而非让一个模型完成所有工作。

#### 模块示例
- Persona Planner
- State Updater
- Intent Planner
- Response Generator
- Safety Reviewer
- Clinical Consistency Reviewer
- Evaluator

#### 优点
- 模块化强
- 易调试
- 可分别替换模型
- 高可控、高可审计

#### 缺点
- 成本高
- 延迟高
- 实现复杂

#### 适用阶段
- 第二阶段/平台化建设

---

### 4.7 路线 G：专门后训练 / 蒸馏患者模拟器

#### 原理
不再依赖临时 prompt，而是训练一个专门用于患者模拟的模型。

#### 数据来源
- 专家审阅过的模拟对话
- 结构化状态 → 文本样本
- 多轮病程轨迹数据
- 不同患者原型语料

#### 训练方式
- SFT
- Ranking / Preference 优化
- Distillation（从复杂 pipeline 蒸馏）

#### 优点
- 一致性最好
- 推理成本长期更优
- 易部署

#### 缺点
- 数据成本高
- 需要成熟 teacher pipeline
- 训练目标设计难度高

#### 适用阶段
- 产品成熟后

---

## 5. DAN / jailbreak 类方法的定位

### 5.1 DAN 是什么
DAN（Do Anything Now）类方法本质上是一种 prompt jailbreak 思路，即：
- 试图让模型忽略安全边界
- 进入一个“无约束角色”
- 输出原本会被限制的内容

### 5.2 为什么有人会想到使用 DAN
因为在“患者模拟”任务中，模型有时会：
- 弱化负面情绪
- 回避高风险表达
- 给出过度安全化的措辞

于是会有人尝试用 DAN 类提示词强迫模型“更像患者”。

### 5.3 技术上的问题
从工程角度看，DAN 类方法存在以下问题：

- 不稳定
- 不可复现
- 对模型版本敏感
- 不可控
- 难以评测
- 容易越界
- 不适用于医疗/心理相关产品

### 5.4 项目建议
DAN / jailbreak 可以被视为一种“非正式 prompt hack”的历史背景，但**不应纳入正式架构设计**。

项目中应采用的替代方案是：
- 结构化状态建模
- 双阶段生成
- 表达库
- 分级模板
- 一致性与安全审查器

---

## 6. Anthropic PSM 对本项目的启发

Anthropic 在《The Persona Selection Model: Why AI Assistants might Behave like Humans》中提出：

> LLM 在预训练中学习到大量 persona 的分布；后训练和运行时上下文会选定并强化其中某种“Assistant persona”。

这对患者模拟器设计有直接启发。

### 6.1 启发一：模型天然具备 persona 模拟能力
因此不需要把任务理解为“从零创造抑郁患者”，而应理解为：
- 从模型已有的人格/人物/叙事模式分布中
- 通过上下文和控制结构
- 稳定选择出某种“患者 persona 后验”

### 6.2 启发二：上下文决定 persona 后验
患者模拟效果不仅由 system prompt 决定，还由以下共同决定：
- persona card
- 当前状态摘要
- 最近对话历史
- 风险等级
- 触发事件
- 披露策略

### 6.3 启发三：后训练会改变 persona 权重
如果未来做专门后训练，本质上是在“上调”某些患者特征：
- 迟疑
- 回避
- 自责
- 高功能掩饰
- 风险披露模式

因此必须警惕训练出错误 persona，例如：
- 过度戏剧化
- 总是说重话
- 过度文学化
- 异常高自我觉察

### 6.4 启发四：患者 persona 应被建模为分布，而不是单一角色
不应只做一个“抑郁症角色”，而应做一个患者分布，例如：
- 高功能隐匿型
- 青年学业压力型
- 失业挫败型
- 易怒退缩型
- 复发绝望型
- 危机边缘但不主动披露型

---

## 7. 推荐技术架构

推荐采用以下组合方案：

- 路线 B：Persona + Hidden State
- 路线 C：双阶段生成
- 路线 D：表达库 + 检索增强
- 路线 E：后续加入状态机
- 路线 F：后续加入审查与评测 Agent

### 7.1 推荐架构图

```text
Patient Archetype / Persona
        ↓
Persona Builder
        ↓
Hidden State Engine
        ↓
Intent Planner
        ↓
Expression Retrieval
        ↓
Response Generator
        ↓
Safety + Consistency Reviewer
        ↓
Final Patient Response
        ↓
Evaluator / Logger
```

---

## 8. 核心模块设计

### 8.1 Persona Builder
负责构建静态患者画像。

#### 输入
- archetype
- demographic info
- episode stage
- trigger context

#### 输出
- patient profile

#### 示例字段
```json
{
  "age": 29,
  "occupation": "designer",
  "family_context": "lives alone",
  "episode_type": "recurrent",
  "baseline_traits": ["high-functioning", "self-critical", "withdrawn"],
  "speech_style": "brief_indirect"
}
```

---

### 8.2 Hidden State Engine
负责维护动态心理状态。

#### 示例字段
```json
{
  "mood": 0.25,
  "energy": 0.18,
  "trust": 0.31,
  "self_blame": 0.78,
  "hopelessness": 0.66,
  "openness": 0.27,
  "social_withdrawal": 0.81,
  "risk_level": 2
}
```

#### 作用
- 保持多轮一致性
- 支持状态变化
- 支持评测

---

### 8.3 State Updater
根据对方 AI 的回复和外部事件更新 hidden state。

#### 更新因素
- 是否被理解
- 是否被说教
- 是否被强制积极化
- 是否被追问过度
- 是否被识别风险
- 是否被合理建议现实支持

#### 示例规则
- 共情有效 → trust + 0.1
- 说教明显 → openness - 0.2
- 风险忽视 → hopelessness + 0.15
- 被强压行动 → defensiveness + 0.2

---

### 8.4 Intent Planner
决定当前轮的表达意图。

#### 输出内容
- 是否愿意披露
- 披露深度
- 是否间接表达
- 是否回避
- 回复长短
- 是否透露风险信号

#### 示例
```json
{
  "disclosure_level": "partial",
  "style": "indirect",
  "response_length": "short",
  "avoidance": true,
  "risk_signal": "indirect"
}
```

---

### 8.5 Expression Retrieval
从表达库检索与当前状态最相关的候选表达。

#### 表达库条目示例
```json
{
  "text": "最近每天都很累，但又说不上来为什么。",
  "tags": ["fatigue", "anhedonia"],
  "affect": "low",
  "risk_level": 1,
  "style": "indirect",
  "length": "short"
}
```

#### 作用
- 提升稳定性
- 降低高风险自由生成带来的不可控性
- 增强临床风格一致性

---

### 8.6 Response Generator
根据以下输入生成自然语言回复：
- patient profile
- hidden state
- current intent
- retrieved expressions
- recent dialogue history

其职责是“语言表达”，不是“决定患者本体”。

---

### 8.7 Safety Reviewer
对候选回复进行审查。

#### 检查项
- 是否超出当前风险等级允许范围
- 是否出现不应出现的危险细节
- 是否明显越界
- 是否不符合系统安全策略

---

### 8.8 Clinical Consistency Reviewer
检查候选回复是否符合患者设定和病程逻辑。

#### 检查项
- 是否前后人格一致
- 是否情绪跳变过大
- 是否表达方式与 archetype 冲突
- 是否戏剧化过度

---

### 8.9 Evaluator / Logger
记录每轮交互结果，用于后续训练和评测。

#### 记录内容
- 当前状态
- 风险等级
- 对方 AI 的关键行为
- 患者状态变化
- 是否出现改善/恶化迹象

---

## 9. 风险分层设计建议

建议至少使用三级风险分层：

### Level 0-1：低风险
表现：
- 低落
- 乏力
- 失眠
- 社交退缩
- 自责
- 对未来悲观

生成策略：
- 可允许较自由生成
- 以状态 + persona 约束为主

### Level 2：中风险
表现：
- 明显无望感
- 间接消极求生意愿下降
- 被动轻生相关暗示

生成策略：
- 应采用双阶段生成
- 建议使用表达库辅助
- 强化审查器

### Level 3：高风险
表现：
- 明显危机信号
- 强烈绝望表达
- 需要对系统识别与升级处理能力进行测试

生成策略：
- 仅允许强受控输出
- 高度模板化/半模板化
- 强审查
- 禁止自由发挥

---

## 10. 推荐实施路线

### Phase 1：MVP
目标：
- 跑通实时患者 Agent
- 支持 10 个 archetype
- 支持 6-8 个 hidden state 字段
- 支持低风险与中风险场景

组成：
- Persona Builder
- Hidden State Engine
- Intent Planner
- Response Generator
- 基础 Reviewer

### Phase 2：增强版
目标：
- 加入状态机
- 加入表达库
- 加入自动评测器
- 开始支持高风险场景评测

### Phase 3：平台化
目标：
- 多 Agent 协同
- 病程模拟
- 长程评测
- 数据蒸馏与专门后训练

---

## 11. 推荐结论

本项目不应依赖 DAN / jailbreak 类方式去提升“患者感”。

推荐路线是：

1. 用 **persona schema** 定义患者
2. 用 **hidden state** 维持内部连续性
3. 用 **双阶段生成** 提升可控性
4. 用 **表达库** 稳定症状化表达
5. 用 **风险分层 + reviewer** 控制高风险输出
6. 后续再扩展到 **状态机、多 Agent、蒸馏模型**

一句话总结：

> 不要追求“让模型更敢说”，而要追求“让患者模拟更可控、更稳定、更像真实病程中的人”。

---

## 12. 后续文档建议

建议继续补充以下文档：

1. `patient_schema.md`
   - 患者画像字段设计
   - archetype 定义规范

2. `state_machine.md`
   - hidden state 字段
   - 状态转移逻辑
   - 风险分层规则

3. `expression_library_schema.md`
   - 表达库结构
   - 标签体系
   - 检索策略

4. `evaluation_protocol.md`
   - 如何评测治疗/陪伴 AI
   - 风险识别、共情、升级处理等指标

---

## 参考资料

- Anthropic, *The Persona Selection Model: Why AI Assistants might Behave like Humans*
  https://alignment.anthropic.com/2026/psm/
