# 视觉风格管理

## 应用预设风格

```bash
# 查看可用预设
cuelight-cli style list-presets

# 应用预设
cuelight-cli style apply <projectId> --preset-id <presetId>
```

## 自定义风格

```bash
# 直接设置风格提示词
cuelight-cli bible update <projectId> --style-prompt "cinematic, moody lighting, shallow depth of field"

# 生成风格参考图
cuelight-cli bible generate-style-image <projectId> --prompt "cyberpunk city at night"

# 应用自定义风格（提示词+参考图）
cuelight-cli style apply <projectId> --style-prompt "..." --ref-image "https://..."
```

## 风格模板管理

```bash
# 保存当前风格为模板
cuelight-cli style save <projectId> --name "赛博朋克夜景"

# 查看已保存模板
cuelight-cli style list

# 应用已保存模板
cuelight-cli style apply <projectId> --style-id <styleId>

# 创建/更新/删除模板
cuelight-cli style create --name "..." --style-prompt "..."
cuelight-cli style update <styleId> --style-prompt "..."
cuelight-cli style delete <styleId>
```
