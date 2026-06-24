# Project

项目命令必须在绑定工作区内执行，创建项目除外。

```bash
cuelight-cli project create --title "项目名" --json
cuelight-cli workspace bind --project-id <projectId> --root <workspacePath>
cuelight-cli workspace current --json
cuelight-cli project update <projectId> --total-episodes <n> --duration <seconds> --json
cuelight-cli project status <projectId> --json
cuelight-cli project set-proposal <projectId> --file ./.cuelight/<projectId>/proposal.txt --json
cuelight-cli project set-design <projectId> --file ./.cuelight/<projectId>/design.txt --json
```

## 工作区规则

- 创建项目后立即绑定工作区。
- 后续显式 projectId 必须等于绑定项目。
- 不从本地目录名、mock 数据、最近项目或置顶项目推断项目。
- `./.cuelight/workspace.json` 不保存 API Key。

## 制作参数

原稿拆解后必须把计划集数和单集秒数写入结构化项目字段，不只写在 design 文本里。

```bash
cuelight-cli project update <projectId> --total-episodes 12 --duration 90 --json
```

规则：

- `totalEpisodes` 写计划完整剧集数，不是当前已创建剧集数。
- `duration` 写单集生产目标秒数；如果设计文本是 `60-90 秒`，结构化字段默认写较高目标 `90`。
- 写入后用 `project status --json` 检查 `planning.totalEpisodes` 和 `planning.durationPerEpisode`。

## Proposal

proposal 是给后续拆剧和生产判断用的项目提案，不是简介。

必须覆盖：

- 类型与题材：如古装宅斗、现代甜宠、悬疑反转、亲子教育短视频。
- 核心卖点：一句话说明用户为什么要看。
- 主冲突：主角目标、阻力、对抗关系。
- 爽点/钩子机制：误会、反转、身份揭露、惩戒、情感拉扯等。
- 目标受众与平台语气：决定节奏、对白密度和画面尺度。
- 生产边界：主要场景数量、角色规模、是否大量依赖特效或高成本动作。

不要写：

- 只有宣传语，没有可执行信息。
- 大段世界观铺陈但没有主冲突。
- 把每集剧情都塞进 proposal。

## Design

design 是项目生产设计，应能指导剧集、角色、场景、分镜继续生成。

必须覆盖：

- 剧集结构：总集数预期、单集时长感、每集结尾钩子方式。
- 主线推进：开局、升级、反转、高潮、收束。
- 人物弧光：主角起点、弱点、成长或黑化方向。
- 关系网络：亲密关系、对抗关系、利益关系。
- 视觉基调：时代、色彩、镜头距离、质感关键词。
- 资产复用计划：核心场景、常驻角色、关键道具。

写入后用 `project status` 验证 proposal/design/worldView/stylePrompt 是否非空，并确认 `planning.totalEpisodes/durationPerEpisode` 与 design 声明一致。
