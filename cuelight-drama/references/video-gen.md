# 视频生成与导出

## 批量生成视频（推荐）

```bash
# 整集批量生成
cuelight-cli ai batch-submit-videos <episodeId>

# 指定分镜子集
cuelight-cli ai batch-submit-videos <episodeId> --storyboard-ids "id1,id2,id3"

# 带风格和比例
cuelight-cli ai batch-submit-videos <episodeId> --style-prompt "cinematic, moody" --aspect-ratio "9:16"
```

## 单个分镜生成

```bash
# 测试单个分镜效果
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --persist

# 固定种子（可复现）
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --seed 42 --persist

# 完整制作（含风格注入）
cuelight-cli ai produce <episodeId> <storyboardId> --style-prompt "..." --aspect-ratio "9:16" --duration 5
```

## 任务监控

```bash
# 查看项目所有 AI 任务
cuelight-cli ai tasks <projectId>

# 查看指定任务状态
cuelight-cli ai task-status <taskId1>,<taskId2>

# 等待任务完成
cuelight-cli ai wait <taskId> --timeout 600 --interval 5
```

## 导出视频

```bash
# 导出整集合并视频
cuelight-cli video export <episodeId>

# 导出指定分镜
cuelight-cli video export <episodeId> --storyboard-ids "id1,id2"
```

## 视频资产管理

```bash
cuelight-cli video list <projectId>
cuelight-cli video get <videoId>
cuelight-cli video delete <videoId>
```
