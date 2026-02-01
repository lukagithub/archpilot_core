# 部署结构分层说明

**更新日期**: 2026-02-01  
**变更类型**: 目录结构优化  
**部署模式**: 完整部署（包含所有组件）

---

## 变更概述

将一键部署生成的项目结构进行分层，区分**通用稳定框架**和**定制化开发区**。

---

## 新的目录结构

```
my_project/                    # 项目根目录
├── archpilot/               # 核心框架层（通用、稳定、不变）
│   ├── Governance/         # 治理规则
│   │   ├── rules/          # 规则文件
│   │   ├── checklists/     # 检查清单
│   │   └── templates/      # 文档模板
│   ├── Agents/             # AI Agent 配置
│   ├── Guides/             # AI 操作指南
│   ├── Prompts/            # Prompt 模板
│   ├── Scripts/            # 脚本工具
│   └── README.md           # 框架层说明
│   └── README.md             # 框架层说明
│
├── L1_Requirements/           # 🎯 定制化开发区
├── L2_Architecture/
├── L3_DetailDesign/
├── L4_Implementation/
├── L5_Verification/
├── ReleaseNote/
├── VERSION
├── .gitignore
└── README.md
```

---

## 设计理念

### archpilot/ - 核心框架层
- **特性**: 通用、稳定、不变
- **来源**: 直接继承自 ArchPilot Core
- **维护**: 尽量不修改，版本升级时整体替换
- **内容**:
  - 治理规则和规范
  - AI Agent 定义
  - Prompt 模板
  - 自动化脚本模板

### 根目录 - 定制化开发区
- **特性**: 项目特定、灵活变化
- **来源**: 基于框架模板创建
- **维护**: 根据项目需求自由开发
- **内容**:
  - L1-L5 架构层文档和代码
  - 项目配置文件
  - 发布说明

---

## 优势

1. **清晰的职责分离**
   - 框架部分和项目部分边界清晰
   - 避免误修改框架文件

2. **便于框架升级**
   - archpilot/ 可整体替换升级
   - 项目代码不受影响

3. **多项目复用**
   - archpilot/ 可作为 Git submodule
   - 多项目共享同一框架版本

4. **降低学习成本**
   - 新成员清楚哪些是框架，哪些是项目代码
   - 文档引用路径明确

---

## 使用建议

### ✅ 推荐做法

1. **引用而非修改**
   ```bash
   # 使用框架模板创建新文档
   cp archpilot/Governance/templates/tpl_requirement.md \
      L1_Requirements/FR_core_001_xxx.md
   ```

2. **扩展而非替换**
   - 项目特定的术语 → 在根目录创建 `PROJECT_GLOSSARY.md`
   - 项目特定的规则 → 在根目录创建 `PROJECT_RULES.md`

3. **版本追踪**
   ```bash
   # 在 README 中记录使用的框架版本
   **ArchPilot Core 版本**: v1.0.0
   ```

### ❌ 避免做法

1. ❌ 直接修改 `archpilot/` 下的文件
2. ❌ 在 `archpilot/` 中添加项目特定内容
3. ❌ 删除 `archpilot/` 目录

---

## 更新的文件

1. **Governance/DEPLOYMENT_FLOW.mmd**
   - 更新流程图体现 archpilot/ 分层

2. **Scripts/deploy_project.sh**
   - 创建 archpilot/ 目录结构
   - 复制核心文件到 archpilot/
   - 生成 archpilot/README.md
   - 更新生成的项目 README 路径引用

---

## 兼容性

- ✅ 不影响 ArchPilot Core 本身的结构
- ✅ 仅影响一键部署后的项目结构
- ✅ 现有的 Core 更新流程不变

---

## 后续计划

1. 考虑将 archpilot/ 作为 Git submodule 的支持
2. 提供框架版本升级脚本
3. 添加多项目共享框架的最佳实践文档

