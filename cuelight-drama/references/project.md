# 项目管理

## 手动创建

```bash
cuelight-cli project create --title "项目名称" --genre "短剧" --total-episodes 10 --duration 120
```

记录返回的 `projectId`，后续所有操作都需要它。

## 从小说/剧本导入

```bash
# 上传源文档
cuelight-cli source create-draft --title "小说名" --file ./novel.txt --goal scope_planning

# 查看分析建议后确认（suggestion-index 从返回结果中选取）
cuelight-cli source confirm-draft <draftId> --suggestion-index 0
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
cuelight-cli season add <projectId> --title "第二季" --planned-episodes 10

# 切换活动季
cuelight-cli season switch <projectId> <seasonId>

# 列出所有季
cuelight-cli season list <projectId>
```
