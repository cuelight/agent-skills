# 场景管理

## 创建场景

```bash
# AI 生成场景描述
cuelight-cli scene generate <projectId> --name "霓虹街道" --description "赛博朋克风格的夜间街道" --use-context

# 手动创建
cuelight-cli scene create <projectId> --name "霓虹街道" --description "..." --base-prompt "..." --ref-image "https://..."
```

## 生成参考图

```bash
# 批量生成缺失参考图
cuelight-cli scene batch-generate-images <projectId>

# 单个场景生成参考图
cuelight-cli scene generate-image <projectId> <sceneId>

# 等待任务完成
cuelight-cli ai tasks <projectId>
```

## 查看和管理

```bash
cuelight-cli scene list <projectId>
cuelight-cli scene get <projectId> <sceneId>
cuelight-cli scene update <projectId> <sceneId> --name "新名" --ref-image "https://..."
cuelight-cli scene delete <projectId> <sceneId>
```
