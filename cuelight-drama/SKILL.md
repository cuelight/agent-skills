---
name: cuelight-drama
description: CueLight CLI 入口与项目写回工作流。Use when Codex needs to read or write CueLight projects through cuelight-cli, bind a local workspace, prepare project-local files, import episodes/storyboards/assets metadata, query task/status, or coordinate CueLight project I/O. For creative rules, route short drama work to $cuelight-shortdrama and film work to $cuelight-film.
---

这个 Skill 只负责 CueLight 项目 I/O、CLI 合同、工作区绑定、平台字段格式和写回验收；不承载短剧或电影的剧作结构规则。创作、诊断、改写和本地类型元数据先按作品类型读取对应 Skill：

- 短剧、短视频连续剧、网文式短剧改编：使用 `$cuelight-shortdrama`。
- 电影、长片、短片、电影化 screenplay、film-data：使用 `$cuelight-film`。

## 使用原则

- **先解析工作区**：进入任意 CueLight 项目工作区后，第一步执行 `cuelight-cli workspace current --json`。
- **未绑定不执行业务命令**：若没有 `./.cuelight/workspace.json` 或 `currentProjectId` 为空，只能引导用户执行 `cuelight-cli workspace bind --project-id <id> --root <path>`。
- **禁止猜项目**：不得从目录名、mock 数据、最近项目、置顶项目或历史聊天猜测当前项目。
- **显式上下文必须一致**：用户明确给出 projectId 时，仍必须与工作区绑定的 `currentProjectId` 一致；不一致时停止并让用户重新绑定或更正参数。
- **CLI 是唯一事实入口**：读状态、写设定、写剧集、写角色场景道具、写分镜、查任务，都通过 `cuelight-cli`。
- **文字类先本地产出再写回**：读取用户给的本地原稿或类型 Skill 产物，整理为 proposal、design、worldView、stylePrompt、episodes、characters、scenes、props、storyboards，再用 CLI 写回。
- **默认不提交媒体生成**：除非用户明确要求，不提交图片、视频或语音任务。

## 类型路由

开始创作规则前先确定作品类型：

1. 读取用户话语、项目 `genre`、`design`、`durationPerEpisode`、`videoAspectRatio` 和原稿形态。
2. 能明确判断时，读取对应类型 Skill。
3. 类型不明确时，只询问用户确认：`短剧` 或 `电影`。

路由规则：

- 短剧：读取 `$cuelight-shortdrama`，由该 Skill 决定短剧节奏、容量、钩子、分集和本地元数据。
- 电影：读取 `$cuelight-film`，由该 Skill 决定三幕/八序列、screenplay、film-data、质量 gate 和导出。

`cuelight-drama` 只负责把类型 Skill 产物转换为 CueLight 平台字段和 CLI 写回命令。

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

优先使用官方一键安装脚本。安装脚本会把 `cuelight-drama`、`cuelight-shortdrama`、`cuelight-film` 等 Agent Skills 安装到用户级全局位置，同时安装 `cuelight-cli`，不依赖当前项目目录。

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

## 本地目录职责

`.cuelight/` 是 CueLight 运行时和导入桥，不是短剧或电影的长期创作元数据目录。

- `./.cuelight/workspace.json`、`./.cuelight/config.json`：工作区绑定与 CLI 配置。
- `./.cuelight/<projectId>/source/`：`source materialize` 生成的平台原稿副本。
- `./.cuelight/<projectId>/staging/import/`：写回 CueLight 前的派生文本/JSON 暂存。
- `./.cuelight/<projectId>/staging/film-data/`：电影 canonical `film-data/` 的导入/校验暂存副本，不作为长期源数据。
- `./.cuelight/<projectId>/sync/link.json`：仅由 `$cuelight-drama` 在准备 staging 或导入后维护的桥接记录；没有该文件时不得猜测同步状态。

Staging 规则：

- `staging/` 是一次性派生物，不是创作源文件；需要改内容时，先改 `cuelight-projects/<type>/<project-slug>/` 下的 canonical 项目，再重新派生 staging。
- 不把 `staging/import/storyboards/*.json`、`staging/film-data/**/prompt.yaml`、`staging/film-data/**/script-links.yaml` 的手工修改反向当作 canonical，除非用户明确要求做 merge，并在 `sync/link.json` 记录来源和时间。
- 外置 Codex 全流程因为 sandbox 限制只写 `.cuelight/<projectId>/staging/` 时，该 staging bundle 只服务本轮 CLI 导入；不生成也不替代 `cuelight-projects/` 长期项目。

`sync/link.json` 最小结构：

```json
{
  "version": 1,
  "type": "shortdrama",
  "canonicalRoot": "cuelight-projects/shortdrama/example",
  "stagingRoot": ".cuelight/project-id/staging",
  "lastPreparedAt": "2026-06-29T00:00:00Z",
  "lastImportedAt": null
}
```

`type` 只允许 `shortdrama` 或 `film`；`canonicalRoot` 可为 `null`，表示当前 staging bundle 来自外置 Codex 一次性工作流，没有长期 canonical 项目。

推荐 import staging 布局：

- `./.cuelight/<projectId>/staging/import/proposal.txt`
- `./.cuelight/<projectId>/staging/import/design.txt`
- `./.cuelight/<projectId>/staging/import/world.txt`
- `./.cuelight/<projectId>/staging/import/style-prompt.txt`
- `./.cuelight/<projectId>/staging/import/characters/<name>-desc.txt`
- `./.cuelight/<projectId>/staging/import/characters/<name>-visual.txt`
- `./.cuelight/<projectId>/staging/import/characters/<name>-voice.txt`
- `./.cuelight/<projectId>/staging/import/scenes/<name>-desc.txt`
- `./.cuelight/<projectId>/staging/import/scenes/<name>-visual.txt`
- `./.cuelight/<projectId>/staging/import/props/<name>-desc.txt`
- `./.cuelight/<projectId>/staging/import/props/<name>-visual.txt`
- `./.cuelight/<projectId>/staging/import/episodes/episode-<number>-outline.txt`
- `./.cuelight/<projectId>/staging/import/episodes/episode-<number>-script.txt`
- `./.cuelight/<projectId>/staging/import/storyboards/episode-<number>.json`

类型 Skill 独立模式下的 `cuelight-projects/shortdrama/`、`cuelight-projects/film/` 是长期 canonical 创作目录，不要求存在 CueLight projectId；只有写回平台时才派生到 `./.cuelight/<projectId>/staging/`。

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
cuelight-cli project set-proposal <projectId> --file ./.cuelight/<projectId>/staging/import/proposal.txt --json
cuelight-cli project set-design <projectId> --file ./.cuelight/<projectId>/staging/import/design.txt --json

cuelight-cli bible get <projectId> --json
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/staging/import/world.txt --json
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/staging/import/style-prompt.txt --json

cuelight-cli character create <projectId> --name "角色名" --description-file ./.cuelight/<projectId>/staging/import/characters/role-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/characters/role-visual.txt --voice-prompt-file ./.cuelight/<projectId>/staging/import/characters/role-voice.txt --json
cuelight-cli scene create <projectId> --name "场景名" --description-file ./.cuelight/<projectId>/staging/import/scenes/place-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/scenes/place-visual.txt --json
cuelight-cli prop create <projectId> --name "道具名" --description-file ./.cuelight/<projectId>/staging/import/props/item-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/props/item-visual.txt --json

cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "分集大纲" --json
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/staging/import/episodes/episode-1-outline.txt --json
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/staging/import/episodes/episode-1-script.txt --json
cuelight-cli episode status <episodeId> --json

cuelight-cli storyboard import-text <episodeId> --file ./.cuelight/<projectId>/staging/import/storyboards/episode-1.json --json
cuelight-cli storyboard status <episodeId> --json
cuelight-cli storyboard get <storyboardId> --json
```

## 原稿或类型产物到落库

用户给本地文本文件或类型 Skill 已生成的本地产物时，不把文件交给平台做草稿流程。Agent 直接读取文件，按类型 Skill 完成内容后写回：

- 制作参数：计划总集数、单集秒数。
- 项目 proposal、design。
- Bible 的 worldView、stylePrompt。
- 剧集大纲和剧本文本。
- 角色、场景、道具。
- 分镜 JSON。

写回要求：

- 先根据项目类型和产物规模判断计划总集数、单集秒数和画幅，写回 `project update --total-episodes <n> --duration <seconds>`。
- proposal 说明核心卖点、受众、类型、主冲突、情绪体验和规模边界。
- design 说明剧集结构、人物弧光、世界规则、主要关系、节奏策略和可生产约束。
- worldView 写稳定设定，不写临时剧情复述。
- episode、style、storyboard 的具体内容遵守通用 reference 和当前类型 Skill。
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

- `references/project.md`
- `references/bible.md`
- `references/episode.md`
- `references/storyboard.md`
- `references/character.md`
- `references/scene.md`
- `references/prop.md`
- `references/style.md`
- `references/video-gen.md`
