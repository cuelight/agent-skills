# 制片台模式（Studio Workspace）

这份文档只描述制片台模式 CLI。不要把这里的命令当作短剧 Agent / 导演流程主路径。

## 核心区别

- Studio 是手动制作台：空项目、资产、分镜、视频可以直接推进
- Studio 不默认要求 source draft、proposal、design、Episode script
- Studio storyboard 可以是 text-only，生成视频时走 `studioMode`
- Studio 专业资产包含基础参考图和规范图版本，不等同于普通角色/场景/道具参考图

短剧 Agent / 导演流程仍使用 `source`、`project status`、`season`、`bible`、`episode`、`director`、`storyboard` 等命令。

## 项目

```bash
# 列出制片台可见项目（排除 director snapshot）
cuelight-cli studio project list --json

# 创建空制片台项目
cuelight-cli studio project create \
  --title "专业制作项目" \
  --video-ratio 9:16 \
  --photoreal \
  --json

# 非仿真项目
cuelight-cli studio project create \
  --title "动画制作项目" \
  --video-ratio 16:9 \
  --non-photoreal \
  --json

# 读取项目详情
cuelight-cli studio project status <projectId> --json

# 更新标题或比例
cuelight-cli studio project update <projectId> --title "新标题" --video-ratio 21:9 --json

# 删除项目
cuelight-cli studio project delete <projectId>
```

默认创建参数：

- `projectType=full_stage`
- `genre=短剧`
- `totalEpisodes=0`
- `durationPerEpisode=15`
- `visualMode=library`
- `videoModelSeries=seedance_vip`
- `omniReferenceFinalModel=seedance-2-0-fast-vip`

## 分集与分镜

```bash
# 分集
cuelight-cli studio episode list <projectId> --json
cuelight-cli studio episode create <projectId> --title "未命名分集" --json
cuelight-cli studio episode update <episodeId> --title "EP01" --summary "..." --content "..." --json
cuelight-cli studio episode delete <episodeId>

# 分镜
cuelight-cli studio storyboard list <episodeId> --json
cuelight-cli studio storyboard get <storyboardId> --json
cuelight-cli studio storyboard create <episodeId> \
  --scene-number 1 \
  --video-prompt "雨夜街角，镜头缓慢推近，人物停在霓虹灯下。" \
  --duration 8 \
  --json
cuelight-cli studio storyboard update <storyboardId> --video-prompt "..." --duration 10 --json
cuelight-cli studio storyboard duplicate <episodeId> <storyboardId> --json
cuelight-cli studio storyboard delete <storyboardId>
```

规则：

- Studio 单集最多 12 个 storyboard
- 默认 `frameMode=t2v`、`shotCount=1`
- 可以只写 `videoPrompt` 和 `duration`
- 若要提升一致性，可补 `--ref-character-ids`、`--ref-scene-id`、`--ref-prop-ids`
- 不要在 Studio 流程中强制要求 Episode script 或 director storyboard-status 通过后才创建分镜

## 专业资产

资产类型只允许：

- `character`
- `scene`
- `prop`

基础操作：

```bash
cuelight-cli studio asset list <projectId> character --json
cuelight-cli studio asset create <projectId> character --name "林小雨" --description "..." --base-prompt "..." --json
cuelight-cli studio asset update <projectId> character <characterId> --height-cm 168 --body-type "标准" --json
cuelight-cli studio asset update <projectId> scene <sceneId> --size-label "约 8m x 12m" --json
cuelight-cli studio asset update <projectId> prop <propId> --size-label "掌心大小" --json
cuelight-cli studio asset delete <projectId> prop <propId>
```

上传图片：

```bash
# 基础参考图
cuelight-cli studio asset upload-image <projectId> character <characterId> --file ./character.png --asset-kind image --json

# 上传专业规范图版本
cuelight-cli studio asset upload-image <projectId> scene <sceneId> --file ./scene-6view.png --asset-kind scene_6view --json
```

生成基础参考图：

```bash
cuelight-cli studio asset generate-reference <projectId> character <characterId> \
  --reference-text "二十岁出头，黑色长发，都市短剧女主，真实肤质。" \
  --json
```

生成专业规范图：

```bash
cuelight-cli studio asset generate-spec <projectId> character <characterId> \
  --asset-kind character_head_closeup_4view \
  --input-mode image_reference \
  --reference-image-url "https://..." \
  --reference-text "保持发型和五官一致" \
  --json

cuelight-cli studio asset generate-spec <projectId> scene <sceneId> \
  --asset-kind scene_6view \
  --input-mode image_reference \
  --reference-image-url "https://..." \
  --json

cuelight-cli studio asset generate-spec <projectId> prop <propId> \
  --asset-kind prop_6view \
  --input-mode image_reference \
  --reference-image-url "https://..." \
  --json
```

支持的 `assetKind`：

- `image`
- `character_head_closeup_4view`
- `character_head_closeup_12view`
- `character_full_body_4view`
- `scene_6view`
- `prop_6view`

支持的 `inputMode`：

- `text_reference`：用文字生成基础参考图
- `image_reference`：基于基础参考图生成规范图
- `upload`：用户上传图片作为当前版本

专业规范图通常需要高级权益；若返回订阅/权益错误，向用户说明这是账号权限问题，不要改用短剧 Agent 流程绕过。

## 资产版本

```bash
cuelight-cli studio asset versions <projectId> character <characterId> --asset-kind image --json
cuelight-cli studio asset versions <projectId> character <characterId> --asset-kind character_full_body_4view --json
cuelight-cli studio asset set-current-version <projectId> <versionId> --json
cuelight-cli studio asset delete-version <projectId> <versionId> --json
```

说明：

- `image` 是基础参考图版本
- 专业规范图使用对应 `assetKind` 查询版本
- 切换 current version 会同步镜像到角色/场景/道具实体字段

## 视频生成与导出

单条生成：

```bash
cuelight-cli studio video generate <projectId> <storyboardId> \
  --duration 8 \
  --model-id video-seedance-2-0-fast-vip \
  --model seedance-2-0-fast-vip \
  --json
```

批量生成：

```bash
cuelight-cli studio video batch-generate <projectId> <episodeId> \
  --storyboard-ids "sb-1,sb-2" \
  --duration 8 \
  --json

cuelight-cli studio video batch-generate <projectId> <episodeId> \
  --storyboard-ids "sb-1,sb-2" \
  --duration-map '{"sb-1":8,"sb-2":12}' \
  --json
```

任务与导出：

```bash
cuelight-cli studio video wait <taskId> --json
cuelight-cli studio video export <episodeId> --storyboard-ids "sb-1,sb-2" --json
```

规则：

- Studio 视频提交走 `studioMode=true`
- Studio 只接受 flexible-duration 视频模型
- `duration` 必须落在当前模型允许范围内
- Studio 允许 text-only storyboard；如果提供角色/场景/道具绑定，系统会尽量使用基础参考图或专业规范图增强一致性

## 与短剧 Agent 命令的边界

不要在 Studio 主路径中默认使用：

```bash
cuelight-cli source draft ...
cuelight-cli season set-proposal ...
cuelight-cli season set-design ...
cuelight-cli director status ...
cuelight-cli director storyboard-status ...
cuelight-cli director import-storyboards ...
```

这些属于短剧 Agent / 导演流程。只有用户明确从 Studio 切回短剧全链路，或需要排障对照底层实体时，才引用它们。
