# ArchPilot Core - Prompts 目录说明

**版本**: v1.0.0  
**最后更新**: 2026-02-01

---

## 概述

本目录包含可直接用于 AI 工具配置的 Prompt 文件，从治理规则中精简提炼而成。

---

## 文件清单

### System Prompt（始终加载）

| 文件 | 用途 | Token 估算 |
|------|------|------------|
| `system_prompt_core.md` | 核心 System Prompt，适用于通用开发任务 | ~1500-2000 |
| `system_prompt_release.md` | 发布场景 System Prompt | ~1000-1500 |

### User Prompt 模板（按需加载）

| 文件 | 用途 | 适用任务 |
|------|------|----------|
| `user_prompt_document.md` | 文档创建任务 | 创建 L1/L2/L3/L5 文档 |
| `user_prompt_code.md` | 代码编写任务 | 编写代码、脚本 |
| `user_prompt_release.md` | 版本发布任务 | 发布流程、Tag 创建 |
| `user_prompt_check.md` | 质量检查任务 | 开发检查、发布检查 |

---

## 使用方式

### 方式一：直接复制到 AI 工具

1. 复制 `system_prompt_core.md` 内容到 AI 工具的 System Prompt 配置
2. 根据任务类型，将对应的 User Prompt 内容附加到对话中

### 方式二：作为 Agent 配置

```yaml
# 示例：CodeBuddy Agent 配置
name: archpilot_dev
system_prompt: !include system_prompt_core.md
user_prompt_templates:
  document: !include user_prompt_document.md
  code: !include user_prompt_code.md
  release: !include user_prompt_release.md
```

### 方式三：动态加载

在对话中根据任务类型动态请求加载：

```
用户：请帮我创建一个 L1 需求文档
AI：[识别任务类型: 创建文档]
    [请求加载: user_prompt_document.md + requirement_template.md]
```

---

## Prompt 分层策略

```
┌─────────────────────────────────────────────┐
│         System Prompt（始终加载）            │
│  ┌─────────────────────────────────────┐   │
│  │ • 角色定义                           │   │
│  │ • 变更保护规则                        │   │
│  │ • L1-L5 架构定义                     │   │
│  │ • 核心术语                           │   │
│  │ • 执行流程                           │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│         User Prompt（按需加载）              │
│  ┌─────────────────────────────────────┐   │
│  │ • 任务相关规则（rules_*.md 精简）     │   │
│  │ • 任务相关模板（templates/*）         │   │
│  │ • 任务相关检查清单                    │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## Token 优化

| 策略 | 说明 |
|------|------|
| 表格替代段落 | 结构化信息更紧凑 |
| 去除解释性文字 | 只保留约束性内容 |
| 分级加载 | 核心规则始终加载，任务规则按需 |
| 使用引用 | 避免重复定义 |

---

## 关联文档

- [Prompt 策略指南](../Governance/PROMPT_STRATEGY.md)
- [文档依赖图](../Governance/DOCUMENT_DEPENDENCY.mmd)
- [Agent 定义](../Agents/)

