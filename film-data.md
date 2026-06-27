下面是一套适合 **CueLight 兼容电影项目** 的完整数据结构设计。它不是简单的 Prompt 表，而是围绕：

```text
电影项目 → 剧本 → 场景结构 → 分镜组 → 镜头 → 生成任务 → 资产版本 → 审核 → 时间线 → 导出
```

来设计。

---

# 1. 总体实体层级

推荐完整层级：

```text
Project 项目
└── Film 影片
    ├── StoryBible 故事圣经
    ├── StyleGuide 风格规范
    ├── Character 角色库
    ├── Location 场景库
    ├── Prop 道具库
    ├── ScriptVersion 剧本版本
    │   ├── ScriptBlock 剧本文本块
    │   └── ScriptPage 剧本分页
    ├── Act 幕
    │   └── Sequence 段落
    │       └── Scene 场
    │           └── Beat 情节点
    │               └── VideoSegment 分镜组 / 生成段
    │                   └── Shot 镜头 / 分镜
    ├── Prompt 提示词
    ├── GenerationTask 生成任务
    ├── Asset 资产 / 生成结果
    ├── Review 审核记录
    ├── Timeline 时间线
    └── Export 导出任务
```

其中最关键的是：

```text
ScriptBlock
→ VideoSegment
→ Shot
→ GenerationTask
→ Asset
→ TimelineClip
```

---

# 2. 推荐集合列表

如果你用 MongoDB / Document DB，可以按这些集合设计：

```text
projects
films
story_bibles
style_guides

characters
locations
props
assets

script_versions
script_blocks
script_pages

acts
sequences
scenes
beats

video_segments
video_segment_script_links
shots

prompts
generation_tasks
reviews

timelines
timeline_tracks
timeline_clips

exports
cost_records
```

如果用 PostgreSQL，也可以基本按同样表结构落地，复杂字段用 `jsonb`。

---

# 3. Project 项目

`projects` 是项目容器，适配短剧、电影、广告、游戏广告等类型。

```json
{
  "project_id": "proj_001",
  "owner_id": "user_001",
  "workspace_id": "ws_001",

  "project_type": "film",
  "title": "荒原修仙：废土的BUG",
  "status": "active",

  "cover_asset_id": "asset_cover_001",

  "spec": {
    "target_duration_sec": 7200,
    "aspect_ratio": "2.39:1",
    "resolution": "4K",
    "fps": 24,
    "language": "zh-CN",
    "subtitle_languages": ["zh-CN", "en-US"]
  },

  "progress": {
    "script": 0.8,
    "storyboard": 0.35,
    "video": 0.12,
    "audio": 0,
    "timeline": 0
  },

  "created_at": "2026-06-27T10:00:00+08:00",
  "updated_at": "2026-06-27T10:30:00+08:00"
}
```

---

# 4. Film 影片信息

`films` 存电影本体信息。

```json
{
  "film_id": "film_001",
  "project_id": "proj_001",

  "title": "荒原修仙：废土的BUG",
  "original_title": "Future Cultivation: Wasteland System Error",

  "genre": ["科幻", "修仙", "废土"],
  "format": "feature_film",
  "target_duration_sec": 7200,

  "logline": "一个废土少女在崩坏的修仙系统中发现世界被错误代码控制。",
  "synopsis": "灵气枯竭后的废土世界中，亚莉娅意外接入残缺修仙系统，并发现整个世界的命运被一段错误代码锁死。",

  "theme": "人在系统命运中的自由意志",
  "tone": "冷峻、史诗、宿命感",

  "rating_target": "PG-13",
  "status": "development"
}
```

---

# 5. StoryBible 故事圣经

`story_bibles` 是全片设定源头。

```json
{
  "story_bible_id": "bible_001",
  "project_id": "proj_001",
  "film_id": "film_001",
  "version": 1,

  "world_setting": "灵气枯竭后的废土世界，修仙宗门遗迹与高科技残骸共存。",
  "core_conflict": "主角试图打破系统锁死的命运规则。",
  "theme": "自由意志与系统命运的冲突",

  "world_rules": [
    "灵力以蓝白色粒子流呈现",
    "系统错误以黑红色数据裂纹呈现",
    "修仙能力来自残缺系统接口"
  ],

  "visual_keywords": [
    "红色荒原",
    "破碎仙门",
    "量子尘暴",
    "赛博符箓",
    "残旧飞剑"
  ],

  "forbidden_elements": [
    "不要出现现代商业街",
    "不要卡通化",
    "不要过度游戏UI化"
  ],

  "created_at": "2026-06-27T10:00:00+08:00"
}
```

---

# 6. StyleGuide 风格规范

`style_guides` 用来统一全片视觉和视频生成风格。

```json
{
  "style_guide_id": "style_001",
  "project_id": "proj_001",
  "film_id": "film_001",

  "name": "废土修仙电影写实风格",
  "output_style": "live-action photoreal cinematic realism",

  "camera_language": {
    "default_fps": 24,
    "default_lens": "35mm cinematic lens",
    "camera_movement": "grounded live-action camera movement",
    "avoid": [
      "过度漂浮镜头",
      "游戏式运镜",
      "不合理快速变焦"
    ]
  },

  "lighting": {
    "palette": ["锈红", "暗紫", "冷蓝灵光", "黑金"],
    "contrast": "medium-high",
    "default_mood": "压迫、荒凉、危险"
  },

  "texture_rules": [
    "自然皮肤纹理",
    "真实布料材质",
    "风沙颗粒真实",
    "金属和护甲有磨损感"
  ],

  "negative_style_rules": [
    "不要彩铅",
    "不要手绘",
    "不要漫画",
    "不要动画风",
    "不要故事板格子",
    "不要纸张纹理"
  ],

  "reference_asset_ids": [
    "asset_style_001",
    "asset_style_002"
  ]
}
```

---

# 7. Character 角色

`characters` 是角色一致性的核心。

```json
{
  "character_id": "char_aria",
  "project_id": "proj_001",
  "film_id": "film_001",

  "name": "亚莉娅",
  "role_type": "protagonist",
  "gender": "female",
  "age": 19,

  "description": "废土中长大的少女，警觉、倔强，拥有异常系统接口。",

  "appearance": {
    "face": "清瘦脸型，眼神锐利，左眼有淡蓝色数据纹",
    "hair": "黑色短发，发尾带灰白尘土",
    "body": "身形瘦削但敏捷",
    "skin": "自然肤色，带风沙晒痕"
  },

  "personality": {
    "traits": ["警觉", "倔强", "行动优先", "不轻易信任"],
    "speech_style": "短句、直接、很少解释"
  },

  "arc": {
    "start": "只相信自己能活下去",
    "middle": "意识到系统背后有更大阴谋",
    "end": "主动选择破坏系统秩序"
  },

  "costumes": [
    {
      "costume_id": "costume_aria_01",
      "name": "废土防辐射服",
      "description": "彩色拼接防辐射外套，磨损边缘，腰间挂旧式符箓模块",
      "asset_ids": ["asset_costume_aria_001"],
      "default": true
    }
  ],

  "reference_assets": {
    "face_refs": ["asset_aria_face_001"],
    "body_refs": ["asset_aria_body_001"],
    "expression_refs": ["asset_aria_expr_001"],
    "costume_refs": ["asset_costume_aria_001"]
  },

  "consistency_rules": [
    "左眼数据纹必须保留",
    "不要变成长发",
    "不要改变年龄感",
    "服装保持彩色拼接防辐射风格"
  ],

  "status": "approved"
}
```

---

# 8. Location 场景库

`locations` 存可复用场景。

```json
{
  "location_id": "loc_red_wasteland",
  "project_id": "proj_001",
  "film_id": "film_001",

  "name": "红色荒原",
  "location_type": "exterior",

  "description": "锈红色沙漠，远处有破碎仙门遗迹和量子尘暴。",
  "visual_elements": [
    "锈红色沙丘",
    "暗紫色天空",
    "远处仙门残骸",
    "漂浮发光尘粒"
  ],

  "lighting": {
    "default_time": "dusk",
    "palette": "锈红、暗紫、冷蓝灵光",
    "mood": "荒凉、危险、史诗"
  },

  "reference_assets": {
    "wide_refs": ["asset_loc_red_wasteland_wide_001"],
    "detail_refs": ["asset_loc_red_wasteland_detail_001"]
  },

  "continuity_rules": [
    "天空保持暗紫色量子尘云",
    "地面保持锈红色沙质纹理",
    "远景保留仙门遗迹轮廓"
  ],

  "status": "approved"
}
```

---

# 9. Prop 道具

`props` 存载具、武器、护目镜、符箓等。

```json
{
  "prop_id": "prop_hoverbike",
  "project_id": "proj_001",
  "film_id": "film_001",

  "name": "悬浮摩托",
  "prop_type": "vehicle",

  "description": "废土改装悬浮摩托，外壳磨损，底部有蓝白色反重力光流。",
  "visual_rules": [
    "车身保持黑色金属和锈蚀边缘",
    "底部悬浮光必须为蓝白色",
    "不要变成现代公路摩托"
  ],

  "reference_asset_ids": [
    "asset_prop_hoverbike_001"
  ],

  "status": "approved"
}
```

---

# 10. Asset 资产统一表

`assets` 存所有图片、视频、音频、字幕、文档、参考图、生成结果。

```json
{
  "asset_id": "asset_video_seg_002_v003",
  "project_id": "proj_001",
  "film_id": "film_001",

  "asset_type": "video_clip",
  "usage_type": "generated_output",

  "name": "Segment 002 后方热源异常 V003",
  "uri": "s3://cuelight/projects/proj_001/videos/seg_002_v003.mp4",
  "thumbnail_uri": "s3://cuelight/projects/proj_001/thumbs/seg_002_v003.jpg",

  "source": {
    "source_type": "generation_task",
    "task_id": "task_000321",
    "target_type": "video_segment",
    "target_id": "seg_001_002"
  },

  "metadata": {
    "duration_sec": 20.4,
    "resolution": "1920x1080",
    "fps": 24,
    "codec": "h264",
    "has_audio": false,
    "width": 1920,
    "height": 1080
  },

  "quality_scores": {
    "character_consistency": 0.87,
    "scene_consistency": 0.92,
    "action_accuracy": 0.81,
    "visual_quality": 0.9,
    "cut_continuity": 0.85
  },

  "review_status": "approved",
  "version": 3,

  "created_at": "2026-06-27T10:25:00+08:00"
}
```

---

# 11. ScriptVersion 剧本版本

`script_versions` 管理剧本版本。

```json
{
  "script_version_id": "script_v003",
  "project_id": "proj_001",
  "film_id": "film_001",

  "version": 3,
  "title": "第三版剧本",
  "status": "active",

  "format_profile": "master_scene_a4_cn_v1",

  "stats": {
    "page_count": 118.6,
    "estimated_duration_sec": 7116,
    "scene_count": 68,
    "word_count": 58620
  },

  "created_by": "user_001",
  "created_at": "2026-06-27T10:00:00+08:00"
}
```

---

# 12. ScriptBlock 剧本文本块

`script_blocks` 是剧本正文的最小结构单位。

```json
{
  "block_id": "blk_001_024",
  "project_id": "proj_001",
  "film_id": "film_001",
  "script_version_id": "script_v003",

  "scene_id": "scene_001",
  "order_index": 24,

  "block_type": "dialogue",
  "character_id": "char_athena7",

  "text": "后方热源信号数量——三百以上。",

  "format": {
    "style": "dialogue",
    "indent_profile": "master_scene_cn"
  },

  "semantic_tags": {
    "characters": ["char_athena7"],
    "locations": ["loc_red_wasteland"],
    "props": [],
    "actions": ["扫描", "警告"],
    "emotion": ["冷静", "紧迫"]
  },

  "created_at": "2026-06-27T10:00:00+08:00",
  "updated_at": "2026-06-27T10:10:00+08:00"
}
```

`block_type` 建议枚举：

```text
scene_heading
action
character
dialogue
parenthetical
transition
shot
insert
montage
intercut
super
note
```

---

# 13. ScriptPage 剧本分页

`script_pages` 用来承载“一页约一分钟”。

```json
{
  "script_page_id": "sp_001",
  "project_id": "proj_001",
  "film_id": "film_001",
  "script_version_id": "script_v003",

  "page_number": 1,
  "format_profile": "master_scene_a4_cn_v1",

  "estimated_duration_sec": 60,

  "block_range": {
    "start_block_id": "blk_001_001",
    "end_block_id": "blk_001_018"
  },

  "scene_ranges": [
    {
      "scene_id": "scene_001",
      "page_fraction": 1.0,
      "estimated_duration_sec": 60
    }
  ]
}
```

如果一页跨两个场景：

```json
{
  "script_page_id": "sp_012",
  "page_number": 12,
  "estimated_duration_sec": 60,
  "scene_ranges": [
    {
      "scene_id": "scene_005",
      "page_fraction": 0.35,
      "estimated_duration_sec": 21
    },
    {
      "scene_id": "scene_006",
      "page_fraction": 0.65,
      "estimated_duration_sec": 39
    }
  ]
}
```

---

# 14. Act 幕

`acts` 存电影大结构。

```json
{
  "act_id": "act_001",
  "project_id": "proj_001",
  "film_id": "film_001",

  "order_index": 1,
  "title": "第一幕：建立与进入",

  "page_start": 1,
  "page_end": 30,
  "estimated_duration_sec": 1800,

  "dramatic_function": "建立世界、主角、诱发事件",
  "turning_point": "亚莉娅发现自己的系统接口可以篡改灵力规则",

  "status": "script_completed"
}
```

---

# 15. Sequence 段落

注意：这里的 `Sequence` 是电影结构中的 12–15 分钟段落，不是 10–30 秒分镜组。

```json
{
  "sequence_id": "seq_001",
  "project_id": "proj_001",
  "film_id": "film_001",
  "act_id": "act_001",

  "order_index": 1,
  "title": "荒原日常",

  "page_start": 1,
  "page_end": 15,
  "estimated_duration_sec": 900,

  "dramatic_goal": "展示亚莉娅在废土中的生存方式",
  "conflict": "亚莉娅被纳米兽群追杀，同时系统出现异常提示",
  "ending_hook": "她第一次看见隐藏在天空中的系统裂缝",

  "status": "script_completed"
}
```

---

# 16. Scene 场

`scenes` 对应电影剧本里的场景标题。

```json
{
  "scene_id": "scene_001",
  "project_id": "proj_001",
  "film_id": "film_001",
  "sequence_id": "seq_001",
  "act_id": "act_001",

  "order_index": 1,

  "slugline": "外景. 红色荒原 - 黄昏",
  "scene_type": "exterior",
  "location_id": "loc_red_wasteland",
  "time_of_day": "dusk",

  "page_start": 1,
  "page_end": 2.3,
  "script_page_count": 2.3,
  "estimated_duration_sec": 138,

  "characters": [
    "char_aria",
    "char_athena7"
  ],

  "props": [
    "prop_hoverbike",
    "prop_glowing_goggles"
  ],

  "dramatic_purpose": "亚莉娅第一次遭遇系统异常引发的兽群攻击。",
  "conflict": "她想逃离荒原，但雅典娜-7判断后方热源数量异常。",

  "scene_summary": "悬浮摩托穿越红色荒原，纳米兽群从沙丘中出现，系统提示发生错误。",

  "continuity_state_in_id": "cont_scene_001_in",
  "continuity_state_out_id": "cont_scene_001_out",

  "coverage": {
    "video_segment_count": 5,
    "shot_count": 24,
    "generated_segment_count": 2,
    "approved_segment_count": 1
  },

  "status": "storyboard_in_progress"
}
```

---

# 17. Beat 情节点

`beats` 用来把一场戏拆成剧情动作单位。

```json
{
  "beat_id": "beat_001_002",
  "project_id": "proj_001",
  "film_id": "film_001",
  "scene_id": "scene_001",

  "order_index": 2,
  "title": "后方热源异常",

  "duration_target_sec": 35,

  "beat_type": "escalation",
  "description": "雅典娜-7发现后方热源数量异常，亚莉娅决定继续向前。",

  "character_goals": {
    "char_aria": "尽快抵达炼塔，不愿绕路",
    "char_athena7": "警告风险并建议规避"
  },

  "turning_detail": "热源数量超过三百，追击规模远超预期",

  "status": "ready_for_segments"
}
```

---

# 18. VideoSegment 分镜组 / 生成段

这是 CueLight 电影模式的核心实体。

`video_segments` 承载 10–30 秒 AIGC 视频生成单元。

```json
{
  "video_segment_id": "seg_001_002",
  "project_id": "proj_001",
  "film_id": "film_001",

  "act_id": "act_001",
  "sequence_id": "seq_001",
  "scene_id": "scene_001",
  "beat_id": "beat_001_002",

  "order_index": 2,

  "title": "后方热源异常",
  "segment_type": "aigc_video_group",

  "duration_target_sec": 20,
  "duration_actual_sec": null,

  "dramatic_purpose": "升级追击压力，让主角被迫做出冒险选择。",
  "segment_summary": "悬浮摩托穿越红色荒原，雅典娜-7检测到后方三百多个热源信号，亚莉娅拉下护目镜准备冲入沙尘暴。",

  "script_refs": [
    {
      "script_version_id": "script_v003",
      "start_block_id": "blk_001_021",
      "end_block_id": "blk_001_034",
      "coverage": "full"
    }
  ],

  "characters": [
    {
      "character_id": "char_aria",
      "costume_id": "costume_aria_01",
      "state": "紧张、专注，正在驾驶悬浮摩托",
      "position": "悬浮摩托前座"
    },
    {
      "character_id": "char_athena7",
      "costume_id": "costume_athena_01",
      "state": "冷静扫描，但语气出现紧迫感",
      "position": "悬浮摩托后座"
    }
  ],

  "location_id": "loc_red_wasteland",

  "props": [
    "prop_hoverbike",
    "prop_glowing_goggles"
  ],

  "asset_refs": {
    "character_refs": [
      "asset_aria_face_001",
      "asset_athena_face_001"
    ],
    "location_refs": [
      "asset_loc_red_wasteland_wide_001"
    ],
    "prop_refs": [
      "asset_prop_hoverbike_001",
      "asset_prop_goggles_001"
    ],
    "style_refs": [
      "asset_style_001"
    ],
    "previous_frame_ref": "asset_keyframe_seg_001_last"
  },

  "continuity": {
    "previous_segment_id": "seg_001_001",
    "next_segment_id": "seg_001_003",
    "continuity_in_id": "cont_seg_001_002_in",
    "continuity_out_id": "cont_seg_001_002_out"
  },

  "shot_ids": [
    "shot_001_002_001",
    "shot_001_002_002",
    "shot_001_002_003",
    "shot_001_002_004",
    "shot_001_002_005"
  ],

  "prompt_id": "prompt_seg_001_002_v002",

  "generation_policy": {
    "mode": "generate_as_group",
    "allow_split_generation": true,
    "fallback_split_sec": [5, 5, 4, 2, 4],
    "preferred_models": ["seedance", "runway_gen3", "pika"]
  },

  "selected_video_asset_id": null,

  "status": "ready_for_generation"
}
```

`status` 建议枚举：

```text
draft
script_linked
prompt_ready
storyboard_ready
keyframe_ready
ready_for_generation
generating
generated
reviewing
approved
rejected
in_timeline
```

---

# 19. VideoSegment 与剧本文本映射

如果只是 MVP，可以直接存在 `video_segments.script_refs`。

如果要做正式系统，建议加独立集合：

```text
video_segment_script_links
```

示例：

```json
{
  "link_id": "link_seg_001_002_blk_001_024",
  "project_id": "proj_001",
  "film_id": "film_001",

  "video_segment_id": "seg_001_002",
  "script_version_id": "script_v003",
  "script_block_id": "blk_001_024",

  "usage_type": "dialogue",
  "coverage": "full",

  "mapped_to": {
    "shot_id": "shot_001_002_002",
    "dialogue_id": "dlg_001_002_001"
  },

  "text_snapshot": "后方热源信号数量——三百以上。",

  "created_at": "2026-06-27T10:12:00+08:00"
}
```

`usage_type` 建议枚举：

```text
scene_heading
action
dialogue
character_state
prop_reference
location_reference
sound_cue
transition
```

---

# 20. Shot 镜头 / 分镜

`shots` 是分镜组下面的单个镜头。

```json
{
  "shot_id": "shot_001_002_002",
  "project_id": "proj_001",
  "film_id": "film_001",

  "scene_id": "scene_001",
  "beat_id": "beat_001_002",
  "video_segment_id": "seg_001_002",

  "order_index": 2,

  "title": "雅典娜扫描",
  "duration_target_sec": 5,

  "shot_type": "medium shot",

  "camera": {
    "framing": "medium shot",
    "movement": "tracking shot",
    "lens": "35mm",
    "depth_of_field": "medium depth of field",
    "angle": "slightly low angle"
  },

  "visual_description": "雅典娜-7坐在悬浮摩托后座，抬起右手扫描后方，蓝色全息热源图在她眼前展开。",

  "characters": [
    {
      "character_id": "char_athena7",
      "action": "抬手扫描后方热源",
      "emotion": "冷静、警觉",
      "position": "悬浮摩托后座"
    }
  ],

  "dialogue": [
    {
      "dialogue_id": "dlg_001_002_001",
      "character_id": "char_athena7",
      "text": "后方热源信号数量——三百以上。",
      "delivery": "冷静、压低声音"
    }
  ],

  "audio": {
    "ambience": "低沉风沙声",
    "sfx": ["悬浮摩托电磁轰鸣", "热源扫描提示音"],
    "music_cue": "低频紧张铺底"
  },

  "script_refs": [
    {
      "script_block_id": "blk_001_024",
      "usage_type": "dialogue"
    }
  ],

  "prompt_id": "prompt_shot_001_002_002_v001",
  "selected_asset_id": null,

  "status": "ready"
}
```

---

# 21. Prompt 提示词

`prompts` 需要同时支持：

```text
分镜组提示词
单镜头提示词
角色图提示词
场景图提示词
视频生成提示词
音频提示词
字幕提示词
```

示例：分镜组提示词。

```json
{
  "prompt_id": "prompt_seg_001_002_v002",
  "project_id": "proj_001",
  "film_id": "film_001",

  "target_type": "video_segment",
  "target_id": "seg_001_002",

  "prompt_type": "video_group_prompt",
  "version": 2,
  "language": "zh-CN",

  "source_refs": {
    "script_version_id": "script_v003",
    "script_blocks": [
      {
        "start_block_id": "blk_001_021",
        "end_block_id": "blk_001_034"
      }
    ],
    "character_ids": ["char_aria", "char_athena7"],
    "location_ids": ["loc_red_wasteland"],
    "prop_ids": ["prop_hoverbike", "prop_glowing_goggles"],
    "style_guide_id": "style_001"
  },

  "source_script_snapshot": "悬浮摩托从锈红色沙丘之间高速掠过。雅典娜-7抬起右手，蓝色全息热源图在她眼前展开。雅典娜-7：后方热源信号数量——三百以上。亚莉娅拉下发光护目镜，没有减速。",

  "compiled_prompt": "生成一个20秒电影化写实视频段落。场景为红色荒原黄昏，悬浮摩托高速穿越锈红色沙丘，暗紫色量子尘暴在远处逼近。亚莉娅坐在前座驾驶，雅典娜-7坐在后座抬手扫描后方热源。镜头由远景进入中景，再切到亚莉娅拉下发光护目镜的特写。雅典娜-7说：后方热源信号数量——三百以上。整体为真人电影写实风格，真实摄影机语言，自然皮肤纹理，真实风沙颗粒。",

  "negative_prompt": "不要卡通，不要插画，不要漫画分镜格，不要改变角色服装，不要让角色离开悬浮摩托，不要出现现代城市，不要改变红色荒原场景。",

  "input_asset_ids": [
    "asset_aria_face_001",
    "asset_athena_face_001",
    "asset_loc_red_wasteland_wide_001",
    "asset_prop_hoverbike_001"
  ],

  "template_id": "tpl_video_segment_seedance_v1",
  "created_by": "system",
  "created_at": "2026-06-27T10:18:00+08:00"
}
```

重点是同时保存：

```text
source_refs
source_script_snapshot
compiled_prompt
negative_prompt
input_asset_ids
```

这样将来可追溯、可复现。

---

# 22. GenerationTask 生成任务

`generation_tasks` 承载模型调用。

```json
{
  "task_id": "task_000321",
  "project_id": "proj_001",
  "film_id": "film_001",

  "task_type": "video_generation",

  "target_type": "video_segment",
  "target_id": "seg_001_002",

  "model": {
    "provider": "seedance",
    "model_name": "seedance_pro",
    "model_version": "2026-06",
    "resolution": "720p",
    "duration_sec": 20,
    "aspect_ratio": "16:9",
    "fps": 24
  },

  "inputs": {
    "prompt_id": "prompt_seg_001_002_v002",
    "reference_asset_ids": [
      "asset_aria_face_001",
      "asset_athena_face_001",
      "asset_loc_red_wasteland_wide_001",
      "asset_prop_hoverbike_001"
    ],
    "first_frame_asset_id": "asset_keyframe_seg_001_002_first",
    "last_frame_asset_id": null
  },

  "params": {
    "seed": 123456,
    "guidance_scale": 7,
    "motion_strength": "medium",
    "camera_motion": true
  },

  "cost": {
    "estimated_credits": 5600,
    "actual_credits": null,
    "currency": "credits"
  },

  "status": "running",
  "progress": 0.85,

  "outputs": {
    "asset_ids": []
  },

  "error": null,

  "created_at": "2026-06-27T10:20:00+08:00",
  "started_at": "2026-06-27T10:21:00+08:00",
  "finished_at": null
}
```

`task_type` 建议枚举：

```text
character_image_generation
location_image_generation
prop_image_generation
storyboard_generation
keyframe_generation
video_generation
audio_generation
voice_generation
subtitle_generation
upscale
interpolation
edit_video
export
```

`target_type` 建议枚举：

```text
character
location
prop
scene
beat
video_segment
shot
timeline
export
```

---

# 23. Review 审核记录

`reviews` 用来记录人工/自动审核。

```json
{
  "review_id": "review_001",
  "project_id": "proj_001",
  "film_id": "film_001",

  "target_type": "asset",
  "target_id": "asset_video_seg_002_v003",

  "related_target": {
    "type": "video_segment",
    "id": "seg_001_002"
  },

  "review_type": "video_quality_review",

  "scores": {
    "character_consistency": 8.7,
    "costume_consistency": 8.5,
    "scene_consistency": 9.2,
    "action_accuracy": 8.1,
    "visual_quality": 9.0,
    "cut_continuity": 8.5,
    "prompt_adherence": 8.4
  },

  "issues": [
    {
      "issue_type": "minor_motion_artifact",
      "description": "第12秒处手部动作略微不自然",
      "severity": "low",
      "timecode_start": 12.0,
      "timecode_end": 12.8
    }
  ],

  "decision": "approved",
  "selected_as_final": true,

  "reviewer_id": "user_001",
  "reviewed_at": "2026-06-27T10:40:00+08:00"
}
```

`decision` 建议枚举：

```text
pending
approved
rejected
needs_regeneration
needs_edit
selected_as_final
```

---

# 24. ContinuityState 连续性状态

`continuity_states` 可以单独建集合，也可以嵌入 Scene / Segment。

正式系统建议单独建。

```json
{
  "continuity_state_id": "cont_seg_001_002_out",
  "project_id": "proj_001",
  "film_id": "film_001",

  "scope": "video_segment",
  "target_id": "seg_001_002",

  "position": "out",

  "characters": {
    "char_aria": {
      "position": "悬浮摩托前座",
      "costume_id": "costume_aria_01",
      "injury": "无明显伤口",
      "held_props": ["prop_glowing_goggles"],
      "emotion": "紧张转为决绝"
    },
    "char_athena7": {
      "position": "悬浮摩托后座",
      "costume_id": "costume_athena_01",
      "injury": "无",
      "emotion": "冷静但紧迫"
    }
  },

  "environment": {
    "location_id": "loc_red_wasteland",
    "weather": "沙尘暴逼近",
    "light": "黄昏暗紫天光",
    "threats": ["后方热源超过三百"]
  },

  "props": {
    "prop_hoverbike": {
      "status": "高速运行",
      "damage": "轻微沙尘刮痕"
    }
  },

  "summary": "亚莉娅拉下护目镜，决定不绕开沙尘暴，而是直接冲进去。"
}
```

---

# 25. Timeline 时间线

## timelines

```json
{
  "timeline_id": "timeline_main_v001",
  "project_id": "proj_001",
  "film_id": "film_001",

  "name": "主时间线 V001",
  "version": 1,

  "duration_sec": 7397.08,

  "status": "editing",

  "track_ids": [
    "track_video_main",
    "track_dialogue_main",
    "track_sfx",
    "track_music",
    "track_subtitle_zh"
  ],

  "created_at": "2026-06-27T11:00:00+08:00"
}
```

## timeline_tracks

```json
{
  "track_id": "track_video_main",
  "timeline_id": "timeline_main_v001",
  "project_id": "proj_001",

  "track_type": "video",
  "name": "视频主轨",
  "order_index": 1,

  "locked": false,
  "visible": true,
  "muted": false
}
```

`track_type` 建议枚举：

```text
video
dialogue
sfx
music
subtitle
transition
overlay
```

## timeline_clips

```json
{
  "clip_id": "clip_tl_0002",
  "timeline_id": "timeline_main_v001",
  "track_id": "track_video_main",
  "project_id": "proj_001",
  "film_id": "film_001",

  "asset_id": "asset_video_seg_002_v003",

  "source": {
    "source_type": "video_segment",
    "video_segment_id": "seg_001_002",
    "scene_id": "scene_001",
    "shot_id": null
  },

  "timeline_in_sec": 20.28,
  "timeline_out_sec": 41.12,

  "source_in_sec": 0,
  "source_out_sec": 20.4,

  "duration_sec": 20.4,

  "transition": {
    "transition_in": "cross_dissolve",
    "transition_out": "cut",
    "transition_duration_sec": 1.0
  },

  "status": "approved"
}
```

---

# 26. Export 导出任务

`exports` 存成片导出任务。

```json
{
  "export_id": "export_001",
  "project_id": "proj_001",
  "film_id": "film_001",
  "timeline_id": "timeline_main_v001",

  "export_type": "preview_video",

  "settings": {
    "resolution": "1920x1080",
    "fps": 24,
    "codec": "h264",
    "format": "mp4",
    "burn_subtitles": true,
    "subtitle_language": "zh-CN"
  },

  "status": "running",
  "progress": 0.72,

  "output_asset_id": null,

  "created_at": "2026-06-27T12:00:00+08:00"
}
```

---

# 27. CostRecord 成本记录

建议把生成消耗单独记录，方便算账。

```json
{
  "cost_record_id": "cost_001",
  "project_id": "proj_001",
  "film_id": "film_001",

  "source_type": "generation_task",
  "source_id": "task_000321",

  "target_type": "video_segment",
  "target_id": "seg_001_002",

  "model_provider": "seedance",
  "model_name": "seedance_pro",

  "credits_used": 5600,
  "currency": "credits",

  "billing_rule": {
    "unit": "second",
    "unit_price_credits": 280,
    "duration_sec": 20
  },

  "created_at": "2026-06-27T10:25:00+08:00"
}
```

---

# 28. 核心关系总结

最关键的关系链：

```text
script_versions
  └── script_blocks
        └── video_segment_script_links
              └── video_segments
                    └── shots
                          └── prompts
                                └── generation_tasks
                                      └── assets
                                            └── reviews
                                                  └── timeline_clips
```

更业务化一点：

```text
剧本文本
→ 选中一段文本
→ 创建分镜组
→ 分镜组生成提示词
→ 拆成镜头
→ 生成视频
→ 审核选版
→ 加入时间线
→ 导出成片
```

---

# 29. 关键索引建议

如果使用 MongoDB，建议至少加这些索引。

## script_blocks

```text
project_id + script_version_id + scene_id + order_index
project_id + script_version_id + block_type
```

## video_segments

```text
project_id + scene_id + order_index
project_id + status
project_id + beat_id
project_id + selected_video_asset_id
```

## shots

```text
project_id + video_segment_id + order_index
project_id + scene_id
project_id + status
```

## prompts

```text
project_id + target_type + target_id + version
project_id + prompt_type
```

## generation_tasks

```text
project_id + status
project_id + target_type + target_id
project_id + task_type
created_at
```

## assets

```text
project_id + asset_type
project_id + source.task_id
project_id + target_type + target_id
review_status
```

## timeline_clips

```text
timeline_id + track_id + timeline_in_sec
project_id + source.video_segment_id
```

---

# 30. 状态枚举建议

## video_segment.status

```text
draft
script_linked
prompt_ready
storyboard_ready
keyframe_ready
ready_for_generation
generating
generated
reviewing
approved
rejected
in_timeline
```

## shot.status

```text
draft
ready
prompt_ready
generating
generated
approved
rejected
in_timeline
```

## generation_task.status

```text
pending
queued
running
succeeded
failed
cancelled
retrying
```

## asset.review_status

```text
unreviewed
reviewing
approved
rejected
selected
archived
```

## script_version.status

```text
draft
active
locked
archived
```

---

# 31. MVP 版本可以先保留哪些集合

如果先做电影模式 MVP，不需要一次性做完全部。

最小可用集合：

```text
projects
films
characters
locations
props
assets

script_versions
script_blocks

scenes
beats
video_segments
video_segment_script_links
shots

prompts
generation_tasks
reviews
timelines
timeline_clips
```

可以暂缓：

```text
script_pages
acts
sequences
continuity_states
timeline_tracks
exports
cost_records
```

但如果你要认真做 **120 分钟电影级项目**，这些最终都需要补上。

---

# 32. 最推荐的核心结构

如果只记一条，CueLight 电影模式的核心数据链路应该是：

```text
Project
→ Film
→ ScriptVersion
→ ScriptBlock
→ Scene
→ Beat
→ VideoSegment
→ Shot
→ Prompt
→ GenerationTask
→ Asset
→ Review
→ TimelineClip
→ Export
```

其中：

```text
ScriptBlock 负责剧本文本
Scene 负责电影场景
Beat 负责剧情动作
VideoSegment 负责 10–30 秒 AIGC 分镜组
Shot 负责单个镜头
Prompt 负责可追溯提示词
GenerationTask 负责模型调用
Asset 负责所有生成结果和参考素材
Review 负责选版和审核
TimelineClip 负责最终成片组装
```

这套结构可以同时支持：

```text
电影剧本写作
剧本页数估时
剧本文本映射分镜组
分镜组提示词生成
角色 / 场景 / 道具资产绑定
单镜头拆解
批量视频生成
多版本审核
时间线剪辑
成片导出
```

也能自然兼容你前面提到的：

```text
一页 ≈ 一分钟
10–30 秒一个分镜组
一个分镜组包含多个分镜
分镜组关联剧本文本、提示词、角色、场景、道具资产
```