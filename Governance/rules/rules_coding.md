# 编码规范

**文档版本**: v1.0.0  
**最后更新**: 2026-02-01  
**适用范围**: 基于本框架的所有代码实现

> 本文档定义了代码编写的规范要求，确保代码质量和可追溯性。

---

## 1. 五层可追溯性规范

### 1.1 层级关系

> **权威来源**: L1-L5 的职责、产出物、目录位置与前缀等内容请参考 `ARCHITECTURE_DEFINITION.md`。

**执行要点**:
- 任何代码文件必须能追溯到上层设计文档
- 追溯关系通过代码注释和元数据维护
- 当层级定义更新时，同步更新代码中的追溯标记

### 1.2 追溯关系链

```
L1_Requirements (需求)
    ↓ implemented_by
L2_Architecture (架构)
    ↓ implemented_by  
L3_DetailDesign (详细设计)
    ↓ implemented_by
L4_Implementation (代码实现)
    ↓ verified_by
L5_Verification (测试验证)
    ↓ validates
L1_Requirements (需求闭环)
```

---

## 2. 代码追溯标记规范

### 2.1 文件头部注释

所有源代码文件必须在头部包含追溯信息：

**C/C++ 示例**：
```cpp
/**
 * @file    module_name.cpp
 * @brief   模块简要描述
 * 
 * @requirement FR_core_001 - 需求标题
 * @architecture SA_core_001 - 架构标题
 * @design DD_core_001 - 设计标题
 * @testcase TC-core-001 - 测试标题
 * 
 * @author  作者名
 * @date    2026-02-01
 * @version 1.0.0
 */
```

**Python 示例**：
```python
"""
模块名称

模块简要描述

Traceability:
    - Requirement: FR_core_001 - 需求标题
    - Architecture: SA_core_001 - 架构标题
    - Design: DD_core_001 - 设计标题
    - Testcase: TC-core-001 - 测试标题

Author: 作者名
Date: 2026-02-01
Version: 1.0.0
"""
```

**JavaScript/TypeScript 示例**：
```javascript
/**
 * @module ModuleName
 * @description 模块简要描述
 * 
 * @requirement FR_core_001 - 需求标题
 * @architecture SA_core_001 - 架构标题
 * @design DD_core_001 - 设计标题
 * @testcase TC-core-001 - 测试标题
 * 
 * @author 作者名
 * @date 2026-02-01
 * @version 1.0.0
 */
```

### 2.2 函数/方法注释

关键函数必须包含追溯标记：

```cpp
/**
 * @brief 函数简要描述
 * 
 * 详细描述（可选）
 * 
 * @param param1 参数1说明
 * @param param2 参数2说明
 * @return 返回值说明
 * 
 * @requirement FR_core_001
 * @design DD_core_001
 * 
 * @note 注意事项
 * @warning 警告信息
 */
```

---

## 3. 命名规范

### 3.1 通用规则

| 类型 | 规则 | 示例 |
|------|------|------|
| 文件名 | snake_case | `user_manager.cpp` |
| 类名 | PascalCase | `UserManager` |
| 函数名 | camelCase 或 snake_case | `getUserInfo` / `get_user_info` |
| 变量名 | camelCase 或 snake_case | `userName` / `user_name` |
| 常量 | UPPER_SNAKE_CASE | `MAX_BUFFER_SIZE` |
| 宏定义 | UPPER_SNAKE_CASE | `ENABLE_DEBUG` |

### 3.2 语言特定规范

**C++**：
- 类名使用 PascalCase
- 成员函数使用 camelCase
- 成员变量使用 `m_` 前缀或 `_` 后缀

**Python**：
- 类名使用 PascalCase
- 函数和变量使用 snake_case
- 私有成员使用 `_` 或 `__` 前缀

**JavaScript/TypeScript**：
- 类名使用 PascalCase
- 函数和变量使用 camelCase
- 常量使用 UPPER_SNAKE_CASE

---

## 4. 错误处理规范

### 4.1 错误码定义

建议定义统一的错误码体系：

| 错误码范围 | 类别 | 说明 |
|------------|------|------|
| 0 | 成功 | 正常执行完成 |
| 1-9 | 通用错误 | 参数错误、权限错误等 |
| 10-19 | 配置错误 | 配置文件问题 |
| 20-29 | 网络错误 | 网络连接问题 |
| 30-39 | 数据错误 | 数据格式、校验问题 |
| 100+ | 业务错误 | 业务逻辑相关错误 |

### 4.2 错误信息规范

错误信息必须包含：
1. 错误位置（文件、函数、行号）
2. 错误原因
3. 解决建议（可选）

```cpp
// 示例：错误处理
if (input == nullptr) {
    LOG_ERROR("[ModuleName::FunctionName] Invalid input: null pointer. "
              "Please ensure the input is properly initialized.");
    return ERROR_INVALID_PARAM;
}
```

---

## 5. 日志规范

### 5.1 日志级别

| 级别 | 用途 | 示例场景 |
|------|------|----------|
| DEBUG | 调试信息 | 变量值、执行流程 |
| INFO | 常规信息 | 启动、关闭、关键步骤 |
| WARN | 警告信息 | 可恢复的异常情况 |
| ERROR | 错误信息 | 影响功能的错误 |
| FATAL | 致命错误 | 程序无法继续运行 |

### 5.2 日志格式

```
[时间戳] [级别] [模块名] 消息内容
```

示例：
```
[2026-02-01T10:30:00] [INFO] [UserManager] User login successful: user_id=12345
[2026-02-01T10:30:01] [ERROR] [DataProcessor] Failed to parse data: invalid format
```

---

## 6. 代码结构规范

### 6.1 文件组织

```
L4_Implementation/
├── src/                    # 源代码
│   ├── core/              # 核心功能
│   ├── utils/             # 工具类
│   └── main.cpp           # 入口文件
├── include/               # 头文件
│   ├── core/
│   └── utils/
├── config/                # 配置文件
└── README.md              # 说明文档
```

### 6.2 代码组织

每个源文件应按以下顺序组织：

1. 版权声明和许可证
2. 文件头部注释（含追溯信息）
3. 包含/导入语句
4. 宏定义和常量
5. 类型定义
6. 全局变量（尽量避免）
7. 函数声明
8. 函数实现

---

## 7. 注释规范

### 7.1 注释原则

- ✅ 解释"为什么"，而不是"做什么"
- ✅ 复杂逻辑必须有注释
- ✅ 公共 API 必须有完整文档注释
- ❌ 不要注释显而易见的代码
- ❌ 不要保留无用的注释代码

### 7.2 TODO/FIXME 标记

```cpp
// TODO: [优先级] 描述待完成的功能
// TODO: [HIGH] 实现缓存机制以提高性能

// FIXME: [问题描述] 需要修复的问题
// FIXME: 边界条件未处理，可能导致数组越界
```

---

## 8. Git 提交规范

### 8.1 提交信息格式

```
<type>(<scope>): <subject>

[body]

[footer]
```

### 8.2 类型定义

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | `feat(core): add user authentication` |
| fix | Bug 修复 | `fix(data): handle null pointer exception` |
| docs | 文档更新 | `docs(readme): update installation guide` |
| style | 格式调整 | `style(core): fix indentation` |
| refactor | 重构 | `refactor(utils): simplify error handling` |
| test | 测试相关 | `test(core): add unit tests for user module` |
| chore | 构建/工具 | `chore(build): update dependencies` |

---

## 9. 检查清单

### 代码提交前检查

- [ ] 文件头部包含完整的追溯信息
- [ ] 命名符合规范
- [ ] 关键函数有文档注释
- [ ] 错误处理完善
- [ ] 日志使用正确的级别
- [ ] 无编译警告
- [ ] 通过静态分析检查
- [ ] 提交信息格式正确

---

## 10. 关联文档

- `ARCHITECTURE_DEFINITION.md` - 架构权威定义
- `rules_naming.md` - 命名规范（文件层面）
- `rules_scripts.md` - 脚本规范
- `../checklists/chk_dev.md` - 开发检查清单

