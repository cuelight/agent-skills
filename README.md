# CueLight Agent Skills

面向 AI coding agent 的技能集合，主要服务于 CueLight / AI Drama Factory 相关工作流。

Skill 本质上是一组可复用的说明、参考资料和模板，用来补充 agent 在特定场景下的判断和执行能力。当前仓库采用 [Agent Skills](https://agentskills.io/) 约定组织内容。

## 仓库内容

当前仓库包含以下技能：

### `cuelight-drama`

用于 CueLight 短剧生产链路的工作流指导，重点覆盖 CLI 驱动的项目推进。

适用场景：

- 继续推进现有短剧项目，而不是从零重新开始
- 处理 director-mode 相关任务，例如视觉设定、选角、分镜、视频生成
- 通过 `@cuelight/cli` 或 `cuelight-cli` 读取项目状态、回写文本资产、提交生成任务
- 梳理项目当前所处阶段，并决定下一步应该补 Bible、Outline、Script 还是 Storyboard

目录说明：

- `cuelight-drama/SKILL.md`：主技能说明
- `cuelight-drama/references/`：项目、Bible、Episode、Storyboard 等参考资料

### `seedance-storyboard`

用于把一个创意、剧情片段或参考素材，转换成适合 Seedance 2.0 使用的专业分镜提示词。

适用场景：

- 用户要生成视频、做短视频、写分镜提示词
- 用户提到 Seedance、即梦、剪映 AI 视频等能力
- 需要把“一个简单想法”细化成可直接投喂模型的镜头脚本
- 需要结合图片、视频、音频等多模态素材组织提示词
- 需要处理视频延长、镜头复刻、角色一致性、多场景衔接等高级生成需求

这个技能的核心能力：

- 引导式提问：先澄清故事、风格、时长、镜头和声音设计
- 分镜拆解：把想法拆成时间轴上的镜头段落
- Prompt 组织：输出符合 Seedance 2.0 使用习惯的结构化提示词
- 多模态引用：支持把图片、视频、音频参考以统一方式写入提示词
- 高级场景覆盖：包括视频延长、角色替换、运镜复刻、特效复刻等

目录说明：

- `seedance-storyboard/SKILL.md`：主技能逻辑与引导流程
- `seedance-storyboard/README.md`：技能详细说明
- `seedance-storyboard/quick-reference.md`：快速参考卡
- `seedance-storyboard/templates/storyboard-template.md`：分镜模板
- `seedance-storyboard/examples/example-prompts.md`：示例 prompts

## 安装

如果你是通过 skills 工具链安装：

```bash
npx skills add cuelight/agent-skills
```

如果你是在本项目中使用，本仓库通常会作为子模块挂载，无需单独重复组织目录结构。

## 使用方式

安装后，agent 会在检测到相关任务时自动选用合适的 skill。

示例：

```text
帮我继续推进这个 CueLight 短剧项目
```

```text
为这一集生成分镜，并告诉我需要执行哪些 CLI 命令
```

```text
把这个创意整理成 Seedance 2.0 的专业分镜提示词
```

```text
参考这张图和这段视频，写一个可以直接用于即梦的视频 prompt
```

## Skill 结构

每个 skill 一般包含：

- `SKILL.md`：给 agent 的主说明
- `references/`：按需加载的补充文档
- `templates/`：可复用模板
- `examples/`：示例输入与输出
- `scripts/`：需要自动化时可调用的辅助脚本

## 维护建议

- 新增 skill 时，优先补齐 `SKILL.md` 与最少必要的参考资料
- 若 skill 依赖固定输出格式，建议同时提供 `templates/`
- 若 skill 面向复杂生成任务，建议提供 `examples/`，降低使用门槛
