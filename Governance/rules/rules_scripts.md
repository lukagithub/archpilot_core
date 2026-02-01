# 脚本执行规范

**文档版本**: v1.0.0  
**最后更新**: 2026-02-01  
**适用范围**: 项目中所有脚本（Python、Bash、Node.js 等）

> 本文档定义了脚本分类、调用方式、输出格式、错误处理规范，是 AI 与自动化平台的唯一权威脚本规范。

---

## 1. 脚本分类与职责

| 分类 | 代表脚本 | 层级 | 级别 | 输出 |
|------|----------|------|------|------|
| 版本管理 | `update_version.py`, `check_versions.py` | L1-L4 | ✅ MUST | 修改 VERSION、JSON 结果 |
| 质量评分 | `calculate_score.py`, `aggregate_scores.py` | L4-L5 | ✅ MUST | JSON: `{score, details}` |
| 文档检查 | `check_naming.py`, `release_checklist.py` | L1-L3 | ⚠️ SHOULD | Markdown/JSON 报告 |
| 追溯验证 | `validate_trace.py`, `extract_metadata.py` | 全层 | ⚠️ SHOULD | CSV/Markdown |
| 报告生成 | `generate_releasenote.py`, `generate_report.py` | 发布 | ✅ MUST | Markdown |

**级别说明**:
- ✅ **MUST**: 脚本缺失或失败即阻断流程
- ⚠️ **SHOULD**: 脚本缺失需记录警告，允许继续但需人工复核
- ⭕ **MAY**: 可选功能

---

## 2. 调用规范

### 2.1 通用约束

- ✅ 所有脚本必须支持 `--help` 并输出参数说明
- ✅ 默认在仓库根路径下运行
- ✅ 脚本必须显式声明依赖（如 requirements.txt）
- ❌ 禁止硬编码路径

### 2.2 参数规范

| 参数类型 | 规范 |
|----------|------|
| 版本参数 | 使用 `--version vX.Y.Z`，禁止混用 `-v` 简写 |
| 输出参数 | 使用 `--output <path>`；若未提供，默认写入 `./out/` |
| 配置参数 | 使用 `--config` 指定 YAML/JSON |
| 环境变量 | 统一使用 `PROJECT_` 前缀 |

### 2.3 调用示例

```bash
# 质量评分
python3 scripts/calculate_score.py \
  --version v1.2.0 \
  --input Governance/dev_trace.csv \
  --output build/reports/score_v1.2.0.json

# 命名检查
python3 scripts/check_naming.py \
  --layer L1 \
  --strict \
  --output build/reports/naming_check.md

# 追溯验证
python3 scripts/validate_trace.py \
  --file Governance/dev_trace.csv \
  --full-chain \
  --output build/reports/trace_validation.json
```

---

## 3. 输出格式

### 3.1 JSON 输出规范

```json
{
  "script": "calculate_score",
  "version": "v1.2.0",
  "timestamp": "2026-02-01T10:30:00Z",
  "status": "success",
  "result": {
    "score": 4.12,
    "details": {
      "D1": 4.5,
      "D2": 4.0,
      "D3": 3.8,
      "D4": 4.3,
      "D5": 4.1
    }
  }
}
```

**必需字段**:
- `script`: 脚本名称
- `timestamp`: ISO 8601 格式时间戳
- `status`: success/failure/warning

**错误输出**:
```json
{
  "script": "calculate_score",
  "timestamp": "2026-02-01T10:30:00Z",
  "status": "failure",
  "error_code": 3,
  "error_message": "D4 score below threshold",
  "hint": "Check L5 test coverage data"
}
```

### 3.2 Markdown 输出规范

- 标题使用 `#`/`##` 分级
- 列表使用 `-` 或 `1.`，禁止混用
- 结尾附带生成时间和脚本名称

```markdown
# 命名检查报告

**生成时间**: 2026-02-01T10:30:00Z  
**脚本**: check_naming.py

## 检查结果

- ✅ L1 命名检查通过
- ⚠️ L2 存在 2 个警告
- ❌ L3 存在 1 个错误

---
*由 check_naming.py 自动生成*
```

---

## 4. 错误处理

### 4.1 退出码规范

| 退出码 | 分类 | 场景 | 行动 |
|--------|------|------|------|
| 0 | 成功 | 正常执行结束 | - |
| 1 | 参数错误 | 缺少必需参数/格式非法 | 打印 `Usage:` 并退出 |
| 2 | 依赖错误 | 缺少命令、库或文件 | 提示缺失依赖 + 解决建议 |
| 3 | 业务校验失败 | 质量不达标、检查未通过 | 输出详细原因，阻断发布 |
| 4 | 外部系统错误 | Git/Docker 返回非零 | 重试或请求人工介入 |
| 10+ | 自定义错误 | 项目特定错误 | 在文档中登记含义 |

### 4.2 错误消息模板

```
[ERROR][脚本名称]
code=错误码
reason=错误原因
hint=解决建议
```

示例：
```
[ERROR][calculate_score]
code=3
reason=D4 score below threshold (2.8 < 3.0)
hint=Check L5 test coverage in L5_Verification/
```

---

## 5. 缺失脚本处理

| 级别 | 处理策略 |
|------|----------|
| ✅ MUST 缺失 | 立即阻断流程，输出 ❌ 报告，请求人工介入 |
| ⚠️ SHOULD 缺失 | 输出 ⚠️ 警告，记录到改进文档，允许继续但需人工复核 |
| ⭕ MAY 缺失 | 记录 ⭕ 提示即可 |

**AI 执行要求**：
- 检测到脚本不存在时，必须引用本节策略生成异常报告
- 不得尝试创建缺失的 MUST 级别脚本（需人工创建）

---

## 6. 脚本开发规范

### 6.1 文件头部

```python
#!/usr/bin/env python3
"""
脚本名称

功能描述

Usage:
    python3 script_name.py --version v1.0.0 --output result.json

Arguments:
    --version   版本号（必需）
    --output    输出路径（可选，默认 ./out/）
    --help      显示帮助

Exit Codes:
    0 - 成功
    1 - 参数错误
    2 - 依赖错误
    3 - 业务校验失败

Author: 作者名
Date: 2026-02-01
"""
```

### 6.2 标准结构（Python）

```python
import argparse
import json
import sys
from datetime import datetime

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='脚本描述')
    parser.add_argument('--version', required=True, help='版本号')
    parser.add_argument('--output', default='./out/result.json', help='输出路径')
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_args()
    
    result = {
        "script": "script_name",
        "version": args.version,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "success",
        "result": {}
    }
    
    # 业务逻辑
    
    # 输出结果
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
```

### 6.3 标准结构（Bash）

```bash
#!/bin/bash
set -e

# 脚本名称
# 功能描述

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "$0")"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

usage() {
    cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Options:
    --version VERSION   版本号（必需）
    --output PATH       输出路径（可选）
    --help              显示帮助

Exit Codes:
    0 - 成功
    1 - 参数错误
    2 - 依赖错误
    3 - 业务校验失败
EOF
}

main() {
    # 参数解析
    while [[ $# -gt 0 ]]; do
        case $1 in
            --version) VERSION="$2"; shift 2 ;;
            --output) OUTPUT="$2"; shift 2 ;;
            --help) usage; exit 0 ;;
            *) log_error "Unknown option: $1"; usage; exit 1 ;;
        esac
    done
    
    # 参数验证
    if [[ -z "$VERSION" ]]; then
        log_error "Missing required argument: --version"
        exit 1
    fi
    
    # 业务逻辑
    log_info "Processing version $VERSION..."
    
    log_info "Done."
}

main "$@"
```

---

## 7. 自测清单

- [ ] 通过静态检查工具（shellcheck、ruff、eslint 等）
- [ ] 提供 `--help` 输出
- [ ] 在 README 中记录使用示例
- [ ] 提供输入/输出样例
- [ ] 错误情况返回正确的退出码
- [ ] JSON 输出包含必需字段

---

## 8. 关联文档

- `rules_release.md` - 发布规则（脚本调用场景）
- `rules_coding.md` - 编码规范
- `../Guides/AI_Release_Automation_Guide.md` - AI 自动化指南

---

## 9. 变更控制

- 任何脚本规范的调整必须更新本文件
- 脚本新增/废弃需同步更新相关规则文档
- AI 执行时以本文件为准

