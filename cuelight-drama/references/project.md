# 项目管理

## 手动创建

```bash
cuelight-cli project create --title "项目名称" --genre "短剧" --total-episodes <episodes> --duration <seconds>
```

记录返回的 `projectId`，后续所有操作都需要它。

说明：

- 这个入口适合没有 source draft 的纯手动建项目
- `CLI + skill` 路线下，文字内容仍默认由外部 agent 自己创作
- 若项目是 `my_script`，这里的 `totalEpisodes` / `duration` 也应先由外部 agent 基于原稿容量判断得出，不要默认填 `10 集`

## 先检查项目状态

```bash
# 推荐外部 agent 先查聚合状态
cuelight-cli project status <projectId> --json

# 查看项目详情
cuelight-cli project get <projectId> --json
```

## 从小说/剧本导入

```bash
# 上传源文档
cuelight-cli source draft create-from-file --title "小说名" --file ./novel.txt --goal scope_planning

# 查看 draft 详情
cuelight-cli source draft get <draftId> --json

# 查看分析建议后确认（suggestion-index 从返回结果中选取）
cuelight-cli source draft confirm <draftId> --suggestion-index 0

# 用已确认 draft 物化项目
cuelight-cli project create --title "项目名称" --source-draft-id <draftId> --json
```

### 原稿模式（my_script）

原稿模式下，外部 agent 的主路径是：

1. 用 CLI 读取原稿与项目状态
2. 自己判断剧情容量、推荐集数和单集时长
3. 自己写 proposal / design / worldView / 角色 / 场景 / outline / script
4. 再通过 CLI 落库

关键原则：

- 不依赖服务端容量推荐作为前提
- 不默认写成 `10 集`
- 不把固定短剧档位当作 `my_script` 的前提

推荐命令链：

```bash
cuelight-cli source draft get <draftId> --json
cuelight-cli project create --title "项目名称" --source-draft-id <draftId> --json
cuelight-cli project get <projectId> --json
cuelight-cli source list <projectId> --json
cuelight-cli source get-original <projectId> <documentId> --json
cuelight-cli project update <projectId> --total-episodes <n> --duration <sec>
cuelight-cli season update <projectId> <seasonId> --planned-episodes <n>
cuelight-cli season update <projectId> <seasonId> --proposal "..." --design "..."
```

### 改编模式（adaptation）

改编模式下，外部 agent 也默认是主创作者：

- 先读 source / draft / scope / current season
- 自己写 proposal / design / worldView / 角色 / 场景 / 分集 / 正文
- 不默认调用系统内置 proposal/design/script 生成

推荐命令链：

```bash
cuelight-cli project status <projectId> --json
cuelight-cli season status <projectId> <seasonId> --json
cuelight-cli source list <projectId> --json
cuelight-cli season update <projectId> <seasonId> --proposal "..." --design "..."
```

## 项目管理

```bash
# 列表
cuelight-cli project list

# 查看详情
cuelight-cli project get <projectId>

# 更新
cuelight-cli project update <projectId> --title "新名称" --genre "悬疑"

# 删除（⚠️ 不可恢复）
cuelight-cli project delete <projectId>
```

## Season 管理

```bash
# 添加新季
cuelight-cli season add <projectId> --title "第二季" --planned-episodes <n>

# 切换活动季
cuelight-cli season switch <projectId> <seasonId>

# 列出所有季
cuelight-cli season list <projectId>

# 查看某季聚合状态
cuelight-cli season status <projectId> <seasonId> --json

# 更新当前季的 proposal / design / 集数规划
cuelight-cli season update <projectId> <seasonId> --planned-episodes <n> --proposal "..." --design "..."
```
