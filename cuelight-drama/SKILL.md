---
name: cuelight-drama
description: CueLight 剧情项目本地 Agent 工作流指引，覆盖短剧、传统番剧和电影项目。Use when creating, adapting, continuing, reviewing, or producing CueLight projects involving project design, episodes, scripts, characters, scenes, props, storyboard scripts, images, or video tasks. If the project type is unclear, confirm whether it is short-drama, anime-series, or film before applying creative rules.
---

这个 Skill 只说明 CueLight 项目的推进方法、类型 profile 和文本/分镜格式。当前项目、工作区根目录、权限和真实状态必须由本地工作区与 `cuelight-cli` 提供。

## 使用原则

- **先解析工作区**：进入任意工作区后，第一步执行 `cuelight-cli workspace current --json`。
- **未绑定不执行业务命令**：若没有 `./.cuelight/workspace.json` 或 `currentProjectId` 为空，只能引导用户执行 `cuelight-cli workspace bind --project-id <id> --root <path>`。
- **禁止猜项目**：不得从目录名、mock 数据、最近项目、置顶项目或历史聊天猜测当前项目。
- **显式上下文必须一致**：用户明确给出 projectId 时，仍必须与工作区绑定的 `currentProjectId` 一致；不一致时停止并让用户重新绑定或更正参数。
- **CLI 是唯一事实入口**：读状态、写设定、写剧集、写角色场景道具、写分镜、查任务，都通过 `cuelight-cli`。
- **业务请求走统一合同**：公开 CLI 命令只依赖项目、剧集、分镜、任务资源，不让 Agent 决策内部历史结构。
- **文字类默认由本地 Agent 创作并直写**：本地读取用户给的原稿文件，产出 proposal、design、worldView、stylePrompt、episodes、characters、scenes、props、storyboards，再用 CLI 写回。
- **默认不提交媒体生成**：除非用户明确要求，不提交图片、视频或语音任务。

## 类型识别与 Profile

开始创作规则前先确定项目类型：

1. 读取用户话语、项目 `genre`、`design`、`durationPerEpisode`、`videoAspectRatio` 和原稿形态。
2. 能明确判断时，选择一个 profile 并读取对应文件。
3. 类型不明确时，先询问用户确认类型，只给出这三个选项：`短剧`、`番剧`、`电影`。确认后再读取对应 profile 并采用对应节奏、容量和画幅规则。

Profile 路由：

- 短剧：读取 `references/profiles/short-drama.md`。
- 传统番剧：读取 `references/profiles/anime-series.md`。
- 电影：读取 `references/profiles/film.md`。

通用规则只负责 CueLight 结构化落库契约；剧作结构、节奏、镜头密度、风格方向和三位专家自检都以当前 profile 为准。

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
  - `./.cuelight/<projectId>/film-three-act-outline.md`（电影项目本地三幕式规划；当前不通过 CLI 写回）
  - `./.cuelight/<projectId>/film-data/`（电影项目本地影子结构；`.yaml` 原生 YAML 文件，当前不通过 CLI 写回；维护前必须读取 `references/profiles/film-data-local.md` 的多节点、索引和时长汇总规则）
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

## 通用写法

以下规则统一适用于 `stylePrompt`、`character.basePrompt`、`scene.basePrompt`、`prop.basePrompt`、`storyboard.videoPrompt`：

- 主体叙述使用中文自然句，不使用纯英文逗号词串作为默认写法。
- 专业摄影、镜头、构图、光影术语保留英文，例如 `medium shot`、`close-up`、`over-the-shoulder`、`rim lighting`。
- 结构化标签保持英文，例如 `<CharacterN>`、`<SceneN>`、`<PropN>`。
- 特殊字符按信息类型使用：音乐 `（）`，音效 `<>`，台词/心声正文 `{}`，字幕 `【】`。
- 保留 `说台词：`、`心想：` 前缀，但必须写成 `<CharacterN>(角色名) 说台词：{台词内容}` 或 `<CharacterN>(角色名) 心想：{心声内容}`。
- 角色/场景/道具的 `basePrompt` 写“基准状态”；剧情时刻、临时情绪和一次性动作写入具体分镜。
- 角色 `basePrompt` 优先按 CueLight 角色视觉顺序写稳定外观：性别、年龄段、身份、肤色、脸型/五官、体态、发型、服装材质、整体气质和基础镜头建议；详细规则见 `references/character.md`。
- `videoPrompt` 写“当前镜头发生什么”；JSON 绑定字段保持结构化字段。

## 结构化绑定

- Storyboard 场景绑定必须走结构化字段；CueLight 以 `referenceSceneId` / `referenceSceneIds` 为准，新写法在文案中使用 `<SceneN>`。
- 关键道具同时需要文案层和结构层引用：文案里使用 `<PropN>`，关键道具最终必须写入 `referencePropIds`。
- 每个 `<CharacterN>(姓名)` 的动作、台词、心理状态必须符合角色描述、本集正文和 beats；不得把其他角色行为转移到当前绑定角色。
- Seedance 系列 `videoPrompt` 默认使用 `镜头1 / 镜头2 / ...`，不强制每个镜头写精确秒数；`plannedVideoDurationSeconds` 单独写入 4-15 秒。
- 完整分集分镜总时长应落在 `project.durationPerEpisode` 的 90%-110%；单条时长优先遵守当前视频模型能力。

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

- 制作参数：计划总集数、单集秒数。
- 项目 proposal、design。
- Bible 的 worldView、stylePrompt。
- 剧集大纲和剧本文本。
- 角色、场景、道具。
- 分镜 JSON。

写作要求：

- 先根据项目类型和原稿规模判断计划总集数、单集秒数和画幅，写回 `project update --total-episodes <n> --duration <seconds>`。
- proposal 说明核心卖点、受众、类型、主冲突、情绪体验和规模边界。
- design 说明剧集结构、人物弧光、世界规则、主要关系、节奏策略和可生产约束。
- worldView 写稳定设定，不写临时剧情复述。
- episode、style、storyboard 的具体写法先读通用 reference，再读当前 profile。
- 电影项目若维护本地 `film-data/`，先读 `references/profiles/film-data-local.md` 的正向生成流程和 capacity few-shot，再按“三幕/八序列规划 -> Act/Sequence/Scene/Beat 索引 -> screenplay blocks/pages -> Segment/Shot/Prompt/Continuity”生成；交付前用 `cuelight-cli internal film-data duration --strict` 和 screenplay quality strict 获取信号，并由 Agent 主动审查产物、写出证据和放行结论。
- 电影项目若从创意说明、历史分析、人物小传、treatment、舞台剧或小说片段生成 `film-data/`，先读 `references/profiles/film.md` 的 Creative Source Adaptation Pass；把分析性内容放入 bible/outline/metadata，把 `script/blocks.yaml` 写成真正 screenplay。
- 电影项目每完成阶段性 screenplay draft 后，必须执行 `references/profiles/film.md` 的 Literary Rewrite Loop Engineering；默认保持本地 metadata、block id 和 production 绑定稳定，并循环到 screenplay quality strict 与 Agent Literary Review Gate 都通过。
- 电影正式 screenplay 在 Literary Rewrite 通过后、交付或导出前，执行 `references/profiles/film.md` 的 Commercialization Punch-up Pass（商业化强化环节）与 Commercial Review Gate（商业化审查门）；工具 `strict ok` 不能单独放行。
- 电影 workflow 中所有 gate 都是 Agent-owned：duration、pagination、playable capacity、rewrite、DOCX 和 production-ready 不能只靠工具 `strict ok` 放行，必须有 Agent 抽查对象、证据、`pass` / `fail` 和下一步许可。
- 电影项目若要求导出 screenplay DOCX，使用 `scripts/export_film_screenplay_docx.py`，以根级 `film-data/script/pages.yaml` 为分页权威；导出前必须完成 Rewrite、screenplay quality strict 和 Agent 审查。
- 电影项目若验收目标限定为“第一幕完整拆解”，按目标片长和剧情容量预算 `act_001`，生成多 Sequence、多 Scene、多 Beat、4-15 秒 Segment 和多 Shot；第二、三幕可先保持 outline-only。
- 角色必须分离保存 `description`、`basePrompt`、`voicePrompt`；场景、道具必须分离保存 `description` 和 `basePrompt`。

## 纯媒体生成

当用户只要求“生成一张图”“拿这张图改图”“生成一段视频”“用这张图做首帧视频”这类独立媒体产物时，走开放 CLI，不进入项目工作流。

```bash
cuelight-cli image models
cuelight-cli video models

cuelight-cli image generate --prompt "赛博朋克城市的猫" --model <model> --size 16:9 --output out.png
cuelight-cli image generate --prompt "改成夜景霓虹海报质感" --model <model> --image-urls ./reference.png --output poster.png

TASK=$(cuelight-cli video generate --prompt "日落下的海岸" --model <model> --duration 5 --aspect-ratio 16:9 --json | jq -r .task_id)
cuelight-cli task wait "$TASK" --output out.mp4
```

约束：

- 引用资源入口使用 CLI 参数和平台资源绑定；公开流程不包含手工上传引用资源步骤。
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
- 当前阶段要求的 outline、script/content、角色、场景、道具和分镜已写回。
- 每个角色有非空 `description`、`basePrompt`、`voicePrompt`；每个场景、道具有非空 `description`、`basePrompt`。
- 角色 `basePrompt` 不缺失性别、年龄段、脸型/五官、体态、发型、服装材质、整体气质和基础镜头建议，且不把剧情动作、临时情绪或人物关系写成外观提示词。
- 资产介绍中不得混写 `basePrompt：`、`voicePrompt：`、`视觉提示词：` 等字段标签。
- 分镜有 `videoPrompt`、`referenceCharacterIds`、`referenceSceneId`；关键道具分镜带 `referencePropIds`。
- 用户未明确要求时，没有提交图片、视频或语音任务。

## 参考

- `references/profiles/short-drama.md`
- `references/profiles/anime-series.md`
- `references/profiles/film.md`
- `references/profiles/film-data-local.md`
- `references/project.md`
- `references/bible.md`
- `references/episode.md`
- `references/storyboard.md`
- `references/character.md`
- `references/scene.md`
- `references/prop.md`
- `references/style.md`
- `references/video-gen.md`
