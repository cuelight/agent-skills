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

八序列映射用于长片页数和分钟规划时，按目标片长估算每个 Sequence 的页数/分钟区间；不要把这个区间直接当成 storyboard item 秒数。

## 本地数据维护

电影项目需要维护比当前平台字段更细的本地影子结构时，读取 `references/profiles/film-data-local.md`。该结构使用 `./.cuelight/<projectId>/film-data/` 下的树形 YAML 文件保存，每个文件直接存原生 YAML，方便机器读取、人类预览和手工微调。

使用边界：

- 当前只维护到 Production：Film、StoryBible、StyleGuide、ScriptVersion、ScriptBlock、ScriptPage、Act、Sequence、Scene、Beat、VideoSegment、Shot、Prompt、ContinuityState。
- 不维护真实生成任务、资产审核、时间线、导出或成本记录；这些仍以当前平台/CLI 能力为准。
- `film-three-act-outline.md` 是人类可读的三幕式上游大纲；结构化 Act/Sequence/Scene/Beat/VideoSegment 进入 `film-data/acts/**` 树。
- 不按实体类型维护全局大表；避免 `structure/*.yaml`、`production/*.yaml`、全局 `script/blocks.yaml` 随长片膨胀。
- 生成或改写 screenplay 时，同步对应 scene 子树的 `script/blocks.yaml`；完成正式分页后，再同步 scene 内 `pages.yaml` 和根级 `film-data/script/pages.yaml`。
- 拆分镜前，先同步 `act.yaml`、`sequence.yaml`、`scene.yaml`、`beat.yaml` 和各级 `index.yaml`；生成分镜组、镜头和提示词时，维护对应 `seg_xxx/` 下的 `segment.yaml`、`shots.yaml`、`prompt.yaml`、`continuity.yaml`。
- 当前每个本地 VideoSegment / CueLight storyboard item 固定按 4-15 秒规划，暂不开放超过 15 秒的单条分镜组；更长的剧情 Beat 必须拆成多个连续 VideoSegment。
- 正式全片分页使用根级 `film-data/script/pages.yaml`：每个 ScriptPage 通过 `block_refs` 指向一个或多个 scene 的 `script/blocks.yaml`。scene 内 `script/pages.yaml` 只做本场页段估算；跨场景页码、DOCX 物理分页和 `1 页 ≈ 1 分钟` 汇总以根级 `script/pages.yaml` 为准。

## 剧本建议

- 正文优先写成 screenplay：场景标题、动作描写、人物名、对白、括号提示、声音标记、转场和特殊格式。
- 可按三幕、八序列、场景组或导演段落组织；不强制每个段落都有短剧式反转。
- 场景要有戏剧目的：角色想要什么、阻力是什么、场景结束时关系或信息发生什么变化。
- 允许沉默、观察、环境、动作和视觉隐喻承担叙事；不要把所有信息都写成对白。
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

错误写法：

```text
林渊很孤独，他想到父亲的话，决定去深矿证明自己。
```

修正为电影剧本：

```text
林渊站在气闸阴影里，头盔内只剩呼吸声。腕屏冷光扫过他的名字，风险标记跳成红色。
```

角色第一次出现时，简洁交代年龄感、身份、外貌或气质：

```text
林渊，24岁，月面矿工，旧式宇航服袖口磨得发白。他动作克制，像是每一步都先在心里算过风险。
```

不要第一次出现就堆满世界观设定；角色信息应分散到行动和对白中体现。

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
- 角色、场景、道具先按稳定资产写入 CueLight；剧本中的临时情绪和一次性动作进入 episode/script 或 storyboard，不写进资产 `basePrompt`。
- AIGC 友好的电影剧本应让系统能抽取角色、场景、道具、动作、情绪、声音和对白；抽象心理必须转成可见可听的行为。

## 分镜建议

- storyboard item 仍按 CueLight 字段落库，当前单条时长固定 4-15 秒；镜头数量和节奏应服务导演意图，可以使用长镜头、静默段落、环境镜头和蒙太奇，但不能把单条 item 放宽到更长时长。
- 分镜必须从最新剧本正文中提炼。若正文从 treatment 改为电影剧本，已有分镜要按新正文重新校准 `videoPrompt` 与 `scriptExcerpt`，不能只做文字润色。
- 不强制每个 storyboard item 都有对白；无对白 item 必须有明确视觉叙事、声音设计、人物行动、主题意象或剪辑作用。
- 场面调度优先于机械切镜：如果一个镜头能通过走位、焦点、遮挡和声音完成关系变化，不要为了凑镜头拆碎。
- 分镜要写清摄影意图：景别、机位、运动、焦点变化、光线、前后景关系、空间变化和声音桥接。
- 多场景可用于平行剪辑、回忆、梦境、电话两端和蒙太奇；如果每个空间都有完整动作弧线，优先拆成多个 storyboard item。
- 项目画幅为 `21:9` 或其他宽银幕比例时，优先宽景、横向调度、前中后景层次和克制特写；不要套用竖屏短剧的大头近景节奏。

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

错误写法：

```text
林渊很孤独，他想到父亲的话，决定去深矿证明自己。本段主要表现主角成长。
```

修正为电影剧本：

```text
内景. 休息舱 - 班前

狭窄休息舱里，白色台灯照着一枚旧铜丝罗盘。

林渊坐在床沿，把罗盘压进内层衣袋。舱外广播提示班前集合。他把工具袋拉链合上，停了一秒，确认没有人看见。

                    林渊（V.O.）
          如果名字是他们给的，我就把它活成自己的。
```

## 三位专家自检

- 电影编剧：检查主题问题、人物欲望、冲突升级、转折和结局是否连贯；检查场景是否推动人物弧光。
- 导演：检查每场戏的场面调度、视线、阻挡、沉默、动作和演员表演是否能承载戏剧变化。
- 摄影/剪辑顾问：检查镜头选择、光线、焦点、运动、长镜头或剪辑点是否有动机；检查组接是否形成视觉叙事而非只复述剧情。

## 验收

- 剧本按电影结构推进，主题和人物弧光清楚。
- screenplay 正文包含清楚的场景标题、可拍动作、可听声音、人物对白或明确无对白表演。
- 首次出现的重要角色有简洁可用的人物呈现。
- O.S./V.O.、转场、插入物、字幕、蒙太奇、闪回等特殊格式使用克制且功能明确。
- 分镜能体现摄影、调度、声音和剪辑意图。
- 每条 storyboard 的 `scriptExcerpt` 能追溯到最新 screenplay 正文。
- 静默、氛围、环境和视觉隐喻都有明确功能。
- 不因使用 CueLight item 化落库而把电影段落压成短剧节奏。
