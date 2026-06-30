---
name: cuelight-film
description: CueLight 电影、长片、短片与电影化 screenplay 创作工作流。Use when Codex needs to create, adapt, continue, review, rewrite, locally maintain, validate, or export film projects, including three-act outlines, eight-sequence planning, screenplay blocks/pages, film-data YAML, Literary Rewrite, Commercialization Punch-up, Agent-owned quality gates, DOCX export, and film storyboard source text. Can work independently from cuelight-cli; use $cuelight-drama only when writing back to a CueLight project.
---

# CueLight 电影创作

使用本 Skill 处理电影、长片、短片和电影化剧本项目。默认目标是 screenplay / 文学剧本、三幕/八序列结构、可拍容量、人物弧光、场面调度和本地 film-data 元数据，而不是短剧式单集钩子。

本 Skill 可脱离 `cuelight-cli` 独立工作，默认在 `cuelight-projects/film/<project-slug>/` 或用户指定目录维护本地元数据、结构文件、YAML、quality reports 和导出文件。只有用户明确要求写回 CueLight 项目时，才再加载 `$cuelight-drama` 并按 CLI 合同转换为平台字段。

## 核心流程

1. **锁定电影项目边界**
   - 明确片长、类型、主题问题、主角欲望、核心冲突、人物弧光、结局形态和目标交付。
   - 若用户只给创意、treatment、分析文章、人物小传、舞台剧或小说片段，先做 Creative Source Adaptation Pass。

2. **建立本地元数据**
   - 默认创建或维护 `manifest.json`、`film-three-act-outline.md` 和 `film-data/`。
   - 结构化 canonical 只放在 `film-data/`：`film-data/film.yaml`、`film-data/story-bible.yaml`、`film-data/style-guide.yaml` 和后续 screenplay / production 树；详细约定读取 `references/film-data-local.md`。
   - 不在项目顶层再维护 `film-metadata.yaml`、`story-bible.yaml`、`style-guide.yaml`，避免与 `film-data/` 同名结构冲突。

3. **写 screenplay**
   - 正文优先写成可拍 screenplay：场景标题、动作、人物名、对白、括号提示、声音标记、转场和特殊格式。
   - 不把 treatment、导演说明、主题解释或分镜提示词混入 `action` / `dialogue`。

4. **执行电影 gate**
   - 每完成阶段性 screenplay draft 后，执行 Literary Rewrite Loop Engineering。
   - 正式交付、DOCX 导出或生产叶节点前，执行 screenplay quality strict、Agent Literary Review Gate、Commercialization Punch-up Pass 和对应 Agent-owned gates。

5. **按需协作 CueLight**
   - 独立模式只维护本地文件，不要求 projectId。
   - 写回 CueLight 时，先使用 `$cuelight-drama` 处理 workspace、CLI、platform fields、episode/storyboard import 和验收。

## 按需读取参考

- 电影项目设计、screenplay 格式、三幕/八序列、rewrite、commercial punch-up、storyboard、DOCX gate 和 few-shot：读取 `references/film.md`。
- 需要本地结构化元数据、film-data YAML、Act/Sequence/Scene/Beat/VideoSegment/Shot/Prompt/Continuity、duration 与 capacity gate 时：读取 `references/film-data-local.md`。
- 需要导出正式 screenplay DOCX 时：使用 `scripts/export_film_screenplay_docx.py`。
- 需要 screenplay 质量、分页、容量、对白读感、重复和本地化术语检查时：使用 `scripts/check_film_screenplay_quality.py`。

## 本地目录约定

默认输出：

```text
cuelight-projects/film/<project-slug>/
├── manifest.json
├── film-three-act-outline.md
├── film-data/
├── quality-reports/
└── exports/
```

`film-data/` 的完整结构由 `references/film-data-local.md` 决定，是电影项目的结构化 canonical 元数据根。`manifest.json` 只做项目索引和 artifact 路由，不复制 film/story-bible/style-guide 正文。写回 CueLight 项目时，先从 canonical `film-data/` 派生到 `./.cuelight/<projectId>/staging/film-data/`，该目录只作为导入/校验暂存副本，不作为长期源数据。

`cuelight-projects/` 是长期项目资料目录，不是临时输出目录；不要默认加入 `.gitignore`。

不要直接维护 `.cuelight/<projectId>/staging/film-data/`；发现 staging 与 canonical 不一致时，以 `cuelight-projects/film/<project-slug>/film-data/` 为准重新派生。外置 Codex 工作流只写 staging 时，该目录只服务本轮 CLI 导入，不替代长期电影项目。

## 输出规则

- 新建电影项目时，先写主题问题、主角欲望、核心冲突、结局形态和片长目标。
- 从创意类原文改编时，分析性内容进入 `film-data/story-bible.yaml`、`film-three-act-outline.md` 或对应 scene/beat metadata；screenplay 只写可见可听的场面。
- 完整长片默认至少维护 3 个 Act、多个 Sequence、多个 Scene、多个 Beat、多个 VideoSegment 和多个 Shot；最小样例必须标记 `sample` / `incomplete`。
- `1 页 ≈ 1 分钟` 只用于 screenplay 和片长规划，不直接套到 Shot 或单条 storyboard item。
- VideoSegment / CueLight storyboard item 固定按 4-15 秒规划；更长 Beat 必须拆成多个连续 VideoSegment。
- DOCX 导出前必须完成 Literary Rewrite、screenplay quality strict 和 Agent 审查。
- 工具 `strict ok` 只是底线信号，不是最终验收；Agent 必须抽读真实产物并写出 `pass` / `fail` 证据。

## 常用命令

```bash
python agent-skills/cuelight-film/scripts/check_film_screenplay_quality.py --film-data-dir <film-data> --strict
python agent-skills/cuelight-film/scripts/check_film_screenplay_quality.py --film-data-dir <film-data> --strict --json
python agent-skills/cuelight-film/scripts/export_film_screenplay_docx.py --film-data-dir <film-data> --output <out.docx> --strict
```

在已安装到用户级 skill 目录时，把路径替换为对应的 `$CODEX_HOME/skills/cuelight-film/scripts/...`、`.codex/skills/cuelight-film/scripts/...` 或实际 skill 路径。

## 质量线

交付前检查：

- 三幕/八序列、主题问题、人物弧光和结局回答一致。
- screenplay 正文能被演员表演、摄影拍摄、剪辑推进。
- 每场戏有戏剧目的：角色想要什么、阻力是什么、结束时信息或关系发生什么变化。
- 对白包含潜台词、关系压力和权力变化，不用口播解释设定。
- 无对白页通过视觉焦点、声音触发、人物反应、危险升级或剪辑动机推进。
- film-data 的时长、分页、容量和 production leaves 能从真实 screenplay 解释。
- DOCX、storyboard 或 CueLight 写回产物都能追溯到最新 screenplay。
- 若存在顶层 `film-metadata.yaml`、`story-bible.yaml`、`style-guide.yaml`，视为旧产物；先合并进 `film-data/` 内的同类结构，再继续正式脚本、质量 gate 或写回准备。
