# 视频生成与导出

## 推荐主路径

```bash
# 先读当前视频阶段状态
cuelight-cli director video-status <episodeId> --json

# 整集批量生成
cuelight-cli director batch-generate-videos <episodeId>

# 单镜补生成
cuelight-cli director generate-video <storyboardId> --episode-id <episodeId> --persist

# 等待任务完成
cuelight-cli director wait-task <taskId> --timeout 600

# 导出整集视频
cuelight-cli director export-videos <episodeId>
```

主路径原则：

- 公开工作流优先使用 `director video-status`、`director batch-generate-videos`、`director generate-video`、`director wait-task`、`director export-videos`
- 先确认 storyboard、角色/场景/道具绑定和参考素材已齐备，再提交视频任务
- `stylePrompt` 若项目级已存在，优先复用，不要额外拼一串纯英文风格词

## 底层 fallback / 排障

```bash
# 底层批量提交
cuelight-cli ai batch-submit-videos <episodeId>

# 底层单镜提交
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --persist

# 带风格和比例的底层批量提交
cuelight-cli ai batch-submit-videos <episodeId> --style-prompt "仿真人短剧质感，克制调色，室内保留 soft diffused light，画面强调门第压迫感。" --aspect-ratio "9:16"

# 完整制作（含风格注入）
cuelight-cli ai produce <episodeId> <storyboardId> --style-prompt "..." --aspect-ratio "9:16" --duration 5
```

定位：

- 仅用于底层补救、兼容旧链路或排障
- 不作为公开 `CLI + skill` 工作流的推荐标题和首屏示例

## 任务监控

```bash
# 查看项目所有 AI 任务
cuelight-cli ai tasks <projectId>

# 查看指定任务状态
cuelight-cli ai task-status <taskId1>,<taskId2>

# 等待任务完成
cuelight-cli ai wait <taskId> --timeout 600 --interval 5
```

说明：

- `ai task-status` / `ai wait` 主要用于任务监控和底层补救
- 不代表视频阶段的公开主工作流入口

## 底层导出与视频资产管理

```bash
# 底层导出整集合并视频
cuelight-cli video export <episodeId>

# 底层导出指定分镜
cuelight-cli video export <episodeId> --storyboard-ids "id1,id2"

# 视频资产管理
cuelight-cli video list <projectId>
cuelight-cli video get <videoId>
cuelight-cli video delete <videoId>
```
