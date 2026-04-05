# 剧集管理

## 外部 Agent 创作剧本（主路径）

```bash
# 创建剧集
cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "..." --season-id <seasonId>

# 从文件覆盖大纲（推荐）
cuelight-cli episode set-outline <episodeId> --file ./outline.txt

# 从文件覆盖剧本（推荐）
cuelight-cli episode set-script <episodeId> --file ./script.txt

# 更新剧集
cuelight-cli episode update <episodeId> --title "新标题" --content "..." --content-file ./script.txt
```

默认原则：

- 不论 `my_script` 还是 `adaptation`，正文优先由外部 agent 自己创作
- 外部 agent 先读当前项目、角色、场景、上一集状态，再自己写大纲和正文
- 不要默认把 `episode generate` / `generate-script` 当作主路径

## 内置文本生成（兜底 / 补救）

```bash
# AI 规划全剧集
cuelight-cli episode generate <projectId>

# AI 续写剧本
cuelight-cli episode generate-script <episodeId> --action continue

# AI 润色剧本
cuelight-cli episode generate-script <episodeId> --action polish

# AI 扩展剧本
cuelight-cli episode generate-script <episodeId> --action expand
```

这些命令保留，但在 `CLI + skill` 路线中的定位是：

- 外部 agent 明确失败时的兜底
- 用户明确要求用系统内置生成时的备选
- 对照、润色、局部补缺的辅助手段

不是默认主路径。

## 原稿模式（my_script）

推荐流程：

```bash
cuelight-cli source get-original <projectId> <documentId> --json
cuelight-cli episode create <projectId> --title "第一集" --number 1 --season-id <seasonId> --summary "..."
cuelight-cli episode set-outline <episodeId> --file ./outline.txt
cuelight-cli episode set-script <episodeId> --file ./script.txt
```

要求：

- 先读原稿全文
- 外部 agent 自己完成容量判断和分集策略
- 再自己写 outline / script

## 改编模式（adaptation）

推荐流程：

```bash
cuelight-cli project status <projectId> --json
cuelight-cli season status <projectId> <seasonId> --json
cuelight-cli episode create <projectId> --title "第一集" --number 1 --season-id <seasonId> --summary "..."
cuelight-cli episode set-outline <episodeId> --file ./outline.txt
cuelight-cli episode set-script <episodeId> --file ./script.txt
```

要求：

- 先读 source / draft / scope / season 状态
- 外部 agent 自己写大纲和正文
- 不默认调用系统内置 proposal/design/script 生成

## 查看和管理

```bash
cuelight-cli episode status <episodeId> --json
cuelight-cli episode list <projectId>
cuelight-cli episode get <episodeId>
cuelight-cli episode delete <episodeId>
```
