---
name: cuelight-drama
description: 短剧制作全链路工作流指引。当用户提及"短剧"、"做剧"、"drama"、"导演模式"、"视觉设定"、"选角"、"角色与场景"、"分镜设计"、"制作列表"、"视频素材库"、"影片制作"、"生成视频"、"导出视频"等关键词时触发。引导 Agent 按 AI Drama Factory 的 UI 工作流推进短剧制作，并在需要时通过 `@cuelight/cli`（命令名 `cuelight-cli`）执行对应操作。
---

这个 Skill 用于把短剧制作任务对齐到 **AI Drama Factory / CueLight 的真实 UI 工作流**，同时保留 `@cuelight/cli` 作为可执行入口。

使用原则：
- **UI 优先**：先按产品里的工作台结构理解任务，再决定用哪些命令执行
- **全链路覆盖**：保留从项目前置准备到视频导出的完整链路
- **CLI 并列**：每个阶段同时给出 UI 中的入口和常用 CLI 命令
- **不要机械套 10 步流水线**：以当前项目状态为准，缺什么补什么，而不是默认从头重做

## 环境配置

```bash
# 安装公开 CLI 包
npm install -g @cuelight/cli

# 验证安装
cuelight-cli --help

# 如需连接本地服务，请显式覆盖默认地址（默认值为 https://cuelight.app）
cuelight-cli config set url http://localhost:3000

# 验证连接
cuelight-cli project list
```

## UI 心智模型

### 1. 编剧前置准备

导演层开始之前，通常需要先有：
- 项目基础信息
- Bible / 世界观基础设定
- 至少部分角色、场景、剧集内容

对应参考：
- [project.md](references/project.md)
- [bible.md](references/bible.md)
- [episode.md](references/episode.md)

### 2. 导演模式三阶段

导演工作流以仓库现有阶段名为准：
1. **视觉设定**
2. **分镜设计**
3. **影片制作**

在 UI 中，大致对应：
- 资产区：`角色与场景 (Visuals)`、`视频素材库 (Video Library)`
- 制作区：`制作列表 (Production)`、集内 `分镜设计与生产`

## 阶段速查

### 前置创建与导入

| 场景 | UI 语义 | 常用命令 |
|------|---------|---------|
| 新建项目 | 创建短剧项目 | `cuelight-cli project create --title "..." --genre "..." --total-episodes N --duration N` |
| 从原文导入 | 从小说/剧本建立项目草稿 | `cuelight-cli source create-draft --title "..." --file ./novel.txt` |
| 初始化 Bible | 生成项目级基础设定 | `cuelight-cli bible generate <projectId>` |
| 规划剧集 | 生成全剧大纲 | `cuelight-cli episode generate <projectId>` |
| 续写/润色剧本 | 补齐单集内容 | `cuelight-cli episode generate-script <episodeId> --action continue\|polish\|expand` |

### 第一阶段：视觉设定

| 场景 | UI 语义 | 常用命令 |
|------|---------|---------|
| 应用风格 | 设置全局视觉风格 | `cuelight-cli style apply <projectId> --preset-id <id>` |
| 补角色图 | 角色参考图准备 | `cuelight-cli character batch-generate-images <projectId>` |
| 补角色视频 | 角色展示视频准备 | `cuelight-cli character batch-generate-videos <projectId>` |
| 补场景图 | 场景参考图准备 | 见 [scene.md](references/scene.md) 中相关命令 |

### 第二阶段：分镜设计

| 场景 | UI 语义 | 常用命令 |
|------|---------|---------|
| 首次生成分镜 | 为某集生成可拍分镜 | `cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait` |
| 修复绑定缺失 | 自动补充角色/场景绑定 | `cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait` |
| 优化单条提示词 | 调整某个分镜质量 | `cuelight-cli ai optimize-prompt <storyboardId>` |
| 手动改单条分镜 | 精确更新 prompt / 绑定 | `cuelight-cli storyboard update <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..."` |

### 第三阶段：影片制作

| 场景 | UI 语义 | 常用命令 |
|------|---------|---------|
| 批量出片 | 整集批量生成视频 | `cuelight-cli ai batch-submit-videos <episodeId>` |
| 单条测试 | 先验证某个分镜效果 | `cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --persist` |
| 等待任务 | 跟踪生成进度 | `cuelight-cli ai wait <taskId> --timeout 600` |
| 导出成片 | 导出整集合并视频 | `cuelight-cli video export <episodeId>` |

## 全链路工作流（按 UI 组织）

### 1. 编剧前置准备

#### UI 中在哪做

- 项目创建、项目导入
- 编剧模式中的 Bible / 剧集 / 剧本内容准备

#### 这一阶段的目标

- 让导演层有可用的项目上下文，而不是在没有剧集和设定的情况下直接做分镜或出片

#### 前置条件

- 如果项目尚未存在，先创建或导入
- 如果完全没有 Bible / 剧集内容，先补齐最基本的故事材料

#### 关键检查项

- 项目标题、题材、总集数等基础字段已存在
- 至少已有 Bible 基础设定或原文来源
- 至少一集有可用的大纲或剧本内容

#### 常用 CLI 命令

```bash
cuelight-cli project create --title "..." --genre "..." --total-episodes N --duration N
cuelight-cli source create-draft --title "..." --file ./novel.txt
cuelight-cli bible generate <projectId>
cuelight-cli episode generate <projectId>
cuelight-cli episode generate-script <episodeId> --action continue
```

#### 何时进入下一阶段

- 当项目已有可用的角色/场景设定基础，且至少存在可供导演参考的剧集内容时，进入 **视觉设定**

### 2. 导演第一阶段：视觉设定

#### UI 中在哪做

- 导演模式顶部阶段条：`视觉设定`
- 资产区 `角色与场景 (Visuals)`
- 全局风格、角色卡、场景卡

#### 这一阶段的目标

- 把“能拍什么”转成“应该长什么样”
- 补齐全局风格、角色参考素材、场景参考素材

#### 前置条件

- 已有项目和基础故事上下文
- 最好已经有角色、场景或 Bible 初稿；没有也可以在此阶段补建

#### 关键检查项

- `stylePrompt` 或等价全局风格已设定
- 全局参考图已具备
- 关键角色至少有 `basePrompt`
- 需要展示视频的角色，已具备图像后再生成视频
- 关键场景至少有 `basePrompt` 和参考图

#### 常用 CLI 命令

```bash
cuelight-cli style apply <projectId> --preset-id <id>
cuelight-cli character batch-generate-images <projectId>
cuelight-cli character batch-generate-videos <projectId>
```

补充参考：
- [style.md](references/style.md)
- [character.md](references/character.md)
- [scene.md](references/scene.md)

#### 何时进入下一阶段

- 当主要角色、主要场景、全局风格都足以支撑分镜生成时，进入 **分镜设计**

### 3. 导演第二阶段：分镜设计

#### UI 中在哪做

- 导演模式 `制作列表 (Production)`
- 进入某一集后，在 `分镜设计与生产` 工作区处理

#### 这一阶段的目标

- 把单集剧本转成可执行分镜
- 修复角色/场景绑定缺失，避免后续视频生成失败

#### 前置条件

- 该集已有剧本内容或足够明确的剧情结构
- 至少主要角色、主要场景、全局风格已准备好

#### 关键检查项

- 分镜已生成，不是空列表
- `referenceCharacterIds` 与 `referenceSceneId` 不缺失
- 手动调整过的分镜不要被无提示覆盖
- 发现绑定缺失时，优先做自动补充和修复

#### 常用 CLI 命令

```bash
cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait
cuelight-cli ai optimize-prompt <storyboardId>
cuelight-cli storyboard update <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..."
```

补充参考：
- [storyboard.md](references/storyboard.md)
- [episode.md](references/episode.md)

#### 何时进入下一阶段

- 当目标剧集已经有可拍分镜，且角色/场景绑定完整时，进入 **影片制作**

### 4. 导演第三阶段：影片制作

#### UI 中在哪做

- 导演模式 `制作列表 (Production)`
- 集内 `分镜设计与生产`
- 资产区 `视频素材库 (Video Library)` 用于回看生成结果

#### 这一阶段的目标

- 基于已就绪的分镜和参考资产生成视频片段
- 在视频素材库汇总、回看和后续导出

#### 前置条件

- 分镜已完成
- 角色与场景引用素材已就绪
- 对批量生成范围有明确边界

#### 关键检查项

- 不要在绑定不完整时直接生成视频
- 批量生成前先确认影响范围
- 单条效果不确定时，先做单条测试，再决定是否整集批量出片

#### 常用 CLI 命令

```bash
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --persist
cuelight-cli ai batch-submit-videos <episodeId>
cuelight-cli ai wait <taskId> --timeout 600
```

补充参考：
- [video-gen.md](references/video-gen.md)

#### 何时进入下一阶段

- 当目标集的视频片段已生成并确认可交付时，进入 **导出与交付**

### 5. 导出与交付

#### UI 中在哪做

- 视频素材库查看结果
- 对目标剧集执行导出

#### 这一阶段的目标

- 输出整集或阶段性成片

#### 前置条件

- 视频任务已完成
- 目标集已有可导出的片段结果

#### 常用 CLI 命令

```bash
cuelight-cli video export <episodeId>
```

#### 关键检查项

- 导出前确认目标剧集和版本
- 不把测试片段误当正式交付结果

## 决策矩阵

### 分镜生成策略

| 场景 | 推荐命令 | 说明 |
|------|---------|------|
| 首次生成某集分镜 | `cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait` | 默认首选，兼顾生成与修复 |
| 生成后有缺失绑定 | `cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait` | 先补角色/场景，再继续 |
| 单个分镜提示词不佳 | `cuelight-cli ai optimize-prompt <storyboardId>` | 先局部优化，不急着全量重做 |
| 重新生成整集（覆盖） | `cuelight-cli storyboard generate <episodeId>` | ⚠️ 会覆盖已有分镜 |
| 手动改单个分镜 | `cuelight-cli storyboard update <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..."` | 精确控制 |

### 视频生成策略

| 场景 | 推荐命令 | 说明 |
|------|---------|------|
| 整集批量出片 | `cuelight-cli ai batch-submit-videos <episodeId>` | 常规制作路径 |
| 单个分镜测试 | `cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId> --persist` | 先验证质感与稳定性 |
| 带风格注入 | `cuelight-cli ai produce <episodeId> <storyboardId> --style-prompt "..." --aspect-ratio "9:16"` | 需要更完整控制时使用 |
| 固定 seed 复现 | `cuelight-cli ai submit-video <storyboardId> --seed 42 --episode-id <episodeId>` | 便于复拍和比对 |

## Agent 行为约束

### 禁止行为

- **禁止**把 skill 仍当成纯 CLI 十步流水线来执行，先看当前项目状态，再决定缺哪一层
- **禁止**在分镜绑定不完整时直接生成视频（`referenceCharacterIds` 为空或 `referenceSceneId` 为空）
- **禁止**在未确认的情况下删除项目或覆盖已有分镜
- **禁止**输出 API key 等敏感配置信息

### 确认要求

- 重新生成整集分镜（会覆盖）前必须告知用户
- 删除项目/剧集/角色前必须确认
- 批量操作（>5 个）前告知用户数量和影响

### 执行规则

- 每步操作后检查返回结果，不要盲目继续
- 生成分镜后**必须**检查未绑定分镜并修复
- Season-bound 项目中新增的角色/场景必须同步到 season bindings
- 优先使用 `--auto-supplement --repair-bindings --wait` 组合
- 先用 UI 语言理解任务，再落到 CLI 命令，不要反过来主导用户

## 故障排查

| 症状 | 原因 | 修复 |
|------|------|------|
| `ECONNREFUSED` / 连接失败 | 服务未启动或地址错误 | `cuelight-cli config get url` 检查地址；确认服务运行 |
| HTTP 401/403 | API key 错误或未配置 | `cuelight-cli config set api-key <key>` |
| 圣经生成返回空内容 | 项目缺少基础信息 | 先补充 `--genre`、`--total-episodes` 等字段 |
| 分镜 `referenceCharacterIds` 为空 | 剧本中角色名与已有角色不匹配 | 执行 `cuelight-cli storyboard generate --auto-supplement --repair-bindings --wait` |
| 视频生成失败 | 角色缺少 `referenceImageUrl` | `cuelight-cli character batch-generate-images <projectId>` |
| 视频生成失败 | 分镜 `videoPrompt` 为空 | `cuelight-cli storyboard get <id>` 检查；`cuelight-cli ai optimize-prompt <id>` 优化 |
| AI 任务超时 | 任务复杂或排队中 | `cuelight-cli ai wait <taskId> --timeout 900 --interval 5` |
| 生成质量不佳 | 风格提示词不够具体 | `cuelight-cli bible update <projectId> --style-prompt "更具体的描述"` |
| 分镜覆盖了手动调整 | 重新执行了 `cuelight-cli storyboard generate` | ⚠️ generate 会覆盖，用 `--auto-supplement` 修复而非重新生成 |

## 核心概念

- **Project** → 一个短剧项目，包含多集
- **Bible** → 项目的基础设定容器，承接风格、角色概述、场景概述
- **Season** → 季度，project 可包含多个 season
- **Episode** → 剧集，包含剧本内容（content）和分镜列表
- **Storyboard** → 分镜，每个对应一个镜头（`videoPrompt` + 角色/场景绑定 + 首帧）
- **Character** → 角色（`name` + `basePrompt` + `referenceImageUrl` + `referenceVideoUrl`）
- **Scene** → 场景（`name` + `basePrompt` + `referenceImageUrl`）
- **ID 关系**：`project -> bible / episodes / characters / scenes`；`episode -> storyboards`；`storyboard -> referenceCharacterIds + referenceSceneId`
