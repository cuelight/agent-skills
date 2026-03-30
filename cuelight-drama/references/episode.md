# 剧集管理

## 生成剧集大纲

```bash
# AI 规划全剧集（需要圣经、角色、场景就绪）
cuelight-cli episode generate <projectId>
```

## 创作剧本

```bash
# AI 续写剧本
cuelight-cli episode generate-script <episodeId> --action continue

# AI 润色剧本
cuelight-cli episode generate-script <episodeId> --action polish

# AI 扩展剧本
cuelight-cli episode generate-script <episodeId> --action expand
```

## 手动创建/编辑

```bash
# 创建剧集
cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "..." --season-id <seasonId>

# 从文件导入剧本内容
cuelight-cli episode create <projectId> --title "第一集" --content-file ./script.txt

# 更新剧集
cuelight-cli episode update <episodeId> --title "新标题" --content "..." --content-file ./script.txt
```

## 查看和管理

```bash
cuelight-cli episode list <projectId>
cuelight-cli episode get <episodeId>
cuelight-cli episode delete <episodeId>
```
