# 消息/Topic 跨仓库追溯链规范

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
**追溯类型**: Topic 定义（proto）→ 发布者（模块）→ 订阅者（模块）

---

## 1. 追溯链定义

### 1.1 消息追溯模型

```
┌─────────────────────────────────────────────────────────────────┐
│                   消息/Topic 追溯链                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────────────────────────────────────────────────┐     │
│    │              proto 仓库 (消息定义层)                   │     │
│    │  ┌─────────────────┐    ┌─────────────────┐          │     │
│    │  │ message_a.proto │    │ message_b.proto │          │     │
│    │  │  - TypeA        │    │  - TypeB        │          │     │
│    │  │  - TypeC        │    │  - TypeD        │          │     │
│    │  └────────┬────────┘    └────────┬────────┘          │     │
│    └───────────┼──────────────────────┼───────────────────┘     │
│                │                      │                          │
│                │ defines              │ defines                  │
│                ▼                      ▼                          │
│    ┌──────────────────────────────────────────────────────┐     │
│    │              Topic 定义 (通道层)                       │     │
│    │  ┌─────────────────┐    ┌─────────────────┐          │     │
│    │  │ /domain/topic_a │    │ /domain/topic_b │          │     │
│    │  │ /domain/topic_c │    │ /domain/topic_d │          │     │
│    │  └────────┬────────┘    └────────┬────────┘          │     │
│    └───────────┼──────────────────────┼───────────────────┘     │
│                │                      │                          │
│       ┌────────┴────────┐    ┌────────┴────────┐                │
│       ▼                 ▼    ▼                 ▼                 │
│  ┌─────────┐      ┌─────────┐   ┌─────────┐   ┌─────────┐      │
│  │Publisher│      │Subscriber│  │Publisher│   │Subscriber│      │
│  │module_a │      │module_b │   │module_c │   │module_d │      │
│  └─────────┘      └─────────┘   └─────────┘   └─────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 追溯关系类型

| 关系类型 | 方向 | 说明 |
|----------|------|------|
| `defines` | proto → Topic | proto 文件定义消息类型 |
| `publishes` | 模块 → Topic | 模块发布消息到 Topic |
| `subscribes` | Topic → 模块 | 模块订阅 Topic 消息 |
| `transforms` | Topic → Topic | 消息转换关系 |

---

## 2. Proto 消息注册

### 2.1 消息定义元数据

每个核心 proto 消息定义 **必须** 包含追溯注释：

```protobuf
/**
 * @proto_id MSG_{domain}_{name}_{seq}
 * @category {category}
 * @publisher {module_name}
 * @subscriber {module_list}
 * @topic /{domain}/{topic_name}
 * @frequency {frequency} (event-driven|periodic)
 * @qos RELIABLE|BEST_EFFORT
 * @design SA_{module}_{seq}
 */
message MessageType {
  required uint64 timestamp = 1;
  required string type = 2;
  repeated Item items = 3;
}
```

### 2.2 消息分类

> **说明**: 项目应根据业务领域定义消息分类。

| 类别 | 前缀 | 说明 | 示例 |
|------|------|------|------|
| 事件通知 | `MSG_event_` | 事件和状态变更 | `MSG_event_status_001` |
| 系统监控 | `MSG_monitor_` | 系统状态、健康度 | `MSG_monitor_health_001` |
| 数据采集 | `MSG_data_` | 数据采集和传输 | `MSG_data_sensor_001` |
| 命令控制 | `MSG_cmd_` | 控制指令 | `MSG_cmd_control_001` |
| 配置管理 | `MSG_config_` | 配置变更 | `MSG_config_param_001` |

---

## 3. Topic 注册表

### 3.1 Topic 注册格式

Topic 注册表存储在 `{project}/TopicRegistry/topic_registry.yaml`:

```yaml
# Topic 注册表
version: "1.0.0"
updated: "YYYY-MM-DD"

topics:
  # === 事件通知 Topic ===
  - topic_id: TOPIC_{domain}_{name}
    topic_name: /{domain}/{topic_name}
    proto_file: proto/{message}.proto
    message_type: {package}.{MessageType}
    category: {category}
    publisher:
      - module: {module_name}
        component: {component_name}
        frequency: {frequency}
        trigger: event-driven|periodic
    subscriber:
      - module: {module_name}
        component: {component_name}
        purpose: {description}
    qos:
      reliability: RELIABLE|BEST_EFFORT
      durability: VOLATILE|TRANSIENT_LOCAL
      history_depth: {depth}
    design_ref: SA_{module}_{seq}
```

### 3.2 Topic 命名规范

| 域 | 前缀 | 示例 |
|-----|------|------|
| 事件域 | `/{domain}/event/` | `/{domain}/event/status` |
| 监控域 | `/{domain}/monitor/` | `/{domain}/monitor/health` |
| 数据域 | `/{domain}/data/` | `/{domain}/data/sensor` |
| 命令域 | `/{domain}/cmd/` | `/{domain}/cmd/control` |

---

## 4. 发布/订阅追溯矩阵

### 4.1 矩阵文件格式

发布/订阅矩阵存储在 `{project}/TopicRegistry/pubsub_matrix.csv`:

```csv
topic_name,proto_type,publisher_module,publisher_component,subscriber_module,subscriber_component,purpose,status,design_ref
/{domain}/event/status,{package}.Status,module_a,ComponentA,module_b,ComponentB,状态展示,implemented,SA_module_a_001
/{domain}/event/status,{package}.Status,module_a,ComponentA,module_c,ComponentC,日志记录,implemented,SA_module_a_001
```

### 4.2 关键 Topic 追溯表（模板）

| Topic | Proto | 发布者 | 订阅者 | 用途 | 设计文档 |
|-------|-------|--------|--------|------|----------|
| `/{domain}/topic_a` | `TypeA` | module_a | module_b, module_c | 事件通知 | SA_xxx |
| `/{domain}/topic_b` | `TypeB` | module_b | module_a, module_d | 数据共享 | SA_xxx |

---

## 5. 验证与校验规则

### 5.1 自动化校验规则

| 规则 ID | 规则描述 | 严重级别 | 检查方式 |
|---------|----------|----------|----------|
| MR-001 | 每个 Topic 必须有明确的 proto 定义 | ERROR | proto 文件检查 |
| MR-002 | 每个 Topic 必须至少有一个发布者 | ERROR | 代码扫描 |
| MR-003 | 每个 Topic 必须至少有一个订阅者 | WARNING | 代码扫描 |
| MR-004 | 发布者声明的 Topic 必须在注册表中存在 | ERROR | 交叉验证 |
| MR-005 | Topic QoS 配置必须在发布者和订阅者之间兼容 | ERROR | QoS 检查 |
| MR-006 | 关键 Topic 必须有设计文档追溯 | WARNING | 元数据检查 |
| MR-007 | Topic 命名必须符合规范 | ERROR | 正则匹配 |

### 5.2 校验脚本接口

```bash
# 验证 Topic 注册表完整性
python validate_topics.py --registry topic_registry.yaml --output report.json

# 扫描代码中的发布/订阅，与注册表对比
python validate_topics.py --scan-code --repo {repo_name} --compare

# 生成发布/订阅关系图
python validate_topics.py --generate-graph --format mermaid --output pubsub_graph.mmd

# 检查孤立 Topic（有定义但无订阅）
python validate_topics.py --check-orphan-topics
```

### 5.3 校验输出格式

```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "summary": {
    "total_topics": 25,
    "with_publisher": 25,
    "with_subscriber": 23,
    "orphan_topics": 2,
    "missing_design_ref": 3
  },
  "issues": [
    {
      "rule_id": "MR-003",
      "severity": "WARNING",
      "topic": "/debug/internal_state",
      "message": "Topic has no subscriber"
    }
  ],
  "pubsub_coverage": {
    "module_a": {"published": 2, "subscribed": 5},
    "module_b": {"published": 3, "subscribed": 8}
  }
}
```

---

## 6. 数据流追溯

### 6.1 端到端数据流示例

```
┌─────────────────────────────────────────────────────────────────┐
│              数据流追溯示例                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [数据源]                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ /data/       │  │ /data/       │  │ /data/       │          │
│  │ source_a     │  │ source_b     │  │ source_c     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                    │
│         └────────────┬────┴────────────┬────┘                    │
│                      ▼                 ▼                         │
│  [处理器]     ┌──────────────────────────────┐                  │
│               │     module_processor          │                  │
│               │  ┌──────────────────────┐    │                  │
│               │  │ Handler_A            │    │                  │
│               │  │ Handler_B            │    │                  │
│               │  └──────────────────────┘    │                  │
│               └──────────────┬───────────────┘                  │
│                              │                                   │
│                              ▼                                   │
│  [输出]       ┌──────────────────────────────┐                  │
│               │ /event/result                │                  │
│               │ /event/status                │                  │
│               └──────────────┬───────────────┘                  │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ module_ui    │  │ module_ctrl  │  │ module_log   │          │
│  │ (展示)       │  │ (控制)       │  │ (记录)       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 数据流追溯元数据

```yaml
dataflow:
  - flow_id: DF_{domain}_{name}_{seq}
    name: 数据流名称
    description: 端到端数据流描述
    design_ref: SA_{module}_{seq}
    
    stages:
      - stage: 1_data_source
        topics:
          - /data/source_a
          - /data/source_b
        
      - stage: 2_processing
        module: {module_name}
        components:
          - Handler_A
          - Handler_B
        
      - stage: 3_output
        topics:
          - /event/result
          - /event/status
        
      - stage: 4_consumers
        subscribers:
          - module: module_ui
            action: 结果展示
          - module: module_ctrl
            action: 控制执行
          - module: module_log
            action: 日志记录
```

---

## 7. 消息版本管理

### 7.1 版本兼容性规则

| 规则 ID | 规则描述 | 影响 |
|---------|----------|------|
| MV-001 | 新增字段使用 optional，保持向后兼容 | 低风险 |
| MV-002 | 禁止删除或重命名已发布的字段 | 破坏性变更 |
| MV-003 | 字段编号一旦分配不可复用 | 数据损坏风险 |
| MV-004 | 类型变更需要新增字段并废弃旧字段 | 需迁移计划 |

### 7.2 版本变更追溯

```yaml
message_changes:
  - message: {package}.{MessageType}
    version: v1.1.0
    date: YYYY-MM-DD
    changes:
      - type: add_field
        field: {field_name}
        field_number: {number}
        reason: {reason}
        design_ref: ADR_{decision}_{seq}
    backward_compatible: true
    
  - message: {package}.{MessageType}
    version: v2.0.0
    date: YYYY-MM-DD
    changes:
      - type: deprecate_field
        field: {field_name}
        field_number: {number}
        reason: {reason}
        migration_guide: DOC_{migration}_{seq}
    backward_compatible: false
```

---

## 8. 代码集成规范

### 8.1 发布者代码追溯

```cpp
/**
 * @file publisher_component.cc
 * @brief 发布者组件
 * 
 * @publishes /{domain}/topic_a ({package}.TypeA)
 * @publishes /{domain}/topic_b ({package}.TypeB)
 * @design SA_{module}_{seq}
 */

class PublisherComponent : public Component<> {
 public:
  /**
   * @topic_pub /{domain}/topic_a
   * @frequency 10Hz, event-driven
   * @design DD_{module}_{component}_{seq}
   */
  void PublishData(const TypeA& data) {
    writer_->Write(data);
  }
};
```

### 8.2 订阅者代码追溯

```cpp
/**
 * @file subscriber_component.cc
 * @brief 订阅者组件
 * 
 * @subscribes /{domain}/topic_a ({package}.TypeA)
 * @subscribes /{domain}/topic_b ({package}.TypeB)
 * @design SA_{module}_{seq}
 */

class SubscriberComponent {
 public:
  /**
   * @topic_sub /{domain}/topic_a
   * @handler OnDataReceived
   * @design DD_{module}_{handler}_{seq}
   */
  void OnDataReceived(const std::shared_ptr<TypeA>& msg) {
    // 处理接收到的消息
  }
};
```

---

## 9. 工具支持

### 9.1 推荐工具链

| 工具 | 用途 | 位置 |
|------|------|------|
| `validate_topics.py` | Topic 注册表验证 | `archpilot_core/Tools/` |
| `scan_pubsub.py` | 扫描代码发布/订阅 | `archpilot_core/Tools/` |
| `generate_topic_graph.py` | 生成 Topic 关系图 | `archpilot_core/Tools/` |
| `proto_trace.py` | Proto 追溯分析 | `archpilot_core/Tools/` |

### 9.2 CI 集成

```yaml
# .github/workflows/topic_validation.yml
name: Topic Validation

on: [push, pull_request]

jobs:
  validate-topics:
    runs-on: ubuntu-latest
    steps:
      - name: Validate Topic Registry
        run: python validate_topics.py --registry topic_registry.yaml
        
      - name: Check PubSub Consistency
        run: python scan_pubsub.py --compare --fail-on-mismatch
```

---

## 附录 A: Topic 清单模板

### A.1 事件通知 Topic

| Topic | Proto | 发布者 | 频率 | 说明 |
|-------|-------|--------|------|------|
| `/{domain}/event/status` | `Status` | module_a | 事件触发 | 状态变更 |
| `/{domain}/event/alert` | `Alert` | module_a | 事件触发 | 告警通知 |

### A.2 监控 Topic

| Topic | Proto | 发布者 | 频率 | 说明 |
|-------|-------|--------|------|------|
| `/{domain}/monitor/health` | `HealthStatus` | module_monitor | 1Hz | 系统健康 |
| `/{domain}/monitor/metrics` | `Metrics` | module_monitor | 1Hz | 性能指标 |

### A.3 数据 Topic

| Topic | Proto | 发布者 | 频率 | 说明 |
|-------|-------|--------|------|------|
| `/{domain}/data/sensor` | `SensorData` | module_driver | 100Hz | 传感器数据 |
| `/{domain}/data/processed` | `ProcessedData` | module_processor | 10Hz | 处理后数据 |

---

**文档编制人**: nobody  
**审核人**: 待定  
**批准人**: 待定
