# 故障处理跨仓库追溯链规范

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
**追溯类型**: 故障码（proto）→ 检测（detector）→ 响应（responder）

---

## 1. 追溯链定义

### 1.1 故障处理追溯模型

```
┌─────────────────────────────────────────────────────────────────┐
│                   故障处理追溯链                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                proto 仓库 (故障码定义层)                 │    │
│  │  ┌─────────────────────────────────────────────────┐   │    │
│  │  │ fault_msg.proto                                 │   │    │
│  │  │  - FaultCode (故障码)                           │   │    │
│  │  │  - FaultLevel (故障等级)                        │   │    │
│  │  │  - DisposalCode (处置码)                        │   │    │
│  │  │  - FaultItem (故障项)                           │   │    │
│  │  └─────────────────────┬───────────────────────────┘   │    │
│  └────────────────────────┼───────────────────────────────┘    │
│                           │ defines                              │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           故障诊断子系统 (检测层)                        │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │    │
│  │  │ detector_a  │  │ detector_b  │  │ detector_c  │    │    │
│  │  │ (检测器 A)  │  │ (检测器 B)  │  │ (检测器 C)  │    │    │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │    │
│  └─────────┼────────────────┼────────────────┼───────────┘    │
│            │                │                │                  │
│            │ detects        │ monitors       │ reports          │
│            ▼                ▼                ▼                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              数据总线子系统 (传输层)                     │    │
│  │  ┌────────────────────────────────────────────────┐   │    │
│  │  │ /fault/code           /system/status           │   │    │
│  │  │ /fault/disposal       /system/health           │   │    │
│  │  └────────────────────────┬───────────────────────┘   │    │
│  └───────────────────────────┼───────────────────────────┘    │
│                              │ dispatches                       │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           闭环响应子系统 (响应层)                        │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │    │
│  │  │ responder_ui│  │ responder_  │  │ responder_  │    │    │
│  │  │ (人机交互)  │  │ control     │  │ logger      │    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘    │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 追溯关系类型

| 关系类型 | 方向 | 说明 |
|----------|------|------|
| `defines` | proto → 检测器 | 故障码定义被检测器使用 |
| `detects` | 检测器 → 故障事件 | 检测器产生故障事件 |
| `dispatches` | 故障事件 → 响应器 | 故障事件分发给响应器 |
| `responds` | 响应器 → 动作 | 响应器执行处置动作 |

---

## 2. 故障码定义规范

### 2.1 故障码编码规则

故障码采用分层编码结构：

```
FaultCode = [模块ID(4位)] + [子系统ID(2位)] + [故障类型(2位)] + [序号(4位)]
           ════════════   ═══════════════   ══════════════   ════════════
              0x0001         0x01              0x01            0x0001
```

**示例**:
- `0x0001010101` = module_a + subsystem_1 + warning + 序号1
- `0x0002010201` = module_b + subsystem_1 + error + 序号1

### 2.2 模块 ID 分配

> **说明**: 项目应根据实际模块结构定义模块 ID 分配表。

| 模块 ID | 仓库 | 说明 |
|---------|------|------|
| `0x0001` | module_a | 模块 A |
| `0x0002` | module_b | 模块 B |
| `0x0003` | module_c | 模块 C |
| `0x0004` | module_d | 模块 D |
| `0x0005` | module_e | 模块 E |

### 2.3 故障类型分配

| 类型 ID | 名称 | 说明 |
|---------|------|------|
| `0x01` | WARNING | 警告级别，不影响运行 |
| `0x02` | ERROR | 错误级别，功能降级 |
| `0x03` | FATAL | 致命级别，需停止运行 |
| `0x04` | EMERGENCY | 紧急级别，立即停止 |

### 2.4 故障码注册表

故障码注册表存储在 `{project}/FaultRegistry/fault_codes.yaml`:

```yaml
# 故障码注册表
version: "1.0.0"
updated: "YYYY-MM-DD"

fault_codes:
  # === module_a ===
  - code: "0x0001010101"
    code_id: ERR_{module_a}_{fault_name}_warning
    module: {module_name}
    subsystem: {subsystem_name}
    type: WARNING
    description: {故障描述}
    detection_logic: {检测条件}
    response_action: DIS_ALARM
    design_ref: SA_{module}_{seq}
    test_ref: TC-{module}-UT-{seq}

  - code: "0x0001010201"
    code_id: ERR_{module_a}_{fault_name}_error
    module: {module_name}
    subsystem: {subsystem_name}
    type: ERROR
    description: {故障描述}
    detection_logic: {检测条件}
    response_action: DIS_STOP
    design_ref: SA_{module}_{seq}
    test_ref: TC-{module}-UT-{seq}
```

---

## 3. 故障检测追溯

### 3.1 检测器注册

每个故障检测器 **必须** 在检测器注册表中登记：

```yaml
# 检测器注册表: {project}/FaultRegistry/detectors.yaml
version: "1.0.0"
updated: "YYYY-MM-DD"

detectors:
  - detector_id: DET_{module}_{detector_name}
    name: {DetectorClassName}
    module: {module_name}
    source_file: {module}/src/{path}/{file}.cc
    input_topics:
      - /data/input_a
      - /data/input_b
    output_codes:
      - ERR_{module}_{fault_name}_warning
      - ERR_{module}_{fault_name}_error
    output_topic: /fault/code
    design_ref: DD_{module}_{detector}_{seq}
    trigger_condition: periodic ({frequency}Hz)
```

### 3.2 检测器代码追溯注解

```cpp
/**
 * @file fault_detector.cc
 * @brief 故障检测器
 *
 * @detector_id DET_{module}_{name}
 * @input_topics /data/input_a, /data/input_b
 * @output_codes ERR_{module}_{fault}_warning, ERR_{module}_{fault}_error
 * @output_topic /fault/code
 * @design DD_{module}_{detector}_{seq}
 * @requirement FR_{safety}_{seq}
 */

class FaultDetector : public RecurrentRunner {
 public:
  /**
   * @detection_rule 故障检测规则
   * @threshold {condition} → WARNING, {condition} → ERROR
   * @output ERR_{module}_{fault}_*
   */
  void RunOnce() override {
    auto value = GetValue();
    if (value < threshold_critical) {
      ReportError(ERR_critical);  // @errcode 0x0001010201
    } else if (value < threshold_warning) {
      ReportError(ERR_warning);   // @errcode 0x0001010101
    }
  }
};
```

---

## 4. 故障响应追溯

### 4.1 响应器注册

```yaml
# 响应器注册表: {project}/FaultRegistry/responders.yaml
version: "1.0.0"
updated: "YYYY-MM-DD"

responders:
  # === UI 响应器 ===
  - responder_id: RSP_ui_alarm
    name: UI_AlarmHandler
    module: {module_ui}
    source_file: {module}/src/{path}/{file}.cc
    input_topic: /fault/code
    input_codes:
      - ERR_{module}_{fault}_warning
    response_action: DIS_ALARM
    action_description: 显示告警提示
    design_ref: DD_{module}_{handler}_{seq}

  # === 控制响应器 ===
  - responder_id: RSP_control_stop
    name: Control_EmergencyStop
    module: {module_control}
    source_file: {module}/src/{path}/{file}.cc
    input_topic: /fault/disposal
    input_codes:
      - ERR_{module}_{fault}_emergency
    response_action: DIS_EMERGENCY_STOP
    action_description: 紧急停止
    design_ref: DD_{module}_{handler}_{seq}

  # === 日志响应器 ===
  - responder_id: RSP_logger_record
    name: Logger_FaultRecord
    module: {module_tools}
    source_file: {module}/src/{path}/{file}.cc
    input_topic: /fault/code
    input_codes:
      - "*"  # 订阅所有故障码
    response_action: LOG_RECORD
    action_description: 记录故障日志
    design_ref: DD_{module}_{logger}_{seq}
```

### 4.2 处置码定义

```yaml
# 处置码定义: {project}/FaultRegistry/disposal_codes.yaml
version: "1.0.0"
updated: "YYYY-MM-DD"

disposal_codes:
  - code: DIS_NOTHING
    value: 0
    description: 无需处置
    actions: []

  - code: DIS_ALARM
    value: 1
    description: 告警提示
    actions:
      - UI 显示警告
      - 语音播报

  - code: DIS_REQUEST_TAKEOVER
    value: 2
    description: 请求人工接管
    actions:
      - UI 显示接管请求
      - 语音提示
      - 记录日志

  - code: DIS_STOP
    value: 3
    description: 减速停止
    actions:
      - 执行停止流程
      - UI 显示停止中
      - 记录日志

  - code: DIS_EMERGENCY_STOP
    value: 4
    description: 紧急停止
    actions:
      - 立即停止
      - UI 显示紧急停止
      - 记录日志
      - 上报云端
```

---

## 5. 端到端追溯矩阵

### 5.1 故障追溯矩阵格式

故障追溯矩阵存储在 `{project}/FaultRegistry/fault_trace_matrix.csv`:

```csv
fault_code,fault_code_id,detector_id,detector_module,input_topics,responder_id,responder_module,disposal_code,design_ref,test_ref
0x0001010101,ERR_{module}_{fault}_warning,DET_{module}_{detector},{module},"/data/input_a,/data/input_b",RSP_ui_alarm,{module_ui},DIS_ALARM,SA_{module}_{seq},TC-{module}-IT-{seq}
0x0001010201,ERR_{module}_{fault}_error,DET_{module}_{detector},{module},"/data/input_a,/data/input_b","RSP_ui_takeover,RSP_control_stop",{modules},DIS_STOP,SA_{module}_{seq},TC-{module}-IT-{seq}
```

### 5.2 端到端追溯表（模板）

| 故障码 | 故障 ID | 检测器 | 输入数据 | 响应器 | 处置码 | 设计文档 | 测试用例 |
|--------|---------|--------|----------|--------|--------|----------|----------|
| 0x0001010101 | ERR_xxx_warning | Detector_A | /data/input_a, /data/input_b | UI | DIS_ALARM | SA_xxx | TC-xxx |
| 0x0001010201 | ERR_xxx_error | Detector_A | /data/input_a, /data/input_b | UI, Control | DIS_STOP | SA_xxx | TC-xxx |

---

## 6. 验证与校验规则

### 6.1 自动化校验规则

| 规则 ID | 规则描述 | 严重级别 | 检查方式 |
|---------|----------|----------|----------|
| FR-001 | 每个故障码必须有唯一的 code_id | ERROR | 注册表扫描 |
| FR-002 | 每个故障码必须有至少一个检测器 | ERROR | 交叉验证 |
| FR-003 | 每个故障码必须有至少一个响应器 | WARNING | 交叉验证 |
| FR-004 | 每个检测器必须有对应的源码实现 | ERROR | 文件检查 |
| FR-005 | 每个响应器必须有对应的源码实现 | ERROR | 文件检查 |
| FR-006 | 故障码编码必须符合编码规则 | ERROR | 正则匹配 |
| FR-007 | EMERGENCY 级故障必须有 DIS_EMERGENCY_STOP 响应 | ERROR | 逻辑检查 |
| FR-008 | 故障码必须有设计文档追溯 | WARNING | 元数据检查 |
| FR-009 | 故障码必须有测试用例追溯 | WARNING | 元数据检查 |
| FR-010 | 检测器输入 Topic 必须在 Topic 注册表中存在 | ERROR | 交叉验证 |

### 6.2 校验脚本接口

```bash
# 验证故障码注册表完整性
python validate_faults.py --registry fault_codes.yaml --output report.json

# 验证检测器-故障码-响应器追溯链
python validate_faults.py --trace-chain --fail-on-broken

# 扫描代码中的故障码使用，与注册表对比
python validate_faults.py --scan-code --repo {repo_name} --compare

# 生成故障处理流程图
python validate_faults.py --generate-flow --format mermaid --output fault_flow.mmd

# 检查孤立故障码（有定义但无响应）
python validate_faults.py --check-orphan-codes

# 验证 EMERGENCY 级故障响应完整性
python validate_faults.py --check-emergency-response
```

### 6.3 校验输出格式

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "summary": {
    "total_fault_codes": 45,
    "with_detector": 45,
    "with_responder": 43,
    "orphan_codes": 2,
    "missing_design_ref": 5,
    "missing_test_ref": 8
  },
  "issues": [
    {
      "rule_id": "FR-003",
      "severity": "WARNING",
      "fault_code": "0x0005010101",
      "message": "Fault code has no responder"
    }
  ],
  "trace_coverage": {
    "module_a": {"codes": 15, "traced": 14},
    "module_b": {"codes": 12, "traced": 11}
  }
}
```

---

## 7. 故障分级响应策略

### 7.1 故障等级与响应映射

| 故障等级 | FaultLevel | 典型场景 | 标准响应 | 响应时限 |
|----------|----------|----------|----------|----------|
| WARNING | LEVEL_WARNING | 资源告警 | DIS_ALARM | 无时限 |
| ERROR | LEVEL_ERROR | 模块超时、功能异常 | DIS_REQUEST_TAKEOVER | 5秒内 |
| FATAL | LEVEL_FATAL | 关键模块失效 | DIS_STOP | 3秒内 |
| EMERGENCY | LEVEL_EMERGENCY | 紧急情况 | DIS_EMERGENCY_STOP | 100ms内 |

### 7.2 响应优先级规则

```yaml
# 响应优先级策略: {project}/FaultRegistry/response_priority.yaml
version: "1.0.0"

priority_rules:
  # 规则1: EMERGENCY 优先级最高，覆盖其他响应
  - rule_id: PRI-001
    condition: fault_level == EMERGENCY
    action: immediate_emergency_stop
    override: all
    priority: 1

  # 规则2: FATAL 级优先于 ERROR
  - rule_id: PRI-002
    condition: fault_level == FATAL
    action: controlled_stop
    override: ERROR, WARNING
    priority: 2

  # 规则3: 同级故障时，取最严重处置
  - rule_id: PRI-003
    condition: multiple_faults_same_level
    action: max_disposal_code
    priority: 3

  # 规则4: WARNING 不影响当前状态
  - rule_id: PRI-004
    condition: fault_level == WARNING
    action: display_alarm_only
    override: none
    priority: 4
```

---

## 8. 跨仓库追溯示例

### 8.1 故障检测端到端追溯

```
┌─────────────────────────────────────────────────────────────────┐
│              故障检测端到端追溯示例                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [proto 仓库]                                                    │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ fault_msg.proto                                       │      │
│  │  - FaultCode (0x0001010301: 紧急故障)                 │      │
│  │  - DisposalCode (DIS_EMERGENCY_STOP)                  │      │
│  └──────────────────────────┬───────────────────────────┘      │
│                             │ defines                            │
│                             ▼                                    │
│  [module_a 仓库]                                                │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Detector_A                                            │      │
│  │  - Input: /data/input_a, /data/input_b                │      │
│  │  - Detection: {condition}                             │      │
│  │  - Output: FaultCode(0x0001010301)                    │      │
│  └──────────────────────────┬───────────────────────────┘      │
│                             │ detects                            │
│                             ▼                                    │
│  [通信层 - Topic]                                               │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ /fault/code                                           │      │
│  │ /fault/disposal                                       │      │
│  └──────────────────────────┬───────────────────────────┘      │
│                             │ dispatches                         │
│            ┌────────────────┼────────────────┐                  │
│            ▼                ▼                ▼                   │
│  [module_ui 仓库]  [module_ctrl 仓库]  [module_log 仓库]        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ UI           │  │ Controller   │  │ DataLogger   │          │
│  │ - 显示紧急   │  │ - 紧急停止   │  │ - 记录日志   │          │
│  │   停止提示   │  │ - 执行动作   │  │ - 上报云端   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  [验证: L5]                                                      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ TC-{module}-IT-{seq}: 紧急故障响应集成测试            │      │
│  │  - 模拟紧急场景                                       │      │
│  │  - 验证紧急停止执行                                   │      │
│  │  - 验证响应时延 < 100ms                               │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 追溯元数据示例

```yaml
# 端到端追溯记录
trace_record:
  trace_id: TRACE_{fault}_{seq}
  description: 故障检测到响应的完整追溯
  created: YYYY-MM-DD
  
  # L1 需求追溯
  requirements:
    - FR_{safety}_{seq}: 故障检测需求
    - FR_{safety}_{seq}: 紧急响应需求
  
  # L2 架构追溯
  architecture:
    - SA_{module}_{seq}: 检测架构
    - SA_{system}_{seq}: 系统架构
  
  # L3 详细设计追溯
  detailed_design:
    - DD_{module}_{detector}_{seq}: 检测器设计
    - DD_{module}_{handler}_{seq}: 响应处理设计
  
  # L4 实现追溯
  implementation:
    - {module}/src/{path}/detector.cc
    - {module}/src/{path}/handler.cc
  
  # 故障码追溯
  fault_codes:
    - code: "0x0001010301"
      code_id: ERR_{module}_{fault}_emergency
      detector: DET_{module}_{detector}
      responders: [RSP_ui_takeover, RSP_control_stop]
      disposal: DIS_EMERGENCY_STOP
  
  # L5 验证追溯
  verification:
    - TC-{module}-UT-{seq}: 单元测试
    - TC-{module}-IT-{seq}: 集成测试
    - TC-{system}-ST-{seq}: 系统测试
```

---

## 9. 工具支持

### 9.1 推荐工具链

| 工具 | 用途 | 位置 |
|------|------|------|
| `validate_faults.py` | 故障码注册表验证 | `archpilot_core/Tools/` |
| `scan_errcode.py` | 扫描代码中的故障码 | `archpilot_core/Tools/` |
| `generate_fault_flow.py` | 生成故障处理流程图 | `archpilot_core/Tools/` |
| `fault_trace_report.py` | 生成追溯报告 | `archpilot_core/Tools/` |

### 9.2 CI 集成

```yaml
# .github/workflows/fault_validation.yml
name: Fault Code Validation

on: [push, pull_request]

jobs:
  validate-faults:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Fault Registry
        run: python validate_faults.py --registry fault_codes.yaml
        
      - name: Check Trace Chain
        run: python validate_faults.py --trace-chain --fail-on-broken
        
      - name: Verify Emergency Response
        run: python validate_faults.py --check-emergency-response
```

---

## 10. 维护流程

### 10.1 新增故障码流程

1. **需求分析**：确定需要检测的故障场景
2. **编码分配**：按编码规则分配新故障码
3. **注册登记**：在 `fault_codes.yaml` 中添加条目
4. **检测器开发**：实现检测逻辑，添加追溯注解
5. **响应器配置**：配置对应的响应器和处置码
6. **追溯更新**：更新追溯矩阵
7. **测试验证**：编写并执行测试用例
8. **文档更新**：更新设计文档追溯

### 10.2 变更评审检查清单

- [ ] 故障码编码符合规则
- [ ] 故障码已在注册表中登记
- [ ] 检测器已在注册表中登记
- [ ] 响应器已配置
- [ ] 追溯矩阵已更新
- [ ] 测试用例已编写
- [ ] 设计文档已更新

---

## 附录 A: 故障码快速查询模板

### A.1 按模块查询

| 模块 | 故障码范围 | 数量 |
|------|------------|------|
| module_a | 0x0001xxxxxx | {count} |
| module_b | 0x0002xxxxxx | {count} |
| module_c | 0x0003xxxxxx | {count} |

### A.2 按等级查询

| 等级 | 故障码特征 | 数量 | 典型响应 |
|------|------------|------|----------|
| WARNING | xxxx01xxxx | {count} | DIS_ALARM |
| ERROR | xxxx02xxxx | {count} | DIS_REQUEST_TAKEOVER |
| FATAL | xxxx03xxxx | {count} | DIS_STOP |
| EMERGENCY | xxxx04xxxx | {count} | DIS_EMERGENCY_STOP |

---

**文档编制人**: nobody  
**审核人**: 待定  
**批准人**: 待定
