# Style

```bash
cuelight-cli style presets --json
cuelight-cli style user-styles --json
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt --json
```

## 写法

风格提示词应统一：

- 画幅：默认短剧竖屏 9:16，除非用户明确要求其他比例。
- 影调：冷暖、对比、饱和度、颗粒感。
- 灯光：soft diffused light、rim lighting、自然侧光、夜景霓虹等。
- 镜头质感：写实、电影感、手持、稳定推近、浅景深。
- 服化道方向：时代、阶层、材质、色彩等级。
- 禁忌项：过度卡通、AI 塑料感、低清、错误时代元素等。

## 示例

```text
仿真人短剧质感，竖屏 9:16，人物近景优先，整体低饱和暖灰调。室内以 soft diffused light 为主，人物边缘保留轻微 rim lighting，镜头稳定推近，浅景深突出面部表演。服化道强调阶层差异，避免卡通化、过度磨皮、低清纹理和错误时代元素。
```

## 注意

- 不要只写“电影感”“高级感”。
- 不要每个角色/场景写互相冲突的风格。
- 如果用户选择了风格预设，`stylePrompt` 应与预设方向一致，而不是覆盖成另一套审美。
