# 分镜管理

## 默认原则

- `cuelight-drama` 自带基础 storyboard 模板，默认先按这里的 JSON 契约写
- `seedance-storyboard` 只是可选增强，用来提升 `videoPrompt` 的镜头语言和导演感，不改变 CueLight 的字段结构
- `videoPrompt` 使用中文自然句，保留必要英文术语和标签，如 `medium shot`、`close-up`、`<CharacterN>`、`<PropN>`

## 基础 JSON 模板

```json
[
  {
    "sceneNumber": 1,
    "shotSize": "medium",
    "videoPrompt": "生成一个由以下 2 个分镜组成的视频。\n本片段场景设定在：<Character2>(赵府荷花池)。\n分镜1 4s：medium shot 先压住池边空气，<Character1>(赵阿萤) 抬手按住 <Prop1>(玉佩)，呼吸被压得很轻。\n分镜2 6s：镜头推近到 close-up，<Character1>(赵阿萤) 目光缓慢转向门口，远处传来木门轻响。",
    "referenceCharacterIds": ["char-1"],
    "referenceSceneId": "scene-1",
    "referencePropIds": ["prop-1"],
    "dialogues": [
      { "character": "赵阿萤", "line": "还不到认输的时候。" }
    ],
    "soundEffects": ["木门轻响", "钟表滴答"]
  }
]
```

字段约束：

- 必填：`sceneNumber`、`shotSize`、`videoPrompt`、`referenceCharacterIds`、`referenceSceneId`
- 可选：`referencePropIds`、`dialogues`、`soundEffects`
- `dialogues` 固定为 `{ character, line }[]`
- `soundEffects` 固定为 `string[]`
- 一条 shot 对应一个 object，`sceneNumber` 按导入顺序递增

## 导演稿模式

### 基础稿 vs 导演稿

- **基础稿**：格式合法、绑定正确、可直接落库
- **导演稿**：单个 storyboard item 内拆成 **2-3 个子分镜**

默认从基础稿升格为导演稿的时机：

- 进入导演工作台精修
- 用户要求“更像导演页”“重写分镜脚本”“增强导演感”
- 单条 `videoPrompt` 已经塞入多个叙事信息点
- 同一镜头组内同时包含环境建立、动作推进、情绪或对白落点

允许保持单分镜的例外：

- 空镜
- 单一动作展示
- 单一情绪特写
- 明确只需要一个视觉落点的短镜头

### 模型时长规则

- **Wanx 系列**：导演稿默认 **固定 10s**
- **Seedance 系列**：导演稿默认 **5-15s**，根据分镜组情节决定

Wanx 的默认节奏：

- 主路径：`4s + 6s`
- 三拍：`3s + 3s + 4s`

Seedance 的默认节奏：

- `5-6s`：单动作、单情绪、单落点
- `7-10s`：2 段或 3 段节拍
- `11-15s`：完整小弧线，但仍控制切镜数量

### 固定写法

每个导演稿 item 必须写成：

- `生成一个由以下 N 个分镜组成的视频。`
- `本片段场景设定在：<CharacterN>(场景名)。`
- `分镜1 Xs：...`
- `分镜2 Ys：...`
- 可选 `分镜3 Zs：...`

固定约束：

- 子分镜默认 **2 个**，只有确实需要“建立 / 推进 / 落点”三拍时才写 **3 个**
- 每条子分镜的信息顺序固定为：
  - 环境/空间锚点
  - 景别/运镜
  - 角色动作或关系变化
  - 对白或音效落点
- 不要混用 `分镜1 4s：...` 和 `0-4秒：...`
- 不要出现连续空行
- scene header 只出现一次；正文不再重复刷 scene tag

## 升格示例

### Wanx 10s：基础稿 -> 导演稿（`4s + 6s`）

基础稿：

```text
生成一个由以下 1 个分镜组成的视频。
本片段场景设定在：<Character2>(赵府荷花池)。
分镜1 10s：固定中景，<Character1>(赵阿萤) 右手按住 <Prop1>(玉佩)，抬眼看向门口，压住呼吸。
```

导演稿：

```text
生成一个由以下 2 个分镜组成的视频。
本片段场景设定在：<Character2>(赵府荷花池)。
分镜1 4s：medium shot 落在荷花池边的静压氛围里，<Character1>(赵阿萤) 右手按住 <Prop1>(玉佩)，先把呼吸收住，远处只剩压低的脚步声。
分镜2 6s：镜头缓慢推近到 close-up，<Character1>(赵阿萤) 指节逐渐发白，目光一点点转向门口方向，空气里只剩钟表轻响和衣料摩擦声。
```

### Wanx 10s：基础稿 -> 导演稿（`3s + 3s + 4s`）

基础稿：

```text
生成一个由以下 1 个分镜组成的视频。
本片段场景设定在：<Character3>(赵府荷花池)。
分镜1 10s：<Character2>(赵宛瑜) 突然把 <Character1>(赵阿萤) 推进池中，池水炸开，她站在岸边冷眼旁观。
```

导演稿：

```text
生成一个由以下 3 个分镜组成的视频。
本片段场景设定在：<Character3>(赵府荷花池)。
分镜1 3s：medium shot 先给池边短暂停顿，红绸倒映在水面轻晃，<Character2>(赵宛瑜) 侧身逼近 <Character1>(赵阿萤)。
分镜2 3s：close-up 骤然切近，<Character2>(赵宛瑜) 猛地抬手把 <Character1>(赵阿萤) 推入池中，落水声当场盖过远处喜乐。
分镜3 4s：over-the-shoulder 收在岸边，池水仍在翻涌，<Character2>(赵宛瑜) 俯看池面，冷声说道：“考验一个男人，也要看他会不会对谁都心软。”
```

### Seedance 7-8s：2 段节拍

```text
生成一个由以下 2 个分镜组成的视频。
本片段场景设定在：<Character2>(实训教室)。
分镜1 3s：wide shot 建立压抑教室空间，学生席和讲台形成压迫纵深，荧光灯冷白，空气很紧。
分镜2 5s：medium close-up 切到 <Character1>(林渊) 一侧，他抬眼顶住前方压力，肩背绷紧，末尾把情绪收在一次克制的吸气上。
```

### Seedance 12-15s：3 段节拍

```text
生成一个由以下 3 个分镜组成的视频。
本片段场景设定在：<Character3>(市井街巷)。
分镜1 4s：wide shot 建立潮湿夜巷，霓虹反光压在地面，行人被挤在远景里。
分镜2 4s：two shot 推进到人物关系，<Character1> 和 <Character2> 彼此试探地停在半步距离，谁都没有先开口。
分镜3 6s：close-up 收在 <Character1> 眼神的细微变化上，远处车流声持续拉长，未说出口的情绪压住整个结尾。
```

## 绑定规则

### 场景

CueLight 的 scene binding 最终以 `referenceSceneId` 为准。

- `本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算有效绑定
- 若通过 `director update-storyboard` 或 `storyboard update` 写分镜，必须同时提供 `referenceSceneId`
- 当 `referenceSceneId` 已提供时，服务端会把 scene header 自动归一化成本镜本地的 `<CharacterN>(场景名)`
- 持久化格式中，场景复用本镜本地、编号接续角色的 `<CharacterN>` 槽位；不要再把场景写成裸中文名

### 道具

关键道具对镜头动作、叙事推进或视觉焦点有实质影响时，需要同时满足两层引用：

- 文案层：在 `videoPrompt` 中使用 `<PropN>`
- 结构层：写入 `referencePropIds`

若只是无关背景陈设，不要强行写 `<PropN>`，也不要滥填 `referencePropIds`。

## 导入与编辑

```bash
# 外部 agent 从文件导入（推荐）
cuelight-cli director import-storyboards <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-<number>.json

# 底层导入
cuelight-cli storyboard import-text <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-<number>.json

# 批量创建
cuelight-cli storyboard batch-create <episodeId> --data-file ./.cuelight/<projectId>/storyboards/episode-<number>.json

# 精确更新绑定
cuelight-cli director update-storyboard <storyboardId> \
  --video-prompt "新的提示词" \
  --ref-character-ids "charId1,charId2" \
  --ref-scene-id "sceneId" \
  --ref-prop-ids "propId1,propId2"

cuelight-cli storyboard update <storyboardId> \
  --video-prompt "新的提示词" \
  --ref-character-ids "charId1,charId2" \
  --ref-scene-id "sceneId" \
  --ref-prop-ids "propId1,propId2"
```

## 导演稿重写操作链

```bash
# 1. 先读现有分镜，判断哪些 item 仍是基础稿
cuelight-cli storyboard list <episodeId> --json
cuelight-cli storyboard get <storyboardId> --json

# 2. 在项目子目录中重写导演稿
# ./.cuelight/<project-key>/storyboards/episode-<number>.json

# 3. 写回
cuelight-cli director import-storyboards <episodeId> --file ./.cuelight/<project-key>/storyboards/episode-<number>.json

# 或逐条更新
cuelight-cli storyboard update <storyboardId> --video-prompt "新的导演稿"

# 4. 抽查
cuelight-cli storyboard get <storyboardId> --json
```

执行规则：

- 默认只改 `videoPrompt`，不默认改 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds`
- 只有导演稿里新增了对当前镜头有实质影响的关键道具，才同步补 `referencePropIds`
- 不要只看 `storyboard-status` 这类聚合状态，必须抽查实体详情

## 导入后校验

不要只看 `storyboard list` 或 `director storyboard-status`。导入后至少抽查一条详情：

```bash
cuelight-cli storyboard list <episodeId> --json
cuelight-cli storyboard get <storyboardId>
```

抽查重点：

- `videoPrompt` 是否保留中文主叙述 + 英文术语
- `referenceCharacterIds` 是否齐全
- `referenceSceneId` 是否正确
- `referencePropIds` 是否仅在关键道具镜头中出现

## 常见错误

- 把 `dialogues` 写成单个字符串，而不是 `{ character, line }[]`
- 把 `soundEffects` 写成整段散文，而不是 `string[]`
- 只在 prompt 里写场景中文名，却没写 `referenceSceneId`
- 只在 prompt 里写 `<PropN>`，却没写 `referencePropIds`
- 把一个镜头组里所有信息都塞进单个 `分镜1 10s：...`，却没有拆出节奏
- 混用 `分镜1 4s：...` 和 `0-4秒：...`
- 在正文里反复刷 scene tag，导致 scene header 失去唯一性
- 使用纯英文逗号词串代替中文镜头描述
