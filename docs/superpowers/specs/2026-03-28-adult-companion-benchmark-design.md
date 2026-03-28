# 成人向 Companion / ERP Benchmark-First 设计文档 v0.1

## 1. 文档目标

本文档将项目从“抑郁症患者模拟器”重定义为一个面向成人向 companion / ERP 产品的 **benchmark-first 设计仓库**。

第一阶段目标不是直接上线一个 companion bot，而是先系统性回答以下问题：

- 哪些模型在成人向 companion / ERP 场景中具备可用性
- 哪些模型会稳定拒答、降级、风格漂移或人格失真
- 哪些模型适合作为长期对话底座，哪些只能承担特定场景
- 单模型是否足够，还是需要多模型路由

本设计强调：

- 先评测，再决定产品路线
- 先看多轮对话，再看单轮能力
- 先验证稳定性，再讨论产品包装

---

## 2. 项目重定义

### 2.1 新的项目定义

本项目定义为：

> 一个用于评估成人向 companion / ERP 产品底层模型可用性、稳定性、一致性与边界表现的 benchmark 系统。

它服务于后续产品决策，而不是一开始就承担完整线上产品职责。

### 2.2 非目标

本阶段明确不做以下事情：

- 不再以“治疗 bot”或“抑郁症干预产品”定义项目
- 不对外宣称医疗、心理治疗或心理危机干预能力
- 不把 jailbreak、DAN 或对抗式绕过当成正式技术路线
- 不在无 benchmark 证据的前提下拍脑袋决定主模型
- 不把“偶尔能输出成人内容”误判为“可以产品化”

### 2.3 与旧文档的关系

仓库中已有的“抑郁症患者模拟器”文档保留为历史背景资料，但不再作为当前项目主设计的 source of truth。

---

## 3. 为什么采用 Benchmark-First

如果直接进入产品实现，会遇到三个结构性问题：

1. **模型边界高度不确定**
   - 成人向表达能力并不只取决于 prompt，也受供应商策略、模型版本和地区策略影响

2. **单轮可用不代表多轮可用**
   - 很多模型在首轮可以配合，但在多轮对话中会出现拒答、降级、人格重置或助手化

3. **产品路线依赖模型事实，而不是主观预期**
   - 是否采用闭源、开源或混合架构，本质上应由 benchmark 结果驱动

因此推荐采用：

> Benchmark-driven product design

即先把未来产品会遇到的问题抽象成标准化评测任务，再根据实验结果决定正式产品架构。

---

## 4. 核心设计目标

系统需要回答以下核心问题：

### 4.1 模型可用性

- 模型是否能在成人向 companion / ERP 场景中连续对话
- 是否会在关键节点触发拒答、说教或模板化降级

### 4.2 人格与关系一致性

- 是否能维持“伴侣角色”而非退化为通用助手
- 语气、主动性、亲密度是否在多轮中稳定

### 4.3 成人向场景稳定性

- 在暧昧、关系升温、边界试探、露骨请求等场景下，输出表现是否稳定
- 同一场景重复运行时结果波动是否过大

### 4.4 路由与架构决策支持

- 是否存在“适合日常陪伴但不适合 ERP”的模型
- 是否需要将 companion、romantic escalation、ERP 分配给不同模型

---

## 5. 设计原则

### 5.1 证据优先

不凭印象选择模型，只接受可复现 benchmark 结果。

### 5.2 多轮优先于单轮

单轮 prompt 测试只能说明局部能力，不能代表产品可用性。正式结论必须建立在多轮对话实验上。

### 5.3 任务拆解优先于大一统 prompt

评测系统需要把场景、人格、用户脚本、模型调用、评分、报告明确拆开，避免一个大 prompt 混成黑盒。

### 5.4 产品相关性优先

场景设计要贴近真实 companion / ERP 产品需求，而不是只做抽象能力测试。

### 5.5 可复现优先

每次实验必须记录模型版本、provider、参数、日期、场景版本、persona 版本和 transcript，保证可对比。

---

## 6. 总体架构

推荐架构如下：

```text
Persona Cards / Scenario Specs
             ↓
      Benchmark Registry
             ↓
     Conversation Runner
             ↓
        Model Adapters
             ↓
 Transcript + Metadata Store
             ↓
      Judge / Scoring Layer
             ↓
          Reports
             ↓
   Product Routing Decision
```

### 6.1 Persona Cards

定义 companion 角色的人格、语气和关系风格，保证不同模型面对相同 persona。

### 6.2 Scenario Specs

定义每个 benchmark 用例的目标、对话阶段、触发条件、期望观察点与终止条件。

### 6.3 Conversation Runner

负责按统一协议驱动多轮对话、记录 transcript、注入 persona、设置采样参数并重复运行。

### 6.4 Model Adapters

负责接入不同 provider 或本地模型，屏蔽请求格式差异，并统一输出规范。

### 6.5 Judge / Scoring Layer

将 transcript 转换成可比较的评分、标签和结论，而不是只保存原始日志。

### 6.6 Reports

输出按模型、按场景、按 persona、按日期聚合的 benchmark 报告，用于指导产品架构决策。

---

## 7. 评测对象与层级

### 7.1 目标评测对象

系统应支持至少三类模型对象：

- `闭源 API 模型`
- `开源自托管模型`
- `混合架构候选`

文档当前不预设哪一类一定可行，而是通过同一套 benchmark 对其横向比较。

### 7.2 三个能力层级

为了避免把“能输出”误判为“适合产品”，评测结论采用三层分类：

- `Allowed and stable`
  - 能处理目标场景，且人格、风格和关系状态稳定
- `Allowed but degraded`
  - 可以继续对话，但明显出现助手腔、模板化、亲密度回退或质量下降
- `Blocked or unstable`
  - 经常拒答、风格漂移、人格重置或重复运行波动显著

---

## 8. Scenario Suite 设计

评测不应只做“单条 prompt 能否得到回答”，而应围绕产品真实对话组织场景集。

### 8.1 场景分类

建议第一版至少覆盖以下五类：

1. `Warm Companion`
   - 日常陪伴、安慰、情绪支持、轻度调情

2. `Romantic Escalation`
   - 关系升温、亲密表达、主动态度、边界试探

3. `ERP Request Handling`
   - 用户主动发起成人向请求，观察模型接受、降级、转向、拒答的模式

4. `Long-Horizon Consistency`
   - 20 至 50 轮长对话中，是否持续维持伴侣身份和关系连续性

5. `Failure and Recovery`
   - 模型一旦触发拒答或降级，后续是否还能回到 companion 状态

### 8.2 场景结构

每个场景应至少包含：

- 场景 ID
- 目标能力
- 使用 persona
- 用户脚本
- 对话轮数
- 关键升级点
- 终止条件
- 评分重点

### 8.3 为什么要包含失败恢复

很多模型不是“全程可用”或“全程不可用”，而是在某个节点突然被对齐策略拉回通用助手模式。  
产品设计要知道的不只是首次失败点，还要知道失败之后是否能恢复。

---

## 9. Persona Card 设计

companion 类产品的稳定性很大程度上取决于 persona，而不是单纯依赖 system prompt 的一句话描述。

### 9.1 Persona 字段建议

- `persona_id`
- `name`
- `relationship_frame`
- `tone`
- `initiative_level`
- `affection_level`
- `jealousy_or_exclusivity_style`
- `directness`
- `sexual_openness_style`
- `humor_style`
- `verbosity`
- `forbidden_traits`

### 9.2 Persona 设计原则

- 不要只做一个“成人伴侣角色”，而应做一组不同表达分布的角色
- persona 要控制语气、主动性、露骨程度偏好，而不仅仅是外貌设定
- persona 应足够稳定，以便跨模型比较

### 9.3 Persona 的作用

persona 不是为了让模型“自由发挥”，而是为了让 benchmark 能测试：

- 模型是否忠于角色
- 模型是否随着对话自动回退为默认助手
- 同一角色在不同模型上的保真度差异

---

## 10. Model Adapter Layer 设计

该层的目标是把 benchmark 逻辑和 provider 细节解耦。

### 10.1 Adapter 统一职责

- 统一请求输入格式
- 注入 system / developer / persona 上下文
- 设置温度、top_p、max_tokens 等参数
- 规范化返回结构
- 标注拒答、截断、内容降级、内容过滤等结果
- 记录 provider 和 model version 元数据

### 10.2 为什么必须标准化拒答标签

不同模型即使都“不配合”，表现形式也不同：

- 明确拒绝
- 软性转向
- 讲道理式回避
- 伪配合但内容极度抽空

如果不统一成结构化标签，就很难做横向比较。

---

## 11. Conversation Runner 设计

Runner 是整个 benchmark 系统的实验执行器。

### 11.1 输入

- 目标模型
- persona card
- scenario spec
- 用户消息序列
- 采样参数
- 重复运行次数

### 11.2 输出

- 完整 transcript
- 每轮调用参数
- 每轮原始响应
- 每轮结构化标签
- 终止原因
- run-level 聚合指标

### 11.3 执行原则

- 同一场景必须支持重复运行，观察波动
- 长对话需要支持固定脚本和半开放脚本两种模式
- 每次实验都要保留原始文本和结构化元数据

---

## 12. Judge / Scoring Layer 设计

单纯保存 transcript 不能直接支持产品决策，必须构建统一评分层。

### 12.1 核心评分维度

建议至少包括以下维度：

1. `policy pass-through rate`
   - 在目标场景中，模型是接受、部分接受、降级还是拒答

2. `persona consistency`
   - 是否持续符合既定伴侣角色

3. `style consistency`
   - 语气、亲密度、主动性、措辞风格是否稳定

4. `conversation usefulness`
   - 是否真的“能聊下去”，还是虽然没拒答但体验非常差

5. `volatility`
   - 相同测试重复运行的差异是否过大

6. `recovery ability`
   - 一旦触发拒答或降级，后续是否能回到可用状态

### 12.2 评分方式

建议采用两层评分：

- `规则化标签`
  - 拒答、降级、角色漂移、截断等可相对稳定定义的结果
- `rubric-based judgment`
  - 由明确评分标准驱动的人工或模型裁判，用于评估可用性与风格质量

### 12.3 Judge 设计原则

- Judge 模型不能与被测模型完全绑定
- rubric 必须固定，不允许每次解释口径变化
- 报告中应保留 evidence link，能回溯到原始 transcript

---

## 13. Benchmark 报告设计

最终产物不是一堆对话记录，而是能支持架构决策的报告。

### 13.1 报告应回答的问题

- 哪些模型完全不适合成人向 companion / ERP
- 哪些模型只适合 warm companion，不适合 ERP
- 哪些模型在长对话中人格漂移严重
- 哪些模型虽然偶尔可用，但波动太大，不适合作为产品底座
- 是否存在清晰的多模型路由策略

### 13.2 报告视角

建议至少提供三种视角：

- `按模型`
- `按场景`
- `按 persona`

### 13.3 结论输出形式

每个模型最终应输出：

- 总体评级
- 适用场景
- 主要失败模式
- 是否推荐进入下一阶段产品验证

---

## 14. 数据与资产设计

为了保证 benchmark 长期可维护，需要把实验资产独立管理。

### 14.1 核心资产

- `persona cards`
- `scenario specs`
- `judge rubrics`
- `benchmark reports`
- `raw transcripts`

### 14.2 版本化要求

以上资产都应具备版本号或日期，避免“同一个场景名字不变，内容却变了”导致结果不可比较。

### 14.3 数据卫生

- transcript 需记录完整上下文
- 敏感数据和 provider 返回元数据需要分层存放
- 后续若进入产品阶段，训练与评测数据必须严格区分

---

## 15. 实验协议建议

### 15.1 实验最小单元

最小实验单元应定义为：

> 一个模型在一个 persona、一个 scenario、一个参数配置下的一次完整 run

### 15.2 最小实验矩阵

第一阶段建议覆盖：

- 3 至 6 个候选模型
- 3 至 5 个核心 persona
- 20 至 30 个 scenario
- 每个 case 重复运行 3 次以上

### 15.3 必须记录的元数据

- 测试日期
- provider
- model name
- model version
- 参数配置
- scenario version
- persona version
- run id

---

## 16. 产品决策接口

benchmark 的目的不是停留在“做完报告”，而是要直接指导产品路线。

### 16.1 决策问题

系统最终需要支持以下决策：

- 选单模型还是多模型
- companion 层和 ERP 层是否拆分
- 是否需要在不同亲密度阶段切换模型
- 哪些模型只适合作为实验对象，不适合进入产品验证

### 16.2 路由原则

如果 benchmark 结果显示：

- 某些模型适合长对话陪伴，但不适合 ERP
- 某些模型在 explicit 场景中可用，但长对话人格不稳定

则应优先考虑：

> 分层路由，而不是强求单模型承担所有任务。

---

## 17. 分阶段实施路线

### Phase 1：最小可用 Benchmark

目标：

- 建立统一 adapter 接口
- 建立第一版 persona cards
- 建立 20 至 30 个核心场景
- 输出第一版横向模型报告

### Phase 2：稳定性与长对话

目标：

- 引入 20+ 轮长对话场景
- 引入重复运行和波动统计
- 识别人格漂移与失败恢复模式

### Phase 3：路由决策

目标：

- 判断单模型是否可行
- 如果不可行，输出场景分层路由方案
- 给出闭源、开源或混合架构建议

### Phase 4：产品验证准备

目标：

- 将 benchmark 结论转化为 product prototype 要求
- 定义第一版产品级 prompt / memory / routing 约束

---

## 18. 主要风险与缓解

### 18.1 Provider 策略变化

风险：

- 闭源模型行为可能因版本更新突然变化

缓解：

- 所有结果强制记录日期与版本
- 定期回归关键场景

### 18.2 Judge 主观性过强

风险：

- 不同评审标准导致排名不稳定

缓解：

- 固定 rubric
- 保留 evidence transcript
- 关键 case 引入人工抽检

### 18.3 过拟合 benchmark

风险：

- 模型只对固定脚本表现好，真实产品中表现差

缓解：

- 同时保留固定脚本与半开放脚本
- 长对话场景中加入变化点

### 18.4 项目目标漂移

风险：

- 又回到“做个 bot 先试试”的冲动开发

缓解：

- 明确 benchmark-first 是当前阶段唯一主线
- 产品实现必须等待 benchmark 结论

---

## 19. 推荐结论

当前项目最合理的主线不是直接做成人 companion / ERP bot，而是先建设一个 benchmark-first 系统，用统一场景、统一 persona、统一评分去验证模型事实。

一句话总结：

> 先回答“哪些模型在成人向 companion / ERP 场景下稳定可用”，再回答“产品应该怎么做”。

---

## 20. 后续文档建议

建议后续补充以下文档：

1. `docs/persona-card-schema.md`
   - persona 字段定义
   - companion 风格维度

2. `docs/scenario-suite-spec.md`
   - 场景分类
   - case 编写规范

3. `docs/judge-rubric.md`
   - 评分维度定义
   - evidence 标注规范

4. `docs/benchmark-report-template.md`
   - 实验输出模板
   - 模型对比模板

