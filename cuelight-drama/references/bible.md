# 圣经（世界观）管理

## 生成圣经

```bash
# AI 生成圣经（世界观、角色概述、场景概述）
cuelight-cli bible generate <projectId>

# 查看生成结果
cuelight-cli bible get <projectId>
```

## 编辑圣经

```bash
# 从文件覆盖世界观（推荐）
cuelight-cli bible set-world <projectId> --file ./world.txt

# 从文件覆盖风格提示词（推荐）
cuelight-cli bible set-style-prompt <projectId> --file ./style-prompt.txt

# 修改世界观
cuelight-cli bible update <projectId> --world-view "赛博朋克都市，霓虹灯映照的雨夜街道"

# 修改风格提示词
cuelight-cli bible update <projectId> --style-prompt "cinematic, moody lighting"

# 修改视觉模式
cuelight-cli bible update <projectId> --visual-mode improv|library|null

# 启用自动附加资源
cuelight-cli bible update <projectId> --auto-attach-assets
```
