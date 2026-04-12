# Director 命令 JSON 输出规范

这份文档约束 `cuelight-cli director ... --json` 的稳定输出字段，供外部 agent 直接消费。

适用原则：

- 只把 `--json` 模式视为稳定契约
- human 输出只给人看，不保证字段、顺序和格式稳定
- 未列出的字段视为附加信息，可以读取，但不要作为强依赖
- 若某个值当前不可得，返回 `null`、`false`、空数组或 `0`，而不是让外部 agent 猜测

## 命令总览

```bash
cuelight-cli director status <projectId> --json
cuelight-cli director visual-status <projectId> --json
cuelight-cli director storyboard-status <episodeId> --json
cuelight-cli director video-status <episodeId> --json
cuelight-cli director configure-visuals <projectId> ... --json
cuelight-cli director set-style-prompt <projectId> --file ./style.txt --json
cuelight-cli director generate-style-image <projectId> --json
cuelight-cli director import-storyboards <episodeId> --file ./storyboards.json --json
cuelight-cli director generate-storyboards <episodeId> --wait --json
cuelight-cli director update-storyboard <storyboardId> ... --json
cuelight-cli director generate-video <storyboardId> --episode-id <episodeId> --json
cuelight-cli director batch-generate-videos <episodeId> --json
cuelight-cli director wait-task <taskId> --json
cuelight-cli director export-videos <episodeId> --json
```

## 1. `director status`

用途：

- 读取项目级导演聚合状态
- 让外部 agent 先判断当前卡在哪个阶段

稳定字段：

```json
{
  "projectId": "project-1",
  "title": "Demo",
  "activeSeasonId": "season-1",
  "visual": {
    "projectId": "project-1",
    "stylePromptReady": true,
    "styleReferenceImageReady": false,
    "visualMode": "improv",
    "shootingMode": "omni_reference",
    "videoAspectRatio": "9:16",
    "characterCount": 2,
    "sceneCount": 3,
    "propCount": 1,
    "characterImagesReady": 1,
    "sceneImagesReady": 2,
    "nextActions": ["generate_style_image"]
  },
  "assetPrep": {
    "characterCount": 2,
    "characterImagesReady": 1,
    "sceneCount": 3,
    "sceneImagesReady": 2,
    "propCount": 1
  },
  "storyboard": {
    "episodeCount": 5,
    "episodesWithSummary": 5,
    "episodesWithScript": 3,
    "storyboardCount": 18
  },
  "video": {
    "storyboardVideos": 6,
    "videoAssetCount": 4
  },
  "nextActions": [
    "generate_style_image",
    "set_episode_scripts",
    "generate_storyboards",
    "generate_storyboard_videos"
  ]
}
```

字段说明：

- `visual`：视觉阶段状态，结构与 `director visual-status` 相同
- `assetPrep`：素材准备聚合信息
- `storyboard`：剧本/分镜总量信息
- `video`：视频产物聚合信息
- `nextActions`：推荐的下一步动作列表，外部 agent 可直接据此排序决策

## 2. `director visual-status`

用途：

- 单独判断视觉设定是否齐备
- 对应内部 skill 的“视觉设定”阶段

稳定字段：

```json
{
  "projectId": "project-1",
  "stylePromptReady": true,
  "styleReferenceImageReady": false,
  "visualMode": "improv",
  "shootingMode": "omni_reference",
  "videoAspectRatio": "9:16",
  "characterCount": 2,
  "sceneCount": 3,
  "propCount": 1,
  "characterImagesReady": 1,
  "sceneImagesReady": 2,
  "nextActions": ["generate_style_image"]
}
```

判断建议：

- `stylePromptReady=false`：先写 `stylePrompt`
- `visualMode=null` 或 `shootingMode=null`：先执行 `director configure-visuals`
- `styleReferenceImageReady=false`：可执行 `director generate-style-image`

## 3. `director storyboard-status`

用途：

- 判断某一集是否已经具备分镜生成/修复/出视频条件

稳定字段：

```json
{
  "episodeId": "episode-1",
  "scriptReady": true,
  "storyboardCount": 6,
  "storyboardsWithCharacters": 5,
  "storyboardsWithScene": 6,
  "storyboardsWithPrompt": 6,
  "needsBindingRepair": true,
  "needsStoryboards": false,
  "nextActions": ["repair_storyboard_bindings"]
}
```

判断建议：

- `scriptReady=false`：先写剧本，不要急着拆镜
- `needsStoryboards=true`：先 `director generate-storyboards` 或 `director import-storyboards`
- `needsBindingRepair=true`：不要直接生成视频
- `storyboardsWithPrompt < storyboardCount`：说明有分镜缺正文提示词

## 4. `director video-status`

用途：

- 判断某一集的视频生成缺口

稳定字段：

```json
{
  "episodeId": "episode-1",
  "storyboardCount": 6,
  "storyboardVideos": 2,
  "needsVideoGeneration": true,
  "readyStoryboardIds": ["sb-1", "sb-2"],
  "pendingStoryboardIds": ["sb-3", "sb-4", "sb-5", "sb-6"],
  "nextActions": ["generate_storyboard_videos"]
}
```

判断建议：

- `needsVideoGeneration=true`：说明仍有分镜未生成视频
- `pendingStoryboardIds`：外部 agent 可据此决定单镜补生成还是整集批量生成

## 5. `director configure-visuals`

用途：

- 写入导演阶段常用视觉配置

输入约束：

- `--visual-mode` 仅允许 `improv|library|null`
- `--shooting-mode` 仅允许 `nine_grid_storyboard|omni_reference`
- `--video-ratio` 仅允许 `9:16|16:9|1:1`
- 至少提供一个可写字段

输出契约：

- 成功时返回与 `director visual-status` 相同结构
- 外部 agent 可以把这条命令的输出当作“写入后的最新视觉状态”

## 6. `director set-style-prompt`

用途：

- 从本地文件覆盖写入 `stylePrompt`

输入约束：

- `--file` 必填
- 文件必须存在
- 文件内容必须为非空文本

输出契约：

- 成功时返回与 `director visual-status` 相同结构

## 7. `director generate-style-image`

用途：

- 提交全局风格图生成任务

稳定字段：

```json
{
  "projectId": "project-1",
  "taskId": "task-1",
  "status": "submitted",
  "nextActions": ["director wait-task task-1"]
}
```

说明：

- 命令还可能附带服务端返回的额外字段
- `taskId` 是外部 agent 后续轮询的主字段

## 8. `director import-storyboards`

用途：

- 从本地 JSON 文件批量导入文字分镜

输入约束：

- `--file` 必填
- 文件必须存在且可解析为 JSON
- JSON 必须是数组，或形如 `{ "items": [...] }`
- 每个 item 至少包含以下任一字段：
  - `sceneNumber`
  - `videoPrompt`
  - `shotSize`
  - `dialogues`
  - `soundEffects`

稳定字段：

```json
{
  "episodeId": "episode-1",
  "importedCount": 6,
  "result": [...]
}
```

说明：

- `result` 为服务端原始导入返回
- 外部 agent 应主要读取 `episodeId` 和 `importedCount`

## 9. `director generate-storyboards`

用途：

- 调用现有分镜生成链路
- 支持等待、自动补齐和绑定修复

输入参数：

- `--wait`
- `--auto-supplement`
- `--repair-bindings`
- `--timeout`
- `--interval`
- `--max-rounds`

稳定字段：

```json
{
  "episodeId": "episode-1",
  "storyboardCount": 6,
  "needsSupplement": false,
  "repairedStoryboardIds": ["sb-2"],
  "submitted": {
    "taskId": "task-1"
  },
  "task": {
    "id": "task-1",
    "status": "completed"
  },
  "supplementRounds": []
}
```

字段说明：

- `storyboardCount`：命令结束后当前集实际拥有的分镜数
- `needsSupplement`：即使流程跑完后仍有补充需求
- `repairedStoryboardIds`：自动修复过绑定的分镜 id 列表
- `submitted` / `task` / `supplementRounds`：沿用既有生成链路返回

## 10. `director update-storyboard`

用途：

- 精确更新单个分镜

输入约束：

- 至少提供一个可更新字段
- `--ref-character-ids` 若传入，必须至少解析出一个非空 id
- `--ref-scene-id` 若传入，不能为空字符串
- `--dialogues`、`--sound-effects` 若传入，必须是合法 JSON
- 若 `videoPrompt` 里写了 `本片段场景设定在：实训教室。` 这类裸场景名，而没有同时提供 `referenceSceneId`，服务端会返回校验错误
- 若同时提供了 `referenceSceneId`，服务端会把 scene header 自动归一化成 canonical scene tag
- 该 scene tag 编号取决于**当前分镜自身的绑定资源顺序**：先是 `referenceCharacterIds`，再是场景；外部 agent 不需要也不应该自己猜 `<CharacterN>`

输出契约：

- 返回服务端更新后的分镜对象
- 该对象字段较多，不要求外部 agent 全量依赖；建议只按自己写入的字段做结果确认

## 11. `director generate-video`

用途：

- 提交单个分镜视频生成

输入约束：

- `--episode-id` 必填

稳定字段：

```json
{
  "storyboardId": "sb-1",
  "episodeId": "episode-1",
  "taskId": "task-1"
}
```

说明：

- 命令还会附带服务端原始返回的额外字段
- 外部 agent 后续应使用 `taskId` 轮询，而不是猜测生成是否已完成

## 12. `director batch-generate-videos`

用途：

- 提交整集或子集分镜的视频批量生成

输入约束：

- `--storyboard-ids` 若传入，必须至少解析出一个非空 id

输出契约：

- 直接透传服务端批量任务返回
- 外部 agent 应优先读取其中的 `taskId` / `id` / `status`

## 13. `director wait-task`

用途：

- 等待任意 AI 任务完成

输入约束：

- `--timeout`：秒，默认 `300`
- `--interval`：秒，默认 `3`

输出契约：

- 成功时返回任务对象
- 失败时 CLI 抛出错误并退出非零状态

外部 agent 使用建议：

- 把 `wait-task` 视为同步屏障
- 若任务失败，直接读取 stderr/json error，不要再猜中间状态

## 14. `director export-videos`

用途：

- 导出整集或指定分镜的视频

输入约束：

- `--storyboard-ids` 若传入，必须至少解析出一个非空 id

输出契约：

- 直接透传服务端导出任务返回
- 外部 agent 应优先读取 `taskId` / `id` / `status`

## 错误输出

当使用 `--json` 时，CLI 错误统一输出到 stderr：

```json
{
  "error": {
    "type": "validation",
    "message": "--episode-id is required"
  }
}
```

稳定字段：

- `error.type`
- `error.message`
- `error.hint`
- `error.code`

常见 `error.type`：

- `validation`
- `not_found`
- `network`
- `auth`
- `timeout`
- `unknown`

外部 agent 规则：

- 先看进程退出码
- 非零时读取 stderr 的 `error.type` 和 `error.message`
- 不要从 stdout 猜测失败原因

## 推荐消费方式

推荐外部 agent 按这个顺序调用：

1. `director status` 或更细粒度的 `visual-status / storyboard-status / video-status`
2. 根据 `nextActions` 决定下一条命令
3. 写入类命令成功后，直接读取它们返回的最新状态，不要额外猜
4. 任务型命令拿到 `taskId` 后，用 `director wait-task`
5. 若需要更细粒度资源字段，再回退到 `bible / storyboard / ai / video` 底层命令
