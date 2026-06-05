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

- **Wanx 系列**：单条可投递 storyboard item 默认按模型最大 **10s** 规划；不是把任意原稿时间段压成 10s
- **Seedance 系列**：单条可投递 storyboard item 默认 **5-15s**，根据模型能力和分镜组情节决定

Wanx 的默认节奏：

- 主路径：`4s + 6s`
- 三拍：`3s + 3s + 4s`

Seedance 的默认节奏：

- `5-6s`：单动作、单情绪、单落点
- `7-10s`：2 段或 3 段节拍
- `11-15s`：完整小弧线，但仍控制切镜数量

### my_script 原稿形态识别

写 my_script 分镜前先判断原稿形态，再决定拆分策略：

- 传统影视/舞台剧本：常见 `時/地/人`、场次号、`△` 动作行、`角色：台词`
- 短视频/教学分镜脚本：常见 `【幕/段落标题 (0:00 - 0:45)】`、`画面`、`音效/BGM`、`台词`、互动等待/倒计时、教学目标
- 混合稿：同时有场次和时间码时，时间码优先决定 item 覆盖范围，场次/画面/动作行用于场景绑定和镜头内容

传统剧本没有原稿时间码时，不要编造 `源时间码`；按场次、动作行、对白密度和首选模型 `maxSeconds` 估算 storyboard item。动作行、场景说明、`△` 行进入镜头和环境；`角色：（动作）台词` / `角色：台词` 都视为角色对白，但括号动作只写进表演描述，不进入 `说台词` 文本。

短视频/教学分镜脚本中，`画面` 进入视觉动作和空间描述；`音效/BGM/互动等待/倒计时` 写进 `videoPrompt` 声音设计，但不当角色对白；只有 `台词` 区块里的角色对白才写 `<CharacterN>(角色名) 说台词：...`。例如 `衣衣（开心拍手）：太棒了` 应写成画面里开心拍手，再写 `<CharacterN>(衣衣) 说台词：太棒了`。

### 原稿时间码拆分规则

原稿里的 `0:00-0:15`、`0:00-0:45` 是剧情覆盖跨度，不是可忽略标签。

处理步骤：

- 先解析时间码：`end - start = sourceDurationSeconds`
- 读取当前首选视频模型的 `maxSeconds`
- 如果 `sourceDurationSeconds <= maxSeconds`，这一条 item 的子分镜秒数合计必须等于覆盖跨度
- 如果 `sourceDurationSeconds > maxSeconds`，必须拆成多条连续 storyboard item，每条覆盖时间片 `<= maxSeconds`
- 最后一段可短于 `maxSeconds`，但最短 3s；不足 3s 时并入前一段并调整秒数
- 原稿时间码写在 item 级别，例如 `源时间码：0:00-0:10`；item 内仍按导演稿拆成 1-3 条子分镜

强制示例：

- 错误：`分镜1 10s：0:00-0:15...`
- 正确：第一条 item 写 `源时间码：0:00-0:10`，并在 item 内拆成 `分镜1 4s` + `分镜2 6s`；第二条 item 写 `源时间码：0:10-0:15`，可写 `分镜1 5s` 或按 3s+2s 合理拆分
- `0:00-0:45` 且 `maxSeconds=10` 时，必须拆成 5 条 item：`0:00-0:10`、`0:10-0:20`、`0:20-0:30`、`0:30-0:40`、`0:40-0:45`，对应 item 总时长 `10+10+10+10+5`；每条 10s item 内仍优先写 4s+6s 或 3s+3s+4s 子分镜

如果 `videoPrompt` 中的时间码跨度超过声明秒数，CLI 验收会判定为 `storyboardTimecodeDurationMismatch`。

原稿时间码只作为保存前校验锚点，不是视频模型生产文本；服务端校验通过后会从落库 `videoPrompt` 清理这些 source range。

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

当 `seedance-storyboard` 被用作增强参考时，每条子分镜应按七要素自然组织：景别、机位、运镜、主体动作、情绪表演、环境变化、声音设计。固定镜头可作为运镜，但仍要写清机位；情绪要落到眼神、呼吸、肩背、手指等可见表演，声音要落到对白、环境音或动作音效。

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
