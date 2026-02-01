# 示例项目说明

本目录用于存放基于 ArchPilot Core 框架创建的示例项目。

---

## 如何基于本框架创建新项目

### 方式一：完整复制

复制整个 `archpilot_core` 目录到目标项目：

```bash
cp -r archpilot_core /path/to/my_project/
```

然后根据项目需求定制化配置。

### 方式二：选择性复制

根据项目需求选择性复制：

```bash
# 创建项目目录
mkdir -p my_project/{Governance,Agents,Guides}

# 复制核心治理文件
cp archpilot_core/Governance/GOVERNANCE_OVERVIEW.md my_project/Governance/
cp archpilot_core/Governance/ARCHITECTURE_DEFINITION.md my_project/Governance/
cp archpilot_core/Governance/GLOSSARY.md my_project/Governance/

# 复制规则文件
cp -r archpilot_core/Governance/rules my_project/Governance/

# 复制主开发 Agent
cp archpilot_core/Agents/agent_dev_main.md my_project/Agents/
```

### 方式三：作为参考

将 `archpilot_core` 作为参考，根据项目特点创建自定义的治理体系。

---

## 定制化要点

### 1. 修改架构定义

编辑 `Governance/ARCHITECTURE_DEFINITION.md`：
- 调整目录路径
- 定义项目特定的子系统
- 修改文件前缀（如需要）

### 2. 补充术语表

编辑 `Governance/GLOSSARY.md`：
- 添加项目特定术语
- 标注术语适用范围

### 3. 调整规则

根据项目需求调整 `Governance/rules/` 下的规则文件：
- 调整质量评分权重
- 修改命名规范
- 定制发布流程

### 4. 配置 Agent

根据 AI 开发环境配置 Agent：
- 调整模型配置
- 修改工具列表
- 更新规则引用路径

---

## 项目模板

### 最小化项目结构

```
my_project/
├── Governance/
│   ├── GOVERNANCE_OVERVIEW.md
│   ├── ARCHITECTURE_DEFINITION.md
│   └── rules/
│       └── rules_agent.md
├── L1_Requirements/
├── L4_Implementation/
├── L5_Verification/
└── VERSION
```

### 完整项目结构

```
my_project/
├── Governance/
│   ├── GOVERNANCE_OVERVIEW.md
│   ├── ARCHITECTURE_DEFINITION.md
│   ├── GLOSSARY.md
│   ├── rules/
│   │   ├── rules_agent.md
│   │   ├── rules_coding.md
│   │   ├── rules_naming.md
│   │   ├── rules_release.md
│   │   └── rules_testcases.md
│   ├── checklists/
│   │   └── dev_checklist.md
│   └── templates/
├── Agents/
│   └── agent_dev_main.md
├── Guides/
│   └── AI_Development_Guide.md
├── L1_Requirements/
├── L2_Architecture/
├── L3_DetailDesign/
├── L4_Implementation/
├── L5_Verification/
├── ReleaseNote/
└── VERSION
```

---

## 相关文档

- [快速开始指南](../QUICK_START.md)
- [AI 开发指南](../Guides/AI_Development_Guide.md)
- [Agent 使用说明](../Agents/README.md)

