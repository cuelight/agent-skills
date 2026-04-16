# 道具管理

## 创建与编辑

```bash
# 手动创建
cuelight-cli prop create <projectId> \
  --name "鎏金簪" \
  --description "赵家嫡女常佩的旧式发簪，是身份与婚事冲突的重要线索物。" \
  --base-prompt "旧式鎏金簪，簪头花丝纹样细密，金属边缘有轻微磨痕，hero shot 展示结构与材质，背景简洁，中文主叙述保留必要英文术语。"

# 更新
cuelight-cli prop update <projectId> <propId> \
  --description "..." \
  --base-prompt "..."
```

写法规则：

- `basePrompt` 使用中文自然句，保留必要英文术语，如 `hero shot`、`product close-up`
- 聚焦单个核心道具的轮廓、结构、材质、纹理和使用痕迹
- 不写角色持握动作，不把道具图写成场景空镜或人物展示图

## 生成参考图

```bash
# 批量生成缺失参考图
cuelight-cli prop batch-generate-images <projectId>

# 单个道具生成参考图
cuelight-cli prop generate-image <projectId> <propId>

# 上传自定义道具图
cuelight-cli prop upload-image <projectId> <propId> --file ./.cuelight/<projectId>/props/<propId>.png
```

## 在 Storyboard 中引用

关键道具对当前镜头有实质影响时，需要同时满足两层引用：

1. 文案层：`videoPrompt` 中使用 `<PropN>`
2. 结构层：写入 `referencePropIds`

示例：

- 下面这个例子是**短时单镜头道具特写**，适用于 `Seedance 5-6s` 的单落点镜头，或作为 Wanx `10s` 导演稿中的某个子分镜片段。
- 不要把它当成 Wanx 默认 storyboard item 模板；若当前目标是 Wanx，优先把道具特写嵌入 `4s + 6s` 或 `3s + 3s + 4s` 的导演稿镜头组。

```json
{
  "sceneNumber": 4,
  "shotSize": "close",
  "videoPrompt": "生成一个由以下 1 个分镜组成的视频。\n本片段场景设定在：<Character2>(赵府荷花池)。\n分镜1 5s：镜头推近到 close-up，<Character1>(赵阿萤) 指腹轻轻刮过 <Prop1>(玉佩) 的裂纹，呼吸声被压得很轻。",
  "referenceCharacterIds": ["char-1"],
  "referenceSceneId": "scene-1",
  "referencePropIds": ["prop-1"]
}
```
