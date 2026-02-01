# 文档命名规范

**文档版本**: v1.1.0  
**最后更新**: 2026-02-01  
**适用范围**: L1-L5 所有层级文档及 Core 框架文件

> 本文档定义了项目中所有文档和文件的命名规则。

---

## 1. 命名目标

1. **一致性**: 所有文档遵循统一的命名规则
2. **可读性**: 文件名清晰反映文档内容和层级归属
3. **可追溯性**: 文件名包含必要的标识符支持追溯
4. **可维护性**: 避免重复和冗余
5. **唯一性**: 编号在各层级内部唯一

---

## 2. Core 文件前缀规范

Core 文件是 ArchPilot 框架的核心组成部分，按类型使用统一前缀。

### 2.1 前缀定义

| 类型 | 前缀 | 示例 | 说明 |
|------|------|------|------|
| **Entry 入口** | UPPER_CASE | `README.md`, `QUICK_START.md` | 全大写命名，业界规范入口文件 |
| **Rules 规则** | `rules_` | `rules_naming.md`, `rules_coding.md` | 约束和规范文件 |
| **Workflow 工作流** | `flow_` | `flow_planning.md`, `flow_release.md` | 工作流程定义 |
| **Templates 模板** | `tpl_` | `tpl_requirement.md`, `tpl_design.md` | 文档模板 |
| **Checklists 检查清单** | `chk_` | `chk_release.md`, `chk_dev.md` | 检查清单文件 |
| **Scripts 脚本** | 按语言后缀 | `validate_trace.py`, `deploy_project.sh` | 自动化脚本 |

### 2.2 命名格式

```
[前缀][功能描述].[扩展名]

示例:
- rules_naming.md      → 命名规范
- flow_planning.md     → 规划工作流
- tpl_requirement.md   → 需求模板
```

### 2.3 Core 文件完整列表

| 目录 | 文件 | 说明 |
|------|------|------|
| `/` | `README.md` | 项目入口 |
| `/` | `QUICK_START.md` | 快速开始 |
| `Governance/` | `ARCHITECTURE_DEFINITION.md` | 架构定义 |
| `Governance/` | `GLOSSARY.md` | 术语表 |
| `Governance/` | `GOVERNANCE_OVERVIEW.md` | 治理总览 |
| `Governance/rules/` | `rules_*.md` | 规则文件 |
| `Governance/workflow/` | `flow_*.md` | 工作流文件 |
| `Governance/templates/` | `tpl_*.md` | 模板文件 |
| `Governance/checklists/` | `chk_*.md` | 检查清单文件 |
| `Scripts/` | `*.py`, `*.sh` | 脚本文件 |

---

## 3. 过程产物前缀规范

过程产物是具体项目开发过程中生成的文档，按 L1-L5 层级使用统一前缀。

### 3.1 前缀定义

| 层级 | 前缀 | 示例 | 说明 |
|------|------|------|------|
| **L1 需求** | `FR_` | `FR_core_001_user_auth.md` | Functional Requirement |
| **L2 架构** | `SA_` | `SA_core_001_auth_arch.md` | Software Architecture |
| **L3 设计** | `DD_` | `DD_core_001_login.md` | Detail Design |
| **L4 实现** | 按语言 | `core_001_auth.cpp` | 代码文件 |
| **L5 测试** | `TC_` | `TC_core_001_unit_login.md` | Test Case |

---

## 4. 核心编号原则

### 4.1 唯一编号规则

1. **层级内部唯一性**:
   - FR 编号在 L1 内部唯一
   - SA 编号在 L2 内部唯一
   - DD 编号在 L3 内部唯一
   - TC 编号在 L5 内部唯一

2. **跨层级映射关系**:
   - 需求编号（FR-XXX）可与架构编号（SA-XXX）形成映射
   - 设计编号可包含架构编号作为前缀

3. **禁止编号重用**:
   - 同一层级内编号不能被不同文档重复使用
   - 已分配的编号即使文档删除也不得重新分配

---

## 3. 各层级命名规范

### 3.1 L1 需求层

**格式**: `FR_[子系统缩写]_[编号]_[描述].md`

| 字段 | 规则 |
|------|------|
| 前缀 | `FR_` |
| 子系统缩写 | 全小写字母（如 core/data/ui） |
| 编号 | 三位数字，从 001 开始 |
| 描述 | snake_case 格式，全小写 |

**示例**:
- `FR_core_001_user_authentication.md`
- `FR_data_002_storage_management.md`

### 3.2 L2 架构层

**格式**: `SA_[子系统缩写]_[编号]_[架构组件].md`

| 字段 | 规则 |
|------|------|
| 前缀 | `SA_` |
| 子系统缩写 | 全小写字母 |
| 编号 | 三位数字，建议与 L1 需求保持逻辑关联 |
| 架构组件 | snake_case 格式 |

**示例**:
- `SA_core_001_authentication_architecture.md`
- `SA_data_002_storage_layer.md`

### 3.3 L3 设计层

#### 单子系统设计

**格式**: `DD_[子系统缩写]_[编号]_[组件名称].md`

**示例**:
- `DD_core_001_login_module.md`
- `DD_data_002_cache_manager.md`

#### 跨子系统交互设计

**格式**: `DD_[源子系统]_[目标子系统]_[交互序号]_[功能名称].md`

**示例**:
- `DD_core_data_101_data_sync.md`（核心功能调用数据管理）
- `DD_ui_core_102_user_action.md`（UI 调用核心功能）

### 3.4 L4 实现层

**格式**: `[子系统缩写]_[编号]_[组件].[扩展名]`

**示例**:
- `core_001_authenticator.cpp`
- `data_002_storage.py`
- `ui_003_dashboard.tsx`

### 3.5 L5 验证层

**格式**: `TC_[子系统]_[编号]_[类型]_[描述].md`

| 字段 | 规则 |
|------|------|
| 前缀 | `TC_` |
| 子系统 | 全小写字母 |
| 编号 | 三位数字 |
| 类型 | unit/integration/system/performance/acceptance |
| 描述 | 下划线连接的小写描述 |

**示例**:
- `TC_core_001_unit_login_basic.md`
- `TC_data_002_integration_storage_sync.md`

---

## 4. 文档元数据规范

### 4.1 YAML Front Matter

每个文档必须包含以下元数据：

```yaml
---
id: FR_core_001
type: requirement
title: 用户认证功能需求
status: draft | review | approved | deprecated
version: v1.0.0
created: 2026-02-01
updated: 2026-02-01
author: 作者名
traces_from: []
traces_to: [SA_core_001]
related: [FR_core_002]
---
```

### 4.2 字段说明

| 字段 | 是否必需 | 说明 |
|------|----------|------|
| id | ✅ | 与文件名一致（不含扩展名） |
| type | ✅ | requirement/architecture/design/implementation/test |
| title | ✅ | 中文标题 |
| status | ✅ | 状态 |
| version | ✅ | 版本号 |
| created | ✅ | 创建时间 |
| updated | ✅ | 更新时间 |
| author | ⚠️ | 作者 |
| traces_from | ✅ | 上游来源 |
| traces_to | ✅ | 下游实现 |
| related | ⭕ | 相关文档 |

---

## 5. 通用命名规则

### 5.1 字符限制

- ✅ 仅使用 ASCII 字母、数字、下划线
- ❌ **禁止使用中划线（短横线 `-`）**：避免在某些工具或代码规范中造成不兼容
- ❌ 禁止使用空格
- ❌ 禁止使用特殊字符（如 `!@#$%^&*()`）
- ❌ 禁止使用中文字符

> **重要**: 所有文件名统一使用下划线 `_` 作为分隔符，不使用中划线 `-`。

### 5.2 大小写规则

| 上下文 | 规则 |
|--------|------|
| 文件名 | snake_case（下划线分隔） |
| 目录名 | PascalCase 或 snake_case |
| 前缀 | UPPER_CASE（如 FR_、SA_、DD_、TC_） |
| 描述部分 | snake_case（下划线分隔） |

### 5.3 长度限制

- 文件名总长度不超过 80 字符
- 描述部分不超过 50 字符

---

## 6. 特殊文件命名

### 6.1 版本相关

| 文件类型 | 命名 |
|----------|------|
| 版本文件 | `VERSION` |
| 变更日志 | `CHANGELOG.md` |
| 发布说明 | `RELEASE_NOTES_v{VERSION}.md` 或 `ReleaseNote/v{VERSION}.md` |
| 发布报告 | `RELEASE_REPORT_v{VERSION}.md` |

### 6.2 治理文档

| 文件类型 | 命名 |
|----------|------|
| 治理总览 | `GOVERNANCE_OVERVIEW.md` |
| 架构定义 | `ARCHITECTURE_DEFINITION.md` |
| 术语表 | `GLOSSARY.md` |
| 规则文件 | `rules_[类型].md` |
| 检查清单 | `[类型]_checklist.md` |

### 6.3 模板文件

| 文件类型 | 命名 |
|----------|------|
| 需求模板 | `tpl_requirement.md` |
| 架构模板 | `tpl_architecture.md` |
| 设计模板 | `tpl_design.md` |
| 测试模板 | `tpl_testcase.md` |
| 发布说明模板 | `tpl_release_notes.md` |
| 发布报告模板 | `tpl_release_report.md` |

---

## 7. 检查清单

### 文件创建前检查

- [ ] 文件名是否遵循层级格式规范？
- [ ] 子系统缩写是否正确？
- [ ] 编号是否在层级内唯一？
- [ ] 描述是否使用正确的大小写格式？
- [ ] 文件名长度是否符合限制？
- [ ] 是否包含禁止的字符？

### 文件创建后检查

- [ ] YAML Front Matter 是否完整？
- [ ] id 是否与文件名一致？
- [ ] traces_from/traces_to 是否正确？

---

## 8. 常见错误与修正

### 错误示例 1：使用空格

❌ `FR core 001 user auth.md`  
✅ `FR_core_001_user_auth.md`

### 错误示例 2：前缀大小写错误

❌ `fr_core_001_user_auth.md`  
✅ `FR_core_001_user_auth.md`

### 错误示例 3：描述使用大写

❌ `FR_core_001_UserAuth.md`  
✅ `FR_core_001_user_auth.md`

### 错误示例 4：测试用例分隔符错误

❌ `TC_core_001_unit_login.md`  
✅ `TC-core-001-unit-login.md`

---

## 9. 关联文档

- `ARCHITECTURE_DEFINITION.md` - 架构权威定义
- `GLOSSARY.md` - 术语标准表
- `rules_testcases.md` - 测试用例命名规范（L5 详细规范）

