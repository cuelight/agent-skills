---
name: cuelight-drama
description: 短剧制作全链路工作流指引。当用户提及"短剧"、"做剧"、"drama"、"导演模式"、"视觉设定"、"选角"、"角色与场景"、"分镜设计"、"制作列表"、"视频素材库"、"影片制作"、"生成视频"、"导出视频"等关键词时触发。引导 Agent 通过 `@cuelight/cli`（命令名 `cuelight-cli`）读取项目状态、编辑文字资源并推进项目；Skill 仅负责流程指导。
---

这个 Skill 只负责说明 CueLight 的项目推进方法，不提供项目运行时状态。所有状态读取、资源详情查询、文字写回、生成任务提交都必须通过 `cuelight-cli` 完成。

## 使用原则

- **CLI 是唯一事实入口**：先查状态，再决定下一步
- **Skill 不承载状态**：不要从 Skill 推断当前项目已经做到哪一步
- **文字类默认由外部 agent 创作并直写**：proposal、design、worldView、角色、场景、Episode outline/script、Storyboard 文本等，默认都先由外部 agent 自己完成，再通过 CLI 落库
- **Storyboard 的场景绑定必须走结构化字段**：`本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算最终引用；CueLight 以 `referenceSceneId` 为准，并由服务端归一化 scene header
- **内置文本生成仅作兜底**：除非用户明确要求、外部 agent 明确失败，或需要对照/补救，否则不要把系统内置文本生成当作主路径
- **生成类继续走内置能力**：图片、视频、语音仍通过现有 AI 命令提交和轮询
- **不要默认从头开始**：用户说“继续项目”时，先执行状态命令

## 环境配置

```bash
bun add -g @cuelight/cli
cuelight-cli --help
cuelight-cli doctor fix-binary
cuelight-cli config set url http://localhost:3000
cuelight-cli project list
```

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
- 若项目是 `adaptation`，先读取 source / draft / scope / current season，再由外部 agent 自行判断 proposal、design、分集与正文
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
cuelight-cli bible set-world <projectId> --file ./world.txt
cuelight-cli director set-style-prompt <projectId> --file ./style-prompt.txt
cuelight-cli director configure-visuals <projectId> --visual-mode improv --shooting-mode omni_reference --video-ratio 9:16
cuelight-cli season update <projectId> <seasonId> --proposal "..." --design "..."
cuelight-cli episode set-outline <episodeId> --file ./outline.txt
cuelight-cli episode set-script <episodeId> --file ./script.txt
cuelight-cli director import-storyboards <episodeId> --file ./storyboards.json
cuelight-cli asset set-content <projectId> <assetId> --file ./asset.txt
```

仍可继续使用已有细粒度更新命令：

```bash
cuelight-cli bible update <projectId> --world-view "..."
cuelight-cli episode update <episodeId> --content-file ./script.txt
cuelight-cli director update-storyboard <storyboardId> --video-prompt "..."
cuelight-cli asset update <projectId> <assetId> --content-file ./asset.txt
```

执行原则：

- 文字内容默认不要先调用系统内置文本生成工具
- 先由外部 agent 根据已读取的原稿、source、scope、season 状态自行产出内容
- 产出后优先写成本地文件，再用 CLI 写回
- 同一资源按顺序写入，不并发提交，避免覆盖
- 若 storyboard prompt 中写了 `本片段场景设定在：...`，在最终落库前必须同时写入 `referenceSceneId`；不要把裸场景名当成唯一绑定来源
- 不要假设 `<Character4>` 之类的 scene tag 在不同分镜里含义固定；场景 tag 取决于当前分镜自身的绑定资源顺序

当且仅当以下情况，才考虑使用内置文本生成命令：

- 用户明确要求使用系统内置生成
- 外部 agent 明确失败，需要补救
- 需要做对照、润色或局部补缺

### 3. 最后提交生成任务

仅在文字和绑定状态就绪后再进入生成阶段：

```bash
cuelight-cli character batch-generate-images <projectId>
cuelight-cli scene batch-generate-images <projectId>
cuelight-cli director generate-style-image <projectId>
cuelight-cli director generate-storyboards <episodeId> --auto-supplement --repair-bindings --wait
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
cuelight-cli season update <projectId> <seasonId> --proposal "..." --design "..."
cuelight-cli bible set-world <projectId> --file ./world.txt
cuelight-cli episode set-outline <episodeId> --file ./outline.txt
cuelight-cli episode set-script <episodeId> --file ./script.txt
```

若项目是 `my_script`：

- 先读原稿全文
- 外部 agent 自行完成容量判断和分集策略
- 先写回 `totalEpisodes` / `plannedEpisodes` / `durationPerEpisode`
- 再继续 proposal、design、角色、场景、outline、script

### 视觉设定

目标：

- `stylePrompt` 已就绪
- 关键角色、场景具备生成参考图的条件

推荐命令链：

```bash
cuelight-cli director status <projectId> --json
cuelight-cli director visual-status <projectId> --json
cuelight-cli style list-presets --json
```

需要写内容时：

```bash
cuelight-cli director set-style-prompt <projectId> --file ./style-prompt.txt
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
cuelight-cli director import-storyboards <episodeId> --file ./storyboards.json
cuelight-cli director update-storyboard <storyboardId> --video-prompt "..." --ref-character-ids "..." --ref-scene-id "..."
cuelight-cli director generate-storyboards <episodeId> --auto-supplement --repair-bindings --wait
```

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

## Fallback 命令

若 `director` 命令组暂时无法覆盖某个细节操作，再回退到现有底层命令：

```bash
cuelight-cli bible update <projectId> ...
cuelight-cli storyboard list <episodeId> --json
cuelight-cli storyboard update <storyboardId> ...
cuelight-cli ai submit-video <storyboardId> --episode-id <episodeId>
cuelight-cli ai batch-submit-videos <episodeId>
cuelight-cli ai wait <taskId>
cuelight-cli video export <episodeId>
```

## 参考文档

- [project.md](references/project.md)
- [director.md](references/director.md)
- [bible.md](references/bible.md)
- [episode.md](references/episode.md)
- [storyboard.md](references/storyboard.md)
- [character.md](references/character.md)
- [scene.md](references/scene.md)
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
