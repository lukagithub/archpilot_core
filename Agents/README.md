# ArchPilot Core - Agent 使用说明

**版本**: v1.0.0  
**最后更新**: 2026-02-01

---

## 概述

本目录包含预定义的 AI Agent 配置，用于在 AI 辅助架构设计环境中约束和指导 AI 行为。

---

## Agent 列表

| Agent | 文件 | 用途 |
|-------|------|------|
| 主开发 Agent | `agent_dev_main.md` | 规则约束下的通用开发任务 |
| 代码审查 Agent | `agent_reviewer.md` | 代码和文档审查 |
| 发布 Agent | `agent_release.md` | 版本发布自动化 |
| QA Agent | `agent_qa.md` | 质量保障任务 |

---

## 使用方式

### 1. CodeBuddy 环境

将 Agent 文件复制到项目的 `.codebuddy/agents/` 目录：

```bash
mkdir -p .codebuddy/agents
cp Agents/agent_dev_main.md .codebuddy/agents/
```

### 2. 其他 AI 环境

将 Agent 文件内容作为 System Prompt 配置到你的 AI 环境中。

---

## 定制化

### 添加新 Agent

1. 复制现有 Agent 文件作为模板
2. 修改元数据（name、description）
3. 根据任务类型调整职责和规则引用
4. 添加到本 README 的 Agent 列表中

### 修改规则引用

Agent 文件中的规则引用路径需要根据实际项目结构调整：

```markdown
## 必须遵循的规则文件
- `Governance/ARCHITECTURE_DEFINITION.md`  # 调整为实际路径
- `Governance/rules/rules_*.md`
```

---

## Agent 设计原则

1. **规则优先**：Agent 必须首先加载和理解项目规则
2. **明确职责**：每个 Agent 有清晰的职责边界
3. **追溯维护**：所有操作保持 L1-L5 追溯完整性
4. **变更保护**：尊重文件保护声明

---

## 关联文档

- [治理总览](../Governance/GOVERNANCE_OVERVIEW.md)
- [AI 开发指南](../Guides/AI_Development_Guide.md)
- [规则文件](../Governance/rules/)

