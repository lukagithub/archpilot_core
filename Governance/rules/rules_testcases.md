# 测试用例命名与追踪规范

**文档版本**: v1.0.0  
**最后更新**: 2026-02-01  
**适用范围**: L5 验证层（测试用例与测试报告）

> 本文档定义了测试用例的命名、编号和追踪规范。

---

## 1. 文件命名规范

### 1.1 格式

```
TC_[subsystem]_[id]_[type]_[description].md
```

### 1.2 字段说明

| 字段 | 规则 | 示例 |
|------|------|------|
| 前缀 | 固定为 `TC_` | `TC_` |
| subsystem | 子系统缩写，全小写 | `core`, `data`, `ui` |
| id | 三位数字，子系统内唯一 | `001`, `012`, `123` |
| type | 测试类型 | `unit`, `integration`, `system` |
| description | 下划线连接的小写描述 | `login_basic`, `data_sync` |

### 1.3 测试类型

| 类型 | 缩写 | 说明 |
|------|------|------|
| unit | unit | 单元测试 |
| integration | integration | 集成测试 |
| system | system | 系统测试 |
| performance | performance | 性能测试 |
| acceptance | acceptance | 验收测试 |

### 1.4 命名示例

- `TC_core_001_unit_login_basic.md`
- `TC_core_002_unit_auth_token.md`
- `TC_data_001_integration_storage_sync.md`
- `TC_ui_001_system_dashboard_load.md`

---

## 2. 测试用例 ID 规则

### 2.1 YAML 元数据

每个测试用例文件必须包含 YAML 元数据：

```yaml
---
id: TC_core_001_unit_login_basic
layer: L5
type: unit
subsystem: core
status: approved
version: v1.0.0
traces_from: [FR_core_001, DD_core_001]
traces_to: []
created: 2026-02-01
updated: 2026-02-01
---
```

### 2.2 ID 规则

- `id` 必须与文件名一致（不含扩展名）
- `id` 在子系统范围内唯一
- 编号按顺序递增，不跳号

---

## 3. 追踪字段要求

### 3.1 追踪元数据

| 字段 | 是否必需 | 说明 |
|------|----------|------|
| traces_from | ✅ | 被验证的 L1/L2/L3 文档编号 |
| traces_to | ⭕ | 通常为空（L5 是末端） |

### 3.2 traces_from 示例

```yaml
# 验证单个需求
traces_from: [FR_core_001]

# 验证需求和设计
traces_from: [FR_core_001, DD_core_001]

# 验证多个相关文档
traces_from: [FR_core_001, FR_core_002, SA_core_001, DD_core_001]
```

---

## 4. 测试执行报告规范

### 4.1 报告必需字段

测试执行报告（CSV 或 JSON）必须包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| test_id | 测试用例 ID | `TC_core_001_unit_login_basic` |
| test_name | 测试名称（可读） | `Login Basic Test` |
| subsystem | 所属子系统 | `core` |
| test_type | 测试类型 | `unit` |
| status | 执行状态 | `passed`/`failed`/`skipped` |
| timestamp | 执行时间（ISO 8601） | `2026-02-01T10:30:00Z` |
| executor | 执行者/环境 | `ci-job-123` |
| artifact | 测试产出路径 | `/artifacts/logs/test.log` |
| traces_from | 验证的文档 | `FR_core_001` |
| verification_ids | 通过的用例编号 | `TC_core_001` |

### 4.2 CSV 格式示例

```csv
timestamp,test_id,test_name,subsystem,test_type,status,executor,artifact,traces_from,verification_ids
2026-02-01T10:30:00Z,TC_core_001_unit_login_basic,Login Basic,core,unit,passed,ci-job-123,/logs/test.log,FR_core_001,TC_core_001
2026-02-01T10:31:00Z,TC_core_002_unit_auth_token,Auth Token,core,unit,failed,ci-job-123,/logs/test.log,FR_core_001,
```

### 4.3 JSON 格式示例

```json
{
  "execution": {
    "timestamp": "2026-02-01T10:30:00Z",
    "executor": "ci-job-123"
  },
  "results": [
    {
      "test_id": "TC_core_001_unit_login_basic",
      "test_name": "Login Basic",
      "subsystem": "core",
      "test_type": "unit",
      "status": "passed",
      "artifact": "/logs/test.log",
      "traces_from": ["FR_core_001"],
      "verification_ids": ["TC_core_001"]
    }
  ],
  "summary": {
    "total": 10,
    "passed": 8,
    "failed": 1,
    "skipped": 1
  }
}
```

---

## 5. 测试用例模板

### 5.1 基本结构

```markdown
---
id: TC_[subsystem]_[id]_[type]_[description]
layer: L5
type: [unit|integration|system|performance|acceptance]
subsystem: [子系统]
status: draft
version: v1.0.0
traces_from: [被验证的文档ID列表]
traces_to: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# TC_[subsystem]_[id]_[type]_[description]

## 1. 测试目的

[简要描述测试目的]

## 2. 前置条件

- [条件1]
- [条件2]

## 3. 测试步骤

1. [步骤1]
2. [步骤2]
3. [步骤3]

## 4. 预期结果

- [预期结果1]
- [预期结果2]

## 5. 测试数据

| 输入 | 预期输出 |
|------|----------|
| 数据1 | 结果1 |
| 数据2 | 结果2 |

## 6. 追溯关系

- **需求**: FR_xxx - [需求标题]
- **设计**: DD_xxx - [设计标题]

## 7. 备注

[其他说明]
```

---

## 6. 检查清单

### 测试用例创建检查

- [ ] 文件名符合 `TC_[subsystem]_[id]_[type]_[desc].md` 格式
- [ ] YAML 元数据完整
- [ ] id 与文件名一致
- [ ] traces_from 列出被验证的文档
- [ ] 测试步骤清晰可执行
- [ ] 预期结果可验证

### 测试报告检查

- [ ] 包含所有必需字段
- [ ] timestamp 为 ISO 8601 格式
- [ ] status 为 passed/failed/skipped
- [ ] traces_from 与用例元数据一致

---

## 7. 常见错误

### 错误示例 1：分隔符错误

❌ `TC-core-001-unit-login.md`（使用中划线）  
✅ `TC_core_001_unit_login.md`（使用下划线）

### 错误示例 2：ID 与文件名不一致

文件名：`TC_core_001_unit_login.md`

❌ YAML:
```yaml
id: TC_core_01_unit_login
```

✅ 修正:
```yaml
id: TC_core_001_unit_login
```

### 错误示例 3：缺少 traces_from

❌ 缺少追溯:
```yaml
traces_from: []
```

✅ 修正:
```yaml
traces_from: [FR_core_001, DD_core_001]
```

---

## 8. 关联文档

- `ARCHITECTURE_DEFINITION.md` - 架构权威定义
- `rules_naming.md` - 命名规范
- `../checklists/chk_dev.md` - 开发检查清单

