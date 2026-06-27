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
- 默认按电影叙事树组织目录：`Act -> Sequence -> Scene -> Beat -> VideoSegment`。不要把长片内容按实体类型塞进全局大表。
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

不要创建超出 Production 的电影本地结构目录。若用户要求提交视频生成、审核资产、整理成片顺序或导出成片，切回当前平台/CLI 能力或说明该本地结构暂不覆盖。

旧式全局聚合文件不再作为默认结构：不要新增 `structure/acts.yaml`、`structure/scenes.yaml`、`production/shots.yaml`、`production/prompts.yaml`、全局 `script/blocks.yaml` 这类会随长片规模膨胀的叶子文件。

## Workflow

1. 从电影创意、梗概或 treatment 起步时，先维护 `film.yaml`、`story-bible.yaml`、`style-guide.yaml` 和 `film-three-act-outline.md`。
2. 写 screenplay 时，更新根级 `script/versions.yaml`，并把正文块写入对应场景目录的 `scene_xxx/script/blocks.yaml`。若需要正式全片分页，同时维护根级 `script/pages.yaml`；scene 内 `pages.yaml` 只保存本场内部页段估算。
3. 拆分镜前，沿树形路径维护 `acts/**/act.yaml`、`sequence.yaml`、`scene.yaml`、`beat.yaml`，并更新各级 `index.yaml`。
4. 生成分镜组、镜头和提示词时，在对应 `seg_xxx/` 目录维护 `segment.yaml`、`script-links.yaml`、`shots.yaml`、`prompt.yaml`、`continuity.yaml`。
5. 写回 CueLight 当前支持的项目、Bible、角色、场景、道具、episode、storyboard 时，继续使用主 skill 和 CLI；本地 film-data 只负责保存电影级结构和可追溯依据。

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

保存**全片正式剧本页码索引**，用于 `1 页 ≈ 1 分钟` 的 screenplay 层估时。它不保存正文全文，只通过 `block_refs` 指向各 scene 的 `script/blocks.yaml`。

当一页跨多个场景时，必须用多个 `block_refs` 表达；不要把跨场景页码拆散到各 scene 子目录里伪装成完整页。

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

- `page_number` 是全片剧本页码，不是 scene 内局部页码。
- `block_refs[].start_block_id` / `end_block_id` 必须能在对应 `script_path` 的 `blocks.yaml` 中找到。
- `block_refs[].page_fraction` 合计通常为 `1.0`；样例或未排满页可使用小于 `1.0`，并标记 `coverage_level: partial_page_sample`。
- `estimated_duration_sec` 是剧本页估时，供 Scene / Sequence / Act / Film 汇总，不直接下推为 Shot 时长。
- 修改剧本文本、插入或删除 block 后，必须重算受影响的 `script/pages.yaml` 页码范围，再检查相关 segment 的 `script_refs` 和 `script-links.yaml`。

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
- Agent 导出正式 screenplay DOCX 时，应优先读取根级 `script/pages.yaml`；没有根级页码索引时，才按 scene 顺序自然排版，不要把 scene 内 partial page 硬拆成 Word 物理页。

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
negative_prompt: 不要卡通，不要插画，不要漫画分镜格，不要改变角色服装，不要让角色离开悬浮摩托，不要出现现代城市。
input_asset_ids:
  - asset_aria_face_001
  - asset_athena_face_001
template_id: tpl_video_segment_seedance_v1
created_at: "2026-06-27T10:18:00+08:00"
updated_at: "2026-06-27T10:18:00+08:00"
```

### `segments/seg_xxx/continuity.yaml`

保存当前 segment 的 in/out 连续性状态。scene 级 continuity 可放在 `scene.yaml` 或单独的 `scene-continuity.yaml`，不要放进全局大表。

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
- 重写某个分镜组时，只更新对应 `seg_xxx/` 子树；除非剧情结构改变，不要改动其他 segment 文件。若重写后超过 15 秒，拆成多个连续 segment，不要放宽单个分镜组时长。
- 如果镜头内容新增/删除角色、场景或关键道具，同时更新该 segment 的 `segment.yaml`、`shots.yaml`、`prompt.yaml` 引用，并确保平台 storyboard JSON 的结构化绑定仍正确。
- 若已有平台资源 ID，保留在 `platform_ref` 中，不要把本地 ID 当成平台 ID。
- 到 `production` 为止停止：不要在本地 film-data 里记录真实模型调用、资产审核结果、成片时间线或导出状态。

## Acceptance

- 本地结构覆盖 `Film -> StoryBible -> StyleGuide -> ScriptVersion -> ScriptBlock -> ScriptPage -> Act -> Sequence -> Scene -> Beat -> VideoSegment -> Shot -> Prompt -> ContinuityState`。
- 树形路径能从 `acts/index.yaml` 逐级找到 `segment.yaml`。
- 每个 `index.yaml` 只做顺序和路径索引，不承载大段正文。
- 每个 `segment.yaml` 都有 `script_refs`、`scene_id`、`beat_id`、`duration_target_sec`、`shot_ids`、`prompt_id`，且 `duration_target_sec` 在 4-15 秒之间。
- 每个 `prompt.yaml` 都有 `source_refs`、`source_script_snapshot`、`compiled_prompt`、`negative_prompt`、`input_asset_ids`。
- `continuity.yaml` 能说明当前 segment 的进入或离开状态。
- 所有本地结构文件可被人类直接打开预览，且文件内容为可直接解析的 YAML。
