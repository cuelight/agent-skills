# 圣经（世界观）管理

## 外部 Agent 写回（主路径）

```bash
# 先读取当前 bible
cuelight-cli bible get <projectId> --json

# 从文件覆盖世界观（推荐）
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/world.txt

# 从文件覆盖风格提示词（推荐）
cuelight-cli director set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt
```

默认原则：

- `worldView`、`stylePrompt` 默认由外部 agent 自己创作，再通过 CLI 写回
- `director set-style-prompt` 是公开工作流里的风格写回主路径
- 不要默认把内置 bible 生成当主路径

## 直接编辑与底层 fallback

```bash
# 修改世界观
cuelight-cli bible update <projectId> --world-view "赛博朋克都市，霓虹灯映照的雨夜街道"

# 底层修改风格提示词
cuelight-cli bible update <projectId> --style-prompt "仿真人短剧质感，克制调色，人物边缘保留 rim lighting，室内采用 soft diffused light，画面强调门第秩序与压迫感。"

# 修改视觉模式
cuelight-cli bible update <projectId> --visual-mode improv|library|null

# 启用自动附加资源
cuelight-cli bible update <projectId> --auto-attach-assets
```

## 内置生成说明

- bible 文本生成能力属于内部旧链路，不属于公开 `CLI + skill` 工作流
- 外部 agent 不要把 `bible generate` 当成常规兜底或默认备选
- 若必须验证内部能力，应明确切到开发/排障语境，而不是继续沿用本 skill 主路径

补充规则：

- `worldView` 正文正常使用中文
- `stylePrompt` 使用中文自然句，保留必要英文专业术语
