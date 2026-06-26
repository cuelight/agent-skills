# Episode

```bash
cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "分集大纲" --json
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt --json
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt --json
cuelight-cli episode status <episodeId> --json
```

## 通用原则

分集大纲用于指导剧本文本和分镜，不是营销简介。剧本文本必须可拍摄，能提取场景、角色、道具、对白、动作和声音触发。

写 episode 前先读取当前类型 profile：

- 短剧：`references/profiles/short-drama.md`
- 番剧：`references/profiles/anime-series.md`
- 电影：`references/profiles/film.md`

若项目类型不明确，先确认类型，再写 outline 或 script。

## Outline

大纲至少交代：

- 本集或本段在整体结构中的位置。
- 本段主要目标、阻力、信息变化和情绪落点。
- 本段涉及的关键角色、场景和道具。
- 与前后内容的边界和衔接方式。

不要只写“主角经历困难并成长”这类不可拍摘要。不同类型的结构模板由 profile 决定：短剧可用强钩子与反转，番剧可用 A/B part 或场景段落，电影可用场景组或序列推进。

## Script / Content

剧本正文至少包含：

- 场景标题或场景转换。
- 人物动作与调度。
- 角色对白或明确的无对白表演。
- 关键道具或屏幕信息。
- 声音触发点，例如门声、脚步声、环境声、电话声、系统提示或明确对白。
- 情绪变化、停顿和节奏标记。

每集或每段必须有清楚边界：当前内容只拍当前事件。后续内容可以作为衔接或钩子出现，但不能替当前段落补主体动作。

## 剧本容量与可分镜性

写 storyboard 前先检查正文容量。正文不足时先扩写剧本，不要让分镜替剧本补窟窿。

- 正文必须能自然拆出目标时长对应的 storyboard item。
- 每个 storyboard item 都应能追溯到正文中的动作、对白、道具、屏幕信息、声音触发或情绪停顿。
- 如果正文只有概述句、小说化 treatment 或剧情说明，先补成可拍台词、动作、空间调度、道具信息、声音和情绪变化。
- 无对白段落可以成立，但必须有清楚的视觉动作、情绪变化、环境声或剪辑目的。
- 传统电影正文按自然场次组织，不需要为了 12 条 storyboard item 机械切成 12 段；分镜从场次、动作和情绪推进中提炼。
- 若用户要求扩写或重写剧本，先更新正文，再同步重做或校准分镜；不要让旧分镜继续承载新正文没有的关键剧情。

## 三位专家自检

写完 outline 和 script 后，按当前 profile 的三位专家自检。发现阻断问题时先修剧本，再生成 storyboard。

通用验收：

- 结构专家确认段落边界、目标、阻力、变化和衔接清楚。
- 人物专家确认角色行动、情绪和关系符合设定与正文。
- 影像专家确认内容可被场景、动作、镜头、声音和道具表达。

## 推荐格式

每集正文推荐按“场景/时间/人物 + 动作行 + 对白 + 道具/屏幕信息 + 声音/停顿”组织。可用传统剧本格式、番剧分场格式、电影场景格式或短视频时间码格式，但必须能直接提取场景、角色、道具、对白和动作。电影项目的更完整 few-shot 见 `references/profiles/film.md`。

传统剧本示例：

```text
1. 内景 / 赵府寿安堂 / 日
人物：赵阿萤、赵宛瑜

△ 赵阿萤站在屏风旁，右手按着袖中的玉佩。
赵宛瑜：你以为今天还能躲过去？
赵阿萤：（压住呼吸）我从没想躲。
```

短视频/教学稿可以使用时间段、画面、台词、音效结构，但写分镜时要按 `references/storyboard.md` 的时间码规则拆分。

## 验收

- `summary` 或 outline 非空。
- `content` 或 script 非空。
- 能提取至少 1 个可绑定场景和 1 个主要角色。
- 内容能自然拆成目标时长对应的 storyboard item，且不需要借后续内容补时长。
- 每个 storyboard item 都能追溯到正文中的动作、对白、道具、屏幕信息、声音触发或情绪停顿。
- 正文不是为了 storyboard item 数量机械分段；storyboard 也没有替正文新增关键剧情、人物关系或结局变化。
- 当前 profile 的三位专家自检无阻断问题。
- 不因写剧本文本而提交图片、视频或语音任务。
