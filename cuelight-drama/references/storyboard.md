# Storyboard

## 默认原则

- `cuelight-drama` 自带基础 storyboard 模板，默认先按这里的 JSON 契约写。
- 其他镜头语言资料只增强 `videoPrompt` 的导演感，不改变 CueLight 的字段结构。
- `videoPrompt` 使用中文自然句，保留必要英文术语和标签，如 `medium shot`、`close-up`、`<CharacterN>`、`<PropN>`。
- 分镜落库必须结构化绑定；文案里的角色名、场景名、道具名不能替代 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds`。

## 基础 JSON 模板

```json
[
  {
    "sceneNumber": 1,
    "shotSize": "medium",
    "plannedVideoDurationSeconds": 12,
    "videoPrompt": "【素材定义】\n<Character1>(赵阿萤) 是当前角色参考，<Character2>(赵府荷花池) 是当前场景参考，<Prop1>(玉佩) 是关键道具参考。\n【分镜时序】\n镜头1：medium shot 固定机位先压住池边空气，<Character1>(赵阿萤) 站在池边右手缓慢按住 <Prop1>(玉佩)，指腹轻轻收紧、呼吸被压得很轻，荷花池冷光和门廊阴影把她夹在画面中央，远处传来压低的脚步声。\n镜头2：镜头缓慢推近到 close-up 并只服务她发现异常的情绪压迫，<Character1>(赵阿萤) 目光一点点转向门口、肩膀保持克制不动，池面反光落在她侧脸和玉佩边缘，远处传来木门轻响。\n【风格画质】\n真人实拍电影写实风格，自然皮肤纹理，真实服装材质，池边冷暖光线克制。",
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

- 必填：`sceneNumber`、`shotSize`、`videoPrompt`、`referenceCharacterIds`、`referenceSceneId`。
- Seedance 项目必填：`plannedVideoDurationSeconds`，范围 4-15。
- 可选：`referencePropIds`、`dialogues`、`soundEffects`。
- `dialogues` 固定为 `{ character, line }[]`。
- `soundEffects` 固定为 `string[]`。
- 一条 shot 对应一个 object，`sceneNumber` 按导入顺序递增。
- `shotSize` 可用 `wide`、`medium`、`close-up`、`over-the-shoulder` 等稳定值；不要把完整镜头描述塞进 `shotSize`。

## 基础稿与精修稿

- **基础稿**：格式合法、绑定正确、可直接落库。
- **精修稿**：Seedance 单个 storyboard item 内使用 **1-8 个镜头** 按事件顺序组织；Wanx/旧格式可拆成 **2-3 个子分镜**，强化节奏、反应、对白落点和导演感。

默认从基础稿升格为精修稿的时机：

- 用户要求“重写分镜脚本”“增强导演感”“更像可拍摄分镜”。
- 单条 `videoPrompt` 已经塞入多个叙事信息点。
- 同一镜头组内同时包含环境建立、动作推进、情绪或对白落点。
- 要进入视频生成前，需要降低模型误解风险。

允许保持单分镜的例外：

- 空镜。
- 单一动作展示。
- 单一情绪特写。
- 明确只需要一个视觉落点的短镜头。

## 模型时长规则

- **Wanx 系列**：单条可投递 storyboard item 默认按模型最大 **10s** 规划；不是把任意原稿时间段压成 10s。
- **Seedance 系列**：单条可投递 storyboard item 使用 **4-15s**，写入 `plannedVideoDurationSeconds`；`videoPrompt` 使用 `镜头1 / 镜头2 / 镜头3` 时间轴化描述，不强制每个镜头写精确秒数。
- **完整分集覆盖**：生成某一集完整分镜时，所有 storyboard item 的 `plannedVideoDurationSeconds` 总和必须等于 `project.durationPerEpisode`；90 秒单集通常拆成 6-9 条 item。

Wanx 的默认节奏：

- 主路径：`4s + 6s`。
- 三拍：`3s + 3s + 4s`。

Seedance 的默认节奏：

- `4-6s`：1-3 个镜头，适合单动作、单情绪或单落点。
- `7-10s`：2-5 个镜头，按事件推进。
- `11-15s`：3-8 个镜头，适合完整小弧线。
- 一镜到底只写 `镜头1`；不要为了凑数量硬拆。
- 若沿用旧 `分镜N Xs` 格式，单个子分镜最短 2s，最长 10s。

Seedance 推荐结构：

```text
【素材定义】
<Character1>(角色名) 是当前角色参考，<Character3>(场景名) 是当前场景参考，<Prop1>(道具名) 是关键道具参考。
【分镜时序】
镜头1：运镜或镜头切换方式，主体动作与表情，位置或空间变化，同步声音/对白/环境声/动作音效。
镜头2：运镜或镜头切换方式，主体动作与表情，位置或空间变化，同步声音/对白/环境声/动作音效。
镜头3：运镜或镜头切换方式，主体动作与表情，位置或空间变化，同步声音/对白/环境声/动作音效。
【风格画质】
整体为真人实拍电影写实风格，自然皮肤纹理，真实服装材质，自然光线。
```

## 原稿形态识别

写分镜前先判断原稿形态，再决定拆分策略：

- 传统影视/舞台剧本：常见 `时/地/人`、场次号、`△` 动作行、`角色：台词`。
- 短视频/教学分镜脚本：常见 `【幕/段落标题 (0:00 - 0:45)】`、`画面`、`音效`、音乐提示、`台词`、互动等待/倒计时、教学目标。
- 混合稿：同时有场次和时间码时，时间码优先决定 item 覆盖范围，场次/画面/动作行用于场景绑定和镜头内容。

传统剧本没有原稿时间码时，不要编造时间码；按场次、动作行、对白密度和首选模型 `maxSeconds` 估算 storyboard item。动作行、场景说明、`△` 行进入镜头和环境；`角色：（动作）台词` / `角色：台词` 都视为角色对白，但括号动作只写进表演描述，不进入 `说台词` 文本。

短视频/教学分镜脚本中，`画面` 进入视觉动作和空间描述；`音效/互动等待/倒计时` 写进 `videoPrompt` 必要声音设计，但不当角色对白；原稿里的音乐提示默认不写入视频提示词，音乐建议后期添加。只有 `台词` 区块里的角色对白才写 `<CharacterN>(角色名) 说台词：...`。例如 `衣衣（开心拍手）：太棒了` 应写成画面里开心拍手，再写 `<CharacterN>(衣衣) 说台词：太棒了`。

## 原稿时间码拆分规则

原稿里的 `0:00-0:15`、`0:00-0:45` 是剧情覆盖跨度，不是可忽略标签。

处理步骤：

- 先解析时间码：`end - start = coveredSeconds`。
- 读取当前首选视频模型的 `maxSeconds`。
- 如果 `coveredSeconds <= maxSeconds`，这一条 item 的子分镜秒数合计必须等于覆盖跨度。
- 如果 `coveredSeconds > maxSeconds`，必须拆成多条连续 storyboard item，每条覆盖时间片 `<= maxSeconds`。
- 最后一段可短于 `maxSeconds`；Seedance 最短 4s，非 Seedance 按模型最小时长处理。不足最小时长时并入前一段并调整秒数。
- 时间码只作为 item 级保存前校验锚点，例如 `原稿时间码：0:00-0:10`；Seedance item 内按 `镜头N` 时间轴写，非 Seedance item 内按精修稿拆成 1-3 条子分镜。

强制示例：

- 错误：`分镜1 10s：0:00-0:15...`
- 正确：第一条 item 写 `原稿时间码：0:00-0:10`，并在 item 内拆成 `分镜1 4s` + `分镜2 6s`；第二条 item 写 `原稿时间码：0:10-0:15`，可写 `分镜1 5s`。
- `0:00-0:45` 且 `maxSeconds=10` 时，必须拆成 5 条 item：`0:00-0:10`、`0:10-0:20`、`0:20-0:30`、`0:30-0:40`、`0:40-0:45`，对应 item 总时长 `10+10+10+10+5`；每条 10s item 内仍优先写 4s+6s 或 3s+3s+4s 子分镜。

如果 `videoPrompt` 中的时间码跨度超过声明秒数，CLI 验收会判定为 `storyboardTimecodeDurationMismatch`。

## 固定写法

Seedance 推荐每个精修稿 item 写成：

- `plannedVideoDurationSeconds`: 4-15。
- `【素材定义】`
- `【分镜时序】`
- `镜头1：...`
- `镜头2：...`
- 可选继续写到 `镜头8：...`
- `【风格画质】`

Wanx / 旧格式精修稿可写成：

- `生成一个由以下 N 个分镜组成的视频。`
- `本片段场景设定在：<CharacterN>(场景名)。`
- `分镜1 Xs：...`
- `分镜2 Ys：...`
- 可选 `分镜3 Zs：...`

固定约束：

- Seedance 镜头数按剧情节奏选择 **1-8 个**；15 秒内可以一镜到底，也可以拆到最多 8 个镜头。
- 每条 `镜头N：` 的信息顺序固定为：运镜或镜头切换方式 -> 主体动作与表情 -> 位置或空间变化 -> 同步声音信息。推荐句式：`镜头N：<运镜/切换方式>，<主体动作与表情>，<位置或空间变化>，<同步声音/对白/环境声/动作音效>。`
- 一镜到底也必须补齐四类信息；没有对白时必须写环境声或动作音效，不能只写视觉动作。
- 不要混用 `分镜1 4s：...` 和 `0-4秒：...`。
- 不要出现连续空行。
- scene header 只出现一次；正文不再重复刷 scene tag。
- `<CharacterN>(角色名) 说台词：...` 必须逐字复制本集正文中同一角色的一整条原文台词；如果只需要表达某句台词的一部分或语义摘要，写成画面/旁白/声音说明，不要使用 `说台词：`。
- 默认不写 BGM、配乐、背景音乐或音乐氛围；只写与画面同步的脚步声、门响、手机提示音、呼吸声、环境声、角色对白或旁白。

## 升格示例

### Wanx 10s：基础稿 -> 精修稿（`4s + 6s`）

基础稿：

```text
生成一个由以下 1 个分镜组成的视频。
本片段场景设定在：<Character2>(赵府荷花池)。
分镜1 10s：固定中景，<Character1>(赵阿萤) 右手按住 <Prop1>(玉佩)，抬眼看向门口，压住呼吸。
```

精修稿：

```text
生成一个由以下 2 个分镜组成的视频。
本片段场景设定在：<Character2>(赵府荷花池)。
分镜1 4s：medium shot 落在荷花池边的静压氛围里，<Character1>(赵阿萤) 右手按住 <Prop1>(玉佩)，先把呼吸收住，远处只剩压低的脚步声。
分镜2 6s：镜头缓慢推近到 close-up，<Character1>(赵阿萤) 指节逐渐发白，目光一点点转向门口方向，空气里只剩钟表轻响和衣料摩擦声。
```

### Wanx 10s：基础稿 -> 精修稿（`3s + 3s + 4s`）

基础稿：

```text
生成一个由以下 1 个分镜组成的视频。
本片段场景设定在：<Character3>(赵府荷花池)。
分镜1 10s：<Character2>(赵宛瑜) 突然把 <Character1>(赵阿萤) 推进池中，池水炸开，她站在岸边冷眼旁观。
```

精修稿：

```text
生成一个由以下 3 个分镜组成的视频。
本片段场景设定在：<Character3>(赵府荷花池)。
分镜1 3s：medium shot 先给池边短暂停顿，红绸倒映在水面轻晃，<Character2>(赵宛瑜) 侧身逼近 <Character1>(赵阿萤)。
分镜2 3s：close-up 骤然切近，<Character2>(赵宛瑜) 猛地抬手把 <Character1>(赵阿萤) 推入池中，落水声当场盖过远处喜乐。
分镜3 4s：over-the-shoulder 收在岸边，池水仍在翻涌，<Character2>(赵宛瑜) 俯看池面，冷声说道：“考验一个男人，也要看他会不会对谁都心软。”
```

### Seedance 7-8s：2 镜头时序

```text
plannedVideoDurationSeconds: 8
【素材定义】
<Character1>(林渊) 是当前角色参考，<Character2>(实训教室) 是当前场景参考。
【分镜时序】
镜头1：wide shot 固定机位建立压抑教室空间，<Character1>(林渊) 坐在第二排左侧、双手缓慢压住桌沿、肩背逐渐绷紧，学生席和讲台形成纵深压迫、荧光灯冷白压在他头顶，空气里只有椅脚轻响。
镜头2：镜头切到 medium close-up 并停在 <Character1>(林渊) 侧前方，<Character1>(林渊) 从低头状态自然过渡到抬眼、喉结轻轻滚动，第二排课桌边缘遮住他半截手背，末尾收在一次克制的吸气声上。
【风格画质】
真人实拍电影写实风格，冷白室内光，自然皮肤纹理，真实校服材质。
```

### Seedance 12-15s：3 镜头小弧线

```text
plannedVideoDurationSeconds: 14
【素材定义】
<Character1>(陈砚) 和 <Character2>(苏晓岚) 是当前角色参考，<Character3>(市井街巷) 是当前场景参考。
【分镜时序】
镜头1：wide shot 固定机位建立潮湿夜巷，<Character1>(陈砚) 站在巷口左侧、右手缓慢松开伞柄、下颌线微微绷住，霓虹反光压在地面并把他和巷口拉开距离，远处车流声被雨声压低。
镜头2：two shot 平视机位轻微横移并只服务两人距离变化，<Character2>(苏晓岚) 从右侧走近半步后停下、脚尖微微内扣，<Character1>(陈砚) 留在左侧前景形成遮挡关系，两人之间只剩雨滴打在伞面的声音。
镜头3：close-up 收在 <Character1>(陈砚) 眼神的细微变化上，<Character1>(陈砚) 从停顿状态自然过渡到抬眼、手指轻轻攥紧伞柄，巷口霓虹反光滑过他的眼角，远处车流声持续拉长。
【风格画质】
真人实拍电影写实风格，冷蓝雨夜色调，真实湿地反光，自然皮肤纹理。
```

精修稿的每条 `镜头N：` 必须按四要素顺序自然写成一句或多句：先写运镜或镜头切换方式，再写主体动作与表情，再写位置或空间变化，最后写同步声音信息。固定镜头可作为运镜，但仍要写清机位；情绪要落到眼神、呼吸、肩背、手指等可见表演，声音要落到对白、环境音或动作音效。

## 绑定规则

### 角色

- `referenceCharacterIds` 至少包含当前镜头中承担动作或情绪焦点的角色。
- 群像镜头不要滥填所有角色，只填对画面理解有必要的角色。
- `videoPrompt` 中使用 `<CharacterN>(角色名)`，编号是本镜本地标签，不要假设跨镜头稳定。

### 场景

CueLight 的 scene binding 最终以 `referenceSceneId` 为准。

- `本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算有效绑定。
- 写分镜时必须同时提供 `referenceSceneId`。
- 当 `referenceSceneId` 已提供时，服务端会把 scene header 自动归一化成本镜本地的 `<CharacterN>(场景名)`。
- 持久化格式中，场景复用本镜本地、编号接续角色的 `<CharacterN>` 槽位；不要再把场景写成裸中文名。

### 道具

关键道具对镜头动作、叙事推进或视觉焦点有实质影响时，需要同时满足两层引用：

- 文案层：在 `videoPrompt` 中使用 `<PropN>`。
- 结构层：写入 `referencePropIds`。

若只是无关背景陈设，不要强行写 `<PropN>`，也不要滥填 `referencePropIds`。

## 导入与编辑

```bash
cuelight-cli storyboard import-text <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-<number>.json --json
cuelight-cli storyboard list <episodeId> --json
cuelight-cli storyboard get <storyboardId> --json
cuelight-cli storyboard update <storyboardId> \
  --video-prompt "新的提示词" \
  --ref-character-ids "charId1,charId2" \
  --ref-scene-id "sceneId" \
  --ref-prop-ids "propId1,propId2" \
  --json
```

执行规则：

- 批量重写时优先从文件导入，保留可审阅的 JSON。
- 精确修订时优先逐条 update。
- 默认只改 `videoPrompt`，不默认改 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds`。
- 如果镜头内容新增/删除角色、场景或关键道具，必须同步更新结构化绑定。
- 写回后用 `cuelight-cli storyboard status <episodeId> --json` 抽查数量与绑定完整性。
