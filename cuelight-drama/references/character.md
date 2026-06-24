# Character

```bash
cuelight-cli character list <projectId> --json
cuelight-cli character create <projectId> --name "角色名" --description-file ./.cuelight/<projectId>/characters/name-desc.txt --base-prompt-file ./.cuelight/<projectId>/characters/name-visual.txt --voice-prompt-file ./.cuelight/<projectId>/characters/name-voice.txt --json
cuelight-cli character update <projectId> <characterId> --description-file ./.cuelight/<projectId>/characters/name-desc.txt --base-prompt-file ./.cuelight/<projectId>/characters/name-visual.txt --voice-prompt-file ./.cuelight/<projectId>/characters/name-voice.txt --json
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

`basePrompt` 写角色稳定视觉基准状态，不写一次性动作。必须覆盖可见外观：脸型、发型、体态、服装、标志性元素。

好的写法：

```text
二十岁出头的闺秀面相，鹅蛋脸，肤色白净偏冷，眉眼线条细长，发髻整洁，穿浅青色织纹襦裙，站姿克制端正，neutral expression，medium shot。
```

避免：

- “她正冲进房间质问对方”这类剧情瞬间。
- “很漂亮很高级”这类不可控泛词。
- 只写人物关系，不写可见外观。

## VoicePrompt

`voicePrompt` 写稳定音色，不写台词、剧情动作或视觉外貌。

必须覆盖：

- 声线类型：男低音、男中音、女中音、女高音等。
- 音色质感：低沉、磁性、清亮、沙哑、温柔、紧绷等。
- 语速节奏：偏慢、利落、急促、克制等。
- 情感基调：可靠、压迫、温和、讥讽、隐忍等。
- 呼吸感/共鸣：胸腔共鸣、鼻音轻、气声明显等。
- 特殊标注：方言、时代腔调、职业语气；没有则省略。
