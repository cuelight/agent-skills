# Bible

```bash
cuelight-cli bible get <projectId> --json
cuelight-cli bible set-world <projectId> --file ./.cuelight/<projectId>/world.txt --json
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt --json
```

## WorldView

`worldView` 写稳定设定、人物关系、规则和叙事基调，不写一次性剧情复述。

建议结构：

- 世界背景：时代、阶层、行业、家庭/组织结构。
- 规则约束：身份制度、能力边界、社会规则、职业规则。
- 核心关系：主角与关键人物的利益、情感、对抗关系。
- 冲突来源：造成持续戏剧张力的结构性矛盾。
- 禁忌边界：不能随意改动的事实、设定或关系。

## StylePrompt

`stylePrompt` 写统一视觉风格，中文为主，可保留英文镜头与灯光术语。

必须覆盖：

- 画幅和构图：如竖屏 9:16、近身压迫感、人物优先。
- 影调和色彩：暖冷关系、饱和度、对比度。
- 光线：soft diffused light、rim lighting、夜景霓虹、自然侧光等。
- 镜头质感：写实短剧、电影感、手持轻微晃动、稳定推近等。
- 服化道方向：时代材质、色彩等级、阶层差异。
- 禁忌项：过度卡通、过度磨皮、低清、错误时代元素等。

示例：

```text
仿真人短剧质感，竖屏 9:16，人物近景优先，写实肤质与克制调色。室内以 soft diffused light 为主，人物边缘保留轻微 rim lighting；外景使用自然侧光和浅景深。服化道强调阶层差异，避免卡通化、过度磨皮、低清纹理和错误时代元素。
```

写入后用 `cuelight-cli project status <projectId> --json` 核验。
