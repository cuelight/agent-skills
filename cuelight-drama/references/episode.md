# Episode

```bash
cuelight-cli episode create <projectId> --title "第一集" --number 1 --summary "分集大纲" --json
cuelight-cli episode set-outline <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-outline.txt --json
cuelight-cli episode set-script <episodeId> --file ./.cuelight/<projectId>/episodes/episode-1-script.txt --json
cuelight-cli episode status <episodeId> --json
```

## Outline

分集大纲用于指导剧本文本和分镜，不是营销简介。

建议按以下节奏写：

- 开场钩子：第一屏/第一场立刻有冲突、疑问或强情绪。
- 目标建立：本集主角要争取、隐藏、逃离或揭露什么。
- 阻力升级：对手、环境、误会或规则如何加压。
- 信息揭露：本集至少一个新信息或关系变化。
- 情绪落点：观众在本集末尾应感到爽、痛、甜、怕或想继续看。
- 结尾钩子：下一集必须追看的悬念。

不要只写“主角经历困难并成长”这类不可拍摘要。

## Script / Content

剧本正文要可拍摄，至少包含：

- 场景标题或场景转换。
- 人物动作与调度。
- 角色对白。
- 关键道具使用方式。
- 情绪变化和停顿。
- 结尾钩子。

传统剧本可以使用：

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
- 第一集能提取至少 1 个可绑定场景、1 个主要角色。
- 不因写剧本文本而提交图片、视频或语音任务。
