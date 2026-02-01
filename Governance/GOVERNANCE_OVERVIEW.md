# ArchPilot Core 治理体系总览

**文档版本**: v1.0.0  
**最后更新**: 2026-02-01  
**适用范围**: 基于 ArchPilot Core 框架的所有项目  
**维护者**: 项目治理委员会

> 本文档是治理体系的入口索引，AI 在执行任务前必须首先阅读本文档。

---

## 1. 治理层级

| 层级 | 目标 | 代表文档 | 面向对象 |
|------|------|----------|----------|
| **核心定义层** | 提供不可变的基线定义 | `ARCHITECTURE_DEFINITION.md`, `GLOSSARY.md` | 所有角色 |
| **规则标准层** | 规定必须遵循的行为与流程 | `rules/*.md` | 研发、AI、自动化脚本 |
| **检查执行层** | 将规则转化为检查项 | `checklists/*.md` | QA、脚本作者 |
| **自动化执行层** | 描述 AI/脚本如何执行 | `../Guides/AI_*.md`, `rules/rules_agent.md` | AI、自动化平台 |

---

## 2. 文档依赖图

```
核心定义层
  ├─ ARCHITECTURE_DEFINITION.md  ─┐
  └─ GLOSSARY.md                  ├─> 规则标准层 (rules/*.md)
                                   └─> 检查执行层 (checklists/*.md)
规则标准层
  ├─ rules_release.md ──┐
  ├─ rules_scripts.md ──┼─> AI_Release_Automation_Guide.md
  └─ rules_tag.md    ───┘
```

**执行原则**:
- 当上层文档更新时，下层文档必须同步引用最新版本
- 任何脚本直接读取的常量（目录、术语）均来自核心定义层
- 发生冲突时，以上层文档为准

---

## 3. 治理执行流程

```
1. 读取核心定义
   ├─ 确认 L1-L5 层级职责
   ├─ 确认术语标准
   └─ 确认目录结构
       ↓
2. 加载规则标准
   ├─ 根据任务类型加载对应规则
   ├─ rules_coding.md（代码任务）
   ├─ rules_naming.md（文件创建）
   ├─ rules_release.md（发布任务）
   └─ rules_agent.md（变更保护）
       ↓
3. 执行检查
   ├─ 使用 checklists/*.md 验证合规性
   └─ 阻断不合规的操作
       ↓
4. 自动化执行
   ├─ 参考 Guides/AI_*.md 执行任务
   └─ 遵循脚本规范
       ↓
5. 评估与改进
   ├─ 生成质量评分报告
   └─ 记录改进建议
```

---

## 4. 快速索引

| 使用场景 | 必看文档 |
|----------|----------|
| 了解 L1-L5 职责 | `ARCHITECTURE_DEFINITION.md` |
| 查找术语写法 | `GLOSSARY.md` |
| 编写代码/脚本 | `rules/rules_coding.md`, `rules/rules_scripts.md` |
| 创建/命名文件 | `rules/rules_naming.md` |
| 发布新版本 | `rules/rules_release.md`, `../Guides/AI_Release_Automation_Guide.md` |
| 编写测试用例 | `rules/rules_testcases.md` |
| 审计质量 | `checklists/chk_dev.md` |

---

## 5. AI 必读规则

AI 在执行任何任务前，**必须**阅读以下文档：

### 5.1 必读文档（MUST）

| 优先级 | 文档 | 目的 |
|--------|------|------|
| 1 | 本文档 | 了解治理体系入口 |
| 2 | `ARCHITECTURE_DEFINITION.md` | 了解 L1-L5 层级定义 |
| 3 | `rules/rules_agent.md` | 了解变更保护规则 |
| 4 | 与任务相关的 `rules/*.md` | 了解具体执行规则 |

### 5.2 条件必读（SHOULD）

| 任务类型 | 额外需读文档 |
|----------|-------------|
| 创建文档 | `rules/rules_naming.md`, 对应层级模板 |
| 编写代码 | `rules/rules_coding.md` |
| 发布版本 | `rules/rules_release.md`, `rules/rules_tag.md` |
| 编写测试 | `rules/rules_testcases.md` |

---

## 6. 维护机制

### 6.1 更新节奏

- 治理委员会每周检查一次文档引用是否失效
- 发现问题立即修复，不等待定期检查

### 6.2 变更流程

1. 提交变更请求，附带影响分析
2. 治理委员会评审
3. 更新文档并同步受影响的下游文档
4. 通知相关方

### 6.3 AI 约束

- AI 在引用 Governance 规则时应先读取本文档
- 对受保护文件的修改必须经人工确认
- 规则冲突时以本文档索引的上层文档为准

---

## 7. 关联文档

- `ARCHITECTURE_DEFINITION.md` - L1-L5 架构权威定义
- `GLOSSARY.md` - 术语标准表
- `rules/rules_agent.md` - AI 变更保护规则
- `../Guides/AI_Development_Guide.md` - AI 开发指南

---

**本文件是治理体系的唯一入口，请勿在其他文档中重复本索引内容。**

