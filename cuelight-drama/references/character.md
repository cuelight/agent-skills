# 角色管理

## 创建角色

```bash
# AI 生成角色描述
cuelight-cli character generate <projectId> --name "林小雨" --description "18岁少女，黑色长发" --use-context

# 手动创建
cuelight-cli character create <projectId> --name "林小雨" --description "..." --base-prompt "..."
```

## 生成参考图/视频/语音

```bash
# 批量生成缺失参考图
cuelight-cli character batch-generate-images <projectId>

# 单个角色生成参考图
cuelight-cli character generate-image <projectId> <characterId>

# 批量生成参考视频（需先有参考图）
cuelight-cli character batch-generate-videos <projectId>

# 生成语音配置
cuelight-cli character generate-voice <projectId> <characterId>

# 等待任务完成
cuelight-cli ai tasks <projectId>
```

## 查看和管理

```bash
cuelight-cli character list <projectId>
cuelight-cli character get <projectId> <characterId>
cuelight-cli character update <projectId> <characterId> --name "新名" --ref-image "https://..."
cuelight-cli character delete <projectId> <characterId>
```
