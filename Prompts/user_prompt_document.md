# User Prompt - 文档创建任务

> 当任务类型为"创建文档"时，将本内容附加到 User Prompt

---

## 任务类型

**创建文档**（L1 需求 / L2 架构 / L3 设计 / L5 测试）

---

## 命名规则（来自 rules_naming.md）

### 文件命名格式

| 层级 | 格式 | 示例 |
|------|------|------|
| L1 需求 | `FR_[子系统]_[编号]_[描述].md` | `FR_core_001_user_auth.md` |
| L2 架构 | `SA_[子系统]_[编号]_[描述].md` | `SA_core_001_auth_arch.md` |
| L3 设计 | `DD_[子系统]_[编号]_[描述].md` | `DD_core_001_login_module.md` |
| L5 测试 | `TC-[子系统]-[编号]-[类型]-[描述].md` | `TC-core-001-unit-login.md` |

### 命名约束

- ✅ 全部小写（前缀除外）
- ✅ 使用下划线分隔（L1-L3），短横线分隔（L5）
- ✅ 描述部分使用 snake_case
- ❌ 禁止空格和特殊字符
- ❌ 文件名长度不超过 80 字符

### 子系统缩写（示例）

| 子系统 | 缩写 |
|--------|------|
| 核心功能 | core |
| 数据管理 | data |
| 用户界面 | ui |
| 工具集 | util |
| 平台管理 | plt |

---

## 元数据要求（MUST）

```yaml
---
id: [与文件名一致，不含扩展名]
layer: [L1|L2|L3|L5]
type: [requirement|architecture|design|test]
title: [中文标题]
status: draft
version: v1.0.0
created: [今天日期]
updated: [今天日期]
author: [作者]
traces_from: [上游文档ID列表]
traces_to: []
related: []
---
```

### 追溯关系设置

| 层级 | traces_from | 说明 |
|------|-------------|------|
| L1 | `[]` | 需求层无上游 |
| L2 | `[FR_xxx]` | 追溯到 L1 需求 |
| L3 | `[SA_xxx]` | 追溯到 L2 架构 |
| L5 | `[FR_xxx, DD_xxx]` | 追溯到需求和设计 |

---

## 文档模板

根据层级选择对应模板：

- L1 需求：`templates/requirement_template.md`
- L2 架构：`templates/architecture_template.md`
- L3 设计：`templates/design_template.md`
- L5 测试：`templates/testcase_template.md`

---

## 执行检查清单

- [ ] 文件名符合命名规范
- [ ] YAML 元数据完整
- [ ] id 与文件名一致
- [ ] traces_from 正确设置
- [ ] 使用了正确的模板结构

