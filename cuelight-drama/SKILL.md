---
name: cuelight-drama
description: CueLight 短剧项目本地 Agent 工作流指引。当用户要创建、续作或验收短剧项目，处理项目设定、剧本大纲、剧本文本、角色、场景、道具、分镜脚本、图片或视频任务时触发。Skill 只说明流程和格式规范，不保存当前项目状态。
---

这个 Skill 只负责说明 CueLight 项目的推进方法和文本/分镜格式。当前项目是谁、工作区根目录在哪里、是否允许写入，都必须由本地工作区和 `cuelight-cli` 提供。

## 使用原则

- **先解析工作区**：进入任意工作区后，第一步执行 `cuelight-cli workspace current --json`。
- **未绑定不执行业务命令**：若没有 `./.cuelight/workspace.json` 或 `currentProjectId` 为空，只能引导用户执行 `cuelight-cli workspace bind --project-id <id> --root <path>`。
- **禁止猜项目**：不得从目录名、mock 数据、最近项目、置顶项目或历史聊天猜测当前项目。
- **显式上下文必须一致**：用户明确给出 projectId 时，仍必须与工作区绑定的 `currentProjectId` 一致；不一致时停止并让用户重新绑定或更正参数。
- **CLI 是唯一事实入口**：读状态、写设定、写剧集、写角色场景道具、写分镜、查任务，都通过 `cuelight-cli`。
- **业务请求走统一合同**：公开 CLI 命令只依赖项目、剧集、分镜、任务资源，不让 Agent 决策内部历史结构。
- **文字类默认由本地 Agent 创作并直写**：本地读取用户给的原稿文件，产出 proposal、design、worldView、stylePrompt、episodes、characters、scenes、props、storyboards，再用 CLI 写回。
- **`cuelight-drama` 自带基础 storyboard 模板**：按本 Skill 的 JSON 模板就能完成合格落库；其他镜头语言资料只作为 `videoPrompt` 增强参考，不改变 CueLight 字段结构。
- **Storyboard 的场景绑定必须走结构化字段**：`本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算最终引用；CueLight 以 `referenceSceneId` 为准。
- **关键道具同时需要文案层和结构层引用**：文案里可使用 `<PropN>`；若该道具对动作、叙事推进或视觉焦点有实质影响，最终必须同时写入 `referencePropIds`。
- **提示词统一使用中文主叙述**：`stylePrompt`、`basePrompt`、`videoPrompt` 都以中文自然句为主，仅保留英文专业术语和标签，如 `medium shot`、`close-up`、`rim lighting`、`<CharacterN>`、`<PropN>`。
- **Seedance 分镜使用镜头时序**：Seedance 系列 `videoPrompt` 默认使用 `镜头1 / 镜头2 / ...`，不强制每个镜头写精确秒数；`plannedVideoDurationSeconds` 单独写入 4-15 秒，单条最多 8 个镜头。
- **完整分集必须覆盖目标时长**：生成某一集完整分镜时，所有 storyboard item 的 `plannedVideoDurationSeconds` 总和必须等于 `project.durationPerEpisode`；90 秒单集通常拆成 6-9 条 item。
- **默认不写 BGM**：分镜提示词默认不输出 BGM、配乐、背景音乐或音乐氛围；音乐建议后期添加，只写必要的人声、环境声和动作音效。
- **默认不提交媒体生成**：除非用户明确要求，不提交图片、视频或语音任务。
- **纯媒体任务例外**：用户只要求独立图片/视频成品时，可直接使用 `image`、`video`、`task` 命令，不需要项目绑定。

## 当前项目上下文

必须按以下顺序解析：

1. 执行 `cuelight-cli workspace current --json`。
2. 若返回 `currentProjectId`，后续业务命令都使用该项目。
3. 若未绑定，只允许执行：

```bash
cuelight-cli workspace bind --project-id <id> --root <workspacePath>
```

4. 若用户只给了候选项目但没有绑定，先让用户确认并绑定。
5. 禁止在未绑定工作区中用显式 projectId 操作项目。

工作区文件示例：

```json
{
  "version": 1,
  "workspaceRoot": "C:\\codes\\cuelight-agent",
  "currentProjectId": "cuelight",
  "skill": "cuelight-drama"
}
```

## 环境配置

优先使用官方一键安装脚本。安装脚本会把 `cuelight-drama` 等 Agent Skills 安装到用户级全局位置，同时安装 `cuelight-cli`，不依赖当前项目目录。

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://cuelight.app/cli_install.ps1 | iex"
```

macOS / Linux：

```bash
curl -fsSL https://cuelight.app/cli_install.sh | bash
```

如果 npm 访问较慢，设置镜像后重试：

```powershell
powershell -ExecutionPolicy Bypass -c "$env:CUELIGHT_NPM_REGISTRY='https://registry.npmmirror.com'; irm https://cuelight.app/cli_install.ps1 | iex"
```

```bash
curl -fsSL https://cuelight.app/cli_install.sh | CUELIGHT_NPM_REGISTRY=https://registry.npmmirror.com bash
```

安装完成后验证并配置 API Key：

```bash
cuelight-cli --version
cuelight-cli doctor fix-binary
cuelight-cli config set api-key <替换为你的API_KEY>
cuelight-cli config show
cuelight-cli project list
```

说明：

- 默认服务地址是 `https://cuelight.app`，公开工作流不要默认改成 `http://localhost:3000`。
- `config show` 应脱敏显示 API Key；不要把真实 API Key 写入公开日志、issue 或可共享 transcript。
- 若只需要单次命令使用密钥，可用 `CUELIGHT_API_KEY=... cuelight-cli ...` 或 `cuelight-cli --api-key ...`。
- 工作区绑定文件只保存当前项目，不保存 API Key。

## 临时文件目录约定

- 所有临时文本/JSON 文件都放在当前工作区的 `./.cuelight/` 下。
- 当前项目文件统一使用：`./.cuelight/<projectId>/`。
- 推荐文件布局：
  - `./.cuelight/<projectId>/proposal.txt`
  - `./.cuelight/<projectId>/design.txt`
  - `./.cuelight/<projectId>/world.txt`
  - `./.cuelight/<projectId>/style-prompt.txt`
  - `./.cuelight/<projectId>/characters/<name>-desc.txt`
  - `./.cuelight/<projectId>/characters/<name>-visual.txt`
  - `./.cuelight/<projectId>/characters/<name>-voice.txt`
  - `./.cuelight/<projectId>/scenes/<name>-desc.txt`
  - `./.cuelight/<projectId>/scenes/<name>-visual.txt`
  - `./.cuelight/<projectId>/props/<name>-desc.txt`
  - `./.cuelight/<projectId>/props/<name>-visual.txt`
  - `./.cuelight/<projectId>/episodes/episode-<number>-outline.txt`
  - `./.cuelight/<projectId>/episodes/episode-<number>-script.txt`
  - `./.cuelight/<projectId>/storyboards/episode-<number>.json`

## 提示词统一写法

以下规则统一适用于 `stylePrompt`、`character.basePrompt`、`scene.basePrompt`、`prop.basePrompt`、`storyboard.videoPrompt`：

- 主体叙述使用中文自然句，不使用纯英文逗号词串作为默认写法。
- 专业摄影、镜头、构图、光影术语保留英文，例如 `medium shot`、`close-up`、`over-the-shoulder`、`rim lighting`。
- 结构化标签保持英文，例如 `<CharacterN>`、`<PropN>`。
- 角色/场景/道具的 `basePrompt` 写“基准状态”，不要写剧情时刻、临时情绪或一次性动作。
- `videoPrompt` 写“当前镜头发生什么”，不要把 JSON 绑定字段混成自然语言说明。

示例：

- `stylePrompt`：`仿真人短剧质感，写实肤质与克制调色，室内以 soft diffused light 为主，人物边缘保留轻微 rim lighting，竖屏 9:16 构图强调近身压迫感。`
- `character.basePrompt`：`二十岁出头的闺秀面相，鹅蛋脸，肤色白净偏冷，眉眼线条细长，发髻整洁，穿浅青色织纹襦裙，站姿克制端正，neutral expression，medium shot。`
- `scene.basePrompt`：`侯府寿安堂的日间内景，厅堂纵深清晰，木质屏风与案几分区明确，暖色自然光从侧窗落入，wide shot 展示礼序空间与主次座位。`
- `prop.basePrompt`：`一支旧式鎏金簪，簪头花丝纹样细密，金属表面有轻微磨痕，冷暖反光克制，hero shot 展示结构与材质。`

## 常用命令

```bash
cuelight-cli workspace current --json
cuelight-cli workspace bind --project-id <projectId> --root <workspacePath>

cuelight-cli project create --title "项目名" --json
cuelight-cli project update <projectId> --total-episodes <n> --duration <seconds> --json
cuelight-cli project status <projectId> --json
cuelight-cli project set-proposal <projectId> --file ./.cuelight/<projectId>/proposal.txt --json
cuelight-cli project set-design <projectId> --file ./.cuelight/<projectId>/design.txt --json

cuelight-cli bible get <projectId> --json
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/world.txt --json
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt --json

cuelight-cli character create <projectId> --name "角色名" --description-file ./.cuelight/<projectId>/characters/role-desc.txt --base-prompt-file ./.cuelight/<projectId>/characters/role-visual.txt --voice-prompt-file ./.cuelight/<projectId>/characters/role-voice.txt --json
cuelight-cli scene create <projectId> --name "场景名" --description-file ./.cuelight/<projectId>/scenes/place-desc.txt --base-prompt-file ./.cuelight/<projectId>/scenes/place-visual.txt --json
cuelight-cli prop create <projectId> --name "道具名" --description-file ./.cuelight/<projectId>/props/item-desc.txt --base-prompt-file ./.cuelight/<projectId>/props/item-visual.txt --json

cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "分集大纲" --json
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt --json
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt --json
cuelight-cli episode status <episodeId> --json

cuelight-cli storyboard import-text <episodeId> --file ./.cuelight/<projectId>/storyboards/episode-1.json --json
cuelight-cli storyboard status <episodeId> --json
cuelight-cli storyboard get <storyboardId> --json
```

## 原稿到落库

用户给本地文本文件时，不把文件交给平台做草稿流程。Agent 直接读取文件，完成以下本地产物后写回：

- 制作参数：计划总集数、单集秒数
- 项目 proposal、design
- Bible 的 worldView、stylePrompt
- 第一集及后续剧集大纲
- 第一集剧本文本
- 角色、场景、道具
- 第一集分镜 JSON

写作要求：

- 先从原稿判断计划总集数和单集秒数，写回 `project update --total-episodes <n> --duration <seconds>`；若设计文本是“60-90 秒”这类范围，结构化 `duration` 默认写较高生产目标（如 90）。
- proposal 要说明核心卖点、受众、类型、主冲突、爽点/反转机制和规模边界。
- design 要说明剧集结构、人物弧光、世界规则、主要关系、单集节奏和可生产约束。
- worldView 写稳定设定，不写临时剧情复述。
- outline 写每集“开场钩子 -> 本集目标 -> 阻力升级 -> 信息/反转 -> 情绪落点 -> 结尾钩子”。
- script/content 必须先满足本集目标时长，再进入分镜；不要靠 storyboard 借用下一集内容补时长。
- 90 秒单集正文建议包含 5 个 beat、12-20 个可拍动作/反应/道具操作、6-12 条有效对白或声音触发点；正文过薄时先扩写剧本。
- 每集必须有清楚边界：本集只拍本集事件；后续集内容只能作为结尾钩子，不进入本集分镜主体。
- script/content 写可拍摄文本，保留人物动作、对白、场景调度、道具/屏幕信息、声音触发和情绪落点。
- 写分镜前先用三位资深编剧视角自检剧本：结构编剧查钩子/目标/反转/悬念和容量，人物编剧查主角主动选择与情绪外化，类型编剧查短剧爽点、危机前兆、信息爆点和可拍狠台词；发现问题先修剧本。
- 角色必须分离保存 `description`、`basePrompt`、`voicePrompt`：介绍写身份关系和叙事功能，视觉提示词写稳定外观，音色写稳定声音特征；不要把 `basePrompt：...` 或 `voicePrompt：...` 混进介绍文件。
- 场景、道具必须分离保存 `description` 和 `basePrompt`：介绍写叙事用途，视觉提示词写可复用基准状态。

## 基础 Storyboard 模板

标准文件：`./.cuelight/<projectId>/storyboards/episode-<number>.json`

```json
[
  {
    "sceneNumber": 1,
    "shotSize": "medium",
    "plannedVideoDurationSeconds": 12,
    "videoPrompt": "【素材定义】\n<Character1>(赵阿萤) 是当前角色参考，<Character2>(赵府荷花池) 是当前场景参考，<Prop1>(玉佩) 是关键道具参考。\n【分镜时序】\n镜头1：medium shot（中景） static shot（固定拍摄），先压住池边的静默空气，<Character1>(赵阿萤) 站在池边右手缓慢按住 <Prop1>(玉佩)，指腹轻轻收紧、目光停在门口方向，荷花池冷光和门廊阴影把她夹在画面中央，远处传来压低的脚步声。\n镜头2：close-up（特写） slow push-in（缓慢推近），只服务她发现异常的情绪压迫，<Character1>(赵阿萤) 指节逐渐发白、肩膀保持克制不动，池边水面反光落在她侧脸和玉佩边缘，空气里只剩钟表轻响和衣料摩擦声。\n【风格画质】\n真人实拍电影写实风格，自然皮肤纹理，真实服装材质，池边冷暖光线克制。",
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

- 必填：`sceneNumber`、`shotSize`、`videoPrompt`、`referenceCharacterIds`、`referenceSceneId`。
- 必填：Seedance 项目必须写 `plannedVideoDurationSeconds`，范围 4-15；非 Seedance 建议也写，或让旧 `分镜N Xs` 自动解析。
- 可选：`referencePropIds`、`dialogues`、`soundEffects`。
- `dialogues` 固定为 `{ character, line }[]`。
- `soundEffects` 固定为 `string[]`。
- 一条 shot 对应一个 object，`sceneNumber` 按导入顺序递增。
- `videoPrompt` 只承担镜头文案；角色、场景、道具的最终绑定分别以 `referenceCharacterIds`、`referenceSceneId`、`referencePropIds` 为准。
- 完整分集分镜的 `plannedVideoDurationSeconds` 总和必须等于项目单集目标时长；例如 90 秒单集可拆成 `12 + 12 + 15 + 12 + 15 + 12 + 12`。
- Seedance `videoPrompt` 推荐三段式：`【素材定义】`、`【分镜时序】`、`【风格画质】`。镜头按事件顺序写 `镜头1` 到最多 `镜头8`。
- 每个 `镜头N：` 必须按固定顺序写四类信息：景别+运镜或镜头切换方式 -> 主体动作与表情 -> 位置或空间变化 -> 同步声音信息。
- 每个镜头开头必须明确景别和运镜，专业英文术语在前，后接中文括注；推荐句式：`镜头N：<shot size 英文>（中文景别） <camera movement 英文>（中文运镜/切换），<主体动作与表情>，<位置或空间变化>，<同步声音/对白/环境声/动作音效>。`
- 景别必须适配项目 `videoAspectRatio`：`16:9 横屏` 优先 `wide shot`、`medium shot`、`two shot`、`over-the-shoulder`、`medium close-up`，适合空间建立、多人关系、车内/仓库/市场调度；`9:16 竖屏` 优先 `medium shot`、`medium close-up`、`close-up`、紧凑 `two shot`，`wide shot` 只用于必要空间建立，`extreme close-up` 只用于证据物或强情绪落点。
- 景别先服务画面内容，再考虑跨景别节奏；不要用竖屏近景逻辑硬套横屏空间戏，也不要用横屏远景逻辑稀释竖屏人物情绪。
- 默认避免相邻镜头只做相邻景别切换；景别层级按 `wide shot -> medium shot -> medium close-up -> close-up -> extreme close-up` 检查，优先跨一个以上景别并承担新的叙事信息。
- 跨分镜组也要检查首尾衔接：上一条 storyboard 的最后一个 `镜头N` 与下一条 storyboard 的 `镜头1` 必须有剪辑理由，例如跨景别、跨空间、跨动作阶段、跨情绪阶段、声音桥接或道具/证据接力。
- 一镜到底也必须补齐四类信息；没有对白时必须写环境声或动作音效，不能只写视觉动作。
- 4-6 秒可写 1-3 个镜头，7-10 秒可写 2-5 个镜头，11-15 秒可写 3-8 个镜头；一镜到底只写 `镜头1`，不要为了凑数量硬拆。
- 动作要具体到手、腿、头部、肩背等部位，补充幅度、速度、力度和动作衔接；情绪要外化为眼神、呼吸、肩背、嘴角、手指、停顿等可见细节。
- 默认不写 BGM、配乐、背景音乐或音乐氛围；只写脚步声、门响、手机提示音、呼吸声、环境声、角色对白或旁白等同步声音。

更完整的分镜时间码、子分镜节奏、绑定和导入规则见 `references/storyboard.md`。

## 纯媒体生成

当用户只要求“生成一张图”“拿这张图改图”“生成一段视频”“用这张图做首帧视频”这类独立媒体产物时，走开放 CLI，不进入项目工作流。

```bash
cuelight-cli image models
cuelight-cli video models

cuelight-cli image generate --prompt "赛博朋克城市的猫" --model <model> --size 16:9 --output out.png
cuelight-cli image generate --prompt "改成夜景霓虹短剧海报质感" --model <model> --image-urls ./reference.png --output poster.png

TASK=$(cuelight-cli video generate --prompt "日落下的海岸" --model <model> --duration 5 --aspect-ratio 9:16 --json | jq -r .task_id)
cuelight-cli task wait "$TASK" --output out.mp4

cuelight-cli video generate --prompt "镜头从人物正面缓慢推近，雨夜霓虹反射" --model <model> --image-urls ./first-frame.png --duration 5 --aspect-ratio 9:16 --output out.mp4
```

约束：

- 不存在公开手工上传引用资源步骤；不要指导用户手工上传引用资源。
- `--image-urls` 是引用资源入口，可用逗号混合多个 URL / 本地路径。
- 不凭 Skill 示例猜模型；先查询模型列表。
- 若用户明确要把产物绑定到某个项目、角色、场景、道具或分镜，再切回对应项目资源命令。

## 验收

完成写回后必须查询：

```bash
cuelight-cli project status <projectId> --json
cuelight-cli episode status <episodeId> --json
cuelight-cli storyboard status <episodeId> --json
```

通过标准：

- proposal、design、worldView、stylePrompt 非空。
- `project status` 的 `planning.totalEpisodes` 与 `planning.durationPerEpisode` 非空，并与 design 中的制作规划一致。
- 第一集 outline 和 script/content 非空。
- 角色、场景、道具至少各 1 个。
- 每个角色有非空 `description`、`basePrompt`、`voicePrompt`；每个场景、道具有非空 `description`、`basePrompt`。
- 资产介绍中不得混写 `basePrompt：`、`voicePrompt：`、`视觉提示词：` 等字段标签。
- 第一集有分镜，且每条分镜有 `videoPrompt`、`referenceCharacterIds`、`referenceSceneId`。
- 关键道具分镜带 `referencePropIds`。
- 用户未明确要求时，没有提交图片、视频或语音任务。

## 参考

- `references/project.md`
- `references/bible.md`
- `references/episode.md`
- `references/storyboard.md`
- `references/character.md`
- `references/scene.md`
- `references/prop.md`
- `references/style.md`
- `references/video-gen.md`
