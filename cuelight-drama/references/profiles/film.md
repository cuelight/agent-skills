# Profile: Film

用于电影、长片、短片或电影化剧本项目。目标是服务主题、人物弧光、场面调度、视觉叙事和剪辑节奏，不套用短剧单集钩子逻辑。

电影项目的核心文本是 **screenplay / 文学剧本**：用可拍摄的画面和对白讲清楚在哪里、什么时候、谁做了什么、谁说了什么。它不是小说 treatment，也不是直接给视频模型的分镜脚本；CueLight 后续再从剧本中提炼场景、Beat、storyboard item 和 Shot。

## 项目设计

- 先明确片长、类型、主题问题、主角欲望、核心冲突、人物弧光和结局形态。
- proposal 写故事命题、类型承诺、主角困境、核心关系、视觉世界和观众情绪。
- design 写三幕结构、八序列结构、场景组或导演段落，说明人物变化、主题递进、声音/摄影/剪辑原则和制作约束。
- 当前 CueLight 尚无电影三幕式结构化字段；完整三幕式大纲先保存为本地规划文件 `./.cuelight/<projectId>/film-three-act-outline.md`，等待后续系统支持。
- 结构估时使用电影层级：`ScriptPage -> Scene -> Sequence -> Act -> Film`。`1 页 ≈ 1 分钟` 只用于剧本和片长规划，不直接套到 Shot 或单条 storyboard item。
- stylePrompt 可写电影摄影、镜头焦段感、自然光或造型光、色彩策略、材质、空间调度、景深和声音基调。
- 画幅默认按用户或项目设置；电影项目通常优先 16:9 或更宽的横屏构图，不默认竖屏。

## 三幕式完整结构大纲

当用户要求“电影大纲”“三幕式”“长片结构”“先做完整结构再写剧本”，或电影项目从创意、梗概、treatment 起步时，先生成或更新本地三幕式大纲，再继续写 project design、episode outline、screenplay 或 storyboard。

本地保存路径固定为：

```text
./.cuelight/<projectId>/film-three-act-outline.md
```

使用规则：

- 这是本地规划产物，不通过当前 `cuelight-cli` 写回，也不替代 `project set-design`。
- `design` 仍写可落库的生产设计；完整三幕结构保存在 `film-three-act-outline.md`。
- 后续写 episode outline、screenplay、storyboard 前，先读取该文件，确保场景、转折、人物弧光和结局一致。
- 用户修改结局、主题问题、主角欲望或人物弧光时，先同步更新该文件，再校准正文和分镜。

推荐模板：

```markdown
# 电影三幕式完整结构大纲

## 基本信息
- 片名：
- 类型：
- 片长目标：
- 主题问题：
- 主角欲望：
- 主冲突：
- 结局形态：

## 第一幕：建立与越界
- 开场状态：
- 主题提出：
- 诱因事件：
- 犹豫 / 拒绝：
- 第一幕转折：

## 第二幕上半：进入新规则
- 新世界 / 新规则：
- 关系推进：
- 承诺兑现：
- Midpoint：

## 第二幕下半：代价与崩塌
- 代价升级：
- 敌对力量逼近：
- 最低谷：
- 第二幕转折：

## 第三幕：选择与回答
- 最终选择：
- 高潮行动：
- 主题回答：
- 结局余韵：

## 八序列映射（可选）
- Sequence 1：
- Sequence 2：
- Sequence 3：
- Sequence 4：
- Sequence 5：
- Sequence 6：
- Sequence 7：
- Sequence 8：
```

八序列映射用于长片页数和分钟规划时，按目标片长估算每个 Sequence 的页数/分钟区间；storyboard item 秒数另按 4-15 秒 VideoSegment 规划。

## Terminology（术语）

电影 workflow 中的英文术语首次使用时配中文，后续优先保持“英文术语（中文）”写法，避免把 gate、rewrite、punch-up 混成普通润色或脚本检查。

- Creative Source Adaptation Pass（创意原文改编环节）：把创意说明、分析、treatment 或其他原文转成 screenplay 场景选择。
- Literary Rewrite Pass（文学精修环节）：阶段性 screenplay draft 完成后的必选文字精修，不默认改变结构和绑定。
- Literary Rewrite Loop Engineering（文学精修循环工程）：按工具红灯、Agent 抽读和 repair loop（修复循环）迭代到可交付。
- Agent-Owned Gates（Agent 主导验收门）：工具只给信号，Agent 必须阅读产物、写证据并决定 pass / fail。
- Agent Literary Review Gate（Agent 文学审查门）：检查 screenplay 是否像成片剧本，而不是只检查 YAML 或脚本指标。
- Commercialization Punch-up Pass（商业化强化环节）：在文学精修后强化类型钩子、外部冲突和场尾推进。
- Commercial Review Gate（商业化审查门）：检查商业钩子、可见冲突和类型承诺是否落到正文事件。
- Pagination De-dup Pass（分页去重环节）：清洗根级 `script/pages.yaml` 的重复 block 覆盖和假分页。
- Playable Capacity Pass（可拍容量验收环节）：确认标称时长由真实可拍、可演、可剪正文支撑。
- Production Leaves Sync Audit（生产叶节点同步审查）：正文变更后抽查 Segment / Shot / Prompt 等叶节点是否同步最新 screenplay。
- DOCX Gate（DOCX 导出验收门）：导出后反读或渲染抽查格式、角色名、对白、动作、转场和分页。
- Production-ready Gate（生产就绪验收门）：汇总全部 gate 结论，决定是否允许进入生产、导出或交付。

## 本地数据维护

电影项目需要维护比当前平台字段更细的本地影子结构时，读取 `references/profiles/film-data-local.md`。该结构使用 `./.cuelight/<projectId>/film-data/` 下的树形 YAML 文件保存，每个文件直接存原生 YAML，方便机器读取、人类预览和手工微调。

使用边界：

- 当前只维护到 Production：Film、StoryBible、StyleGuide、ScriptVersion、ScriptBlock、ScriptPage、Act、Sequence、Scene、Beat、VideoSegment、Shot、Prompt、ContinuityState。
- 不维护真实生成任务、资产审核、时间线、导出或成本记录；这些仍以当前平台/CLI 能力为准。
- `film-three-act-outline.md` 是人类可读的三幕式上游大纲；结构化 Act/Sequence/Scene/Beat/VideoSegment 进入 `film-data/acts/**` 树。
- 不按实体类型维护全局大表；避免 `structure/*.yaml`、`production/*.yaml`、全局 `script/blocks.yaml` 随长片膨胀。
- 生成顺序固定为：三幕/八序列规划 -> Act/Sequence/Scene/Beat 索引 -> screenplay blocks/pages -> Literary Rewrite Loop Engineering（文学精修循环工程）-> Commercialization Punch-up Pass（商业化强化环节）-> Segment/Shot/Prompt/Continuity。先确定结构数量，再写实体正文；目录 skeleton 只说明文件位置。
- 生成或改写 screenplay 时，同步对应 scene 子树的 `script/blocks.yaml`；完成正式分页后，再同步 scene 内 `pages.yaml` 和根级 `film-data/script/pages.yaml`。
- 拆分镜前，先同步 `act.yaml`、`sequence.yaml`、`scene.yaml`、`beat.yaml` 和各级 `index.yaml`；生成分镜组、镜头和提示词时，维护对应 `seg_xxx/` 下的 `segment.yaml`、`shots.yaml`、`prompt.yaml`、`continuity.yaml`。
- 当前每个本地 VideoSegment / CueLight storyboard item 固定按 4-15 秒规划，暂不开放超过 15 秒的单条分镜组；更长的剧情 Beat 必须拆成多个连续 VideoSegment。
- 正式全片页码估算使用根级 `film-data/script/pages.yaml`：每个 ScriptPage 通过 `block_refs` 指向一个或多个 scene 的 `script/blocks.yaml`。scene 内 `script/pages.yaml` 只做本场页段估算；跨场景页码、覆盖索引和 `1 页 ≈ 1 分钟` 汇总以根级 `script/pages.yaml` 为准。DOCX 默认按正文自然流式排版，物理分页由 Word 根据版式生成。
- 长片默认至少维护 3 个 Act、多个 Sequence、多个 Scene、多个 Beat、多个 VideoSegment 和多个 Shot。只有用户明确要求“最小样例 / POC / 只演示一段”时，才允许每层单节点，并必须在相关状态或说明中标记 `sample` / `incomplete`。
- 完成本地结构后，用 CLI 内部工具汇总时长：

```bash
cuelight-cli internal film-data duration --project-id <projectId>
cuelight-cli --json internal film-data duration --project-id <projectId>
cuelight-cli internal film-data duration --project-id <projectId> --strict
```

该工具只读本地 YAML，不写回平台；用它检查父子时长汇总、segment 4-15 秒约束和 shot 合计是否匹配 segment。

### Agent-Owned Gates（Agent 主导验收门）

电影路径中的所有 gate 都由 Agent 负责最终判断。`--strict`、duration check、分页去重、DOCX 导出检查和质量脚本只提供信号；`strict ok` 不是 production-ready 结论。

每个正式 gate 都按三步执行：

1. Run tool：运行对应脚本或 CLI，记录命令、范围、结果和 issue。
2. Read artifacts：Agent 直接阅读或抽查真实产物，例如 scene `blocks.yaml`、根级 `script/pages.yaml`、duration 汇总节点、DOCX 反读段落或渲染页。
3. Decide：写出 `pass` / `fail`、证据短句、问题类型和下一步许可；没有 Agent 结论的报告视为 `draft_not_reviewed`，不得标记 `production_ready`。

常见 gate 的 Agent 判断重点：

- Duration gate：除 `issues=[]` 外，说明标称时长是否由 screenplay 容量、scene/beat 分布和剧情密度支撑。
- Pagination gate：除无重复 block 外，抽查跨页阅读连续性，确认没有截断理解、大片空白或复制页冒充容量。
- Playable capacity gate：除字符数达标外，判断正文是否真实可拍、可演、可剪，而不是堆叠伪动作或变量模板。
- DOCX gate：除导出成功外，反读或渲染抽查格式，确认角色名、对白、动作、转场和自然分页可读。
- Production-ready gate：汇总所有 gate 的 Agent 结论，明确是否允许进入 Segment / Shot / Prompt、DOCX 导出、生成或交付。
- Commercial review gate：除脚本干净外，判断场景是否有事件钩子、可见冲突、类型承诺和场尾推进。
- 若工具通过但 Agent 抽读发现公式化文本、同场动作复用、意象空转、场尾无推进或冲突未外化，必须判定 `fail`，进入 repair loop（修复循环），并记录 fail 原因、修复范围和下游许可。

### First Act Production Pass

当任务是“第一幕完全拆出来”或“验证第一幕”时，按下面顺序交付 `act_001`：

1. 目标片长：先写 `film.yaml.final_target_duration_sec`。90 分钟长片的完整 `act_001` 通常预算为 16-27 分钟；低于 18% 时标记为 `sample` / `partial`，或继续扩展场次和镜头。
2. Act duration budget：`act_001.estimated_duration_sec` 对齐第一幕 screenplay 页数和剧情容量；第二、三幕若暂不展开，可保留空 `sequences/index.yaml`，对应估时写 `0` 或省略。
3. Sequence beats：用八序列规划拆出多个 Sequence，再按每个 Sequence 的戏剧任务决定 Scene 数量。
4. Scene screenplay：每个 Scene 先写可拍 screenplay blocks，再把动作推进拆成多个 Beat；完整第一幕的 Scene、Beat、Segment 和 Shot 数量应随事件密度变化。
5. Production leaves：每个 Beat 继续拆成 4-15 秒 VideoSegment，Segment 内用多个 Shot 覆盖动作、视线、声音和剪辑点。
6. Strict validation：交付前运行 `cuelight-cli internal film-data duration --project-id <projectId> --strict`，确认 index 完整、父子时长可汇总、Segment 与 Shot 时长匹配；Agent 还要说明第一幕时长是否由真实 scene 容量支撑。
7. Screenplay quality loop：从创意类原文生成 `film-data/` 后，执行 `Literary Rewrite Loop Engineering`，直到质量脚本无 error，且 Agent 文学审查明确 `pass`。

### Creative Source Adaptation Pass

当输入是创意说明、历史分析、人物小传、treatment、舞台剧、小说片段或混合材料时，先完成改编判断，再写 screenplay：

1. Source type：标记原文主要形态和可直接使用的材料。历史分析、理论说明和人物心理分析进入 `story-bible.yaml`、`film-three-act-outline.md`、scene/beat metadata。
2. Dramatic choice：把抽象论点转成场景选择：谁想要什么、谁阻拦、空间如何施压、物件如何承担记忆或权力、场景结束时关系发生什么变化。
3. Screenplay scene：只写可拍动作、可听声音、角色真实台词、沉默、物件、走位和空间关系。创作目的、主题解释、导演说明和分镜提示词不进入 `action` 或 `dialogue`。
4. Production binding：screenplay blocks 稳定后，再从正文拆 Beat、Segment、Shot 和 Prompt；不要用摘要性 treatment 直接生成 production leaves。

对历史/理论/报告类输入，优先做文学化选择，而不是逐句改写：保留事实节点和权力关系，重新创造能让观众看见的动作、声音、物件和潜台词。

### Pagination De-dup Pass

Pagination De-dup 是正式电影 screenplay 的必选阶段门。完成 Literary Rewrite、screenplay quality strict 和 Agent 文学审查后，进入 Segment / Shot / Prompt 绑定、DOCX 导出或生成阶段之前，必须清洗根级 `film-data/script/pages.yaml` 的分页引用。

执行规则：

1. Root pages as authority：以根级 `script/pages.yaml` 为正式分页来源；scene 内 `script/pages.yaml` 只作局部估算。
2. Split multi-page scenes：同一个 scene 覆盖多页时，把 `block_refs` 拆成连续、非重叠的 block ranges。例如第一页覆盖 `blk_001`-`blk_008`，第二页从 `blk_009` 开始。
3. Preserve capacity：若当前目标是完整第一幕或正式 production-ready，不通过删除重复页来降低容量；先拆非重叠页段，必要时补写 screenplay 内容后再分页。
4. Clean before production：根级 `script/pages.yaml` 中同一 `script_path#block_id` 不应被多个 ScriptPage 重复覆盖；重复页只能作为 `sample` / `draft_not_cleaned`，不能进入分镜、生成或 DOCX 正式交付。
5. Recheck：分页清洗后运行 screenplay quality strict 和 duration strict；DOCX 导出脚本在 `--strict` 下也会拦截重复 block 导出。Agent 必须抽读至少 3 个跨页边界，确认阅读连续、无大段空白、无复制页冒充容量，再给出分页 gate 的 `pass` / `fail`。

### Playable Capacity Pass

Playable Capacity 是正式电影 screenplay 的硬验收门。结构时长必须由真实可拍正文支撑，不能只靠 `estimated_duration_sec`、Segment 数量或重复 `script_refs` 把时长“填满”。

执行规则：

1. Match text to time：完整 `act_001` 若标称 1080 秒，screenplay 正文应至少接近 18 分钟的可读/可演容量。中文剧本底线按约 320 字/分钟估算；18 分钟至少约 5760 个 screenplay 字符，复杂动作戏通常需要更多。
2. Count non-repeated capacity：正式分页后，每个 ScriptPage 的可拍容量按去重后正文计算；重复模板句、跨页复用长句和复制来的环境描写不计入有效容量。每页保底 `320` 个非重复 screenplay 字符，推荐目标 `350-420`。
3. Expand scenes, not labels：若正文容量不足，优先扩写 scene 内动作节拍、反应、走位、沉默、物件递进和可说出口的台词；不要只增加 Beat / Segment / Shot 数量，也不要用同一句氛围描写填充多个 action block。
4. Unique segment binding：每个 4-15 秒 VideoSegment 应绑定到独立或更窄的 screenplay block range。多个 Segment 不应重复引用同一组 `start_block_id` / `end_block_id` 来冒充不同可拍内容。
5. Recheck：进入 production leaves、DOCX 导出或验收前，运行 `check_film_screenplay_quality.py --strict`；若报告 `screenplay_capacity_underfit`、`page_playable_capacity_underfit`、`repeated_playable_fragment`、`repeated_sentence_skeleton`、`templated_screenplay_pattern`、`synthetic_rewrite_template` 或 `duplicate_segment_script_ref`，不得标记为 production-ready。脚本变绿后，Agent 仍需抽读正文，确认容量来自真实动作、对白、沉默和可剪节奏，而不是伪动作堆叠。

### Literary Rewrite Pass

Literary Rewrite 是正式电影 screenplay 的必选阶段门。每完成一个阶段性 screenplay draft，都必须先执行 Rewrite，再进入 production leaves、最终验收或交付。阶段性 draft 包括：单个 scene 初稿、一个 sequence 的 scenes 初稿、`act_001` 初稿、从 creative source 改编出的 screenplay 初稿。

只有用户明确要求 quick POC / sample / fixture 时可以跳过 Rewrite；跳过时必须在相关 status 或验收报告中标记 `sample` / `draft_not_rewritten`，不得作为正式 screenplay 验收通过。Rewrite 目标是提升表达，不重新做结构拆分。

执行顺序：

1. Lock draft scope：先确认本轮 screenplay draft 的范围和父级节点，例如 scene、sequence 或 `act_001`；如果 production leaves 已存在，默认保持 Act / Sequence / Scene / Beat / Segment / Shot 数量不变。
2. Read scene context：每次只处理一个 scene，先读 `scene.yaml`、`beats/index.yaml`、`script/blocks.yaml`，再查相关 segment 的 `script_refs` / `script-links.yaml`。
3. Rewrite text：优先改 `action.text`、`dialogue.text`，必要时微调 `parenthetical`、声音、转场和 `semantic_tags`；默认保留 `block_id`、`order_index`、`block_type`。
4. Preserve bindings：只改文字表达时，不重排 block，不改 segment / shot / prompt 结构；若必须新增、删除或重排 block，同步更新 pages、script refs 和 affected production leaves。
5. Recheck：Rewrite 后运行 `check_film_screenplay_quality.py --strict`；报告中的 `literaryScore.score` 应达到 `passingScore`，且无 error。若本轮已有 production leaves 或准备交付，再运行 duration strict。工具通过后必须进入 Agent Literary Review Gate，不能直接放行。

Anti-template gate：

- 每一幕都必须完成真正的 Rewrite，不把“容量补齐”和“结构生成”当作文学精修。中段尤其要把胜利、授权、回收、背叛或关系破裂等拐点写成具体对手戏。
- `action.text` 不使用变量填充句式，例如“第 N 道军令落下，X 被 Y 到 Z 旁，A 停住半步，B 声从队尾压过来”。动作要来自该场具体空间、人物选择和物件变化。
- `dialogue.text` 不使用角色固定口号模板，例如“这第 N 步若退……”“第 N 行字写下去……”“第 N 道功劳我认……”。同一角色在不同场景的台词应因关系、风险和场景压力改变。
- 检查方式：抽看每个 sequence 至少 2 个 scene，确认 action 不是可替换变量模板，dialogue 不是同一句换数字或换道具。若脚本报告 `templated_screenplay_pattern`、`repeated_sentence_skeleton` 或 `synthetic_rewrite_template`，先 Rewrite，再继续分镜或导出。若脚本未报告但 Agent 读到新模板，也必须判定 fail。

精修目标：

- 人物声口：主角、对手、盟友和权力人物应有不同语言指纹；台词来自身份、关系、风险和当场目标，不靠同一种沉郁语气覆盖所有角色。
- 潜台词：台词表面谈军令、衣食、路途，底下压尊严、控制、债务和未来背叛。
- 动作节奏：让停顿、迟疑、避视、手部动作、走位和沉默承担心理变化。
- 物件递进：衣物、食物、印章、通行证、名册、铃声等意象每次出现都承担新关系，不机械重复。
- 空间压力：让门槛、台阶、通道、渡口、密室等空间改变人物权力位置。
- 语言克制：减少主题直说、工整口号、解释性对白和“漂亮但不可演”的句子。

精修时，保留能服务表演和叙事的简洁句。不要把每句都改成华丽文学句；电影剧本首先要可演、可拍、可剪。

### Commercialization Punch-up Pass（商业化强化环节）

Commercialization Punch-up Pass（商业化强化环节）发生在 Literary Rewrite Pass（文学精修环节）通过之后、DOCX 导出 / Production-ready Gate（生产就绪验收门）/ 生成阶段之前。它不是改成快节奏爽文，也不是重建结构；默认保持 Act / Sequence / Scene / Beat / Segment / Shot 数量、页数、时长、`block_id`、`script_refs` 和 production leaves 数量稳定。

执行目标：

1. Scene hook：每场都能说清 entrance objective（入场目标）、external obstacle（外部阻力）、visible conflict（可见冲突）和 turn/end hook（转折/场尾钩子）。
2. Type promise：类型承诺落到剧情事件，例如调查、诱捕、公开选择、权力回收、家庭摊牌、战场胜负手、规则反噬或空间封锁；不要把“类型卖点”“市场定位”写进 `action.text` 或 `dialogue.text`。
3. Externalize conflict：把内在犹豫、心理压力和主题问题转成可拍动作、可听声音、对手戏、制度压力、物件变化或空间阻挡。
4. Preserve tone：保留电影文学质感，但减少只服务氛围的慢铺陈；每个细节要推动信息、关系、权力位置、节奏或场尾推进。
5. Sync leaves：若已存在 production leaves，正文 punch-up 后执行 Production Leaves Sync Audit（生产叶节点同步审查），抽查 affected Segment / Shot / Prompt 是否追溯到最新 screenplay。

中性 few-shot：

```text
Before: 主角站在走廊里，感到自己被家庭排斥。
After: 主角推开餐厅门，所有人同时停筷；她的位置被新椅子占住，父亲把遗嘱信封压到盘子下。
Hook: 家庭排斥外化为公开座位和遗嘱压力。

Before: 调查员意识到公司在撒谎。
After: 调查员要求调监控，值班主管当场切断屏幕；走廊另一端的销毁车已经开始装箱。
Hook: 抽象怀疑外化为证据被销毁的倒计时。

Before: 士兵害怕继续进攻。
After: 退路桥被炸断，军官把最后一卷绷带扔到前线，后排士兵只能把盾牌朝向敌火。
Hook: 内心恐惧外化为退路消失和阵线选择。
```

### Commercial Review Gate（商业化审查门）

Commercial Review Gate（商业化审查门）由 Agent 主动审查，不能只依赖 `strict ok`。Act 级或全片范围至少抽读开端、中段、转折和结尾；sequence 或 scene 范围抽读本轮改动的关键场。

Agent 必须判断：

- 事件钩子是否清楚：观众能否一句话复述这场发生了什么。
- 冲突是否可见、可演、可剪：阻力是否落到人物、制度、物件、空间或行动，而不是解释性说明。
- 场尾是否推进下一场：信息、关系、权力位置或危险是否发生变化。
- 类型承诺是否落到正文事件：悬疑有证据压力，家庭片有关系摊牌，战争片有战术选择，传记片有人物命运拐点，犯罪片有规则和代价。
- 人物选择是否改变局面：角色不是只发表观点，而是在压力中做出选择。
- Scene Progression（场内递进）是否成立：同一物件或意象再次出现时必须承担新功能，例如信息揭示、权力转移、人物选择、关系变化或剪辑推进。

若工具通过但 Agent 读到同场动作复用、意象空转、场尾无推进、冲突没有外化或商业钩子不可复述，Commercial Review Gate（商业化审查门）必须判定 `fail`，进入 repair loop（修复循环）。

### Scene Progression（场内递进） / Anti-Filler（反填充）

Scene Progression（场内递进）要求同一 scene 的动作、物件、视线、沉默和空间关系持续产生新信息。可以复用核心物件或意象，但每次出现必须改变人物处境、关系压力、权力位置、观众信息或剪辑节奏。

Anti-Filler（反填充）规则：

- 不用同一组环境描写、道具动作、视线、沉默或过渡句反复填满 ScriptPage。
- 不通过扩大 Segment 数量、重复 action block 或重复 `script_refs` 来制造标称时长。
- 容量不足时，优先扩写真实冲突、走位、反应、对手戏、沉默和可执行动作。
- 如果把地点、道具或角色名替换后场景仍基本成立，说明该场缺少不可互换的戏剧功能，继续 Rewrite 或 Punch-up。

### Production Leaves Sync Audit（生产叶节点同步审查）

任意 Literary Rewrite Pass（文学精修环节）、Commercialization Punch-up Pass（商业化强化环节）或 repair loop（修复循环）修改 `script/blocks.yaml` 后，若 production leaves 已存在，必须同步 affected leaves，并由 Agent 抽查证据。

审查要求：

- 抽查 affected segment 的 `script-links.yaml`，确认 `text_snapshot` 对应最新 block 文本。
- 抽查 `prompt.yaml.source_script_snapshot` 和 `prompt.yaml.compiled_prompt`，确认未保留旧句或旧场面调度。
- 抽查 `shots.yaml.visual_description`，确认镜头描述仍对应该 Segment 的最新动作。
- 如果只改文字表达，保持 `block_id`、`order_index`、`block_type`、`script_refs`、pages 和时长稳定；若无法保持，必须同步修复所有引用并重新运行 gate。
- 验收报告记录抽查的 segment、发现或未发现的问题、同步结论和下游许可。

### Literary Rewrite Loop Engineering

Literary Rewrite 不是单次润色，而是红绿循环。每完成一个 scene / sequence / act 的 screenplay draft，按下面 loop 迭代，直到脚本检查和 Agent 文学审查都绿：

1. Draft：先写完整场景正文，保留 `block_id`、`order_index`、`block_type` 和 pages / segment refs 的可追溯性。
2. Run gate：运行 `check_film_screenplay_quality.py --film-data-dir <film-data> --strict`，范围明确时加 `--act-id <act_id>`；若已有 production leaves，同时运行 duration strict。
3. Read red signals：把 error 当成必须重写的信号，不用解释绕过。重点处理 `generic_literary_filler`、`spatial_logic_mismatch`、`unexpected_role_mention`、`templated_screenplay_pattern`、`repeated_sentence_skeleton`、`repeated_playable_fragment`、容量不足和重复分页。
4. Rewrite by cause：按失败原因改正文。模板化就重写场景动作和对白；容量不足就增加真实冲突、走位、反应和沉默；角色错置就核对 `semantic_tags.characters` 与场内人物；空间错位就按 slugline 和场景物件重写 blocking。
5. Agent Literary Review Gate：每轮脚本变绿后，Agent 抽读本轮范围内关键 scene；若范围是 act，至少覆盖开端、中段、转折和结尾各 1 场。用文学评审标准判断是否像成片剧本，而不是“可通过脚本的文本”。
6. Stop condition：只有同时满足 `strict ok`、无红灯关键词、Agent 评审关键 scene 达到 B+ 以上、没有明显跨场套话、关键转折落到具体行为，才允许进入 Segment / Shot / Prompt、DOCX 导出或交付。

Agent 文学审查按这些问题判定，并必须写出 `pass` / `fail`、抽读 scene、证据短句和下一步许可：

- 关键拐点是否写成具体对手戏或可见行为，而不是 metadata 解释。
- 人物声口是否分化：主角不只陈述创伤，对手不只解释权术，盟友不只表达两难；同一句台词换角色后不应仍然成立。
- 每场是否有不可互换的空间、物件和动作；如果把地名/道具换掉仍能成立，继续 Rewrite。
- 是否存在“文学化模板”：风、灰、袖口、影子、无人说出口、声音成线等意象跨场复用但没有新意义。
- 是否存在脚本未覆盖的新模板绕过，例如“某令已听见”“某甲色/甲冷痕”“从话里退出来”“落成门、手和脚步之间的距离”等公式化变体。
- 动作是否物理可拍：室外不写屋内反应，缺席人物不进入 action，物件不做不合理动作。
- 对白是否能由演员说出口，且包含关系压力和潜台词；漂亮口号不算合格。

Loop 记录写入验收报告：列出本轮范围、失败信号、修复动作、strict 结果、Agent 抽读对象、证据、`pass` / `fail` 和是否允许下游生产。只列工具结果、不写 Agent 审查证据的报告视为 `draft_not_reviewed`。

## 剧本建议

- 正文优先写成 screenplay：场景标题、动作描写、人物名、对白、括号提示、声音标记、转场和特殊格式。
- 可按三幕、八序列、场景组或导演段落组织；不强制每个段落都有短剧式反转。
- 场景要有戏剧目的：角色想要什么、阻力是什么、场景结束时关系或信息发生什么变化。
- 允许沉默、观察、环境、动作和视觉隐喻承担叙事；对白服务于潜台词和关系压力。
- 对白应体现潜台词和关系压力；避免解释性台词替代画面。
- 长场戏要写清人物走位、空间关系、视线、节奏变化和场面调度。

### Screenplay 格式

场景标题用于标明地点、内外景和时间。推荐写法：

```text
外景. 月球背面采矿站外 - 月昼
内景. 休息舱 - 班前
内/外景. 行驶中的悬浮车 - 连续
```

也兼容中文制片格式：

```text
1. 外景 / 月球背面采矿站外 / 月昼
人物：林渊
```

只要地点、时间、内外景发生明显变化，就新开一个场景标题。常用时间词包括：`日`、`夜`、`清晨`、`上午`、`午后`、`黄昏`、`深夜`、`连续`、`稍后`、`同时`、`闪回`。

动作描写只写镜头能看到、声音能听到的内容：

- 用现在时：写“走进、看见、停下”，避免“走进了、看见了”。
- 写动作、表情、声音、环境、物体变化和可见反应。
- 心理必须转成行为、表情、动作节奏或声音。
- 段落保持短，通常 1-4 行。
- 不滥写导演镜头指令；文学剧本不需要每句都写“镜头推近”。
- `action` 中不写“本场主要表现”“用于建立”“主题是”“象征”等创作说明；这些内容放进 scene/beat metadata 或 `note`。
- `dialogue` 中只写角色实际说出口的话；“盟友承诺……”“领袖当众宣布……”这类摘要要改成角色台词或动作。

Treatment input：

```text
林渊很孤独，他想到父亲的话，决定去深矿证明自己。
```

Screenplay output：

```text
林渊站在气闸阴影里，头盔内只剩呼吸声。腕屏冷光扫过他的名字，风险标记跳成红色。
```

角色第一次出现时，简洁交代年龄感、身份、外貌或气质：

```text
林渊，24岁，月面矿工，旧式宇航服袖口磨得发白。他动作克制，像是每一步都先在心里算过风险。
```

角色第一次出现时只给可拍、可感知的信息；世界观信息分散到行动和对白中体现。

### 对白、声音和特殊格式

对白使用独立人物名和对白正文。括号提示只写简短语气、动作或说话对象，不写长心理分析。

```text
                    林渊
              （压低声音）
          你听见了吗？
```

O.S. / 画外表示角色在现场但暂时不在画面中；V.O. / 旁白表示旁白、内心独白、回忆声、电话另一端或非现场声音。

```text
                    林山（O.S.）
          别信机器给你取的名字。

                    林渊（V.O.）
          如果名字是他们给的，我就把它活成自己的。
```

转场只在有特殊意义时写，不需要每场都写：

```text
切至：
淡入：
淡出。
叠化至：
猛切至：
匹配剪辑至：
```

特殊格式按叙事功能单独标注：

```text
插入：腕屏

风险等级：红色。
```

```text
字幕：2147年，月球背面艾特肯盆地。
```

```text
蒙太奇：

- 林渊在矿机阴影下记录氧气读数。
- 他把旧铜丝罗盘藏进工具袋。
- 月尘从安全门缝里缓慢落下。

蒙太奇结束。
```

```text
闪回：

外景. 地球海边 - 黄昏

十岁的林渊站在潮水边，看着父亲把罗盘放进他手心。

闪回结束。
```

## CueLight 转换链路

电影项目在 CueLight 中按以下完整平台链路推进：

```text
Screenplay / ScriptBlock
-> ScriptPage 估时
-> Scene 场景
-> Beat 情节点
-> VideoSegment / storyboard item（当前 4-15 秒）
-> Shot 镜头
-> GenerationTask 生成任务
-> Asset 视频结果
-> Timeline 成片
```

这是完整远期链路；当前本地 `film-data/` 只维护到 `VideoSegment -> Shot -> Prompt -> ContinuityState`，不在本地记录真实 `GenerationTask`、`Asset`、`Review`、`Timeline` 或 `Export` 状态。

执行要点：

- episode script 保存 screenplay 正文，不把分镜提示词当作剧本文本。
- storyboard item 从最新 screenplay 中提炼；每条 `scriptExcerpt` 必须能追溯到正文里的场景标题、动作、对白、道具、屏幕信息、声音触发或情绪停顿。
- Beat 可以覆盖超过单条分镜组上限的戏剧动作，但写入本地 `segment.yaml` 或 CueLight storyboard 前必须拆成 4-15 秒的连续 VideoSegment。
- 如果正文从 treatment 改成 screenplay，已有 storyboard 要按新正文重新校准 `videoPrompt` 与 `scriptExcerpt`，不能只做表面润色。
- 角色、场景、道具先按稳定资产写入 CueLight；电影角色资产同样遵守通用 `character.basePrompt` 外观顺序，剧本中的临时情绪、场面动作和剧情状态进入 screenplay / episode / storyboard，不写进资产 `basePrompt`。
- AIGC 友好的电影剧本应让系统能抽取角色、场景、道具、动作、情绪、声音和对白；抽象心理必须转成可见可听的行为。
- 导出正式 screenplay DOCX 前，必须先完成 Literary Rewrite Pass、screenplay quality strict 和 Agent 文学审查；DOCX 正文顺序以根级 `film-data/script/pages.yaml` 为准。

DOCX 导出：

```bash
python .codex/skills/cuelight-drama/scripts/export_film_screenplay_docx.py \
  --film-data-dir .cuelight/<projectId>/film-data \
  --output .cuelight/<projectId>/screenplay.docx \
  --strict
```

导出脚本只读本地 YAML；它按 `script/pages.yaml` 的 `page_number` 和 `block_refs` 顺序收集正文，但默认不把 ScriptPage 变成物理 page break。正式 DOCX 让 Word 自然分页并使用页脚页码。若需要审计 ScriptPage 映射，可加 `--page-break-per-script-page --show-page-labels`；若需要视觉检查，可加 `--render-check-dir <dir>`。DOCX gate 必须由 Agent 反读或渲染抽查，确认角色名、动作、对白、转场和分页自然，不能只以“导出成功”放行。

## 分镜建议

- storyboard item 仍按 CueLight 字段落库，当前单条时长固定 4-15 秒；镜头数量和节奏应服务导演意图，可以使用长镜头、静默段落、环境镜头和蒙太奇，但不能把单条 item 放宽到更长时长。
- 分镜必须从最新剧本正文中提炼。若正文从 treatment 改为电影剧本，已有分镜要按新正文重新校准 `videoPrompt` 与 `scriptExcerpt`，不能只做文字润色。
- 不强制每个 storyboard item 都有对白；无对白 item 必须有明确视觉叙事、声音设计、人物行动、主题意象或剪辑作用。
- 场面调度优先于机械切镜：一个镜头能通过走位、焦点、遮挡和声音完成关系变化时，保留完整表演节奏。
- 分镜要写清摄影意图：景别、机位、运动、焦点变化、光线、前后景关系、空间变化和声音桥接。
- 多场景可用于平行剪辑、回忆、梦境、电话两端和蒙太奇；如果每个空间都有完整动作弧线，优先拆成多个 storyboard item。
- 项目画幅为 `21:9` 或其他宽银幕比例时，优先宽景、横向调度、前中后景层次和克制特写，形成电影宽银幕节奏。

## Few-shot

### 电影正文示例

```text
外景. 月球背面采矿站外 - 月昼

艾特肯盆地的灰黑地平线横向铺开。巨型履带矿机缓慢移动，远处的采矿站像一座贴在月壤上的铁城。

林渊，24岁，月面矿工，旧式宇航服袖口磨得发白。他站在气闸阴影里，头盔内只剩呼吸声。

腕屏冷光扫过他的名字，风险标记跳成红色。

                    林山（V.O.）
          别信机器给你取的名字。

林渊没有回头。他把袖口压紧，向月面迈出一步。

切至：
```

### 从 screenplay 提炼的 Seedance storyboard 示例

```json
{
  "sceneNumber": 1,
  "shotSize": "wide",
  "plannedVideoDurationSeconds": 15,
  "scriptExcerpt": "外景. 月球背面采矿站外 - 月昼：艾特肯盆地横向铺开，林渊站在气闸阴影里；林山旁白说“别信机器给你取的名字。”林渊压紧袖口，向月面迈出一步。",
  "videoPrompt": "【素材定义】\n<Character1>(林渊) 是当前角色参考，<Character2>(林山/父亲记忆) 是当前旁白声音参考，<Scene1>(月球背面采矿站外) 是当前场景参考。\n【分镜时序】\n镜头1：long shot（远景） static shot（固定拍摄），<Scene1>(月球背面采矿站外) 的灰黑地平线横向铺开，巨型履带矿机在远处缓慢移动，<Character1>(林渊) 被压在气闸阴影里，只听见头盔内沉重呼吸声。\n镜头2：medium close-up（中近景） cut-in（切入），<Scene1>(月球背面采矿站外) 中腕屏冷光扫过 <Character1>(林渊) 的名字和红色风险标记，<Character2>(林山/父亲记忆) 旁白说道：{别信机器给你取的名字。}\n镜头3：wide shot（宽景） slow lateral tracking（缓慢横移），<Scene1>(月球背面采矿站外) 中 <Character1>(林渊) 把袖口压紧并向月面迈出一步，人物被宽银幕地平线吞没，远处矿机低频轰鸣持续。\n【风格画质】\n21:9 宽银幕科幻电影质感，横向空间调度，冷色月面工业光，写实材质，克制表演，低频环境声。",
  "referenceCharacterIds": ["char-linyuan", "char-father-memory"],
  "referenceSceneId": "scene-lunar-station",
  "referenceSceneIds": ["scene-lunar-station"],
  "referencePropIds": []
}
```

### Treatment 改写示例

Treatment input：

```text
林渊很孤独，他想到父亲的话，决定去深矿证明自己。本段主要表现主角成长。
```

Screenplay output：

```text
内景. 休息舱 - 班前

狭窄休息舱里，白色台灯照着一枚旧铜丝罗盘。

林渊坐在床沿，把罗盘压进内层衣袋。舱外广播提示班前集合。他把工具袋拉链合上，停了一秒，确认没有人看见。

                    林渊（V.O.）
          如果名字是他们给的，我就把它活成自己的。
```

### Analysis input -> Screenplay output

Analysis input：

```text
边境军医长期被军方当成工具。新任指挥官用一次公开保护，让她把对职位的服从转成对个人知遇的忠诚，这份忠诚后来会成为她做出错误选择的心理根源。
```

Adaptation brief：

```text
戏剧选择：不用人物解释“创伤补偿”。让军医在众目睽睽中被公开保下，让过去的被抛弃与当下的保护相撞。指挥官的温情要像救命，也像债务。
场景压力：野战医院外，军纪官要求带走军医；指挥官必须当众选择保人或保规矩。
物件：临时通行章、染血袖标、未拆的止血包、军纪官的拘押令。
```

Screenplay output：

```text
外景. 野战医院门口 - 夜

雨水顺着帐篷边缘流下。担架一具接一具抬进来，军纪官站在灯下，手里攥着拘押令。

军医林岚摘下染血手套，袖标被雨打湿。她看见拘押令上的名字，手指在止血包边缘停住。

指挥官顾衡从救护车旁走来，摘下自己的临时通行章。

                    顾衡
          今晚所有伤员都要过她的手。人，你明天再带。

他把通行章按到林岚袖标上。军纪官没接话，灯下的雨声忽然显得很响。

顾衡拿起一包未拆的止血带，递到林岚手里。

                    顾衡
          先救人。账，算到我这里。

林岚没有立刻接。她看着那枚通行章，雨水从指节滴到泥里。

                    林岚
          这句话，您最好记得比我久。
```

### Literary rewrite few-shot

Action before：

```text
指挥官把通行章交给林岚。旁边的人都安静下来。
```

Action after：

```text
顾衡没有立刻把通行章递出去。他先看了一眼军纪官手里的拘押令。

救护车尾门合上，金属声把旁边的低语压下去。

通行章按到林岚袖标上时，她的手还停在止血包边缘，没有收回。
```

Dialogue before：

```text
                    顾衡
          我会保护你，你不用害怕。
```

Dialogue after：

```text
                    顾衡
          今晚别停手。

他把止血带递过去。

                    顾衡
          明天他们问罪，先问我。
```

Voice before：

```text
                    林岚
          您救了我，我一定会报答您。
```

Voice after：

```text
                    林岚
          我今晚留下。

她把通行章别正，转身走回帐内。

                    林岚
          但这枚章，别让我一个人背。
```

## 三位专家自检

- 电影编剧：检查主题问题、人物欲望、冲突升级、转折和结局是否连贯；检查场景是否推动人物弧光。
- 导演：检查每场戏的场面调度、视线、阻挡、沉默、动作和演员表演是否能承载戏剧变化。
- 摄影/剪辑顾问：检查镜头选择、光线、焦点、运动、长镜头或剪辑点是否有动机；检查组接是否形成视觉叙事而非只复述剧情。

## 验收

- 剧本按电影结构推进，主题和人物弧光清楚。
- screenplay 正文包含清楚的场景标题、可拍动作、可听声音、人物对白或明确无对白表演。
- 创意类原文已完成改编：分析性概念进入 bible/outline/metadata，`action` 和 `dialogue` 是可拍、可演、可听的 screenplay 正文。
- 文学精修只在结构合格后执行；默认保持结构、block id、script refs 和 production leaves 稳定。
- `check_film_screenplay_quality.py --strict` 不报告 error；若有 warning，必须能解释为有意的 `note`、特殊格式或 Agent 可接受的文学选择。`strict ok` 只是底线信号，不是最终验收。
- Agent-Owned Gates 已全部记录：duration、pagination、playable capacity、rewrite、DOCX 或 production-ready gate 都有工具结果、抽查对象、证据、`pass` / `fail` 和下一步许可。
- 若交付 DOCX，使用根级 `script/pages.yaml` 导出；DOCX 中场景标题、动作、人物名、对白、括号提示和转场应有清晰不同的段落格式。
- 首次出现的重要角色有简洁可用的人物呈现。
- O.S./V.O.、转场、插入物、字幕、蒙太奇、闪回等特殊格式使用克制且功能明确。
- 分镜能体现摄影、调度、声音和剪辑意图。
- 每条 storyboard 的 `scriptExcerpt` 能追溯到最新 screenplay 正文。
- 静默、氛围、环境和视觉隐喻都有明确功能。
- 不因使用 CueLight item 化落库而把电影段落压成短剧节奏。
