# Style

```bash
cuelight-cli style presets --json
cuelight-cli style user-styles --json
cuelight-cli bible set-style-prompt <projectId> --file ./.cuelight/<projectId>/style-prompt.txt --json
```

## 通用写法

风格提示词应与当前 profile 一致。先确认项目类型，再选择画幅、镜头质感和美术方向：

- 短剧：读取 `references/profiles/short-drama.md`。
- 番剧：读取 `references/profiles/anime-series.md`。
- 电影：读取 `references/profiles/film.md`。

stylePrompt 至少覆盖：

- 画幅和构图逻辑。
- 影调：冷暖、对比、饱和度、颗粒感或动画色彩层次。
- 灯光：soft diffused light、rim lighting、自然侧光、夜景霓虹、动画摄影处理等。
- 镜头质感：写实、动画演出、电影摄影、手持、稳定推近、浅景深等。
- 服化道或美术方向：时代、阶层、材质、色彩等级、作画线条或场景设计。
- 禁忌项：过度卡通、AI 塑料感、低清、错误时代元素、与 profile 不一致的画幅或镜头语言。

## 示例

短剧、番剧、电影的示例分别见对应 profile。不要把某一 profile 的示例当作全局默认。

## 注意

- 不要只写“电影感”“高级感”。
- 不要每个角色/场景写互相冲突的风格。
- 如果用户选择了风格预设，`stylePrompt` 应与预设方向一致，而不是覆盖成另一套审美。
