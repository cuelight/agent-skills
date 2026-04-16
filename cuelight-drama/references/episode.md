# 剧集管理

## 外部 Agent 创作剧本（主路径）

```bash
# 创建剧集
cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "..." --season-id <seasonId>

# 从文件覆盖大纲（推荐）
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt

# 从文件覆盖剧本（推荐）
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt

# 更新剧集
cuelight-cli episode update <episodeId> --title "新标题" --content-file ./.cuelight/<projectId>/episodes/episode-1-script.txt
```

默认原则：

- 不论 `my_script` 还是 `adaptation`，正文优先由外部 agent 自己创作
- 外部 agent 先读当前项目、角色、场景、上一集状态，再自己写大纲和正文
- 不要默认把 `episode generate` / `generate-script` 当主路径

## 内置文本生成说明

- 剧集文本生成能力属于内部旧链路，不属于公开 `CLI + skill` 工作流
- 外部 agent 默认自己写 outline / script，再通过 `episode set-outline` / `episode set-script` 落库
- 不要把 `episode generate` / `generate-script` 当成常规兜底或默认备选

## 原稿模式（my_script）

推荐流程：

```bash
cuelight-cli source get-original <projectId> <documentId> --json
cuelight-cli episode create <projectId> --title "第一集" --number 1 --season-id <seasonId> --summary "..."
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt
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
cuelight-cli source draft get <draftId> --json
cuelight-cli episode create <projectId> --title "第一集" --number 1 --season-id <seasonId> --summary "..."
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt
```

要求：

- 先读 source 原文、`source draft get --json` 的结构化结果、project/season 状态
- 外部 agent 自己写大纲和正文
- 不默认调用系统内置 proposal/design/script 生成

说明：

- `scope` / `suggestions` 以 `source draft get --json` 的返回结构为准
- 不要把 `scope` 理解成一个单独的 CLI 命令

## 查看和管理

```bash
cuelight-cli episode status <episodeId> --json
cuelight-cli episode list <projectId>
cuelight-cli episode get <episodeId>
cuelight-cli episode delete <episodeId>
```
