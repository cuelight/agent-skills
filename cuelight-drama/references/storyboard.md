# 分镜管理

## 生成分镜（推荐方式）

```bash
# 全量生成 + 自动修复绑定（推荐）
cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait

# 自定义超时和轮询
cuelight-cli storyboard generate <episodeId> --auto-supplement --repair-bindings --wait --timeout 600 --interval 5 --max-rounds 3
```

> **重要**：`generate` 会覆盖已有分镜。如需修复绑定而非重新生成，使用 `--auto-supplement --repair-bindings`。

## 生成后检查

生成分镜后**必须**检查绑定状态：

```bash
# 查看剧集聚合状态
cuelight-cli episode status <episodeId> --json

# 查看分镜列表，检查 referenceCharacterIds 和 referenceSceneId
cuelight-cli storyboard list <episodeId> --json

# 查看单个分镜详情
cuelight-cli storyboard get <storyboardId>
```

如果存在未绑定的分镜（`referenceCharacterIds` 为空），重新执行带修复参数的生成命令。

## 场景引用约束

CueLight 的 scene binding 不是靠 prompt 里的中文场景名推断的，最终以结构化字段 `referenceSceneId` 为准。

- `本片段场景设定在：实训教室。` 这类裸场景名只能算文案，不算有效绑定
- 若通过 `director update-storyboard` 或服务端工具写分镜，必须同时提供 `referenceSceneId`
- 当 `referenceSceneId` 已提供时，服务端会把 scene header 自动归一化成 canonical scene tag
- 这个 canonical scene tag 是**当前分镜组的局部编号**，由当前分镜的 `referenceCharacterIds` 顺序决定；不是全项目固定编号
- 不要让外部 agent 自己硬猜 `<CharacterN>` 场景标签编号；让服务端根据当前分镜绑定统一生成

推荐写法：

```bash
cuelight-cli director update-storyboard <storyboardId> \
  --video-prompt "生成一个由以下 2 个分镜组成的视频。本片段场景设定在：实训教室。..." \
  --ref-scene-id "<sceneId>" \
  --ref-character-ids "<charId1>,<charId2>"
```

不推荐写法：

```bash
# 只有 prompt 里的裸场景名，没有结构化绑定
本片段场景设定在：实训教室。
```

## 手动创建/编辑

```bash
# 创建单个分镜
cuelight-cli storyboard create <episodeId> --scene-number 1 --video-prompt "..." --shot-size "medium" --dialogues "角色A:台词" --sound-effects "雨声"

# 外部 agent 从文件导入文字分镜（推荐）
cuelight-cli storyboard import-text <episodeId> --file ./storyboards.json

# 批量创建（JSON 数据）
cuelight-cli storyboard batch-create <episodeId> --data-file ./storyboards.json

# 更新分镜（精确控制绑定）
cuelight-cli storyboard update <storyboardId> \
  --video-prompt "新的提示词" \
  --ref-character-ids "charId1,charId2" \
  --ref-scene-id "sceneId" \
  --video-clip-url "https://..."

# 优化提示词
cuelight-cli ai optimize-prompt <storyboardId>
```

## 查看和管理

```bash
cuelight-cli storyboard list <episodeId>
cuelight-cli storyboard get <storyboardId>
cuelight-cli storyboard delete <storyboardId>
```
