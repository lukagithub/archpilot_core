# V-Model 跨仓库追溯链规范

> **⚠️ AI 变更保护声明**
>
> 本文件受 AI 变更保护：
> 1. AI 如需修改此文件，必须输出详细的变更理由
> 2. 必须经过人工确认后才能进行任何修改
> 3. 严格禁止 AI 自动修改此文件
>
> **说明**: 该约束确保本文件的修改必须经过人工审查和批准。

**文档版本**: v1.0.0  
**最后更新**: 2026-02-02  
**适用范围**: 基于 ArchPilot Core 框架的多仓库系统  
**追溯类型**: L1 需求 → L2 架构设计 → L3 详细设计（类/函数）

---

## 1. 追溯链定义

### 1.1 层级映射

```
┌─────────────────────────────────────────────────────────────────┐
│                        V-Model 追溯链                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    L1_Requirements                    L5_Verification            │
│    ┌─────────────┐                    ┌─────────────┐           │
│    │  FR_xxx     │◄──────────────────►│  TC-xxx     │           │
│    │  (需求规格) │    validates       │  (系统测试) │           │
│    └─────────────┘                    └─────────────┘           │
│           │                                  ▲                   │
│           │ traces_to                        │ verified_by       │
│           ▼                                  │                   │
│    L2_Architecture                    L5_Verification            │
│    ┌─────────────┐                    ┌─────────────┐           │
│    │  SA_xxx     │◄──────────────────►│  TC-xxx     │           │
│    │  (架构设计) │    validates       │  (集成测试) │           │
│    └─────────────┘                    └─────────────┘           │
│           │                                  ▲                   │
│           │ traces_to                        │ verified_by       │
│           ▼                                  │                   │
│    L3_DetailDesign                    L5_Verification            │
│    ┌─────────────┐                    ┌─────────────┐           │
│    │  DD_xxx     │◄──────────────────►│  TC-xxx     │           │
│    │  (详细设计) │    validates       │  (单元测试) │           │
│    └─────────────┘                    └─────────────┘           │
│           │                                  ▲                   │
│           │ traces_to                        │ verified_by       │
│           ▼                                  │                   │
│    L4_Implementation                                            │
│    ┌─────────────┐                                              │
│    │  源代码文件 │                                               │
│    │  .cc/.h     │                                               │
│    └─────────────┘                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 追溯关系类型

| 关系类型 | 方向 | 说明 |
|----------|------|------|
| `traces_to` | L1 → L2 → L3 → L4 | 需求分解到设计再到实现 |
| `traces_from` | L4 → L3 → L2 → L1 | 实现向上追溯到需求 |
| `verified_by` | L1/L2/L3 → L5 | 设计被测试验证 |
| `validates` | L5 → L1/L2/L3 | 测试验证设计 |

---

## 2. 文档标识规范

### 2.1 ID 命名规则

| 层级 | 前缀 | 格式 | 示例 |
|------|------|------|------|
| L1 | `FR_`, `US_`, `AC_` | `{前缀}{仓库}_{序号}` | `FR_module_a_001` |
| L2 | `SA_`, `ARCH_`, `ADR_` | `{前缀}{仓库}_{序号}` | `SA_subsystem_001` |
| L3 | `DD_`, `IF_` | `{前缀}{仓库}_{模块}_{序号}` | `DD_module_a_component_001` |
| L4 | `IMPL_`, `MOD_` | `{前缀}{仓库}_{文件路径}` | `IMPL_module_a_handler` |
| L5 | `TC-`, `TR-` | `TC-{仓库}-{类型}-{序号}` | `TC-module_a-UT-001` |

### 2.2 仓库简称映射

> **说明**: 项目应根据实际仓库结构定义简称映射表。

| 仓库全名 | 简称 | 说明 |
|----------|------|------|
| {repository_name} | {abbr} | {description} |
| module_a | mod_a | 示例模块 A |
| module_b | mod_b | 示例模块 B |
| common_lib | common | 公共库 |

---

## 3. 元数据规范

### 3.1 Markdown 文档元数据

每个追溯文档 **必须** 包含 YAML 头部：

```yaml
---
id: SA_module_a_001                    # 唯一标识符
title: 模块 A 架构设计                  # 文档标题
layer: L2                              # 所属层级
category: architecture                 # 文档类别
status: approved                       # draft|review|approved|deprecated
version: v1.0.0                        # 文档版本
# 追溯关系
traces_from:                           # 上游依赖
  - FR_feature_001                     # 来源需求
  - FR_feature_002
traces_to:                             # 下游分解
  - DD_module_a_component_001
  - DD_module_a_component_002
related:                               # 相关文档
  - SA_subsystem_overview
  - ADR_design_decision_001
# 验证关系
verified_by:                           # 验证用例
  - TC-module_a-IT-001
  - TC-module_a-IT-002
# 元信息
owner: {team-name}                     # 负责团队
created: YYYY-MM-DD                    # 创建日期
updated: YYYY-MM-DD                    # 更新日期
repo: {repository_name}                # 源仓库
---
```

### 3.2 源代码追溯注解

在关键源代码文件中使用注释标记追溯关系：

```cpp
/**
 * @file component_handler.cc
 * @brief 组件处理器实现
 *
 * @requirement FR_feature_001, FR_feature_002
 * @design SA_module_a_001, DD_module_a_component_001
 * @testcase TC-module_a-UT-001, TC-module_a-UT-002
 */

// 关键函数/类级别标注
/**
 * @class ComponentHandler
 * @design DD_module_a_component_001
 * @see module_a/src/handler/component_handler.h
 */
```

---

## 4. 追溯矩阵规范

### 4.1 追溯矩阵文件格式

追溯矩阵使用 CSV 格式存储，位于 `{project}/TraceMatrix/` 目录：

**文件命名**: `trace_matrix_{仓库}_{层级}.csv`

**列定义**:
```csv
source_id,source_layer,target_id,target_layer,relation_type,status,remarks
FR_feature_001,L1,SA_module_a_001,L2,traces_to,verified,模块 A 架构
SA_module_a_001,L2,DD_module_a_component_001,L3,traces_to,verified,组件详设
DD_module_a_component_001,L3,component_handler.cc,L4,traces_to,verified,源代码实现
FR_feature_001,L1,TC-module_a-ST-001,L5,verified_by,passed,系统级测试
```

### 4.2 追溯覆盖率指标

| 指标名称 | 计算公式 | 目标值 |
|----------|----------|--------|
| 需求覆盖率 | 有 L2 追溯的 L1 文档数 / L1 文档总数 | ≥ 95% |
| 设计覆盖率 | 有 L3 追溯的 L2 文档数 / L2 文档总数 | ≥ 90% |
| 实现覆盖率 | 有代码追溯的 L3 文档数 / L3 文档总数 | ≥ 85% |
| 测试覆盖率 | 有 L5 验证的 L1 文档数 / L1 文档总数 | ≥ 90% |

---

## 5. 验证与校验

### 5.1 自动化校验规则

| 规则 ID | 规则描述 | 严重级别 | 检查方式 |
|---------|----------|----------|----------|
| VR-001 | L1 文档必须至少有一个 `traces_to` 到 L2 | ERROR | 脚本扫描 |
| VR-002 | L2 文档必须有 `traces_from` 指向 L1 | ERROR | 脚本扫描 |
| VR-003 | L3 文档必须有对应的 L4 实现 | WARNING | 脚本扫描 |
| VR-004 | 关键 L1 需求必须有 L5 验证 | ERROR | 脚本扫描 |
| VR-005 | 追溯 ID 必须在目标文档中存在 | ERROR | 交叉引用检查 |
| VR-006 | 循环依赖检测 | ERROR | 图分析 |

### 5.2 校验脚本接口

```bash
# 验证单个仓库的追溯完整性
python validate_trace.py --repo {repo_name} --output report.json

# 全量扫描并生成覆盖率报告
python validate_trace.py --all --coverage --output coverage_report.html

# 检查断链（orphan 文档）
python validate_trace.py --check-orphans --layer L2
```

### 5.3 校验输出格式

```json
{
  "repo": "{repo_name}",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "summary": {
    "total_documents": 15,
    "with_trace": 14,
    "orphan_documents": 1,
    "coverage_rate": 0.933
  },
  "issues": [
    {
      "rule_id": "VR-001",
      "severity": "ERROR",
      "document": "FR_feature_003",
      "message": "Missing traces_to in L2 layer"
    }
  ],
  "coverage_by_layer": {
    "L1_to_L2": 0.95,
    "L2_to_L3": 0.90,
    "L3_to_L4": 0.88,
    "L1_verified": 0.92
  }
}
```

---

## 6. 跨仓库追溯

### 6.1 仓库间依赖声明

当追溯关系跨越仓库边界时，使用完整路径标识：

```yaml
traces_from:
  - proto:FR_message_001             # proto 仓库的需求
traces_to:
  - module_b:SA_feature_001          # module_b 仓库的设计
  - module_c:SA_interface_001        # module_c 仓库的设计
```

### 6.2 跨仓库追溯示例

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  proto 仓库      │      │   module_a      │      │   module_b 仓库  │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ FR_message_001  │──────►│ SA_module_a_001 │──────►│ SA_module_b_001 │
│ (消息定义需求)   │      │ (功能设计)       │      │ (展示设计)       │
└─────────────────┘      └─────────────────┘      └─────────────────┘
         │                        │                        │
         │                        ▼                        ▼
         │               ┌─────────────────┐      ┌─────────────────┐
         │               │ handler.cc      │      │ display.cc      │
         │               └─────────────────┘      └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     L5: 集成测试用例                             │
│  TC-subsystem-IT-001: 端到端功能验证                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. 维护流程

### 7.1 追溯文档更新触发条件

| 触发事件 | 动作 | 责任人 |
|----------|------|--------|
| 新增 L1 需求 | 创建追溯条目，关联 L2 设计 | 需求分析师 |
| 新增 L2 设计 | 更新上游 traces_from，创建下游 traces_to | 架构师 |
| 代码变更 | 检查 @design 注释是否需要更新 | 开发者 |
| 测试用例变更 | 更新 verified_by 关系 | 测试工程师 |
| 文档废弃 | 标记 status=deprecated，检查依赖影响 | 文档所有者 |

### 7.2 定期审计

- **周审计**: CI 流水线自动执行追溯完整性检查
- **月审计**: 生成覆盖率报告，识别断链和孤立文档
- **季度审计**: 全量追溯矩阵审查，更新过期追溯关系

---

## 8. 工具支持

### 8.1 推荐工具链

| 工具 | 用途 | 位置 |
|------|------|------|
| `validate_trace.py` | 追溯完整性验证 | `archpilot_core/Tools/` |
| `generate_matrix.py` | 生成追溯矩阵 | `archpilot_core/Tools/` |
| `trace_visualizer.py` | 可视化追溯图 | `archpilot_core/Tools/` |

### 8.2 IDE 集成

- **VSCode 插件**: Markdown YAML 元数据自动补全
- **CLion**: 代码注释中追溯标签的语法高亮

---

## 附录 A: 追溯模板

### A.1 L1 需求文档模板

```markdown
---
id: FR_{repo}_{seq}
title: 需求标题
layer: L1
status: draft
traces_to: []
verified_by: []
owner: {team-name}
created: YYYY-MM-DD
---

# 需求标题

## 1. 需求描述
...

## 2. 验收条件
- [ ] AC-001: ...
- [ ] AC-002: ...

## 3. 追溯说明
- 相关设计: SA_xxx
- 相关测试: TC-xxx
```

### A.2 L2 架构文档模板

```markdown
---
id: SA_{repo}_{seq}
title: 架构设计标题
layer: L2
status: draft
traces_from: [FR_xxx]
traces_to: [DD_xxx]
verified_by: [TC-xxx]
owner: {team-name}
created: YYYY-MM-DD
---

# 架构设计标题

## 1. 设计目标
追溯需求: FR_xxx

## 2. 架构概述
...

## 3. 模块分解
详细设计: DD_xxx
```

---

**文档编制人**: nobody  
**审核人**: 待定  
**批准人**: 待定
