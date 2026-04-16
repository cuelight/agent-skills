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
# 主路径：用 director 写回风格提示词
cuelight-cli director set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt

# 主路径：生成风格参考图
cuelight-cli director generate-style-image <projectId> --prompt "仿真人宅院短剧海报感主视觉，暖色灯火与木质厅堂形成层次，ensemble cast 构图强调门第压迫与人物对峙。"

# 应用自定义风格（提示词+参考图）
cuelight-cli style apply <projectId> --style-prompt "..." --ref-image "https://..."
```

## 底层 fallback

```bash
# 底层设置风格提示词
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt

# 或直接传参
cuelight-cli bible update <projectId> --style-prompt "仿真人短剧质感，人物肤质写实，室内以 soft diffused light 为主，边缘保留轻微 rim lighting，画面保持 shallow depth of field。"

# 底层生成风格参考图
cuelight-cli bible generate-style-image <projectId> --prompt "仿真人宅院短剧海报感主视觉，暖色灯火与木质厅堂形成层次，ensemble cast 构图强调门第压迫与人物对峙。"
```

写法规则：

- `stylePrompt` 使用中文自然句，保留必要英文术语，如 `soft diffused light`、`rim lighting`
- 不再把纯英文逗号词串当默认写法
- 重点写整体质感、光线、色调、构图倾向和题材气质

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
