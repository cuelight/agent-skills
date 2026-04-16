# 场景管理

## 创建场景（主路径）

```bash
# 手动创建
cuelight-cli scene create <projectId> --name "霓虹街道" --description "..." --base-prompt "夜间街道纵深清晰，霓虹招牌与潮湿路面形成反光层次，街道左右店铺布局明确，wide shot 展示空间关系与行进方向。" --ref-image "https://..."

# 更新已有场景
cuelight-cli scene update <projectId> <sceneId> --name "新名" --description "..." --base-prompt "..."
```

写法规则：

- `name`、`description`、`basePrompt` 默认由外部 agent 自己编写
- `basePrompt` 使用中文自然句，保留必要英文术语，如 `wide shot`
- 写场景的基准状态，聚焦结构、布局、基础光线和空间方向
- 不写具体剧情人物，不把场景 prompt 写成情节片段

## 内置文本生成说明

- 场景文本生成能力属于内部旧链路，不属于公开 `CLI + skill` 工作流
- 外部 agent 默认自己写 `description` 和 `basePrompt`，再通过 `scene create/update` 落库
- 不要把 `scene generate` 当成常规兜底或默认备选

## 生成参考图

```bash
# 批量生成缺失参考图
cuelight-cli scene batch-generate-images <projectId>

# 单个场景生成参考图
cuelight-cli scene generate-image <projectId> <sceneId>

# 等待任务完成
cuelight-cli ai tasks <projectId>
```

## 查看和管理

```bash
cuelight-cli scene list <projectId>
cuelight-cli scene get <projectId> <sceneId>
cuelight-cli scene delete <projectId> <sceneId>
```
