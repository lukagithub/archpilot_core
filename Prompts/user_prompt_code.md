# User Prompt - 代码/脚本编写任务

> 当任务类型为"编写代码/脚本"时，将本内容附加到 User Prompt

---

## 任务类型

**代码编写** / **脚本编写**

---

## 代码追溯标记（来自 rules_coding.md）

### 文件头部注释（MUST）

**C/C++**:
```cpp
/**
 * @file    filename.cpp
 * @brief   模块简述
 * 
 * @requirement FR_xxx - 需求标题
 * @design DD_xxx - 设计标题
 * 
 * @author  作者
 * @date    YYYY-MM-DD
 * @version 1.0.0
 */
```

**Python**:
```python
"""
模块名称

模块简述

Traceability:
    - Requirement: FR_xxx - 需求标题
    - Design: DD_xxx - 设计标题

Author: 作者
Date: YYYY-MM-DD
Version: 1.0.0
"""
```

---

## 命名规范（来自 rules_coding.md）

| 类型 | 规则 | 示例 |
|------|------|------|
| 文件名 | snake_case | `user_manager.cpp` |
| 类名 | PascalCase | `UserManager` |
| 函数名 | camelCase/snake_case | `getUserInfo` |
| 变量名 | camelCase/snake_case | `userName` |
| 常量 | UPPER_SNAKE_CASE | `MAX_SIZE` |

---

## 脚本规范（来自 rules_scripts.md）

### 通用要求

- ✅ 支持 `--help` 参数
- ✅ 使用 `--version vX.Y.Z` 格式
- ✅ 使用 `--output <path>` 指定输出
- ❌ 禁止硬编码路径

### 退出码规范

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 依赖错误 |
| 3 | 业务校验失败 |
| 4 | 外部系统错误 |

### JSON 输出格式（MUST）

```json
{
  "script": "脚本名称",
  "timestamp": "ISO 8601 时间戳",
  "status": "success|failure|warning",
  "result": {}
}
```

---

## 错误处理规范

### 错误消息格式

```
[ERROR][模块名]
code=错误码
reason=错误原因
hint=解决建议
```

### 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 调试信息 |
| INFO | 常规信息 |
| WARN | 警告 |
| ERROR | 错误 |

---

## Git 提交规范

### 提交格式

`<type>(<scope>): <subject>`

### 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| refactor | 重构 |
| test | 测试相关 |
| chore | 构建/工具 |

---

## 执行检查清单

### 代码任务

- [ ] 文件头部包含追溯注释
- [ ] 命名符合规范
- [ ] 关键函数有文档注释
- [ ] 错误处理完善
- [ ] 无编译警告

### 脚本任务

- [ ] 支持 `--help`
- [ ] 使用标准参数格式
- [ ] JSON 输出包含必需字段
- [ ] 退出码正确

