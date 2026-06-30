# 本地落盘产物契约

当用户要求“创作一个剧本”“完整项目”“本地落盘”“生成产物”“保存为文件”时，按本契约组织输出。默认根目录：

```text
cuelight-projects/shortdrama/<project-slug>/
```

`<project-slug>` 使用小写英文、数字和连字符；如果用户只给中文标题，先生成可读 slug，例如《她在离婚夜封神》用 `divorce-night-queen`。

## 目录

- [标准目录](#标准目录)
- [产物定义](#产物定义)
- [可选分镜支线](#可选分镜支线)
- [落盘顺序](#落盘顺序)

## 标准目录

```text
<project-slug>/
├── manifest.json
├── 00-brief.md
├── 01-concept.md
├── 02-characters.md
├── 03-story-machine.md
├── 04-season-outline.md
├── episodes/
│   ├── ep-001.md
│   └── ep-002.md
├── quality-check.md
└── exports/
    └── full-script.md
```

如果用户只要大纲，可以先生成 `manifest.json` 到 `04-season-outline.md` 和 `quality-check.md`；如果用户要可拍剧本，至少生成第一集 `episodes/ep-001.md`。`exports/full-script.md` 是固定占位产物，脚手架可以创建；只有用户需要整稿、汇总稿或交付稿时才填充完整内容。

## 产物定义

### manifest.json

机器可读索引。必须包含项目标题、slug、类型、主情绪、集数、产物路径、状态。

`status` 只允许：

- `scaffold`：脚手架已创建，正文产物尚未填充。
- `draft`：已有可读初稿，但仍可能缺集、缺分镜或未完成总检。
- `partial`：用户只要求部分产物，未覆盖完整短剧项目。
- `ready`：当前请求范围内的产物、路径和 `quality-check.md` 已完成收口。

```json
{
  "title": "她在离婚夜封神",
  "slug": "divorce-night-queen",
  "format": "短剧",
  "primaryEmotion": "复仇爽",
  "episodeCount": 24,
  "status": "draft",
  "artifacts": {
    "brief": "00-brief.md",
    "concept": "01-concept.md",
    "characters": "02-characters.md",
    "storyMachine": "03-story-machine.md",
    "seasonOutline": "04-season-outline.md",
    "episodes": "episodes/",
    "qualityCheck": "quality-check.md",
    "fullScript": "exports/full-script.md"
  }
}
```

### 00-brief.md

记录用户需求和交付边界，不做文学扩写。

必须包含：

- 原始需求
- 目标形式：短剧 / 短视频连续剧 / 网文式短剧改编 / 分镜源文本等
- 目标观众
- 主情绪
- 集数、单集时长或字数
- 禁区：不能写什么、不能碰什么、必须避开的表达
- 已确认假设

### 01-concept.md

定义故事的商业承诺。

必须包含：

- 一句话故事
- 观众承诺：“这个故事让观众感到 ___”
- 幻想兑现
- 现实缺口
- 故事发动机：人物驱动 / 事件驱动 / 情绪驱动
- 主梦境订单
- 第一屏如何证明主梦境订单
- 付费点或追更点
- 第一屏钩子

### 02-characters.md

把人物写成可制造剧情的装置，而不是简历。

每个主要人物必须包含：

- 外显身份
- 内含欲望
- 伤口或秘密
- 与主角的关系压力
- 能主动制造的事件
- 情绪功能：让观众爽、虐、急、怕、笑或心疼什么

主角必须额外包含：

- 可执行目标
- 不可退让的底线
- 第一集能被看见的弱势
- 中后段能被看见的反击能力

反派必须额外包含：

- 压迫手段
- 误判主角的点
- 阶段性升级动作
- 被打脸时的公众代价

### 03-story-machine.md

定义故事如何持续生产冲突。

必须包含：

- 主欲望
- 主阻碍
- 核心信息差：观众知道什么，主角知道什么，反派知道什么
- 信息牌投放：台词、动作/表情、道具/环境、旁白/闪回
- 预期循环：每一轮如何建立期待、阻断期待、兑现或反转
- 升级阶梯：压力从轻到重的 5-8 级
- 有效事件检查：关键事件是否有冲突、有改变、有目的
- 爽点 / 虐点 / 甜点 / 悬念点的分布原则
- 每集至少改变的变量：地位、关系、危险、秘密、资源或情绪温度

### 04-season-outline.md

给出全剧结构。

短剧建议包含：

- 总集数
- 4-6 个阶段
- 每阶段的主矛盾、情绪任务、关键反转
- 分集表：集数、标题、本集目标、核心冲突、结尾钩子

复杂短剧或网文式短剧改编建议包含：

- 卷 / 篇章结构
- 每卷主目标、阶段反派、关键秘密、情绪兑现
- 前 10 章详细钩子

### episodes/ep-001.md

单集剧本文本。正文默认使用 `fountain` 代码块承载中文好莱坞式格式，以保留缩进对齐。每集必须包含：

- 本集目标
- 开场钩子
- 出场角色：在 Markdown 外层列角色功能
- 场次列表
- 剧本正文：`fountain` 代码块、`INT./EXT. 地点 - 时间` 场景标题、动作段、角色名、对白
- 信息差或反转
- 情绪兑现
- 本集质量审查
- 结尾卡点

写法要求：

- 场景标题顶格；动作段顶格；角色名约 20 个前导空格；对白约 10 个前导空格。
- 台词短，冲突清楚。
- 少写心理解释，多写动作、表情、停顿、公众反应。
- 每场都让地位、关系、危险、秘密、资源或情绪温度发生变化。

### quality-check.md

阶段审查日志和交付前总检。必须包含：

- 阶段审查：需求锁定、概念承诺、人物机器、故事机器、全剧结构、单集剧本、交付收口。
- 每个阶段的状态：通过 / 需返工 / 暂缺。
- 每个阶段的通过项、风险、返工动作。
- 最终总检。

最终总检必须包含：

- 开头钩子是否够快
- 观众承诺是否清晰
- 主角欲望是否可执行
- 反派压力是否主动
- 信息差是否稳定
- 情绪兑现是否可见
- 集尾钩子是否迫使继续看
- manifest 状态、路径和实际产物是否一致
- 当前最该修改的 3 个问题

### exports/full-script.md

固定占位、按需填充的汇总稿。用于把 `01-concept.md`、`02-characters.md`、`04-season-outline.md` 和已完成集数整合为一个可交付文件。不要替代分文件产物；它只做汇总。用户没有要求整稿时，保留占位说明即可。

## 可选分镜支线

只有用户明确要求分镜、AI 视频或 storyboard 时，才生成：

```text
storyboard/
├── ep-001-beats.md
└── ep-002-beats.md
```

启用分镜支线时，`manifest.json` 的 `artifacts` 增加：

```json
{
  "storyboard": "storyboard/"
}
```

### storyboard/ep-001-beats.md

面向分镜或 AI 视频的镜头前文本。每个 beat 必须包含：

- 地点
- 人物位置
- 可见动作
- 表情
- 道具或视觉焦点
- 台词 / 旁白
- 情绪目的
- 与下一 beat 的连接

## 落盘顺序

1. 先创建目录和 `manifest.json`。
2. 写 `00-brief.md`，锁定用户需求与假设。
3. 写 `01-concept.md` 到 `04-season-outline.md`，先搭机器。
4. 写 `episodes/`，每写一集同步更新 `quality-check.md` 的阶段审查。
5. 用户明确要求分镜时，再写对应 `storyboard/`。
6. 最后更新 `manifest.json` 与 `quality-check.md` 的交付收口。
7. 用户需要整稿时，再生成 `exports/full-script.md`。
