# Scene

```bash
cuelight-cli scene list <projectId> --json
cuelight-cli scene create <projectId> --name "场景名" --description-file ./.cuelight/<projectId>/staging/import/scenes/place-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/scenes/place-visual.txt --json
cuelight-cli scene update <projectId> <sceneId> --description-file ./.cuelight/<projectId>/staging/import/scenes/place-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/scenes/place-visual.txt --json
```

## 内容要求

场景 description 应包含：

- 剧情用途：承载哪些冲突、关系或信息揭露。
- 复用范围：哪些集或哪些类型场面会反复使用。
- 调度重点：人物可进入、躲藏、对峙、观察的位置。

不要在 description 中写 `basePrompt：...` 或视觉提示词字段标签。

## BasePrompt

场景 `basePrompt` 是可复用取景地的视觉基准状态，应包含：

- 空间结构：入口、主行动区、遮挡物、前后景。
- 时代/行业感：建筑、家具、设备、材质。
- 光线：自然光、人工光、夜景、阴影方向。
- 可调度区域：人物可以站、坐、进入、躲藏、对峙的位置。
- 可复用视觉符号：门、屏风、讲台、病床、监控屏、窗等。
- 禁忌项：不该出现的时代元素或现代设备。

好的写法：

```text
侯府寿安堂的日间内景，厅堂纵深清晰，木质屏风与案几分区明确，暖色自然光从侧窗落入，wide shot 展示礼序空间与主次座位。
```

避免：

- 只写“古代大厅”“现代办公室”。
- 把单场剧情动作写进场景基准状态。
- 没有可调度空间，导致后续分镜只能写人物特写。
