#!/bin/bash
#
# ArchPilot Core - 一键部署脚本
#
# 功能：基于 ArchPilot Core 框架快速创建新项目
# 用法：./deploy_project.sh <项目名称> [目标路径]
#
# 示例：
#   ./deploy_project.sh my_project              # 在当前目录创建
#   ./deploy_project.sh my_project /path/to    # 在指定路径创建
#
# Author: ArchPilot Core Framework
# Date: 2026-02-01
# Version: 1.0.0

set -e

# ============ 颜色定义 ============
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ============ 脚本信息 ============
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_ROOT="$(dirname "$SCRIPT_DIR")"
VERSION="1.0.0"

# ============ 日志函数 ============
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${CYAN}[STEP]${NC} $1"; }
log_done() { echo -e "${GREEN}[DONE]${NC} $1"; }

# ============ 帮助信息 ============
show_help() {
    cat << EOF
╔══════════════════════════════════════════════════════════════════╗
║          ArchPilot Core - 一键部署脚本 v${VERSION}                  ║
╚══════════════════════════════════════════════════════════════════╝

用法: $0 <项目名称> [目标路径] [选项]

参数:
    项目名称        新项目的名称（必需）
    目标路径        创建项目的目录（可选，默认当前目录）

选项:
    -h, --help      显示帮助信息
    -f, --full      完整模式（复制所有文件）
    -m, --minimal   最小模式（仅核心文件）
    -i, --init-git  初始化 Git 仓库
    --no-prompts    不复制 Prompts 目录
    --no-scripts    不复制 Scripts 目录

示例:
    $0 my_project                    # 在当前目录创建 my_project
    $0 my_project /path/to -f -i    # 完整模式 + Git 初始化
    $0 my_project . -m              # 最小模式

EOF
}

# ============ 默认配置 ============
PROJECT_NAME=""
TARGET_DIR="."
MODE="standard"  # standard, full, minimal
INIT_GIT=false
COPY_PROMPTS=true
COPY_SCRIPTS=true

# ============ 参数解析 ============
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -f|--full)
                MODE="full"
                shift
                ;;
            -m|--minimal)
                MODE="minimal"
                shift
                ;;
            -i|--init-git)
                INIT_GIT=true
                shift
                ;;
            --no-prompts)
                COPY_PROMPTS=false
                shift
                ;;
            --no-scripts)
                COPY_SCRIPTS=false
                shift
                ;;
            -*)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                if [[ -z "$PROJECT_NAME" ]]; then
                    PROJECT_NAME="$1"
                elif [[ "$TARGET_DIR" == "." ]]; then
                    TARGET_DIR="$1"
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$PROJECT_NAME" ]]; then
        log_error "缺少项目名称参数"
        show_help
        exit 1
    fi
}

# ============ 显示 Banner ============
show_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
    _             _     ____  _ _       _      ____
   / \   _ __ ___| |__ |  _ \(_) | ___ | |_   / ___|___  _ __ ___
  / _ \ | '__/ __| '_ \| |_) | | |/ _ \| __| | |   / _ \| '__/ _ \
 / ___ \| | | (__| | | |  __/| | | (_) | |_  | |__| (_) | | |  __/
/_/   \_\_|  \___|_| |_|_|   |_|_|\___/ \__|  \____\___/|_|  \___|

EOF
    echo -e "${NC}"
    echo -e "${BLUE}架构领航核心 - 一键部署脚本 v${VERSION}${NC}"
    echo ""
}

# ============ 创建目录结构 ============
create_directories() {
    log_step "创建项目目录结构..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    # 创建核心目录
    mkdir -p "$project_path"/{Governance/{rules,checklists,templates},Agents,Guides}

    # L1-L5 目录
    mkdir -p "$project_path"/{L1_Requirements,L2_Architecture,L3_DetailDesign}
    mkdir -p "$project_path"/L4_Implementation/src
    mkdir -p "$project_path"/L5_Verification/{unit,integration}

    # 其他目录
    mkdir -p "$project_path"/ReleaseNote

    if [[ "$MODE" != "minimal" ]]; then
        if [[ "$COPY_PROMPTS" == true ]]; then
            mkdir -p "$project_path"/Prompts
        fi
        if [[ "$COPY_SCRIPTS" == true ]]; then
            mkdir -p "$project_path"/Scripts
        fi
    fi

    log_done "目录结构创建完成"
}

# ============ 复制核心文件 ============
copy_core_files() {
    log_step "复制核心治理文件..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    # 核心定义文件
    cp "$CORE_ROOT/Governance/GOVERNANCE_OVERVIEW.md" "$project_path/Governance/"
    cp "$CORE_ROOT/Governance/ARCHITECTURE_DEFINITION.md" "$project_path/Governance/"
    cp "$CORE_ROOT/Governance/GLOSSARY.md" "$project_path/Governance/"
    cp "$CORE_ROOT/Governance/DOCUMENT_DEPENDENCY.mmd" "$project_path/Governance/"

    # 规则文件
    cp "$CORE_ROOT/Governance/rules/"*.md "$project_path/Governance/rules/"

    # 检查清单
    cp "$CORE_ROOT/Governance/checklists/"*.md "$project_path/Governance/checklists/"

    # 模板文件
    cp "$CORE_ROOT/Governance/templates/"*.md "$project_path/Governance/templates/"

    log_done "核心文件复制完成"
}

# ============ 复制 Agent 文件 ============
copy_agent_files() {
    log_step "复制 Agent 定义文件..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    cp "$CORE_ROOT/Agents/"*.md "$project_path/Agents/"

    log_done "Agent 文件复制完成"
}

# ============ 复制指南文件 ============
copy_guide_files() {
    log_step "复制 AI 指南文件..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    cp "$CORE_ROOT/Guides/"*.md "$project_path/Guides/"

    log_done "指南文件复制完成"
}

# ============ 复制 Prompts 文件 ============
copy_prompt_files() {
    if [[ "$COPY_PROMPTS" != true ]] || [[ "$MODE" == "minimal" ]]; then
        return
    fi

    log_step "复制 Prompts 文件..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    if [[ -d "$CORE_ROOT/Prompts" ]]; then
        cp "$CORE_ROOT/Prompts/"*.md "$project_path/Prompts/" 2>/dev/null || true
    fi

    log_done "Prompts 文件复制完成"
}

# ============ 复制脚本文件 ============
copy_script_files() {
    if [[ "$COPY_SCRIPTS" != true ]] || [[ "$MODE" == "minimal" ]]; then
        return
    fi

    log_step "复制脚本模板..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    cp "$CORE_ROOT/Scripts/"*.py "$project_path/Scripts/" 2>/dev/null || true
    cp "$CORE_ROOT/Scripts/README.md" "$project_path/Scripts/" 2>/dev/null || true

    log_done "脚本文件复制完成"
}

# ============ 生成项目 README ============
generate_readme() {
    log_step "生成项目 README..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"
    local today=$(date +%Y-%m-%d)

    cat > "$project_path/README.md" << EOF
# ${PROJECT_NAME}

**版本**: v0.1.0
**创建日期**: ${today}
**基于**: ArchPilot Core 框架

---

## 📋 项目概述

[项目描述]

---

## 🏗️ 目录结构

\`\`\`
${PROJECT_NAME}/
├── Governance/              # 治理规则
│   ├── rules/              # 规则文件
│   ├── checklists/         # 检查清单
│   └── templates/          # 文档模板
├── Agents/                  # AI Agent 配置
├── Guides/                  # AI 操作指南
├── L1_Requirements/         # L1 需求层
├── L2_Architecture/         # L2 架构层
├── L3_DetailDesign/         # L3 设计层
├── L4_Implementation/       # L4 实现层
├── L5_Verification/         # L5 验证层
├── ReleaseNote/            # 发布说明
└── VERSION                  # 版本文件
\`\`\`

---

## 🚀 快速开始

### 1. 创建第一个需求文档

\`\`\`bash
cp Governance/templates/requirement_template.md L1_Requirements/FR_core_001_[描述].md
\`\`\`

### 2. 配置 AI Agent

将 \`Agents/agent_dev_main.md\` 配置到你的 AI 开发环境。

### 3. 开始开发

使用 AI 辅助完成 L1 → L2 → L3 → L4 → L5 的开发流程。

---

## 📖 相关文档

- [治理总览](Governance/GOVERNANCE_OVERVIEW.md)
- [架构定义](Governance/ARCHITECTURE_DEFINITION.md)
- [AI 开发指南](Guides/AI_Development_Guide.md)

---

## 📝 变更记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v0.1.0 | ${today} | 初始版本，基于 ArchPilot Core 创建 |

EOF

    log_done "README 生成完成"
}

# ============ 生成 VERSION 文件 ============
generate_version() {
    log_step "生成 VERSION 文件..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    echo "v0.1.0" > "$project_path/VERSION"

    log_done "VERSION 文件生成完成"
}

# ============ 生成 .gitignore ============
generate_gitignore() {
    log_step "生成 .gitignore..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    cat > "$project_path/.gitignore" << 'EOF'
# Build outputs
build/
out/
dist/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
tmp/
temp/

# Test outputs
coverage/
.coverage
htmlcov/
EOF

    log_done ".gitignore 生成完成"
}

# ============ 初始化 Git ============
init_git_repo() {
    if [[ "$INIT_GIT" != true ]]; then
        return
    fi

    log_step "初始化 Git 仓库..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    cd "$project_path"
    git init -b main
    git add -A
    git commit -m "feat: initial project setup based on ArchPilot Core"
    cd - > /dev/null

    log_done "Git 仓库初始化完成"
}

# ============ 更新项目路径 ============
update_project_paths() {
    log_step "更新项目配置..."

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    # 更新 ARCHITECTURE_DEFINITION.md 中的项目名
    if [[ -f "$project_path/Governance/ARCHITECTURE_DEFINITION.md" ]]; then
        sed -i.bak "s/基于 ArchPilot Core 框架的所有项目/${PROJECT_NAME} 项目/g" \
            "$project_path/Governance/ARCHITECTURE_DEFINITION.md"
        rm -f "$project_path/Governance/ARCHITECTURE_DEFINITION.md.bak"
    fi

    log_done "项目配置更新完成"
}

# ============ 显示完成信息 ============
show_completion() {
    local project_path="$TARGET_DIR/$PROJECT_NAME"
    local full_path=$(cd "$project_path" && pwd)

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    🎉 项目创建成功！                              ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "项目名称: ${CYAN}${PROJECT_NAME}${NC}"
    echo -e "项目路径: ${CYAN}${full_path}${NC}"
    echo -e "部署模式: ${CYAN}${MODE}${NC}"
    echo ""
    echo -e "${YELLOW}下一步操作:${NC}"
    echo ""
    echo -e "  1. 进入项目目录:"
    echo -e "     ${BLUE}cd ${full_path}${NC}"
    echo ""
    echo -e "  2. 查看项目文档:"
    echo -e "     ${BLUE}cat README.md${NC}"
    echo ""
    echo -e "  3. 创建第一个需求文档:"
    echo -e "     ${BLUE}cp Governance/templates/requirement_template.md L1_Requirements/FR_core_001_xxx.md${NC}"
    echo ""
    echo -e "  4. 配置 AI Agent 并开始开发"
    echo ""

    if [[ "$INIT_GIT" == true ]]; then
        echo -e "${GREEN}Git 仓库已初始化，首次提交已完成。${NC}"
        echo ""
    fi
}

# ============ 主函数 ============
main() {
    show_banner
    parse_args "$@"

    local project_path="$TARGET_DIR/$PROJECT_NAME"

    # 检查目标是否已存在
    if [[ -d "$project_path" ]]; then
        log_error "目标目录已存在: $project_path"
        exit 1
    fi

    # 检查 Core 目录
    if [[ ! -d "$CORE_ROOT/Governance" ]]; then
        log_error "ArchPilot Core 目录结构不完整"
        exit 1
    fi

    echo -e "项目名称: ${CYAN}${PROJECT_NAME}${NC}"
    echo -e "目标路径: ${CYAN}${TARGET_DIR}${NC}"
    echo -e "部署模式: ${CYAN}${MODE}${NC}"
    echo ""

    # 执行部署步骤
    create_directories
    copy_core_files
    copy_agent_files
    copy_guide_files
    copy_prompt_files
    copy_script_files
    generate_readme
    generate_version
    generate_gitignore
    update_project_paths
    init_git_repo

    show_completion
}

# ============ 执行 ============
main "$@"
