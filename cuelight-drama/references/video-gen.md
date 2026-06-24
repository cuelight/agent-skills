# Video

默认不提交视频任务。用户明确要求生成视频时才执行：

```bash
cuelight-cli video models --json
cuelight-cli storyboard get <storyboardId> --json
cuelight-cli video generate --model <model> --prompt "<prompt>" --duration 8 --json
cuelight-cli task wait <taskId> --json
```

项目内视频状态查询：

```bash
cuelight-cli video list <projectId> --json
cuelight-cli video get <videoId> --json
cuelight-cli task get <taskId> --json
```

## 生成前检查

生成前必须确认：

- storyboards 已落库。
- 每条目标分镜有 `videoPrompt`。
- 每条目标分镜有 `referenceCharacterIds` 和 `referenceSceneId`。
- 关键道具有 `referencePropIds`。
- 用户明确要求提交视频任务。
- 已查询 `video models`，模型和时长符合能力范围。

## Prompt 要求

- 保持 `videoPrompt` 的中文主叙述。
- 保留 `<CharacterN>`、`<PropN>` 标签，不把绑定信息改成裸中文名。
- 不把多个相距很远的剧情段落压进一个短视频任务。
- 时长必须与分镜文本的子分镜秒数相符。

## 禁止

- 验收文字落库时顺手提交视频任务。
- 在未绑定项目工作区里提交项目相关视频任务。
- 用未查询过的模型名硬编码生成。
