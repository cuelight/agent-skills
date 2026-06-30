# Character

```bash
cuelight-cli character list <projectId> --json
cuelight-cli character create <projectId> --name "角色名" --description-file ./.cuelight/<projectId>/staging/import/characters/name-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/characters/name-visual.txt --voice-prompt-file ./.cuelight/<projectId>/staging/import/characters/name-voice.txt --json
cuelight-cli character update <projectId> <characterId> --description-file ./.cuelight/<projectId>/staging/import/characters/name-desc.txt --base-prompt-file ./.cuelight/<projectId>/staging/import/characters/name-visual.txt --voice-prompt-file ./.cuelight/<projectId>/staging/import/characters/name-voice.txt --json
```

## 内容要求

角色 description 应包含：

- 身份：年龄段、职业/阶层、关系位置。
- 性格：稳定性格，不写单场情绪。
- 目标：当前阶段最想要什么。
- 关系：与主角、对手、亲密人物的关系。
- 表演要点：眼神、站姿、动作习惯、说话节奏。

不要在 description 中写 `basePrompt：...`、`voicePrompt：...` 或视觉/音色字段标签。

## BasePrompt

`basePrompt` 写角色稳定视觉基准状态，不写一次性动作。它应是单段中文自然句，不是英文逗号词串，也不是散文式人物分析。

优先按以下顺序写可见外观：

- 性别。
- 年龄 / 年龄段。
- 人种 / 民族 / 时代身份。
- 肤色。
- 脸型 / 骨相。
- 眉眼鼻唇等高辨识五官。
- 身高 / 体态。
- 发型 / 发色。
- 日常服装材质。
- 稳定标志性元素。
- 整体气质。
- 少量镜头建议，例如 `neutral expression`、`medium shot`。

好的写法：

```text
女性，二十岁出头，古装宅院闺秀，肤色白净偏冷，鹅蛋脸，眉眼线条细长，鼻梁小巧，唇色浅，身形纤细，黑发盘成整洁低发髻，穿浅青色织纹襦裙，袖口有细密暗纹，整体气质克制端正、清冷安静，neutral expression，medium shot。
```

```text
男性，三十岁左右，近现代城市刑警，肤色偏深小麦色，方脸，眉骨明显，眼型狭长，鼻梁高，唇线紧，身形高大结实，黑色短发，穿深灰色旧夹克和黑色棉质内衫，领口有轻微磨损，整体气质沉稳警觉、压迫感强，neutral expression，medium shot。
```

避免：

- “她正冲进房间质问对方”这类剧情瞬间。
- “雨夜里他刚杀完人”这类临时场景或一次性情绪。
- “她是男主的姐姐、家族继承人”这类只写关系和叙事功能。
- “很漂亮很高级”“电影感强”这类不可控泛词。
- 写成 `basePrompt：...`、`视觉提示词：...` 等字段标签。
- 使用大段英文逗号词串作为默认写法。

## VoicePrompt

`voicePrompt` 写稳定音色，不写台词、剧情动作或视觉外貌。

必须覆盖：

- 声线类型：男低音、男中音、女中音、女高音等。
- 音色质感：低沉、磁性、清亮、沙哑、温柔、紧绷等。
- 语速节奏：偏慢、利落、急促、克制等。
- 情感基调：可靠、压迫、温和、讥讽、隐忍等。
- 呼吸感/共鸣：胸腔共鸣、鼻音轻、气声明显等。
- 特殊标注：方言、时代腔调、职业语气；没有则省略。
