---
name: cuelight-drama
description: 短剧制作全链路工作流指引。当用户提及"短剧"、"做剧"、"drama"、"导演模式"、"视觉设定"、"选角"、"角色与场景"、"分镜设计"、"制作列表"、"视频素材库"、"影片制作"、"生成视频"、"导出视频"等关键词时触发。引导 Agent 通过 `@cuelight/cli`（命令名 `cuelight-cli`）读取项目状态、编辑文字资源并推进项目；Skill 仅负责流程指导。
---

这个 Skill 只负责说明 CueLight 的项目推进方法，不提供项目运行时状态。所有状态读取、资源详情查询、文字写回、生成任务提交都必须通过 `cuelight-cli` 完成。

## 使用原则

- **CLI 是唯一事实入口**：先查状态，再决定下一步
- **Skill 不承载状态**：不要从 Skill 推断当前项目已经做到哪一步
- **文字类默认由外部 agent 创作并直写**：proposal、design、worldView、角色、场景、Episode outline/script、Storyboard 文本等，默认都先由外部 agent 自己完成，再通过 CLI 落库
- **`cuelight-drama` 自带基础 storyboard 模板**：按本 skill 的 JSON 模板就能完成合格落库；`seedance-storyboard` 只是可选增强，用来提升 `videoPrompt` 的导演感和镜头语言
- **Storyboard 的场景绑定必须走结构化字段**：`本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算最终引用；CueLight 以 `referenceSceneId` 为准，并把场景文案规范成“本镜本地、编号接续角色的 `<CharacterN>(场景名)`”
- **关键道具同时需要文案层和结构层引用**：文案里可使用 `<PropN>`；若该道具对动作、叙事推进或视觉焦点有实质影响，最终必须同时写入 `referencePropIds`
- **提示词统一使用中文主叙述**：`stylePrompt`、`basePrompt`、`videoPrompt` 都以中文自然句为主，仅保留英文专业术语和标签，如 `medium shot`、`close-up`、`rim lighting`、`<CharacterN>`、`<PropN>`
- **默认不使用内置文本生成**：公开 `cli + skill` 组合不依赖 CueLight 内部 chat/agent，也不把文本类内置 AI 当公开能力
- **生成类继续走内置能力**：图片、视频、语音仍通过现有 AI 命令提交和轮询
- **不要默认从头开始**：用户说“继续项目”时，先执行状态命令
- **内部命令不属于公开工作流**：`cuelight-cli internal ...` 仅供开发/排障，不作为外部 agent 常规路径

## 环境配置

```bash
bun add -g @cuelight/cli
cuelight-cli --help
cuelight-cli doctor fix-binary
cuelight-cli config set url http://localhost:3000
cuelight-cli project list
```

## 临时文件目录约定

- 所有临时文本/JSON 文件都放在**当前目录**下，但必须按项目分子目录存放
- 统一使用：`./.cuelight/<project-key>/`
- `project-key` 规则：
  - 已有 `projectId` 时用 `<projectId>`
  - 只有 `draftId` 时用 `draft-<draftId>`
  - 仅有标题草稿时用 `draft-<sanitized-title>`
- 推荐文件布局：
  - `./.cuelight/<project-key>/world.txt`
  - `./.cuelight/<project-key>/style-prompt.txt`
  - `./.cuelight/<project-key>/proposal.txt`
  - `./.cuelight/<project-key>/design.txt`
  - `./.cuelight/<project-key>/episodes/episode-<number>-outline.txt`
  - `./.cuelight/<project-key>/episodes/episode-<number>-script.txt`
  - `./.cuelight/<project-key>/storyboards/episode-<number>.json`
  - `./.cuelight/<project-key>/assets/<assetId>.txt`

## 提示词统一写法

以下规则统一适用于 `stylePrompt`、`character.basePrompt`、`scene.basePrompt`、`prop.basePrompt`、`storyboard.videoPrompt`：

- 主体叙述使用中文自然句，不使用纯英文逗号词串作为默认写法
- 专业摄影、镜头、构图、光影术语保留英文，例如 `medium shot`、`close-up`、`over-the-shoulder`、`rim lighting`
- 结构化标签保持英文，例如 `<CharacterN>`、`<PropN>`
- 角色/场景/道具的 `basePrompt` 写“基准状态”，不要写剧情时刻、临时情绪或一次性动作
- `videoPrompt` 写“当前镜头发生什么”，不要把 JSON 绑定字段混成自然语言说明

示例：

- `stylePrompt`：`仿真人短剧质感，写实肤质与克制调色，室内以 soft diffused light 为主，人物边缘保留轻微 rim lighting，竖屏 9:16 构图强调近身压迫感。`
- `character.basePrompt`：`二十岁出头的闺秀面相，鹅蛋脸，肤色白净偏冷，眉眼线条细长，发髻整洁，穿浅青色织纹襦裙，站姿克制端正，neutral expression，medium shot。`
- `scene.basePrompt`：`侯府寿安堂的日间内景，厅堂纵深清晰，木质屏风与案几分区明确，暖色自然光从侧窗落入，wide shot 展示礼序空间与主次座位。`
- `prop.basePrompt`：`一支旧式鎏金簪，簪头花丝纹样细密，金属表面有轻微磨痕，冷暖反光克制，hero shot 展示结构与材质。`

## 基础 Storyboard 模板

`cuelight-drama` 自身提供基础模板，默认先按这个模板写。只有当用户明确需要更强的导演感、Seedance 风格镜头语言或更复杂的时间轴拆解时，才把 `agent-skills/seedance-storyboard` 当作 `videoPrompt` 的可选增强参考。

标准文件：`./.cuelight/<projectId>/storyboards/episode-<number>.json`

```json
[
  {
    "sceneNumber": 1,
    "shotSize": "medium",
    "videoPrompt": "生成一个由以下 2 个分镜组成的视频。\n本片段场景设定在：<Character2>(赵府荷花池)。\n分镜1 4s：medium shot 先压住池边的静默空气，<Character1>(赵阿萤) 右手按住 <Prop1>(玉佩)，目光停在门口方向，远处传来压低的脚步声。\n分镜2 6s：镜头缓慢推近到 close-up，<Character1>(赵阿萤) 指节逐渐发白，却始终没有松手，空气里只剩钟表轻响和衣料摩擦声。",
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

字段规则：

- 必填：`sceneNumber`、`shotSize`、`videoPrompt`、`referenceCharacterIds`、`referenceSceneId`
- 可选：`referencePropIds`、`dialogues`、`soundEffects`
- `dialogues` 固定为 `{ character, line }[]`
- `soundEffects` 固定为 `string[]`
- 一条 shot 对应一个 object，`sceneNumber` 按导入顺序递增
- `videoPrompt` 持久化后采用“标签+中文名”格式：角色 `<CharacterN>(中文名)`、场景使用本镜本地的 `<CharacterN>(中文名)`、道具 `<PropN>(中文名)`
- `videoPrompt` 只承担镜头文案；角色、场景、道具的最终绑定分别以 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds` 为准
- `referencePropIds` 仅在道具对动作、叙事推进或视觉焦点有实质影响时填写，不要求所有分镜都带
- `seedance-storyboard` 若被使用，只增强 `videoPrompt` 的镜头语言，不改变这里的 JSON 字段和类型

## 导演稿重写规范

这里把 storyboard 文本明确分成两种交付层级：

- **基础稿**：格式合法、绑定正确、可直接落库
- **导演稿**：在一个 storyboard item 内拆成 **2-3 个子分镜**，强化节奏、反应、对白落点和导演感

默认升级为导演稿的时机：

- 进入导演工作台精修
- 用户明确要求“更像导演页”“重写分镜脚本”“增强导演感”
- 单条 `videoPrompt` 已经塞入多个叙事信息点
- 同一镜头组内同时存在“环境建立 + 动作推进 + 情绪落点/对白落点”

允许保持单分镜的例外：

- 空镜
- 单一动作展示
- 单一情绪特写
- 明确只需要一个视觉落点的短镜头

### 时长决策

- **Wanx 系列**：导演稿默认按 **固定 10s** 编写
- **Seedance 系列**：导演稿按 **5-15s** 编写，由当前分镜组的情节密度决定

Wanx 系列的默认规则：

- 每个 storyboard item 默认就是一个 **10s** 镜头组
- 不为 Wanx 自行改成 6s / 8s / 12s，除非用户明确指定，或产品规则已经变化
- 默认优先使用以下节奏：
  - `4s + 6s`
  - `3s + 3s + 4s`

Seedance 系列的默认规则：

- `5-6s`：单动作、单情绪、单落点
- `7-10s`：建立 -> 变化 -> 收束
- `11-15s`：完整小弧线，但仍控制切镜数量
- 当 `seedance-storyboard` 被用作增强时，它只增强镜头语言；写回 CueLight 时仍以本 skill 的结构和绑定规则为准

### 子分镜拆法

每个导演稿 item 必须写成：

- `生成一个由以下 N 个分镜组成的视频。`
- `本片段场景设定在：<CharacterN>(场景名)。`
- `分镜1 Xs：...`
- `分镜2 Ys：...`
- 可选 `分镜3 Zs：...`

固定约束：

- 子分镜默认 **2 个**；只有确实需要“建立 / 推进 / 落点”三拍时才写 **3 个**
- 每条子分镜的信息顺序固定为：
  - 环境/空间锚点
  - 景别/运镜
  - 角色动作或关系变化
  - 对白或音效落点
- 不要混用 `分镜1 4s：...` 和 `0-4秒：...` 两套格式
- 不要出现连续空行
- scene header 只出现一次；正文不再重复刷 scene tag

默认节奏模板：

- **Wanx 10s 主路径**：`4s + 6s`
- **Wanx 10s 三拍**：`3s + 3s + 4s`
- **Seedance 7-8s**：优先 2 段节拍
- **Seedance 12-15s**：允许 3 段节拍

### 导演稿重写操作链

标准流程：

1. 用 `storyboard list/get` 读取现有分镜，判断哪些 item 仍是基础稿。
2. 在 `./.cuelight/<project-key>/storyboards/episode-<number>.json` 中把目标 item 重写成导演稿。
3. 默认只改 `videoPrompt`，不默认改 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds`。
4. 若导演稿里新增了对当前镜头有实质影响的关键道具，再同步补 `referencePropIds`。
5. 用 `director import-storyboards` 或 `storyboard update` 写回。
6. 回写后必须用 `storyboard get` 抽查 2-3 条，不只看聚合状态。

## Source Draft 启动

从 source 文件进入项目时，优先走完整公开链路：

```bash
cuelight-cli source draft create-from-file --title "项目标题" --file ./source.txt --goal scope_planning
cuelight-cli source draft get <draftId> --json
cuelight-cli source draft confirm <draftId> --suggestion-index 0
cuelight-cli project create --title "项目标题" --source-draft-id <draftId> --json
cuelight-cli project status <projectId> --json
```

说明：

- `scope` / `suggestions` 以 `source draft get --json` 返回内容为准
- 不要假设存在单独的 `scope` 命令
- 若用户说“从小说/原稿继续”，先确认是已有 `projectId` 还是仍停留在 `draftId`

## 标准工作方式

导演相关操作优先使用 `director` 命令组；现有 `bible`、`storyboard`、`ai`、`video` 等底层命令保留为 fallback，不作为主路径。

### 1. 先读状态

优先使用：

```bash
cuelight-cli director status <projectId> --json
cuelight-cli director visual-status <projectId> --json
cuelight-cli director storyboard-status <episodeId> --json
cuelight-cli director video-status <episodeId> --json
cuelight-cli episode get <episodeId> --json
cuelight-cli source draft get <draftId> --json
```

判断规则：

- 若项目是 `my_script`，先读取原稿全文，再由外部 agent 自行做剧情容量判断
- 若项目是 `adaptation`，先读取 source 原文、`source draft get --json` 的结构化结果，以及 current season，再由外部 agent 自行判断 proposal、design、分集与正文
- 缺 `worldView` / `stylePrompt`，先补 Bible
- 缺 Episode `summary`，先补大纲
- 缺 Episode `content`，先补剧本
- 缺 Storyboard，先写文字分镜或再触发生成
- Storyboard 绑定不完整，不直接出视频

原稿模式额外要求：

- `my_script` 的容量判断默认由外部 agent 自己完成，不依赖服务端推荐值
- 不要默认写成 `10 集`
- 不要把固定短剧档位当作 `my_script` 的前提条件
- 外部 agent 应基于原稿正文，自行给出：
  - `recommendedEpisodes`
  - `recommendedDuration`
  - `capacityRationale`
  - `episodeSplitStrategy`
- 形成判断后，再通过 CLI 写回 `project.totalEpisodes`、`season.plannedEpisodes`、必要时 `durationPerEpisode`

### 2. 再写文字资源

优先使用稳定的文件写入命令：

```bash
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/world.txt
cuelight-cli director set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt
cuelight-cli director configure-visuals <projectId> --visual-mode improv --shooting-mode omni_reference --video-ratio 9:16
cuelight-cli season set-proposal <projectId> <seasonId> --file ./.cuelight/<projectId>/proposal.txt
cuelight-cli season set-design <projectId> <seasonId> --file ./.cuelight/<projectId>/design.txt
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-<number>-outline.txt
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-<number>-script.txt
cuelight-cli director import-storyboards <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-<number>.json
cuelight-cli asset set-content <projectId> <assetId> --file ./.cuelight/<projectId>/assets/<assetId>.txt
```

仍可继续使用已有细粒度更新命令：

```bash
cuelight-cli bible update <projectId> --world-view "..."
cuelight-cli episode update <episodeId> --content-file ./.cuelight/<project-key>/episodes/episode-<number>-script.txt
cuelight-cli director update-storyboard <storyboardId> --video-prompt "..."
cuelight-cli asset update <projectId> <assetId> --content-file ./.cuelight/<project-key>/assets/<assetId>.txt
```

执行原则：

- 文字内容默认不要先调用系统内置文本生成工具
- 先由外部 agent 根据已读取的原稿、`source draft get --json` 的结构化结果、project/season 状态自行产出内容
- 产出后优先写成本地文件，再用 CLI 写回
- 同一资源按顺序写入，不并发提交，避免覆盖
- 若 storyboard prompt 中写了 `本片段场景设定在：...`，在最终落库前必须同时写入 `referenceSceneId`；不要把裸场景名当成唯一绑定来源
- 若 storyboard 中出现对当前镜头有实质影响的关键道具，在最终落库前必须同时写入 `referencePropIds`
- 不要假设 `<Character4>` 之类的 scene tag 在不同分镜里含义固定；场景 tag 取决于当前分镜自身的绑定资源顺序
- 避免把不同项目的临时文件混在同一目录里；切换项目时先切换 `./.cuelight/<project-key>/`

不要把内部文本生成命令写进常规操作链。若确实要做内部调试，应明确使用 `cuelight-cli internal ...`，并向用户说明这不属于公开 CLI 工作流。

### 3. 最后提交生成任务

仅在文字和绑定状态就绪后再进入生成阶段：

```bash
cuelight-cli character batch-generate-images <projectId>
cuelight-cli scene batch-generate-images <projectId>
cuelight-cli prop batch-generate-images <projectId>
cuelight-cli director generate-style-image <projectId>
cuelight-cli director batch-generate-videos <episodeId>
cuelight-cli director generate-video <storyboardId> --episode-id <episodeId> --persist
cuelight-cli director wait-task <taskId> --timeout 600
cuelight-cli director export-videos <episodeId>
```

## 阶段建议

### 编剧准备

目标：

- 项目基础信息齐全
- proposal / design / Bible 已由外部 agent 写入
- 至少一集有大纲或剧本正文

推荐命令链：

```bash
cuelight-cli director status <projectId> --json
cuelight-cli season status <projectId> <seasonId> --json
cuelight-cli director visual-status <projectId> --json
cuelight-cli episode list <projectId> --json
cuelight-cli episode status <episodeId> --json
```

需要写内容时：

```bash
cuelight-cli season set-proposal <projectId> <seasonId> --file ./.cuelight/<projectId>/proposal.txt
cuelight-cli season set-design <projectId> <seasonId> --file ./.cuelight/<projectId>/design.txt
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/world.txt
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-<number>-outline.txt
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-<number>-script.txt
```

若项目是 `my_script`：

- 先读原稿全文
- 外部 agent 自行完成容量判断和分集策略
- 先写回 `totalEpisodes` / `plannedEpisodes` / `durationPerEpisode`
- 再继续 proposal、design、角色、场景、outline、script

### 视觉设定

目标：

- `stylePrompt` 已就绪
- 关键角色、场景、道具具备生成参考图的条件

推荐命令链：

```bash
cuelight-cli director status <projectId> --json
cuelight-cli director visual-status <projectId> --json
cuelight-cli style list-presets --json
cuelight-cli prop list <projectId> --json
```

需要写内容时：

```bash
cuelight-cli director set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt
cuelight-cli director configure-visuals <projectId> --visual-mode improv --shooting-mode omni_reference --video-ratio 9:16
cuelight-cli style apply <projectId> --preset-id <presetId>
cuelight-cli director generate-style-image <projectId>
```

### 分镜设计

目标：

- Episode 已有剧本
- Storyboard 文本已写入或已生成
- 角色/场景绑定完整

推荐命令链：

```bash
cuelight-cli director storyboard-status <episodeId> --json
```

需要写内容时：

```bash
cuelight-cli director import-storyboards <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-<number>.json
cuelight-cli director update-storyboard <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..." --ref-prop-ids "..."
```

执行要求：

- 默认先按本 skill 的基础 JSON 模板产出可落库分镜
- 进入导演工作台精修时，默认把基础稿升级为导演稿
- 若目标模型是 Wanx，导演稿默认按固定 `10s` 编写；若目标模型是 Seedance，按 `5-15s` 并根据分镜组情节决定时长
- Wanx 导演稿优先使用 `4s + 6s` 或 `3s + 3s + 4s`
- `seedance-storyboard` 只在需要增强 `videoPrompt` 的镜头语言时再参考，不是默认前置步骤
- `videoPrompt` 仍然必须保持中文主叙述，只保留必要英文术语和标签
- 单个 storyboard item 默认拆成 2-3 个子分镜；空镜、单动作、单情绪特写才保留单分镜
- 导入后不要只看 `storyboard list` 或 `director storyboard-status`；至少抽查 `storyboard get <storyboardId>`，确认 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds` 真正落库

### 影片制作

目标：

- Storyboard 已齐全
- 绑定完整
- 再提交视频生成

推荐命令链：

```bash
cuelight-cli director video-status <episodeId> --json
cuelight-cli director batch-generate-videos <episodeId>
cuelight-cli director wait-task <taskId> --timeout 600
cuelight-cli director export-videos <episodeId>
```

## 底层 Fallback 命令

若 `director` 命令组暂时无法覆盖某个细节操作，再回退到现有底层命令。它们只用于补细节和排障，不应替代公开主路径：

```bash
cuelight-cli bible update <projectId> ...
cuelight-cli storyboard list <episodeId> --json
cuelight-cli storyboard update <storyboardId> ...
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId>
cuelight-cli ai batch-submit-videos <episodeId>
cuelight-cli ai wait <taskId>
cuelight-cli video export <episodeId>
```

## 修复路径

常见单点修复命令：

```bash
# 单角色
cuelight-cli character upload-image <projectId> <characterId> --file ./.cuelight/<projectId>/characters/<characterId>.png
cuelight-cli character generate-image <projectId> <characterId>
cuelight-cli character generate-video <projectId> <characterId>

# 单场景
cuelight-cli scene upload-image <projectId> <sceneId> --file ./.cuelight/<projectId>/scenes/<sceneId>.png
cuelight-cli scene generate-image <projectId> <sceneId>

# 单道具
cuelight-cli prop upload-image <projectId> <propId> --file ./.cuelight/<projectId>/props/<propId>.png
cuelight-cli prop generate-image <projectId> <propId>

# 单分镜
cuelight-cli director update-storyboard <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..." --ref-prop-ids "..."
cuelight-cli director generate-video <storyboardId> --episode-id <episodeId> --persist

# 任务与版本
cuelight-cli ai task-status <taskId>
cuelight-cli ai wait <taskId>
cuelight-cli resource-version list <projectId> --entity-type character --entity-id <characterId> --asset-kind image
cuelight-cli resource-version list <projectId> --entity-type scene --entity-id <sceneId> --asset-kind image
cuelight-cli resource-version list <projectId> --entity-type prop --entity-id <propId> --asset-kind image
```

## 参考文档

- [project.md](references/project.md)
- [director.md](references/director.md)
- [bible.md](references/bible.md)
- [episode.md](references/episode.md)
- [storyboard.md](references/storyboard.md)
- [character.md](references/character.md)
- [scene.md](references/scene.md)
- [prop.md](references/prop.md)
- [style.md](references/style.md)
- [video-gen.md](references/video-gen.md)

## Agent 行为约束

- 继续项目时，先执行状态命令，不要默认创建新资源
- 不要把 Skill 当作状态源
- 不论 `my_script` 还是 `adaptation`，正文默认优先由外部 agent 完成
- 除非用户明确要求，否则不要把 `episode generate` / `generate-script` 当作默认路径
- 不要在绑定不完整时直接生成视频
- 大段文字不要贴在聊天里，优先写文件后通过 CLI 落库
- 批量覆盖型操作前先告知用户影响范围
- 若 CLI 报 binary 缺失或不可执行，先执行 `cuelight-cli doctor fix-binary`
- 若某个命令只能在 `cuelight-cli internal ...` 下找到，说明它是内部调试能力，不要把它当作公开交付路径
