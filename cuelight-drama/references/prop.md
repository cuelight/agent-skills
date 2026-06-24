# Prop

```bash
cuelight-cli prop list <projectId> --json
cuelight-cli prop create <projectId> --name "道具名" --description-file ./.cuelight/<projectId>/props/item-desc.txt --base-prompt-file ./.cuelight/<projectId>/props/item-visual.txt --json
cuelight-cli prop update <projectId> <propId> --description-file ./.cuelight/<projectId>/props/item-desc.txt --base-prompt-file ./.cuelight/<projectId>/props/item-visual.txt --json
```

## 内容要求

道具 description 应包含：

- 类型与用途：它是什么，用来做什么。
- 叙事作用：身份凭证、威胁工具、记忆线索、误会证据等。
- 使用方式：谁会拿、藏、递、摔、打开或注视它。
- 可见特征：镜头中必须看清的识别点。

不要在 description 中写 `basePrompt：...` 或视觉提示词字段标签。

## BasePrompt

道具 `basePrompt` 写可复用视觉基准状态，应包含外观尺寸、材质、颜色、磨损、纹理、拍摄重点。

好的写法：

```text
一支旧式鎏金簪，簪头花丝纹样细密，金属表面有轻微磨痕，冷暖反光克制，hero shot 展示结构与材质。
```

## 分镜引用

对剧情推进有实质影响的道具，需要在相关分镜中同时满足：

- `videoPrompt` 文案使用 `<PropN>`。
- JSON 写入 `referencePropIds`。

背景陈设不要滥填为关键道具。
