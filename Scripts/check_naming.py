#!/usr/bin/env python3
"""
命名规范检查脚本模板

功能：检查项目文件命名是否符合 rules_naming.md 定义的规范

Usage:
    python3 check_naming.py --layer L1 --output result.json
    python3 check_naming.py --all-layers --strict

Arguments:
    --layer LAYER   指定检查层级（L1/L2/L3/L4/L5）
    --all-layers    检查所有层级
    --strict        严格模式，警告也视为错误
    --output PATH   输出路径（默认 ./out/naming_check.json）
    --help          显示帮助

Exit Codes:
    0 - 成功，无错误
    1 - 参数错误
    2 - 依赖错误（目录不存在等）
    3 - 检查失败（发现命名问题）

Author: ArchPilot Core Framework
Date: 2026-02-01
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ============ 配置常量（根据项目调整） ============

# 层级目录配置
LAYER_CONFIG = {
    "L1": {
        "directory": "L1_Requirements",
        "prefix_pattern": r"^FR_[a-z]+_\d{3}_[a-z_]+\.md$",
        "description": "需求文档"
    },
    "L2": {
        "directory": "L2_Architecture",
        "prefix_pattern": r"^SA_[a-z]+_\d{3}_[a-z_]+\.md$",
        "description": "架构文档"
    },
    "L3": {
        "directory": "L3_DetailDesign",
        "prefix_pattern": r"^DD_[a-z]+_\d{3}_[a-z_]+\.md$",
        "description": "设计文档"
    },
    "L4": {
        "directory": "L4_Implementation",
        "prefix_pattern": r"^[a-z]+_\d{3}_[a-z_]+\.(cpp|h|py|js|ts)$",
        "description": "实现代码"
    },
    "L5": {
        "directory": "L5_Verification",
        "prefix_pattern": r"^TC_[a-z]+_\d{3}_[a-z]+_[a-z_]+\.md$",
        "description": "测试用例"
    }
}


# ============ 核心功能 ============

def check_layer_naming(layer: str, project_root: str, strict: bool = False) -> dict:
    """检查指定层级的命名规范"""
    config = LAYER_CONFIG.get(layer)
    if not config:
        return {"error": f"Unknown layer: {layer}"}

    directory = Path(project_root) / config["directory"]
    if not directory.exists():
        return {
            "layer": layer,
            "directory": str(directory),
            "status": "skipped",
            "reason": "Directory not found",
            "files_checked": 0,
            "errors": [],
            "warnings": []
        }

    pattern = re.compile(config["prefix_pattern"])
    errors = []
    warnings = []
    files_checked = 0

    for file_path in directory.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            files_checked += 1
            filename = file_path.name

            # 跳过特殊文件
            if filename in ["README.md", "INDEX.md", ".gitkeep"]:
                continue

            # 检查命名规范
            if not pattern.match(filename):
                if filename.endswith(".md") or filename.endswith((".cpp", ".h", ".py", ".js", ".ts")):
                    errors.append({
                        "file": str(file_path.relative_to(project_root)),
                        "issue": "Naming pattern mismatch",
                        "expected_pattern": config["prefix_pattern"]
                    })

    status = "passed"
    if errors:
        status = "failed"
    elif warnings and strict:
        status = "failed"
    elif warnings:
        status = "warning"

    return {
        "layer": layer,
        "directory": str(directory),
        "status": status,
        "files_checked": files_checked,
        "errors": errors,
        "warnings": warnings
    }


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='检查项目文件命名是否符合规范',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 check_naming.py --layer L1
    python3 check_naming.py --all-layers --strict
    python3 check_naming.py --layer L1 --output result.json
        """
    )
    parser.add_argument('--layer', choices=['L1', 'L2', 'L3', 'L4', 'L5'],
                        help='指定检查层级')
    parser.add_argument('--all-layers', action='store_true',
                        help='检查所有层级')
    parser.add_argument('--strict', action='store_true',
                        help='严格模式')
    parser.add_argument('--output', default='./out/naming_check.json',
                        help='输出路径')
    parser.add_argument('--project-root', default='.',
                        help='项目根目录')
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 参数验证
    if not args.layer and not args.all_layers:
        print("Error: Must specify --layer or --all-layers", file=sys.stderr)
        return 1

    # 确定要检查的层级
    layers_to_check = []
    if args.all_layers:
        layers_to_check = list(LAYER_CONFIG.keys())
    else:
        layers_to_check = [args.layer]

    # 执行检查
    results = []
    overall_status = "passed"

    for layer in layers_to_check:
        result = check_layer_naming(layer, args.project_root, args.strict)
        results.append(result)
        if result.get("status") == "failed":
            overall_status = "failed"
        elif result.get("status") == "warning" and overall_status != "failed":
            overall_status = "warning"

    # 构建输出
    output = {
        "script": "check_naming",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": overall_status,
        "strict_mode": args.strict,
        "layers_checked": layers_to_check,
        "results": results,
        "summary": {
            "total_layers": len(layers_to_check),
            "passed": sum(1 for r in results if r.get("status") == "passed"),
            "failed": sum(1 for r in results if r.get("status") == "failed"),
            "warnings": sum(1 for r in results if r.get("status") == "warning"),
            "skipped": sum(1 for r in results if r.get("status") == "skipped")
        }
    }

    # 输出结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Check completed. Results written to: {output_path}")
    print(f"Status: {overall_status}")

    # 返回退出码
    if overall_status == "failed":
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())

