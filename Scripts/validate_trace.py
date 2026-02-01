#!/usr/bin/env python3
"""
追溯关系验证脚本模板

功能：验证 L1-L5 追溯关系的完整性

Usage:
    python3 validate_trace.py --full-chain --output result.json
    python3 validate_trace.py --from L1 --to L5

Arguments:
    --full-chain    验证完整追溯链
    --from LAYER    起始层级
    --to LAYER      目标层级
    --output PATH   输出路径（默认 ./out/trace_validation.json）
    --help          显示帮助

Exit Codes:
    0 - 成功，追溯完整
    1 - 参数错误
    2 - 依赖错误
    3 - 追溯链不完整

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


# ============ 配置常量 ============

LAYER_DIRECTORIES = {
    "L1": "L1_Requirements",
    "L2": "L2_Architecture",
    "L3": "L3_DetailDesign",
    "L4": "L4_Implementation",
    "L5": "L5_Verification"
}

LAYER_ORDER = ["L1", "L2", "L3", "L4", "L5"]


# ============ 核心功能 ============

def extract_yaml_metadata(file_path: Path) -> dict:
    """从 Markdown 文件中提取 YAML 元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 简单的 YAML front matter 解析
        if content.startswith('---'):
            end_index = content.find('---', 3)
            if end_index != -1:
                yaml_content = content[3:end_index].strip()
                metadata = {}
                for line in yaml_content.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        # 简单处理列表
                        if value.startswith('[') and value.endswith(']'):
                            value = [v.strip() for v in value[1:-1].split(',') if v.strip()]
                        metadata[key] = value
                return metadata
    except Exception as e:
        pass
    return {}


def collect_layer_documents(project_root: str, layer: str) -> list:
    """收集指定层级的所有文档"""
    directory = Path(project_root) / LAYER_DIRECTORIES.get(layer, "")
    if not directory.exists():
        return []

    documents = []
    for file_path in directory.rglob("*.md"):
        if file_path.name not in ["README.md", "INDEX.md"]:
            metadata = extract_yaml_metadata(file_path)
            if metadata.get("id"):
                documents.append({
                    "id": metadata.get("id"),
                    "file": str(file_path.relative_to(project_root)),
                    "layer": layer,
                    "traces_from": metadata.get("traces_from", []),
                    "traces_to": metadata.get("traces_to", [])
                })

    return documents


def validate_trace_chain(project_root: str) -> dict:
    """验证完整追溯链"""
    all_documents = {}
    layer_docs = {}

    # 收集所有层级文档
    for layer in LAYER_ORDER:
        docs = collect_layer_documents(project_root, layer)
        layer_docs[layer] = docs
        for doc in docs:
            all_documents[doc["id"]] = doc

    # 分析追溯关系
    trace_issues = []
    trace_stats = {
        "total_documents": len(all_documents),
        "by_layer": {layer: len(docs) for layer, docs in layer_docs.items()},
        "complete_traces": 0,
        "broken_traces": 0,
        "missing_upstream": 0,
        "missing_downstream": 0
    }

    # 检查每个文档的追溯关系
    for doc_id, doc in all_documents.items():
        layer_index = LAYER_ORDER.index(doc["layer"])

        # 检查 traces_from（上游）
        if layer_index > 0:  # 非 L1 应该有上游
            traces_from = doc.get("traces_from", [])
            if isinstance(traces_from, str):
                traces_from = [traces_from] if traces_from else []

            if not traces_from:
                trace_stats["missing_upstream"] += 1
                trace_issues.append({
                    "document": doc_id,
                    "layer": doc["layer"],
                    "issue": "Missing traces_from",
                    "severity": "warning"
                })
            else:
                # 验证引用的文档是否存在
                for ref in traces_from:
                    if ref and ref not in all_documents:
                        trace_stats["broken_traces"] += 1
                        trace_issues.append({
                            "document": doc_id,
                            "layer": doc["layer"],
                            "issue": f"Referenced document not found: {ref}",
                            "severity": "error"
                        })

        # 检查 traces_to（下游）- L5 不需要
        if layer_index < len(LAYER_ORDER) - 1:
            traces_to = doc.get("traces_to", [])
            if isinstance(traces_to, str):
                traces_to = [traces_to] if traces_to else []

            # traces_to 为空是警告，不是错误
            if not traces_to:
                trace_stats["missing_downstream"] += 1

    # 计算完整追溯数
    trace_stats["complete_traces"] = (
        trace_stats["total_documents"] -
        trace_stats["broken_traces"] -
        trace_stats["missing_upstream"]
    )

    # 计算完整度
    if trace_stats["total_documents"] > 0:
        completeness = (trace_stats["complete_traces"] / trace_stats["total_documents"]) * 100
    else:
        completeness = 0

    # 确定状态
    status = "passed"
    if trace_stats["broken_traces"] > 0:
        status = "failed"
    elif trace_stats["missing_upstream"] > trace_stats["total_documents"] * 0.3:
        status = "warning"

    return {
        "status": status,
        "completeness": round(completeness, 2),
        "statistics": trace_stats,
        "issues": trace_issues
    }


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='验证 L1-L5 追溯关系完整性',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--full-chain', action='store_true',
                        help='验证完整追溯链')
    parser.add_argument('--from', dest='from_layer',
                        choices=['L1', 'L2', 'L3', 'L4', 'L5'],
                        help='起始层级')
    parser.add_argument('--to', dest='to_layer',
                        choices=['L1', 'L2', 'L3', 'L4', 'L5'],
                        help='目标层级')
    parser.add_argument('--output', default='./out/trace_validation.json',
                        help='输出路径')
    parser.add_argument('--project-root', default='.',
                        help='项目根目录')
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    if not args.full_chain and not (args.from_layer and args.to_layer):
        print("Error: Must specify --full-chain or both --from and --to",
              file=sys.stderr)
        return 1

    # 执行验证
    result = validate_trace_chain(args.project_root)

    # 构建输出
    output = {
        "script": "validate_trace",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": result["status"],
        "project_root": os.path.abspath(args.project_root),
        "validation_type": "full_chain" if args.full_chain else f"{args.from_layer}_to_{args.to_layer}",
        "completeness_percentage": result["completeness"],
        "statistics": result["statistics"],
        "issues": result["issues"],
        "summary": {
            "total_issues": len(result["issues"]),
            "errors": sum(1 for i in result["issues"] if i.get("severity") == "error"),
            "warnings": sum(1 for i in result["issues"] if i.get("severity") == "warning")
        }
    }

    # 输出结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Validation completed. Results written to: {output_path}")
    print(f"Status: {result['status']}")
    print(f"Completeness: {result['completeness']}%")

    if result["status"] == "failed":
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())

