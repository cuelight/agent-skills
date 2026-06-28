# Film Data Local

用于 CueLight 电影项目的本地影子结构维护。它把 `agent-skills/film-data.md` 中从 Film 到 Production 的核心链路压缩成本地 YAML 文件约定，方便 Agent 在正式系统支持前维护电影级结构。

本文件只覆盖：

```text
Film -> StoryBible -> StyleGuide -> ScriptVersion -> ScriptBlock -> ScriptPage -> Act -> Sequence -> Scene -> Beat -> VideoSegment -> Shot -> Prompt -> ContinuityState
```

不维护生成任务、资产审核、时间线、导出、成本记录。提交媒体生成、查询任务、资产选版仍走当前 `cuelight-cli` 和平台事实。

## 存储原则

- 根目录固定为 `./.cuelight/<projectId>/film-data/`。
- 所有本地结构文件都使用 `.yaml`，每个 `.yaml` 文件只保存一个 YAML object 或 YAML array，不再包 Markdown 标题或 fenced block。
- 默认按电影叙事树组织目录：`Act -> Sequence -> Scene -> Beat -> VideoSegment`。长片内容按父子树展开，避免实体类型全局大表。
- 每级目录可以有一个 `index.yaml`，只保存子节点引用、顺序、标题、状态和文件路径；`index.yaml` 不保存大段 screenplay、prompt、shot 或 continuity 正文。
- 实体正文放在对应节点文件：`act.yaml`、`sequence.yaml`、`scene.yaml`、`beat.yaml`、`segment.yaml`。
- scene 目录内保存该场 screenplay：`script/blocks.yaml`、`script/pages.yaml`。
- segment 目录内保存 production：`segment.yaml`、`script-links.yaml`、`shots.yaml`、`prompt.yaml`、`continuity.yaml`。
- 若单个 segment 的 `shots.yaml` 仍过大，再拆成 `shots/shot_001.yaml`、`shots/shot_002.yaml`；小样例可保留一个 `shots.yaml`。
- 单对象文件保存 YAML object；列表文件保存 YAML array。
- 不使用 JSONL；所有结构化数据都直接写在 `.yaml` 文件内。
- 所有实体都保留 `project_id`、可选 `film_id`、稳定本地 id、`status`、`created_at`、`updated_at`。索引项至少保留 id、`order_index`、标题、状态、目标文件路径。
- 已落库到 CueLight 的角色、场景、道具或 storyboard item，使用 `platform_ref` 记录平台 ID；未落库对象使用本地 ID，后续写回后补齐映射。
- YAML value 中只要包含英文冒号、井号、花括号、方括号、换行、前后空格或容易被解析成布尔/数字的内容，就用双引号包裹，保证文件可被 YAML parser 直接读取。
- `char_*`、`loc_*`、`prop_*` 这类本地 ID 不得凭空出现；必须来自已落库平台资源、主 skill 的 `characters/`、`scenes/`、`props/` 文本资产，或在当前文件的 `platform_ref` / `local_ref_status` 中明确标记为 `pending_binding`。
- 时间字段分层使用：`estimated_duration_sec` 用于 Act / Sequence / Scene / Beat 的剧情估时；`duration_target_sec` 只用于可投递的 VideoSegment / Shot。
- 当前每个 VideoSegment / storyboard item 的 `duration_target_sec` 固定为 4-15 秒，暂不开放超过 15 秒的单条分镜组。Beat 超过 15 秒时，必须拆成多个连续 `seg_xxx`。

## 节点数量与拆分规则

目录 skeleton 只说明文件位置，不代表推荐生成规模。Agent 生成真实电影结构时，先根据三幕式、八序列、剧本页数和正文容量决定节点数量，再写 YAML 文件。

- 长片默认使用 3 个 Act；短片可少于 3 个 Act，但必须在 `film.yaml` 或 `film-three-act-outline.md` 中说明结构选择。
- 长片默认使用多个 Sequence；八序列结构应映射为多个 `seq_xxx`。
- 每个 Sequence 通常包含多个 Scene；Scene 对应 screenplay 场景标题，地点、时间、人物组合或戏剧目标明显变化时新开 Scene。
- 每个 Scene 通常拆出多个 Beat；Beat 是场景内动作、信息、情绪或关系变化的单位，不是 storyboard item。
- Beat 可以超过 15 秒，但写入 production 叶子时必须拆成多个连续 VideoSegment；任何 `seg_xxx/segment.yaml` 的 `duration_target_sec` 都必须在 4-15 秒之间。
- 每个 VideoSegment 通常包含 2-5 个 Shot；允许 1 个 Shot 的例外仅限空镜、单一动作展示、单一情绪特写或明确的一镜到底。
- 每级 `index.yaml` 必须列出当前父节点下的全部子节点引用。未完成的子树应在父节点 `status` 中标记 `partial`、`sample` 或 `incomplete`。
- 只有用户明确要求“最小样例 / POC / 只演示一段”时，才允许 Act -> Sequence -> Scene -> Beat -> Segment 每层单节点；这种结果不能标记为完整电影结构。

### 第一幕完整拆解推荐流程

当用户要求“第一幕完全拆出来”“完整拆第一幕”“验证第一幕”或类似目标时，优先把 `act_001` 做成可生产的完整子树；第二幕和第三幕可以保留 outline-only 粗结构。

1. 先定片长预算：`film.yaml.final_target_duration_sec` 记录最终长片目标；完整 `act_001` 推荐占全片 18%-30%。90 分钟长片的第一幕通常约 16-27 分钟。
2. 再定叙事容量：按第一幕事件阶段拆 Sequence，按地点/时间/人物组合/戏剧目标拆 Scene，按动作、信息、关系或情绪转折拆 Beat。
3. 再落 production 叶子：Beat 按 4-15 秒拆 VideoSegment；每个 Segment 通常包含 2-5 个 Shot，并让 Shot 时长合计解释 Segment 时长。
4. 最后跑 `cuelight-cli internal film-data duration --project-id <projectId> --strict`，用汇总结果确认父子时长一致。

验收下限只用于兜底：`act_001` 至少 2 个 Sequence；每个第一幕 Sequence 至少 2 个 Scene；每个第一幕 Scene 至少 2 个 Beat；超过 15 秒的 Beat 至少拆 2 个 Segment。实际生成应按剧情容量自然变化。

Self-check：

- `target_duration_sec` 等于本轮已展开范围的可汇总时长；`final_target_duration_sec` 保留最终长片目标。
- 若第二幕和第三幕只做 outline-only，对应 `act.yaml.estimated_duration_sec` 写 `0` 或省略，并保留空的 `sequences/index.yaml`。
- 完整第一幕低于最终长片目标 18% 时，将 `status` 标为 `sample` / `partial`，或继续扩展第一幕容量。
- 交付前确认结构不是均匀最低树：child 数量和时长应能解释源稿事件密度。

## 时长汇总规则

电影本地结构必须能从叶子向上解释时长：

- `film.yaml.target_duration_sec` 与 `acts/index.yaml` 下所有 `act.yaml.estimated_duration_sec` 汇总应基本一致。
- `act.yaml.estimated_duration_sec` 应由其 Sequence 汇总解释；`sequence.yaml.estimated_duration_sec` 应由其 Scene 汇总解释；`scene.yaml.estimated_duration_sec` 应由其 Beat 汇总解释。
- `beat.yaml.estimated_duration_sec` 应由其 `segments/index.yaml` 下所有 `segment.yaml.duration_target_sec` 汇总解释。
- `segment.yaml.duration_target_sec` 应与同目录 `shots.yaml` 中所有 `shot.duration_target_sec` 汇总一致。
- 根级 `script/pages.yaml` 是 screenplay 层估时来源，用于和 Film / Act / Sequence 汇总交叉检查；它不直接替代 Shot 或 Segment 时长。
- 默认允许 2 秒以内的四舍五入误差；超过误差时必须解释或修正。

本地校验使用 CLI 内部工具：

```bash
cuelight-cli internal film-data duration --project-id <projectId>
cuelight-cli --json internal film-data duration --project-id <projectId>
cuelight-cli internal film-data duration --project-id <projectId> --strict
```

该命令只读 `./.cuelight/<projectId>/film-data/`，汇总各层数量和秒数，并报告父子时长不一致、segment 超出 4-15 秒、shot 合计不等于 segment、缺失文件或 YAML 解析失败等问题。

基础格式。实际文件例如 `film.yaml` 只保存下面的 YAML 内容，不再包 Markdown 标题或 fenced block：

```yaml
film_id: film_001
project_id: proj_001
title: 荒原修仙：废土的BUG
format: feature_film
target_duration_sec: 7200
status: development
updated_at: "2026-06-27T10:30:00+08:00"
```

## 文件布局

推荐默认树形布局：

```text
./.cuelight/<projectId>/film-data/
  film.yaml
  story-bible.yaml
  style-guide.yaml

  script/
    versions.yaml
    pages.yaml

  acts/
    index.yaml
    act_001/
      act.yaml
      sequences/
        index.yaml
        seq_001/
          sequence.yaml
          scenes/
            index.yaml
            scene_001/
              scene.yaml
              script/
                blocks.yaml
                pages.yaml
              beats/
                index.yaml
                beat_001/
                  beat.yaml
                  segments/
                    index.yaml
                    seg_001/
                      segment.yaml
                      script-links.yaml
                      shots.yaml
                      prompt.yaml
                      continuity.yaml
```

本地结构只覆盖 Production 之前的影子数据。若用户要求提交视频生成、审核资产、整理成片顺序或导出成片，切回当前平台/CLI 能力或说明该本地结构暂不覆盖。

旧式全局聚合文件不再作为默认结构：使用树形子目录替代 `structure/acts.yaml`、`structure/scenes.yaml`、`production/shots.yaml`、`production/prompts.yaml`、全局 `script/blocks.yaml` 这类会随长片规模膨胀的叶子文件。

## Workflow

1. 从电影创意、梗概或 treatment 起步时，先维护 `film.yaml`、`story-bible.yaml`、`style-guide.yaml` 和 `film-three-act-outline.md`。
2. 写阶段性 screenplay draft 时，更新根级 `script/versions.yaml`，并把正文块写入对应场景目录的 `scene_xxx/script/blocks.yaml`。阶段可以是单个 scene、一个 sequence、`act_001` 或其他明确交付范围。
3. 阶段性 screenplay draft 完成后，必须执行 Literary Rewrite Loop Engineering（文学精修循环工程）；只有明确的 quick POC / sample / fixture 可跳过，并必须标记 `sample` / `draft_not_rewritten`。
4. 每轮 Rewrite 后运行 `python .codex/skills/cuelight-drama/scripts/check_film_screenplay_quality.py --film-data-dir <film-data> --strict`；若报告 `generic_literary_filler`、`spatial_logic_mismatch`、`unexpected_role_mention`、模板、重复、容量或分页 error，按原因继续 Rewrite。
5. 脚本变绿后，执行 Agent Literary Review Gate（Agent 文学审查门）：Agent 抽读本轮范围内至少 3 个关键 scene；act 级至少覆盖开端、中段、转折、结尾各 1 场。审查要写出 `pass` / `fail`、证据短句和是否允许下游生产；抽读不合格时继续 Rewrite，不能进入 production-ready。
6. Literary Rewrite 通过后，执行 Dialogue Readability Gate（对白读感验收门）：以根级 `script/pages.yaml` 为权威，按 `block_refs` 反查真实 blocks，统计每页 dialogue 数、说话人数量、speaker turns 和 action/dialogue 交错；单说话人对白页必须记录独白、广播、系统语音、审讯压迫、仪式宣告或无对手戏等明确例外。
7. Dialogue Readability 通过后，执行 Action/Suspense Page Gate（动作悬念页验收门）与 Reveal Chain Gate（揭示链验收门）：无对白或少对白页不按 dialogue 数量失败，但必须记录视觉焦点、声音触发、人物反应、动作阻力、危险升级或剪辑动机；页面没有推进时继续 Rewrite。
8. 进入分镜 / 生成 / DOCX 导出前，执行 Commercialization Punch-up Pass（商业化强化环节）和 Commercial Review Gate（商业化审查门）：每场检查 entrance objective（入场目标）、external obstacle（外部阻力）、visible conflict（可见冲突）和 turn/end hook（转折/场尾钩子）。若 `strict ok` 但 Agent 抽读发现同场动作复用、意象空转、冲突未外化或场尾无推进，判定 `fail` 并进入 repair loop（修复循环）。
9. 进入分镜、生成或 DOCX 导出前，执行 Pagination De-dup Pass（分页去重环节）：根级 `script/pages.yaml` 的多页 scene 必须拆成连续、非重叠 block ranges，同一 `script_path#block_id` 不能被多个 ScriptPage 重复覆盖。Agent 还要抽查跨页阅读连续性，确认没有截断理解、大片空白或复制页冒充容量。
10. 拆分镜前，沿树形路径维护 `acts/**/act.yaml`、`sequence.yaml`、`scene.yaml`、`beat.yaml`，并更新各级 `index.yaml`。若 production leaves 已存在，Rewrite / Punch-up / Repair 必须保持 `block_id`、pages、`script_refs` 和 production 绑定稳定；无法保持时必须同步修复所有引用。
11. 生成分镜组、镜头和提示词时，在对应 `seg_xxx/` 目录维护 `segment.yaml`、`script-links.yaml`、`shots.yaml`、`prompt.yaml`、`continuity.yaml`。正文改写后执行 Production Leaves Sync Audit（生产叶节点同步审查），抽查 affected segment 的 `script-links.yaml`、`prompt.yaml` 和 `shots.yaml` 是否追溯最新 screenplay。
12. 每个正式 gate 都要写入验收报告：双语 gate 名称、工具结果、Agent 抽查对象、文本或结构证据、`pass` / `fail`、下一步许可。只列 `strict ok` 或导出成功而没有 Agent 审查证据，视为 `draft_not_reviewed`。
13. 写回 CueLight 当前支持的项目、Bible、角色、场景、道具、episode、storyboard 时，继续使用主 skill 和 CLI；本地 film-data 只负责保存电影级结构和可追溯依据。

## Core Files

### `film.yaml`

保存电影本体信息。

```yaml
film_id: film_001
project_id: proj_001
title: 荒原修仙：废土的BUG
original_title: "Future Cultivation: Wasteland System Error"
genre:
  - 科幻
  - 修仙
  - 废土
format: feature_film
target_duration_sec: 7200
logline: 一个废土少女在崩坏的修仙系统中发现世界被错误代码控制。
synopsis: 灵气枯竭后的废土世界中，亚莉娅意外接入残缺修仙系统，并发现整个世界的命运被一段错误代码锁死。
theme: 人在系统命运中的自由意志
tone: 冷峻、史诗、宿命感
status: development
created_at: "2026-06-27T10:00:00+08:00"
updated_at: "2026-06-27T10:30:00+08:00"
```

### `script/versions.yaml`

保存剧本版本列表。当前生效版本只能有一个 `status: active`。正文不放在这里，正文放在 scene 子树。

```yaml
- script_version_id: script_v001
  project_id: proj_001
  film_id: film_001
  version: 1
  title: 第一版剧本
  status: active
  format_profile: master_scene_a4_cn_v1
  stats:
    page_count: 118.6
    estimated_duration_sec: 7116
    scene_count: 68
    word_count: 58620
  created_at: "2026-06-27T10:00:00+08:00"
  updated_at: "2026-06-27T10:30:00+08:00"
```

### `script/pages.yaml`

保存**全片剧本页码估算与正文覆盖索引**，用于 `1 页 ≈ 1 分钟` 的 screenplay 层估时和 block traceability。它不保存正文全文，也不默认控制 DOCX 的物理分页；正文通过 `block_refs` 指向各 scene 的 `script/blocks.yaml`。

当一页跨多个场景时，必须用多个 `block_refs` 表达；跨场景页码以根级 `script/pages.yaml` 为权威。

```yaml
- script_page_id: sp_037
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  page_number: 37
  estimated_duration_sec: 60
  coverage_level: full_page
  block_refs:
    - scene_id: scene_002_009
      script_path: acts/act_002/sequences/seq_004/scenes/scene_002_009/script/blocks.yaml
      start_block_id: blk_002_090
      end_block_id: blk_002_094
      page_fraction: 0.35
      estimated_duration_sec: 21
    - scene_id: scene_002_010
      script_path: acts/act_002/sequences/seq_004/scenes/scene_002_010/script/blocks.yaml
      start_block_id: blk_002_095
      end_block_id: blk_002_101
      page_fraction: 0.65
      estimated_duration_sec: 39
  status: locked
  updated_at: "2026-06-27T10:30:00+08:00"
```

使用约束：

- `page_number` 是全片 screenplay 估算页码，不是 scene 内局部页码，也不是 DOCX 默认物理页码。
- `block_refs[].start_block_id` / `end_block_id` 必须能在对应 `script_path` 的 `blocks.yaml` 中找到。
- 多页 scene 必须拆成连续、非重叠的 `block_refs`；正式 production-ready 数据中，同一 `script_path#block_id` 不能被多个 ScriptPage 重复覆盖。
- `block_refs[].page_fraction` 表示估时权重，不表示 Word 实际版面填充率；合计通常为 `1.0`。样例或未排满页可使用小于 `1.0`，并标记 `coverage_level: partial_page_sample`。
- 单个 ScriptPage 的 `page_fraction` 不应大于 `1.0`；若一段内容估算超过一页，拆成多个 ScriptPage 或改用 scene/beat duration estimate 解释。
- `coverage_level: full_page` 只表示估时页覆盖完整，不承诺 DOCX 渲染后填满一页。若尚未做正式分页校准，优先使用 `coverage_level: timing_estimate` / `draft_page_estimate`。
- `estimated_duration_sec` 是剧本页估时，供 Scene / Sequence / Act / Film 汇总，不直接下推为 Shot 时长。
- 修改剧本文本、插入或删除 block 后，必须重算受影响的 `script/pages.yaml` 页码范围，再检查相关 segment 的 `script_refs` 和 `script-links.yaml`。
- 如果发现第 1-2 页、第 3-5 页这类复制了同一整场 block range 的重复页，先清洗为非重叠页段；需要保持正式容量时，不能简单删页缩水。
- 正式 DOCX 导出默认优先使用根级 `script/pages.yaml` 收集正文顺序，但不把每个 ScriptPage 强制导出为物理页；Word 根据正文自然分页，scene 内 `script/pages.yaml` 只作局部估算。
- 使用 `scripts/export_film_screenplay_docx.py` 导出时，先完成 Literary Rewrite Pass、screenplay quality strict 和 Agent 文学审查；导出脚本只读 YAML，不回写 film-data。
- 正式 DOCX 正文不显示调试用 `第 N 页` 段落；页码由页脚承担。只有排查分页映射时才使用 `--page-break-per-script-page --show-page-labels`，硬分页审计模式下从 scene 中段开始的页必须补 continuation heading。
- DOCX 中 dialogue speaker 应显示剧本读者可读的角色名；`character_id` 保持为稳定绑定 ID，导出时从 `story-bible.yaml` 的 `characters[].name` 映射显示名。
- DOCX gate 由 Agent 最终放行：导出后反读段落或渲染抽查页面，确认角色名、对白、动作、转场和自然分页可读；导出成功本身不能作为验收结论。
- Dialogue Readability Gate 也以根级 `script/pages.yaml` 为权威：按每个 `block_refs` 反查真实 blocks，逐页统计 `dialogue` 数、说话人数量、speaker turns 和 action/dialogue 交错。互动页默认至少 2 个对白块和 2 个 speaker turns；有对白但只有 1 个说话人的页必须在页面 note 或 `dialogue_exception` / `dialogue_readability_exception` 中说明例外原因。
- 无对白页不因 `dialogue` 数量失败；但正式页必须能通过 action/suspense page 口径说明页面视觉焦点、声音或物件触发、人物反应、动作阻力和小推进。若只是环境氛围或长动作说明，不能作为 full_page 放行。
- Reveal chain 抽查以根级页面为单位，确认 `block_refs` 对应 blocks 形成“空间状态 -> 视角/特写/插入 -> 声音或物件变化 -> 人物反应 -> 新危险/选择/剪辑动机”的链条。
- 硬分页 DOCX 导出用于审计时，必须抽查导出页的实际读感，确认不会从 YAML 上看容量足够、导出后却变成单角色独白页或连续口播页。

## Index Files

`index.yaml` 只做导航和顺序，不承载大内容。

```yaml
- act_id: act_001
  order_index: 1
  title: 第一幕：建立与进入
  file: acts/act_001/act.yaml
  status: script_completed

- act_id: act_002
  order_index: 2
  title: 第二幕：代价与崩塌
  file: acts/act_002/act.yaml
  status: outline_completed
```

Sequence、Scene、Beat、Segment 的索引也采用同样原则：只保留 id、顺序、标题、状态、file，必要时可附 `estimated_duration_sec` 或 `slugline`。

`file` 路径推荐统一写成**相对 film-data 根目录**的路径，例如 `acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_001/beat.yaml`。内部校验工具可兼容 index 所在目录的相对路径，但正式 production-ready 元数据应优先使用根相对路径，避免不同工具解析歧义。

### 正向 capacity few-shot

下面示例展示一个 90 分钟长片的完整第一幕拆解方式：`3 sequences -> 7 scenes -> 23 beats -> 36 segments -> 100 shots`，`act_001` 汇总为 1260 秒。重点是不同父节点有不同 child count，且父子时长可以逐层解释。

`film.yaml`：

```yaml
film_id: film_001
project_id: proj_001
title: 星环断层
format: feature_film
target_duration_sec: 1260
final_target_duration_sec: 5400
status: act_001_production_ready
```

`acts/index.yaml`：

```yaml
- act_id: act_001
  order_index: 1
  title: 第一幕：边境与越界
  estimated_duration_sec: 1260
  file: acts/act_001/act.yaml
  status: production_ready

- act_id: act_002
  order_index: 2
  title: 第二幕：深入与代价
  estimated_duration_sec: 0
  file: acts/act_002/act.yaml
  status: outline_only

- act_id: act_003
  order_index: 3
  title: 第三幕：返回断层
  estimated_duration_sec: 0
  file: acts/act_003/act.yaml
  status: outline_only
```

第一幕容量分布：

```yaml
act_001:
  estimated_duration_sec: 1260
  sequences:
    - sequence_id: seq_001
      title: 边境事故与返航命令
      scene_count: 2
      beat_count: 7
      estimated_duration_sec: 390
    - sequence_id: seq_002
      title: 回到基地与临时授权
      scene_count: 3
      beat_count: 9
      estimated_duration_sec: 450
    - sequence_id: seq_003
      title: 私人承诺与任务绑定
      scene_count: 2
      beat_count: 7
      estimated_duration_sec: 420
  production_totals:
    scenes: 7
    beats: 23
    segments: 36
    shots: 100
```

`acts/act_001/sequences/index.yaml`：

```yaml
- sequence_id: seq_001
  order_index: 1
  title: 边境事故与返航命令
  estimated_duration_sec: 390
  file: acts/act_001/sequences/seq_001/sequence.yaml
  status: script_completed

- sequence_id: seq_002
  order_index: 2
  title: 回到基地与临时授权
  estimated_duration_sec: 450
  file: acts/act_001/sequences/seq_002/sequence.yaml
  status: outline_completed

- sequence_id: seq_003
  order_index: 3
  title: 私人承诺与任务绑定
  estimated_duration_sec: 420
  file: acts/act_001/sequences/seq_003/sequence.yaml
  status: outline_completed
```

`acts/act_001/sequences/seq_001/scenes/index.yaml`：

```yaml
- scene_id: scene_001_001
  order_index: 1
  slugline: 外景. 星环维修栈道 - 深夜
  estimated_duration_sec: 180
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/scene.yaml
  status: script_completed

- scene_id: scene_001_002
  order_index: 2
  slugline: 外景. 星环外缘检修桥 - 连续
  estimated_duration_sec: 210
  file: acts/act_001/sequences/seq_001/scenes/scene_001_002/scene.yaml
  status: script_completed
```

`acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/index.yaml`：

```yaml
- beat_id: beat_001_001
  order_index: 1
  title: 林岚离开检修队
  estimated_duration_sec: 45
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_001/beat.yaml
  status: ready_for_segments

- beat_id: beat_001_002
  order_index: 2
  title: 调度员发现工牌空缺
  estimated_duration_sec: 60
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/beat.yaml
  status: ready_for_segments

- beat_id: beat_001_003
  order_index: 3
  title: 救援车冲出闸门
  estimated_duration_sec: 75
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_003/beat.yaml
  status: ready_for_segments
```

`beat_001_002/segments/index.yaml`：该 Beat 为 60 秒，拆成 5 个连续 12 秒 VideoSegment。

```yaml
- video_segment_id: seg_001_002_001
  order_index: 1
  title: 空位与工牌
  duration_target_sec: 12
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/segments/seg_001_002_001/segment.yaml
  status: storyboard_ready

- video_segment_id: seg_001_002_002
  order_index: 2
  title: 调度员调亮监控
  duration_target_sec: 12
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/segments/seg_001_002_002/segment.yaml
  status: storyboard_ready

- video_segment_id: seg_001_002_003
  order_index: 3
  title: 闸口指向外缘
  duration_target_sec: 12
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/segments/seg_001_002_003/segment.yaml
  status: storyboard_ready

- video_segment_id: seg_001_002_004
  order_index: 4
  title: 救援车惊动警灯
  duration_target_sec: 12
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/segments/seg_001_002_004/segment.yaml
  status: storyboard_ready

- video_segment_id: seg_001_002_005
  order_index: 5
  title: 调度员追入外缘
  duration_target_sec: 12
  file: acts/act_001/sequences/seq_001/scenes/scene_001_001/beats/beat_001_002/segments/seg_001_002_005/segment.yaml
  status: storyboard_ready
```

`seg_001_002_001/segment.yaml`：

```yaml
video_segment_id: seg_001_002_001
project_id: proj_001
film_id: film_001
act_id: act_001
sequence_id: seq_001
scene_id: scene_001_001
beat_id: beat_001_002
order_index: 1
title: 空位与工牌
duration_target_sec: 12
script_refs:
  - script_version_id: script_v001
    start_block_id: blk_001_041
    end_block_id: blk_001_048
    coverage: full
shot_ids:
  - shot_001_002_001
  - shot_001_002_002
  - shot_001_002_003
prompt_id: prompt_seg_001_002_001_v001
status: storyboard_ready
updated_at: "2026-06-27T10:30:00+08:00"
```

`seg_001_002_001/shots.yaml`：Shot 合计等于 Segment 的 12 秒。

```yaml
- shot_id: shot_001_002_001
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002_001
  order_index: 1
  title: 检修舱空位
  duration_target_sec: 4
  shot_type: wide shot
  visual_description: 检修舱内白灯低闪，林岚的工位只剩未扣上的安全带和半张未签的交接单。
  status: ready

- shot_id: shot_001_002_002
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002_001
  order_index: 2
  title: 调度员按住值班表
  duration_target_sec: 5
  shot_type: medium shot
  visual_description: 调度员一手按住值班表，一手调亮监控屏，眼神从疑惑转成紧张。
  status: ready

- shot_id: shot_001_002_003
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002_001
  order_index: 3
  title: 空缺被确认
  duration_target_sec: 3
  shot_type: close-up
  visual_description: 值班表上“林岚”二字旁的工牌状态变成离线，闸外警铃突然压过风声。
  status: ready
```

## Tree Entities

### `acts/act_xxx/act.yaml`

保存单个 Act 的结构信息。

```yaml
act_id: act_001
project_id: proj_001
film_id: film_001
order_index: 1
title: 第一幕：建立与进入
page_start: 1
page_end: 30
estimated_duration_sec: 1800
dramatic_function: 建立世界、主角、诱发事件。
turning_point: 亚莉娅发现自己的系统接口可以篡改灵力规则。
dramatic_question: 亚莉娅能否意识到系统异常不是偶然，而是命运规则的裂缝？
turning_result: 她从被动逃生转向主动接近系统真相。
status: script_completed
updated_at: "2026-06-27T10:30:00+08:00"
```

### `sequences/seq_xxx/sequence.yaml`

Sequence 是电影结构中的 12-15 分钟段落，不是 4-15 秒分镜组；它只能用 `estimated_duration_sec` 做剧情估时。

```yaml
sequence_id: seq_001
project_id: proj_001
film_id: film_001
act_id: act_001
order_index: 1
title: 荒原日常
page_start: 1
page_end: 15
estimated_duration_sec: 900
dramatic_goal: 展示亚莉娅在废土中的生存方式。
conflict: 亚莉娅被纳米兽群追杀，同时系统出现异常提示。
ending_hook: 她第一次看见隐藏在天空中的系统裂缝。
dramatic_question: 亚莉娅能否活着穿过荒原，并理解追击背后的异常？
turning_result: 她发现追击规模不合常理，世界规则开始露出破绽。
status: script_completed
updated_at: "2026-06-27T10:30:00+08:00"
```

### `scenes/scene_xxx/scene.yaml`

Scene 对应 screenplay 里的场景标题。

```yaml
scene_id: scene_001
project_id: proj_001
film_id: film_001
act_id: act_001
sequence_id: seq_001
order_index: 1
slugline: 外景. 红色荒原 - 黄昏
scene_type: exterior
location_id: loc_red_wasteland
time_of_day: dusk
page_start: 1
page_end: 2.3
estimated_duration_sec: 138
characters:
  - char_aria
  - char_athena7
props:
  - prop_hoverbike
  - prop_glowing_goggles
dramatic_purpose: 亚莉娅第一次遭遇系统异常引发的兽群攻击。
conflict: 她想逃离荒原，但雅典娜-7判断后方热源数量异常。
dramatic_question: 亚莉娅是选择规避风险，还是冲向异常中心？
turning_result: 她选择不绕路，主动进入沙尘暴和系统异常的交界处。
scene_summary: 悬浮摩托穿越红色荒原，纳米兽群从沙丘中出现，系统提示发生错误。
continuity_state_in_id: cont_scene_001_in
continuity_state_out_id: cont_scene_001_out
platform_ref:
  scene_id: scene-platform-1
status: storyboard_in_progress
updated_at: "2026-06-27T10:30:00+08:00"
```

### `scenes/scene_xxx/script/blocks.yaml`

保存该场 screenplay 的最小文本块。每个 block 必须能回到剧本文本，不用分镜提示词替代正文。

质量边界：

- `action.text` 写镜头能看到、声音能听到、演员能执行的内容，例如人物走位、表情、物件、环境声和可见反应。
- `dialogue.text` 写角色实际说出口的台词；摘要式句子应改写成台词、动作或 `note`。
- 创作目的、主题解释、人物心理分析、导演意图、分镜提示词进入 `scene.yaml`、`beat.yaml`、`note` block 或 prompt 文件，不进入 `action` / `dialogue`。
- `character_id` 必须绑定到真实角色本地 ID 或平台 ID；`"undefined"`、空字符串和占位符视为脏数据。
- 同一长句跨多个 scene 重复出现时，优先重写为该场独有的空间、动作和声音。

```yaml
- block_id: blk_001_001
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001
  order_index: 1
  block_type: scene_heading
  text: 外景. 红色荒原 - 黄昏
  semantic_tags:
    locations:
      - loc_red_wasteland
  created_at: "2026-06-27T10:00:00+08:00"
  updated_at: "2026-06-27T10:00:00+08:00"

- block_id: blk_001_024
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001
  order_index: 24
  block_type: dialogue
  character_id: char_athena7
  text: 后方热源信号数量——三百以上。
  semantic_tags:
    characters:
      - char_athena7
    locations:
      - loc_red_wasteland
    props: []
    actions:
      - 扫描
      - 警告
    emotion:
      - 冷静
      - 紧迫
  created_at: "2026-06-27T10:00:00+08:00"
  updated_at: "2026-06-27T10:10:00+08:00"
```

创意/分析原文进入 screenplay blocks 前，应先完成改编选择。正向示例：

```yaml
- block_id: blk_004_001
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001_004
  order_index: 1
  block_type: scene_heading
  text: 外景. 轨道基地发射台 - 上午
  semantic_tags:
    locations:
      - loc_launch_platform

- block_id: blk_004_002
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001_004
  order_index: 2
  block_type: action
  text: 维修队员在冷风中列队。林岚站在发射台下，袖口磨破，冻裂的手垂在身侧。
  semantic_tags:
    characters:
      - char_lan
    locations:
      - loc_launch_platform

- block_id: blk_004_003
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001_004
  order_index: 3
  block_type: dialogue
  character_id: char_commander
  text: 今晚所有伤员都要过你的手。明天他们问责，先问我。
  semantic_tags:
    characters:
      - char_commander
      - char_lan
    props:
      - prop_temp_pass
      - prop_medkit
```

推荐 `block_type`：

```text
scene_heading, action, character, dialogue, parenthetical, transition, shot, insert, montage, intercut, super, note
```

### `scenes/scene_xxx/script/pages.yaml`

保存**本场内部页段估算**，用于在 scene 子树内快速理解这场戏覆盖哪些 block。它不是全片正式分页的唯一来源；只要出现跨场景页码，就以根级 `film-data/script/pages.yaml` 为准。

```yaml
- script_page_id: sp_scene_001_001
  project_id: proj_001
  film_id: film_001
  script_version_id: script_v001
  scene_id: scene_001
  local_page_index: 1
  estimated_duration_sec: 48
  coverage_level: partial_page_sample
  block_range:
    start_block_id: blk_001_001
    end_block_id: blk_001_012
  global_page_refs:
    - script_page_id: sp_001
      page_fraction: 0.8
  updated_at: "2026-06-27T10:30:00+08:00"
```

使用约束：

- scene 内 `pages.yaml` 的 `block_range` 只允许引用同一 scene 的 `blocks.yaml`。
- `local_page_index` 是 scene 内局部顺序，不等于全片 `page_number`。
- 若该 scene 已进入正式剧本排版，使用 `global_page_refs` 指向根级 `script/pages.yaml`。
- Agent 导出正式 screenplay DOCX 时，应优先读取根级 `script/pages.yaml`；没有根级页码索引时，才按 scene 顺序自然排版，scene 内 partial page 只作为场内估算。

### `beats/beat_xxx/beat.yaml`

Beat 是场景内的剧情动作单位，是分镜组的上游。

```yaml
beat_id: beat_001_002
project_id: proj_001
film_id: film_001
scene_id: scene_001
order_index: 2
title: 后方热源异常
estimated_duration_sec: 35
beat_type: escalation
description: 雅典娜-7发现后方热源数量异常，亚莉娅决定继续向前。
dramatic_question: 热源异常会迫使亚莉娅改变路线吗？
character_goals:
  char_aria: 尽快抵达炼塔，不愿绕路。
  char_athena7: 警告风险并建议规避。
turning_detail: 热源数量超过三百，追击规模远超预期。
turning_result: 亚莉娅拉下护目镜，决定冲入沙尘暴。
status: ready_for_segments
updated_at: "2026-06-27T10:30:00+08:00"
```

## Production Leaves

### `segments/seg_xxx/segment.yaml`

VideoSegment 是本地电影模式核心，代表 4-15 秒 AIGC 分镜组 / storyboard item。它仍然只是本地规划，不等同于提交生成任务；超过 15 秒的 Beat 必须拆成多条连续 VideoSegment，再进入 storyboard、prompt 或后续生成链路。

```yaml
video_segment_id: seg_001_002
project_id: proj_001
film_id: film_001
act_id: act_001
sequence_id: seq_001
scene_id: scene_001
beat_id: beat_001_002
order_index: 2
title: 后方热源异常
segment_type: aigc_video_group
duration_target_sec: 15
dramatic_purpose: 升级追击压力，让主角被迫做出冒险选择。
dramatic_question: 这一段是否让观众明确感到追击规模失控？
turning_result: 亚莉娅从逃离状态转入迎向危险的主动选择。
segment_summary: 悬浮摩托穿越红色荒原，雅典娜-7检测到后方三百多个热源信号，亚莉娅拉下护目镜准备冲入沙尘暴。
entry_frame_intent: 用宽景建立红色荒原和高速运动方向，让观众先感到空间压迫。
exit_frame_intent: 收在亚莉娅拉下护目镜并冲向沙尘暴中心，形成下一段的动作承接。
script_refs:
  - script_version_id: script_v001
    start_block_id: blk_001_021
    end_block_id: blk_001_034
    coverage: full
shot_ids:
  - shot_001_002_001
  - shot_001_002_002
  - shot_001_002_003
  - shot_001_002_004
prompt_id: prompt_seg_001_002_v001
status: storyboard_ready
updated_at: "2026-06-27T10:30:00+08:00"
```

### `segments/seg_xxx/script-links.yaml`

保存 VideoSegment 与 ScriptBlock 的细粒度映射。MVP 可只存在 `segment.yaml.script_refs`，但做重写或追溯时优先维护该文件。

```yaml
- link_id: link_seg_001_002_blk_001_024
  project_id: proj_001
  film_id: film_001
  video_segment_id: seg_001_002
  script_version_id: script_v001
  script_block_id: blk_001_024
  usage_type: dialogue
  coverage: full
  mapped_to:
    shot_id: shot_001_002_002
    dialogue_id: dlg_001_002_001
  text_snapshot: 后方热源信号数量——三百以上。
  created_at: "2026-06-27T10:12:00+08:00"
  updated_at: "2026-06-27T10:12:00+08:00"
```

推荐 `usage_type`：

```text
scene_heading, action, dialogue, character_state, prop_reference, location_reference, sound_cue, transition
```

### `segments/seg_xxx/shots.yaml`

保存分镜组下的镜头列表。若该文件过大，再拆为 `shots/shot_xxx.yaml`。

```yaml
- shot_id: shot_001_002_001
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002
  order_index: 1
  title: 荒原追击
  duration_target_sec: 4
  shot_type: wide shot
  camera:
    framing: wide shot
    movement: lateral tracking shot
    lens: 28mm
    depth_of_field: deep focus
    angle: eye level
  visual_description: 悬浮摩托从锈红色沙丘之间高速掠过，后方尘线逐渐逼近。
  entry_frame_intent: 建立红色荒原和高速运动方向。
  exit_frame_intent: 把追击压力推向后座扫描动作。
  script_refs:
    - script_block_id: blk_001_021
      usage_type: action
  prompt_id: prompt_shot_001_002_001_v001
  status: ready

- shot_id: shot_001_002_002
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002
  order_index: 2
  title: 雅典娜扫描
  duration_target_sec: 5
  shot_type: medium shot
  camera:
    framing: medium shot
    movement: tracking shot
    lens: 35mm
    depth_of_field: medium depth of field
    angle: slightly low angle
  visual_description: 雅典娜-7坐在悬浮摩托后座，抬起右手扫描后方，蓝色全息热源图在她眼前展开。
  entry_frame_intent: 从上一镜的高速荒原运动中切入后座扫描动作。
  exit_frame_intent: 以全息热源图的异常数量作为下一镜亚莉娅反应的动机。
  script_refs:
    - script_block_id: blk_001_024
      usage_type: dialogue
  prompt_id: prompt_shot_001_002_002_v001
  status: ready

- shot_id: shot_001_002_003
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002
  order_index: 3
  title: 亚莉娅反应
  duration_target_sec: 3
  shot_type: close-up
  camera:
    framing: close-up
    movement: slow push-in
    lens: 50mm
    depth_of_field: shallow depth of field
    angle: eye level
  visual_description: 亚莉娅听见热源数量后没有回头，只把护目镜慢慢拉下。
  entry_frame_intent: 承接热源异常的压力。
  exit_frame_intent: 让决定进入沙尘暴成为可见动作。
  script_refs:
    - script_block_id: blk_001_030
      usage_type: action
  prompt_id: prompt_shot_001_002_003_v001
  status: ready

- shot_id: shot_001_002_004
  project_id: proj_001
  film_id: film_001
  scene_id: scene_001
  beat_id: beat_001_002
  video_segment_id: seg_001_002
  order_index: 4
  title: 冲入尘暴
  duration_target_sec: 3
  shot_type: long shot
  camera:
    framing: long shot
    movement: slow dolly back
    lens: 35mm
    depth_of_field: deep focus
    angle: low angle
  visual_description: 悬浮摩托冲向暗紫色尘暴中心，人物轮廓被沙尘吞没。
  entry_frame_intent: 从主角决定转入空间动作。
  exit_frame_intent: 收在尘暴吞没画面，承接下一段。
  script_refs:
    - script_block_id: blk_001_034
      usage_type: action
  prompt_id: prompt_shot_001_002_004_v001
  status: ready
```

### `segments/seg_xxx/prompt.yaml`

保存可追溯提示词。必须同时保留来源、快照、编译结果、负面约束和输入资产。

```yaml
prompt_id: prompt_seg_001_002_v001
project_id: proj_001
film_id: film_001
target_type: video_segment
target_id: seg_001_002
prompt_type: video_group_prompt
version: 1
language: zh-CN
source_refs:
  script_version_id: script_v001
  script_blocks:
    - start_block_id: blk_001_021
      end_block_id: blk_001_034
  character_ids:
    - char_aria
    - char_athena7
  location_ids:
    - loc_red_wasteland
  prop_ids:
    - prop_hoverbike
    - prop_glowing_goggles
  style_guide_id: style_001
source_script_snapshot: 悬浮摩托从锈红色沙丘之间高速掠过。雅典娜-7抬起右手，蓝色全息热源图在她眼前展开。雅典娜-7：后方热源信号数量——三百以上。亚莉娅拉下发光护目镜，没有减速。
compiled_prompt: 生成一个15秒电影化写实分镜组。场景为红色荒原黄昏，悬浮摩托高速穿越锈红色沙丘，暗紫色量子尘暴在远处逼近。亚莉娅坐在前座驾驶，雅典娜-7坐在后座抬手扫描后方热源。
negative_prompt: 卡通化、插画感、漫画分镜格、角色服装漂移、角色离开悬浮摩托、现代城市元素。
input_asset_ids:
  - asset_aria_face_001
  - asset_athena_face_001
template_id: tpl_video_segment_seedance_v1
created_at: "2026-06-27T10:18:00+08:00"
updated_at: "2026-06-27T10:18:00+08:00"
```

### `segments/seg_xxx/continuity.yaml`

保存当前 segment 的 in/out 连续性状态。scene 级 continuity 可放在 `scene.yaml` 或单独的 `scene-continuity.yaml`，按所在 scene 子树维护。

```yaml
- continuity_state_id: cont_seg_001_002_in
  project_id: proj_001
  film_id: film_001
  scope: video_segment
  target_id: seg_001_002
  position: in
  summary: 亚莉娅仍在逃离纳米兽群，沙尘暴尚未逼近。
  updated_at: "2026-06-27T10:25:00+08:00"

- continuity_state_id: cont_seg_001_002_out
  project_id: proj_001
  film_id: film_001
  scope: video_segment
  target_id: seg_001_002
  position: out
  characters:
    char_aria:
      position: 悬浮摩托前座
      held_props:
        - prop_glowing_goggles
      emotion: 紧张转为决绝
  environment:
    location_id: loc_red_wasteland
    weather: 沙尘暴逼近
    light: 黄昏暗紫天光
  summary: 亚莉娅拉下护目镜，决定不绕开沙尘暴，而是直接冲进去。
  updated_at: "2026-06-27T10:25:00+08:00"
```

## Update Rules

- 改三幕大纲或结局时，先更新 `film-three-act-outline.md`，再同步 `acts/**/act.yaml`、`sequence.yaml`、`scene.yaml` 和相关 `index.yaml`。
- 改剧本正文时，先更新对应 scene 子树的 `script/blocks.yaml`，再同步 scene 内 `script/pages.yaml` 和根级 `script/pages.yaml` 的 block 范围；随后检查该 scene 下所有 segment 的 `script_refs`、`script-links.yaml`、`prompt.yaml.source_script_snapshot` 是否仍能追溯正文。
- 做文学精修时，每次以单个 scene 为单位：先读 `scene.yaml`、`beats/index.yaml`、`script/blocks.yaml`，再查该 scene 下 segment 的 `segment.yaml`、`script-links.yaml` 和 `script_refs`。
- 文学精修只改文字表达时，保持 `block_id`、`order_index`、`block_type`、scene 内 `pages.yaml`、根级 `script/pages.yaml` 和 segment `script_refs` 稳定；只同步必要的 `semantic_tags` 和 `source_script_snapshot`。
- 文学精修若新增、删除或重排 block，必须同步更新 scene 内 `pages.yaml`、根级 `script/pages.yaml`、受影响 segment 的 `script_refs`、`script-links.yaml`、`prompt.yaml.source_script_snapshot`，并重新检查所有引用的 `start_block_id` / `end_block_id`。
- 重写某个分镜组时，只更新对应 `seg_xxx/` 子树；除非剧情结构改变，其他 segment 文件保持稳定。若重写后超过 15 秒，拆成多个连续 segment，单个分镜组仍保持 4-15 秒。
- 如果镜头内容新增/删除角色、场景或关键道具，同时更新该 segment 的 `segment.yaml`、`shots.yaml`、`prompt.yaml` 引用，并确保平台 storyboard JSON 的结构化绑定仍正确。
- 改任何时长字段后，运行 `cuelight-cli internal film-data duration --project-id <projectId>` 检查汇总；准备交付或批量写回前使用 `--strict`。
- 若已有平台资源 ID，保留在 `platform_ref` 中；本地 ID 与平台 ID 分层记录。
- 到 `production` 为止停止：真实模型调用、资产审核结果、成片时间线或导出状态仍由平台/CLI 记录。

## Acceptance

- 本地结构覆盖 `Film -> StoryBible -> StyleGuide -> ScriptVersion -> ScriptBlock -> ScriptPage -> Act -> Sequence -> Scene -> Beat -> VideoSegment -> Shot -> Prompt -> ContinuityState`。
- 树形路径能从 `acts/index.yaml` 逐级找到 `segment.yaml`。
- 非样例电影结构必须有多个 Sequence、Scene、Beat、VideoSegment 和 Shot；如果是最小样例，必须标记 `sample` / `incomplete`。
- 每个 `index.yaml` 只做顺序和路径索引，不承载大段正文。
- 每个 `segment.yaml` 都有 `script_refs`、`scene_id`、`beat_id`、`duration_target_sec`、`shot_ids`、`prompt_id`，且 `duration_target_sec` 在 4-15 秒之间。
- 每个 `shots.yaml` 的 `duration_target_sec` 合计等于对应 `segment.yaml.duration_target_sec`，误差不超过 2 秒。
- 每个 `prompt.yaml` 都有 `source_refs`、`source_script_snapshot`、`compiled_prompt`、`negative_prompt`、`input_asset_ids`。
- `continuity.yaml` 能说明当前 segment 的进入或离开状态。
- `cuelight-cli internal film-data duration --project-id <projectId> --strict` 不报告 error；若验收目标是第一幕完整拆解，也不得报告 `cardinality_*` warning。Agent 还必须说明时长是否由真实 screenplay 容量、scene/beat 分布和剧情密度支撑。
- 从创意类原文生成 screenplay blocks 后，运行 `python .codex/skills/cuelight-drama/scripts/check_film_screenplay_quality.py --film-data-dir <film-data> --strict`；`action` / `dialogue` 中不应混入创作说明、摘要式对白、模板复读、变量填充式句型、文学化套话、空间逻辑错位、场内角色错置或 `"undefined"` 角色 ID，`literaryScore.score` 应达到 `passingScore`。若报告 `templated_screenplay_pattern`、`repeated_sentence_skeleton`、`synthetic_rewrite_template`、`generic_literary_filler`、`spatial_logic_mismatch` 或 `unexpected_role_mention`，必须先进入 Literary Rewrite Loop，不能进入 production-ready。
- 验收报告必须记录 Literary Rewrite Loop Engineering（文学精修循环工程）和所有 Agent-Owned Gates（Agent 主导验收门）：本轮范围、红灯 issue、修复动作、strict 结果、Agent 抽查对象、证据短句、`pass` / `fail` 和是否允许下游生产。只有脚本通过且 Agent 审查达到文学级合格线，才可标记 `production_ready`；只列工具结果的报告视为 `draft_not_reviewed`。
- Dialogue Readability Gate 必须读取 `check_film_screenplay_quality.py --strict --json` 的 `dialogueReadability.pages`；正式页不得报告 `page_dialogue_underfit`、`single_speaker_dialogue_page`、`dialogue_turn_underfit`、`dialogue_action_interleave_missing` 或 `unlocalized_screenplay_term`，除非验收报告写明例外页、例外原因和 Agent 放行证据。
- Action/Suspense Page Gate 与 Reveal Chain Gate 必须记录无对白页/动作悬念页的抽查证据：视觉焦点、声音触发、人物反应、动作阻力、危险升级或剪辑动机。验收报告不得把“每页必须塞对白”当成规则。
- 正式 screenplay 通过文学审查后、进入 DOCX / production-ready / 生成阶段前，必须记录 Commercialization Punch-up Pass（商业化强化环节）与 Commercial Review Gate（商业化审查门）：说明关键场的入场目标、外部阻力、可见冲突、场尾钩子和类型承诺如何落到正文事件。若工具 strict 通过但 Agent 抽读发现同场动作复用、意象空转、冲突未外化或场尾无推进，验收结论必须为 `fail`，并记录 repair loop（修复循环）。
- 正式标称时长必须由真实 screenplay 容量支撑；完整第一幕 1080 秒至少应有约 5760 个 screenplay 字符，并通过 `screenplay_capacity_underfit` 检查。正式分页还必须通过去重后逐页容量检查：每个 ScriptPage 保底 `320` 个非重复可拍字符，推荐 `350-420`；重复模板句、跨页复用长句和复制来的环境描写不计入有效容量。Segment 不得重复绑定同一组 `script_refs` 来填充时长。
- Literary Rewrite Pass（文学精修环节）或 Commercialization Punch-up Pass（商业化强化环节）后再次运行 duration strict 和 screenplay quality strict；若未新增/删除 block，抽查 segment `script_refs` 应仍指向原 `block_id` 范围，并执行 Production Leaves Sync Audit（生产叶节点同步审查）：抽查 affected segment 的 `script-links.yaml`、`prompt.yaml.source_script_snapshot`、`prompt.yaml.compiled_prompt` 和 `shots.yaml.visual_description` 是否追溯最新 screenplay。
- 进入分镜、生成或正式 DOCX 导出前，根级 `script/pages.yaml` 不应报告 `duplicate_page_block_ref`；多页 scene 的 ScriptPage 必须覆盖不同 block 区间。
- 导出正式 screenplay DOCX 前，确认根级 `script/pages.yaml` 可解析且每个 `block_refs` 能找到对应 block；导出后至少反读 DOCX 段落，条件允许时渲染前 3 页检查格式。
- 中文剧本正文默认使用 `视角：`、`特写：`、`跟拍：`、`声音：`、`画外：`、`旁白：`、`插入：`；DOCX gate 需要检查正文不含 `SOUND`、`INSERT`、`CLOSE ON`、`ANGLE ON`、`MOVING WITH` 这类未本地化提示。
- 所有本地结构文件可被人类直接打开预览，且文件内容为可直接解析的 YAML。
