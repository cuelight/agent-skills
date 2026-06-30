from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_slug(value: str) -> str:
    if not SLUG_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("slug must use lowercase letters, digits, and hyphens")
    return value


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def episode_name(index: int) -> str:
    return f"ep-{index:03d}"


def build_manifest(
    title: str,
    slug: str,
    fmt: str,
    emotion: str,
    episodes: int,
    include_storyboard: bool,
) -> dict[str, object]:
    current_season_episodes = min(episodes, 60) if episodes > 5 else episodes
    artifacts = {
        "brief": "00-brief.md",
        "concept": "01-concept.md",
        "characters": "02-characters.md",
        "storyMachine": "03-story-machine.md",
        "seasonOutline": "04-season-outline.md",
        "episodes": "episodes/",
        "qualityCheck": "quality-check.md",
        "fullScript": "exports/full-script.md",
    }
    if include_storyboard:
        artifacts["storyboard"] = "storyboard/"

    return {
        "title": title,
        "slug": slug,
        "format": fmt,
        "primaryEmotion": emotion,
        "episodeCount": episodes,
        "seasonCount": ((episodes - 1) // 60) + 1,
        "currentSeason": 1,
        "secondsPerEpisode": 120 if episodes > 5 else None,
        "seasonRuntimeMinutes": round((current_season_episodes * 120) / 60, 2) if episodes > 5 else None,
        "status": "scaffold",
        "artifacts": artifacts,
    }


def resolve_output_root(root: Path, script_path: Path) -> Path:
    if root.is_absolute():
        return root.resolve()

    cwd = Path.cwd().resolve()
    skill_root = script_path.resolve().parents[1]
    if cwd == skill_root or skill_root in cwd.parents:
        raise ValueError(
            "relative --root would write inside the skill directory; "
            "run from the user workspace or pass an absolute --root"
        )
    return (cwd / root).resolve()


def scaffold(
    project_dir: Path,
    title: str,
    slug: str,
    fmt: str,
    emotion: str,
    episodes: int,
    overwrite: bool,
    include_storyboard: bool,
) -> None:
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "episodes").mkdir(exist_ok=True)
    if include_storyboard:
        (project_dir / "storyboard").mkdir(exist_ok=True)
    (project_dir / "exports").mkdir(exist_ok=True)

    manifest = build_manifest(title, slug, fmt, emotion, episodes, include_storyboard)
    manifest_path = project_dir / "manifest.json"
    if overwrite or not manifest_path.exists():
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    write_text(
        project_dir / "00-brief.md",
        f"""# {title} - 需求简报

## 原始需求

## 目标形式
- 形式：{fmt}
- 集数：{episodes}
- 主情绪：{emotion}
- 主梦境订单：掌控者型 / 关系者型 / 逃避者型
- 护梦三指标：
  - 安全感：
  - 高效满足感：
  - 强化真实感：

## 目标观众

## 样本容量分析
- 样本文字量：
- 段落量 / 章节结构：
- 核心事件数：
- 可拍场景数：
- 关键反转数：
- 情绪兑现点数：
- 预估总容量：短篇 / 中篇 / 长篇
- 默认单集时长：
  - 预估 5 集以上：120 秒 / 集
  - 预估 5 集以内：按剧情实际控制在 60-180 秒 / 集
- 预估总集数：{episodes}
- 预估总时长：{round((episodes * 120) / 60, 2) if episodes > 5 else "按剧情实际估算"}
- 是否超过 60 集：{"是" if episodes > 60 else "否"}
- 是否分季：{"是" if episodes > 60 else "否"}
- 当前处理范围：{"第一季，最多 60 集 / 120 分钟" if episodes > 60 else "当前请求范围"}
- 容量判断依据：
- 单集正文容量口径：只统计 `## 剧本正文` 下 `text` 代码块内部可表演正文；外层 Markdown、质量审查、场次列表，以及 `时/地/人/场号/楔子` 等格式行不计入。
- 120 秒正文目标：建议 900-1300 个中文字符；超过 1500 个中文字符必须压缩、拆集或说明用户明确要求更长。

## 交付边界
- 必须包含：
- 不要包含：

## 已确认假设
""",
        overwrite,
    )

    write_text(
        project_dir / "01-concept.md",
        f"""# {title} - 核心概念

## 一句话故事

## 观众承诺
这个故事让观众感到：

## 主情绪
{emotion}

## 幻想兑现

## 现实缺口

## 故事发动机
- 主发动机：
- 辅助发动机：
- 选择理由：

## 主梦境订单

## 第一屏如何证明订单

## 付费点或追更点

## 第一屏钩子
""",
        overwrite,
    )

    write_text(
        project_dir / "02-characters.md",
        f"""# {title} - 人物

## 主角
- 外显身份：
- 内含欲望：
- 伤口或秘密：
- 可执行目标：
- 不可退让的底线：
- 第一集能被看见的弱势：
- 中后段能被看见的反击能力：
- 情绪功能：

### 主角 8 要素
| 要素 | 内容 |
| --- | --- |
| 身份 | |
| 欲望 | |
| 问题 | |
| 负价值观 | |
| 动作 | |
| 阻碍 | |
| 结果 | |
| 正价值观 | |

## 反派
- 外显身份：
- 压迫手段：
- 误判主角的点：
- 阶段性升级动作：
- 被打脸时的公众代价：

### 反派 8 要素
| 要素 | 内容 |
| --- | --- |
| 身份 | |
| 欲望 | |
| 问题 | |
| 负价值观 | |
| 动作 | |
| 阻碍 | |
| 结果 | |
| 正价值观 | |

## 关键配角
""",
        overwrite,
    )

    write_text(
        project_dir / "03-story-machine.md",
        f"""# {title} - 故事机器

## 主欲望

## 主阻碍

## 核心信息差
- 观众知道：
- 主角知道：
- 反派知道：

## 信息牌投放
| 信息 | 谁知道 | 投放方式：台词 / 动作表情 / 道具环境 / 旁白闪回 | 所在场景 |
| --- | --- | --- | --- |

## 预期循环
1.
2.
3.

## 升级阶梯
1.
2.
3.
4.
5.

## 情绪点分布

## 每集必须改变的变量

## 有效事件检查
| 关键事件 | 有冲突 | 有改变 | 有目的 |
| --- | --- | --- | --- |
""",
        overwrite,
    )

    write_text(
        project_dir / "04-season-outline.md",
        f"""# {title} - 全剧大纲

## 总体结构
- 总集数：{episodes}
- 主情绪：{emotion}

## 容量结论（承接样本容量分析）
- 预估总集数：{episodes}
- 单集时长：{120 if episodes > 5 else "60-180"} 秒
- 预估总时长：{round((episodes * 120) / 60, 2) if episodes > 5 else "按剧情实际估算"} 分钟
- 季数：{1 if episodes <= 60 else "按 60 集 / 120 分钟上限分季"}
- 当前处理季：第一季
- 第一季范围：{"1-60 集" if episodes > 60 else f"1-{episodes} 集"}
- 第一季总时长：{120 if episodes > 60 else (round((episodes * 120) / 60, 2) if episodes > 5 else "按剧情实际估算")} 分钟
- 截断原则：超过 60 集时默认只处理第一季，第一季不超过 60 集 / 120 分钟，并在季末设置阶段性高潮或强钩子。
- 分集密度原则：

## 阶段结构

## 10 序列骨架（复杂短剧结构可选）
| 序列 | 功能 | 本剧内容 |
| --- | --- | --- |
| 开场 | 立刻展示类型、人物处境和情绪订单 | |
| 建置 | 建立日常规则、关系压力和主缺口 | |
| 激励 | 事件逼主角进入不可逆行动 | |
| 进展 | 主角初步获利或误判胜利路径 | |
| 转折 | 新信息改变目标、敌我或代价 | |
| 再转 | 压力升级，旧办法失效 | |
| 危机 | 主角接近失去最重要的东西 | |
| 导入 | 真相、资源或选择把故事推向决战 | |
| 高潮 | 主矛盾正面解决，情绪承诺兑现 | |
| 结局 | 关系、身份、秩序落位，并留下余味或钩子 | |

## 分集表

| 集数 | 标题 | 本集目标 | 核心冲突 | 结尾钩子 |
| --- | --- | --- | --- | --- |
""",
        overwrite,
    )

    scaffold_episodes = min(episodes, 60) if episodes > 60 else episodes
    for index in range(1, scaffold_episodes + 1):
        name = episode_name(index)
        write_text(
            project_dir / "episodes" / f"{name}.md",
            f"""# 第 {index} 集

## 本集目标
- 改变了什么：
- 主情绪：
- 通向下一集的钩子：

## 开场钩子

## 场次列表

## 出场角色
- 主角：
- 反派 / 压迫者：
- 关键配角：
- 围观 / 功能角色：

## 剧本正文

```text
开场钩子
时：夜
地：酒店宴会厅
人：主角、反派、关键配角、围观者

　△宾客围成一圈。主角站在中央，所有目光压向他/她。
　△反派把一份文件推到主角面前。
反派：你以为今天还有人会帮你？
　△主角没有后退，只把手里的证据翻到最后一页。
主角：不用别人帮。

　　　　　　时：夜（接）
　　　１　　地：宴会厅门口
　　　　　　人：主角、反派、众人

　△门口传来脚步声。所有人回头。
　△主角看向反派，声音平稳。
主角：你们该看清楚了。
```

## 信息差或反转

## 情绪兑现

## 结尾卡点

## 本集质量审查
- Markdown 外层是否列出出场角色：
- 剧本正文是否使用 text 代码块：
- 120 秒单集是否只统计 text 代码块内部可表演正文：
- 可表演正文中文字符数是否在 900-1300 建议区间；若超过 1500 是否已压缩或拆集：
- 是否使用本地化剧集台本格式：
- 每场是否有时、地、人：
- 正式场次是否保留缩进排版，场号是否嵌在地行左侧：
- 动作段是否使用缩进 △：
- 对白是否使用“角色：对白”：
- 旁白、闪回和镜头提示是否使用中文：
- 开场 10-30 秒内是否有可见冲突：
- 开场是否有负面情节或戏剧扳机：
- 每场是否改变地位、关系、危险、秘密、资源或情绪温度：
- 信息牌是否通过台词、动作、道具或短闪回可见：
- 情绪兑现是否可见：
- 爽点 / 虐点是否留出反应展示：
- 台词是否删废话、带潜台词、有角色指纹：
- 集尾是否留下未解决问题：
- 结尾是否阻断情绪自然回落：
""",
            overwrite,
        )
        if include_storyboard:
            write_text(
                project_dir / "storyboard" / f"{name}-beats.md",
                f"""# 第 {index} 集分镜 Beat

## Beat 1
- 地点：
- 人物位置：
- 可见动作：
- 表情：
- 视觉焦点：
- 台词 / 旁白：
- 情绪目的：
- 连接：
""",
                overwrite,
            )

    write_text(
        project_dir / "quality-check.md",
        f"""# {title} - 质量检查

## 阶段审查

### 1. 需求锁定
- 状态：暂缺
- 产物：00-brief.md
- 通过项：
- 风险：
- 返工动作：

### 2. 概念承诺
- 状态：暂缺
- 产物：01-concept.md
- 通过项：
- 风险：
- 返工动作：

### 3. 人物机器
- 状态：暂缺
- 产物：02-characters.md
- 通过项：
- 风险：
- 返工动作：

### 4. 故事机器
- 状态：暂缺
- 产物：03-story-machine.md
- 通过项：
- 风险：
- 返工动作：

### 5. 全剧结构
- 状态：暂缺
- 产物：04-season-outline.md
- 通过项：
- 风险：
- 返工动作：

### 6. 单集剧本
- 状态：暂缺
- 产物：episodes/ep-xxx.md
- 通过项：
- 风险：
- 返工动作：

### 7. 文学精修
- 状态：暂缺
- 产物：quality-check.md / episodes/ep-xxx.md / 04-season-outline.md
- 通过项：
- 风险：
- 返工动作：

### 8. 交付收口
- 状态：暂缺
- 产物：quality-check.md / manifest.json / 按需 exports/full-script.md
- 通过项：
- 风险：
- 返工动作：

## 阶段专项审查
- 样本容量分析是否完成：
- 是否按 5 集阈值选择单集时长：
- 中长篇是否默认使用 120 秒 / 集：
- 120 秒是否作为目标时长而不是最低时长：
- 单集正文容量是否只统计 `text` 代码块内部可表演正文：
- 120 秒单集可表演正文是否控制在 900-1300 个中文字符；超过 1500 是否压缩或拆集：
- 超过 60 集是否分季，并默认只处理第一季：
- 第一季是否不超过 60 集 / 120 分钟：
- 分集表是否存在容量不足、越集补戏或后半季概述化：
- 梦境订单是否单一明确：
- 护梦三指标是否成立：
- 主发动机是否只选一个：
- 信息牌是否落到台词、动作、道具或旁白：
- 关键事件是否有冲突、有改变、有目的：
- 主角和反派是否完成 8 要素：
- 10 序列是否需要；若需要，功能是否完整：
- 开场负面情节或戏剧扳机是否足够快：
- 爽点是否包含压力、点燃、爆发、展示：
- 人物真实感是否成立，主角是否有代价或失控点：
- 台词质感是否避免现代解释腔和口号腔：
- 情绪层次是否不止打脸：
- 反派动机是否有欲望、利益、恐惧和误判：
- 关系线是否避免男主或盟友工具化：
- 后半季节奏是否避免概述式安稳岁月：
- 伦理认同是否避免女主无铺垫反派化：

## 最终总检
- 样本容量结论：
- 第一季范围：
- 开头钩子：
- 观众承诺：
- 主角欲望：
- 反派压力：
- 信息差：
- 情绪兑现：
- 集尾钩子：
- 文学精修是否完成：
- manifest 状态、路径和实际产物是否一致：

## 当前最该修改的 3 个问题
> 优先记录文学精修阶段发现的问题。

1.
2.
3.
""",
        overwrite,
    )

    write_text(
        project_dir / "exports" / "full-script.md",
        f"""# {title} - 汇总稿

> 从分文件产物汇总，不替代源文件。
""",
        overwrite,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a local short-drama project scaffold.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("cuelight-projects/shortdrama"),
        help="Output root. Prefer an absolute workspace path.",
    )
    parser.add_argument("--slug", required=True, type=validate_slug)
    parser.add_argument("--title", required=True)
    parser.add_argument("--format", default="短剧")
    parser.add_argument("--emotion", default="复仇爽")
    parser.add_argument("--episodes", type=int, default=1)
    parser.add_argument("--include-storyboard", action="store_true", help="Create optional storyboard beat files.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.episodes < 1:
        parser.error("--episodes must be >= 1")

    try:
        output_root = resolve_output_root(args.root, Path(__file__))
    except ValueError as error:
        parser.error(str(error))

    project_dir = output_root / args.slug
    scaffold(
        project_dir,
        args.title,
        args.slug,
        args.format,
        args.emotion,
        args.episodes,
        args.overwrite,
        args.include_storyboard,
    )
    print(project_dir.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
