# ArchPilot Core 快速开始指南

**版本**: v1.0.0  
**适用**: 基于本框架创建新项目的架构师/开发团队

---

## 📋 前置准备

### 1. 环境要求

- Git（版本管理）
- Bash（Linux/macOS/WSL/Git Bash）
- Python 3.8+（脚本执行）
- AI 助手（如 GitHub Copilot、CodeBuddy、Cursor 等）

### 2. 理解核心概念

| 概念 | 说明 |
|------|------|
| **L1-L5 架构** | 五层文档驱动开发：需求→架构→设计→实现→验证 |
| **治理规则** | AI 和人工都必须遵循的标准化规则 |
| **追溯关系** | 每个下层产物必须追溯到上层来源 |
| **变更保护** | 关键文件的修改需要人工确认 |

---

## 🚀 一键部署（推荐）

### 方式一：使用部署脚本

```bash
# 进入 ArchPilot Core 目录
cd archpilot_core

# 基本用法：创建新项目
./Scripts/deploy_project.sh my_project

# 指定目标路径
./Scripts/deploy_project.sh my_project /path/to/workspace

# Git 初始化
./Scripts/deploy_project.sh my_project /path/to -i
```

### 常用选项

| 选项 | 说明 |
|------|------|
| `-i, --init-git` | 初始化 Git 仓库并完成首次提交 |
| `-h, --help` | 显示帮助 |

### 部署完成后

```bash
# 进入新项目目录
cd my_project

# 查看项目结构
ls -la

# 开始使用
cat README.md
```

---

## 📦 手动部署（备选）

如果不使用部署脚本，可以手动复制：

### 步骤 1：初始化项目结构

```bash
# 创建项目根目录
mkdir my_project && cd my_project

# 复制框架（假设 archpilot_core 在同级目录）
cp -r ../archpilot_core/Governance ./
cp -r ../archpilot_core/Agents ./
cp -r ../archpilot_core/Guides ./

# 创建 L1-L5 目录结构
mkdir -p L1_Requirements L2_Architecture L3_DetailDesign L4_Implementation L5_Verification
```

### 步骤 2：定制化配置

编辑 `Governance/ARCHITECTURE_DEFINITION.md`，修改目录路径：

```yaml
# 示例：将路径修改为你的项目结构
L1_Directory: my_project/L1_Requirements/
L2_Directory: my_project/L2_Architecture/
L3_Directory: my_project/L3_DetailDesign/
L4_Directory: my_project/L4_Implementation/
L5_Directory: my_project/L5_Verification/
```

### 步骤 3：创建首个需求文档

使用模板创建第一个 L1 需求文档：

```bash
cp Governance/templates/tpl_requirement.md L1_Requirements/FR_core_001_basic_feature.md
```

编辑文件，填写需求内容：

```yaml
---
id: FR_core_001
layer: L1
status: draft
version: v0.1.0
traces_from: []
traces_to: []
---
# FR_core_001 基础功能需求

## 1. 需求概述
[描述需求目标和背景]

## 2. 功能需求
[详细的功能需求列表]

## 3. 验收条件
[可验证的验收标准]
```

### 步骤 4：配置 AI Agent

将 `Agents/agent_dev_main.md` 配置到你的 AI 开发环境中。以 CodeBuddy 为例：

```bash
mkdir -p .codebuddy/agents
cp Agents/agent_dev_main.md .codebuddy/agents/
```

### 步骤 5：开始 AI 辅助开发

现在你可以：

1. **让 AI 理解规则**：
   ```
   请阅读 Governance/ 目录下的规则文件，理解本项目的开发规范。
   ```

2. **让 AI 创建架构设计**：
   ```
   基于 L1_Requirements/FR_core_001_basic_feature.md 的需求，
   创建对应的 L2 架构设计文档。
   ```

3. **让 AI 检查追溯完整性**：
   ```
   检查 L1-L5 的追溯关系是否完整，是否有断裂的追溯链。
   ```

---

## 📁 推荐的项目结构

```
my_project/
├── Governance/                    # 治理规则（从框架复制）
│   ├── ARCHITECTURE_DEFINITION.md
│   ├── GLOSSARY.md
│   ├── rules/
│   ├── checklists/
│   └── templates/
│
├── Agents/                        # AI Agent 配置
│   └── agent_dev_main.md
│
├── Guides/                        # AI 操作指南
│
├── L1_Requirements/               # L1 需求层
│   └── FR_xxx_*.md
│
├── L2_Architecture/               # L2 架构层
│   └── SA_xxx_*.md
│
├── L3_DetailDesign/               # L3 设计层
│   └── DD_xxx_*.md
│
├── L4_Implementation/             # L4 实现层
│   └── src/
│
├── L5_Verification/               # L5 验证层
│   ├── unit/
│   └── integration/
│
├── Scripts/                       # 自动化脚本
│
├── VERSION                        # 版本文件
└── README.md                      # 项目说明
```

---

## 🔧 常用配置

### 配置子系统

在 `Governance/ARCHITECTURE_DEFINITION.md` 中定义项目的子系统：

```markdown
| 子系统 | 缩写 | 职责 |
|--------|------|------|
| 核心功能 | core | 核心业务逻辑 |
| 数据管理 | data | 数据存储与处理 |
| 用户界面 | ui | 用户交互界面 |
| 工具集 | util | 通用工具和辅助功能 |
```

### 配置命名前缀

在 `Governance/rules/rules_naming.md` 中定义文件命名规则：

```markdown
| 层级 | 前缀 | 格式 |
|------|------|------|
| L1 | FR_ | FR_[子系统]_[编号]_[描述].md |
| L2 | SA_ | SA_[子系统]_[编号]_[描述].md |
| L3 | DD_ | DD_[子系统]_[编号]_[描述].md |
| L5 | TC- | TC-[子系统]-[编号]-[类型]-[描述].md |
```

### 配置质量评分

在 `Governance/rules/rules_release.md` 中调整评分权重：

```markdown
| 维度 | 权重 | 说明 |
|------|------|------|
| D1: 文档完整性 | 20% | 根据项目特点调整 |
| D2: 追溯关系 | 15% | 追溯要求高可增加 |
| D3: 功能实现 | 30% | 功能导向项目可增加 |
| D4: 测试验证 | 25% | 质量要求高可增加 |
| D5: 代码质量 | 10% | 长期维护项目可增加 |
```

---

## ✅ 检查清单

### 初始化完成检查

- [ ] 项目目录结构已创建
- [ ] Governance 规则文件已复制并定制
- [ ] Agent 配置文件已就位
- [ ] 首个 L1 需求文档已创建
- [ ] AI 助手已配置并能识别规则

### 开发流程检查

- [ ] 每个需求都有对应的 L1 文档
- [ ] L2 架构设计追溯到 L1 需求
- [ ] L3 详细设计追溯到 L2 架构
- [ ] L4 实现追溯到 L3 设计
- [ ] L5 测试验证覆盖 L1 需求

---

## 🆘 常见问题

### Q1: AI 不遵循规则怎么办？

确保 Agent 配置文件正确，并在对话开始时提示 AI：

```
请先阅读 Governance/GOVERNANCE_OVERVIEW.md，理解本项目的治理规则后再执行任务。
```

### Q2: 如何添加新的规则？

1. 在 `Governance/rules/` 下创建新规则文件
2. 在 `Governance/GOVERNANCE_OVERVIEW.md` 中添加索引
3. 更新 Agent 配置文件，引用新规则

### Q3: 追溯关系如何维护？

1. 每个文档的 YAML Front Matter 中维护 `traces_from` 和 `traces_to`
2. 使用 `Scripts/validate_trace.py` 验证追溯完整性
3. AI 在创建下层文档时自动建立追溯关系

---

## 📖 下一步

- 阅读 [AI 开发指南](Guides/AI_Development_Guide.md) 了解详细的 AI 协作流程
- 查看 [Agent 使用说明](Agents/README.md) 配置专项 Agent
- 参考 [示例项目](Examples/README.md) 学习最佳实践

