# 角色管理

## 创建角色（主路径）

```bash
# 手动创建
cuelight-cli character create <projectId> --name "林小雨" --description "..." --base-prompt "二十岁上下的少女面相，鹅蛋脸，黑色长发，眼神克制清亮，穿浅灰色日常便装，neutral expression，medium shot。"

# 更新已有角色
cuelight-cli character update <projectId> <characterId> --name "新名" --description "..." --base-prompt "..."
```

写法规则：

- `name`、`description`、`basePrompt` 默认由外部 agent 自己编写
- `basePrompt` 使用中文自然句，保留必要英文术语，如 `medium shot`、`neutral expression`
- 写角色的基准外观，不写剧情瞬间动作、临时情绪或特殊事件服装
- 先写稳定识别特征，再写穿着和整体气质

## 内置文本生成说明

- 角色文本生成能力属于内部旧链路，不属于公开 `CLI + skill` 工作流
- 外部 agent 默认自己写 `description` 和 `basePrompt`，再通过 `character create/update` 落库
- 不要把 `character generate` 当成常规兜底或默认备选

## 生成参考图/视频/语音

```bash
# 批量生成缺失参考图
cuelight-cli character batch-generate-images <projectId>

# 单个角色生成参考图
cuelight-cli character generate-image <projectId> <characterId>

# 批量生成参考视频（需先有参考图）
cuelight-cli character batch-generate-videos <projectId>

# 生成语音配置
cuelight-cli character generate-voice <projectId> <characterId>

# 等待任务完成
cuelight-cli ai tasks <projectId>
```

## 查看和管理

```bash
cuelight-cli character list <projectId>
cuelight-cli character get <projectId> <characterId>
cuelight-cli character delete <projectId> <characterId>
```
