# ArchPilot Core 文档目录

本目录存放可视化文档和补充说明。

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `DEPLOYMENT_FLOW.mmd` | 项目部署流程可视化（Mermaid） |

---

## 查看 Mermaid 图表

### 方式一：VS Code 插件

安装 "Markdown Preview Mermaid Support" 插件，直接预览 `.mmd` 文件。

### 方式二：在线工具

将 `.mmd` 文件内容粘贴到 [Mermaid Live Editor](https://mermaid.live/)。

### 方式三：GitHub 渲染

GitHub 原生支持 Mermaid 渲染，直接查看文件即可。

---

## DEPLOYMENT_FLOW.mmd 说明

该图展示了从 ArchPilot Core 框架部署到具体项目的完整流程：

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  ArchPilot Core │ --> │  部署脚本       │ --> │  新项目         │
│  （源框架）      │     │  deploy_project │     │  （my_project） │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       ▼                       │
        │               ┌───────────────┐               │
        │               │ 部署模式选择   │               │
        │               │ 标准/完整/最小 │               │
        │               └───────────────┘               │
        │                                               │
        └───────────────────────────────────────────────┘
                              复制
```

详细流程请查看 [DEPLOYMENT_FLOW.mmd](DEPLOYMENT_FLOW.mmd)。

