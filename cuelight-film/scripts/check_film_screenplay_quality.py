#!/usr/bin/env python3
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


CREATIVE_NOTE_PATTERNS = [
    r"本场主要表现",
    r"本段主要表现",
    r"主要表现",
    r"用于建立",
    r"用.{0,12}建立",
    r"用.{0,12}表现",
    r"这不是一句解释",
    r"主题是",
    r"象征",
    r"戏剧功能",
    r"创作目的",
    r"导演意图",
    r"人物心理",
    r"心理锚点",
    r"认知型信任",
    r"权力距离",
    r"在戏剧构作中",
    r"压在局势上的承诺",
]

DIALOGUE_SUMMARY_PATTERNS = [
    r"^[\u4e00-\u9fff]{2,4}(承诺|宣布|质问|表示|说明|解释|告诉|回忆|想起)",
    r"^这不是一句解释",
    r"：.+(承诺|宣布|质问|表示|说明|解释)",
    r"本句",
]

GENERIC_ACTION_PATTERNS = [
    r"风声、帐火或军旗先于人物进入画面",
    r"空间把权力距离压到观众面前",
]

GENERIC_LITERARY_FILLER_PATTERNS = [
    r"像一只被拽住气息的袋子",
    r"没人再问刚才那句话该不该记入军报",
    r"这句话没有人说出口",
    r"给那句没有问出口的话留下",
    r"声音从碎裂变成一条线",
    r"靴底在.+上蹭出干涩的轻响",
    r"像在看一条刚画出来的界线",
    r"把最窄的路口让给一队迟疑的人",
    r"动作轻得几乎像在道歉",
]

SPATIAL_LOGIC_MISMATCH_PATTERNS = [
    r"(外景|山道|河岸|山口|校场|驿道|战场|远营).{0,80}屋内",
    r"(宫门影|空剑架|冷炭盆|兵符匣|齐地户籍|抽兵令|湿弓弦|旧井).{0,20}(滚到脚边|被推过一道浅坑)",
    r"冷炭盆压在案上或掌心里",
    r"铜盘压在案上或掌心里",
]

SCREENPLAY_ROLE_NAMES = {
    "char_hanxin": "韩信",
    "char_liubang": "刘邦",
    "char_xiaohe": "萧何",
    "char_cao_can": "曹参",
}

SLOGAN_DIALOGUE_PATTERNS = [
    r"天下.*(陪你|为你|随你)",
    r"万死不辞",
    r"恩重如山",
    r"一生不敢忘",
    r"用天下.*还",
    r"大汉.*基业",
]

TEMPLATED_SCREENPLAY_PATTERNS = [
    r".+的第[一二三四五六七八九十百零\d]+道军令落下，.+被.+到.+旁，.+停住半步，.+声从队尾压过来",
    r"这第[一二三四五六七八九十百零\d]+步若退，.+就不再听我",
    r"第[一二三四五六七八九十百零\d]+次列阵我看见了，可兵心还要再验",
    r"第[一二三四五六七八九十百零\d]+行字写下去，恩情和法度就分不开了",
    r"第[一二三四五六七八九十百零\d]+道功劳我认，.+也要回到规矩里",
    r"页\d+的灯影贴着地面移开，近旁一名军吏把封绳重新勒紧，人物的呼吸跟着慢下来",
]

SYNTHETIC_REWRITE_TEMPLATE_PATTERNS = [
    r"[一二三四五六七八九十百零\d甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥玄黄赤白青黑金玉石]令已听见",
    r"[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥玄黄赤白青黑金玉石天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰余成岁律吕调阳云腾致雨露结为霜]{1,4}甲色",
    r"[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥玄黄赤白青黑金玉石天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰余成岁律吕调阳云腾致雨露结为霜]{1,4}甲冷痕",
    r"从话里退出来",
    r"落成门、手和脚步之间的距离",
    r"场面从战功的喧声转成可执行的冷秩序",
]

MOTIF_TERMS = [
    "王袍",
    "热肉",
    "将印",
    "虎符",
    "军册",
    "钟声",
]

VISIBLE_ACTION_HINTS = [
    "走",
    "站",
    "坐",
    "看",
    "望",
    "听",
    "抓",
    "握",
    "放",
    "抬",
    "低",
    "停",
    "转",
    "推",
    "拉",
    "跪",
    "递",
    "披",
    "铺",
    "压",
    "落",
    "划",
    "冒",
    "滑",
    "渗",
    "响",
    "风",
    "雨",
    "雪",
    "声",
    "灯",
    "门",
    "手",
    "眼",
    "脚",
    "衣",
    "剑",
    "马",
    "钟",
]

PLACEHOLDER_CHARACTER_IDS = {"", "undefined", "null", "none", "todo", "tbd", "unknown"}
LITERARY_SCORE_PASSING = 80
MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE = 320
MIN_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE = 320
TARGET_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE = (350, 420)
REPEATED_FRAGMENT_MIN_CHARS = 22
PAGE_CAPACITY_BLOCK_TYPES = {"action", "dialogue", "parenthetical", "sound"}
SCRIPT_BODY_BLOCK_TYPES = {"action", "dialogue", "parenthetical", "shot", "insert", "sound", "super", "transition"}
UNLOCALIZED_SCREENPLAY_TERMS = [
    "SOUND",
    "INSERT",
    "CLOSE ON",
    "ANGLE ON",
    "MOVING WITH",
]
DIALOGUE_INTERLEAVE_BLOCK_TYPES = {"action", "parenthetical", "sound", "insert", "shot"}
DIALOGUE_EXCEPTION_KEYWORDS = [
    "独白",
    "广播",
    "系统语音",
    "审讯压迫",
    "仪式宣告",
    "无对手戏",
    "monologue",
    "broadcast",
    "system voice",
]


def rel_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def issue(level, issue_type, message, path, block=None, text=None):
    data = {
        "level": level,
        "type": issue_type,
        "message": message,
        "path": str(path).replace("\\", "/"),
    }
    if block and isinstance(block, dict):
        block_id = block.get("block_id")
        if block_id is not None:
            data["blockId"] = str(block_id)
        order_index = block.get("order_index")
        if order_index is not None:
            data["orderIndex"] = order_index
        block_type = block.get("block_type")
        if block_type is not None:
            data["blockType"] = str(block_type)
    if text:
        data["text"] = str(text)[:160]
    return data


def load_blocks(path: Path, root: Path, issues):
    if yaml is None:
        issues.append(
            issue(
                "error",
                "pyyaml_missing",
                "PyYAML is required to parse screenplay block YAML.",
                rel_path(path, root),
            )
        )
        return []

    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.append(
            issue(
                "error",
                "yaml_parse_error",
                f"Cannot parse screenplay blocks YAML: {exc}",
                rel_path(path, root),
            )
        )
        return []

    if loaded is None:
        return []

    if not isinstance(loaded, list):
        issues.append(
            issue(
                "error",
                "blocks_not_list",
                "screenplay blocks YAML must be a list of block objects.",
                rel_path(path, root),
            )
        )
        return []

    return loaded


def has_pattern(text, patterns):
    return any(re.search(pattern, text) for pattern in patterns)


def looks_like_visible_action(text):
    if not text:
        return False
    return any(hint in text for hint in VISIBLE_ACTION_HINTS)


def normalize_text(text):
    return re.sub(r"\s+", "", str(text or ""))


def contains_unlocalized_screenplay_term(text):
    upper = str(text or "").upper()
    return next((term for term in UNLOCALIZED_SCREENPLAY_TERMS if term in upper), None)


def page_status_is_formal(page):
    coverage = str(page.get("coverage_level", "") or "").lower()
    status = str(page.get("status", "") or "").lower()
    informal_markers = ("sample", "partial", "draft", "timing_estimate")
    if any(marker in coverage for marker in informal_markers):
        return False
    if any(marker in status for marker in ("sample", "partial", "draft")):
        return False
    return coverage in {"full_page", "locked", "production_ready"} or status in {"locked", "production_ready", "final"}


def page_issue_level(page, strict):
    return "error" if strict and page_status_is_formal(page) else "warning"


def page_has_dialogue_exception(page):
    fields = [
        page.get("dialogue_exception"),
        page.get("dialogue_readability_exception"),
        page.get("dialogue_gate_exception"),
        page.get("note"),
        page.get("notes"),
    ]
    text = " ".join(str(item) for item in fields if item)
    return any(keyword.lower() in text.lower() for keyword in DIALOGUE_EXCEPTION_KEYWORDS)


def block_speaker(block):
    for key in ("character_id", "speaker_id", "speaker", "character_name", "speaker_name"):
        value = block.get(key)
        if value:
            return str(value)
    return "unknown"


def normalize_sentence_skeleton(text):
    value = str(text or "")
    value = re.sub(r"第[一二三四五六七八九十百零\d]+", "第N", value)
    value = re.sub(r"页\d+", "页N", value)
    value = re.sub(r"blk_[A-Za-z0-9_]+", "blk_N", value)
    value = re.sub(r"\d+", "N", value)
    value = re.sub(r"[ \t\r\n]+", "", value)
    return value


def split_playable_fragments(text):
    parts = re.split(r"(?<=[。！？!?；;])", str(text or ""))
    fragments = []
    for part in parts:
        fragment = part.strip()
        if fragment:
            fragments.append(fragment)
    return fragments


def block_allowed_role_names(block):
    tags = block.get("semantic_tags") or {}
    character_ids = []
    if isinstance(tags, dict):
        raw = tags.get("characters") or []
        if isinstance(raw, list):
            character_ids = [str(item) for item in raw]
    if not character_ids and block.get("character_id"):
        character_ids = [str(block.get("character_id"))]
    return {SCREENPLAY_ROLE_NAMES[item] for item in character_ids if item in SCREENPLAY_ROLE_NAMES}


def unexpected_role_mentions(text, allowed_names):
    mentioned = {name for name in SCREENPLAY_ROLE_NAMES.values() if name in text}
    if not mentioned:
        return set()
    if not allowed_names:
        return set()
    return mentioned - allowed_names


def inspect_block(block, path, root):
    issues = []
    rel = rel_path(path, root)

    if not isinstance(block, dict):
        return [
            issue(
                "error",
                "block_not_object",
                "Each screenplay block must be a YAML object.",
                rel,
                text=block,
            )
        ]

    block_type = str(block.get("block_type", "")).strip()
    text = str(block.get("text", "") or "").strip()
    character_id = block.get("character_id")

    if block_type in {"action", "dialogue"} and not text:
        issues.append(
            issue(
                "error",
                "empty_screenplay_text",
                f"{block_type} block must have non-empty text.",
                rel,
                block,
            )
        )

    if character_id is not None and str(character_id).strip().lower() in PLACEHOLDER_CHARACTER_IDS:
        issues.append(
            issue(
                "error",
                "placeholder_character_id",
                "character_id must not be an undefined placeholder.",
                rel,
                block,
                text,
            )
        )

    if block_type in {"action", "dialogue"} and has_pattern(text, CREATIVE_NOTE_PATTERNS):
        issues.append(
            issue(
                "warning",
                "creative_note_in_screenplay",
                "action/dialogue text looks like a creative note or analysis instead of screenplay.",
                rel,
                block,
                text,
            )
        )

    if block_type in SCRIPT_BODY_BLOCK_TYPES:
        term = contains_unlocalized_screenplay_term(text)
        if term:
            issues.append(
                issue(
                    "error",
                    "unlocalized_screenplay_term",
                    f"Chinese screenplay body contains unlocalized screenplay function term '{term}'. Use localized terms such as 声音：、插入：、特写：、视角： or 跟拍：.",
                    rel,
                    block,
                    text,
                )
            )

    if block_type in {"action", "dialogue"} and has_pattern(text, TEMPLATED_SCREENPLAY_PATTERNS):
        issues.append(
            issue(
                "error",
                "templated_screenplay_pattern",
                "screenplay text looks like a variable-filled template instead of scene-specific dramatic writing.",
                rel,
                block,
                text,
            )
        )

    if block_type in {"action", "dialogue"} and has_pattern(text, SYNTHETIC_REWRITE_TEMPLATE_PATTERNS):
        issues.append(
            issue(
                "error",
                "synthetic_rewrite_template",
                "screenplay text looks like a formulaic rewrite-gate bypass pattern; strict checks are only signals, and the agent must review the actual scene before accepting it.",
                rel,
                block,
                text,
            )
        )

    if block_type in {"action", "dialogue"} and has_pattern(text, GENERIC_LITERARY_FILLER_PATTERNS):
        issues.append(
            issue(
                "error",
                "generic_literary_filler",
                "screenplay text uses reusable literary filler instead of scene-specific action, behavior, or subtext.",
                rel,
                block,
                text,
            )
        )

    if block_type == "dialogue":
        if has_pattern(text, DIALOGUE_SUMMARY_PATTERNS):
            issues.append(
                issue(
                    "warning",
                    "dialogue_looks_like_summary",
                    "dialogue text looks like a summary of speech instead of spoken words.",
                    rel,
                    block,
                    text,
                )
            )
        if has_pattern(text, SLOGAN_DIALOGUE_PATTERNS):
            issues.append(
                issue(
                    "warning",
                    "dialogue_may_be_thematic_slogan",
                    "dialogue may state theme too directly; check character voice and subtext.",
                    rel,
                    block,
                    text,
                )
            )
        if len(text) > 90 and "。" in text:
            issues.append(
                issue(
                    "warning",
                    "dialogue_too_expository",
                    "dialogue is long and sentence-like; check that it is playable spoken text.",
                    rel,
                    block,
                    text,
                )
            )

    if block_type == "action":
        allowed_names = block_allowed_role_names(block)
        unexpected_names = unexpected_role_mentions(text, allowed_names)
        if unexpected_names:
            issues.append(
                issue(
                    "error",
                    "unexpected_role_mention",
                    f"action mentions role(s) not present in this block's character binding: {', '.join(sorted(unexpected_names))}.",
                    rel,
                    block,
                    text,
                )
            )
        if has_pattern(text, SPATIAL_LOGIC_MISMATCH_PATTERNS):
            issues.append(
                issue(
                    "error",
                    "spatial_logic_mismatch",
                    "action text appears physically inconsistent with the scene space or prop behavior.",
                    rel,
                    block,
                    text,
                )
            )
        if len(text) < 6:
            issues.append(
                issue(
                    "warning",
                    "action_too_short",
                    "action block is too short to carry screen action.",
                    rel,
                    block,
                    text,
                )
            )
        if not looks_like_visible_action(text):
            issues.append(
                issue(
                    "warning",
                    "action_lacks_visible_or_audible_detail",
                    "action text may lack visible action, audible sound, object, or performable behavior.",
                    rel,
                    block,
                    text,
                )
            )
        if has_pattern(text, GENERIC_ACTION_PATTERNS):
            issues.append(
                issue(
                    "warning",
                    "generic_action_template",
                    "action text matches a reusable template instead of scene-specific staging.",
                    rel,
                    block,
                    text,
                )
            )

    return issues


def collect_blocks(film_data_dir: Path):
    return sorted(film_data_dir.glob("acts/**/scenes/*/script/blocks.yaml"))


def path_matches_act(path_value, act_id):
    if not act_id:
        return True
    normalized = str(path_value or "").replace("\\", "/")
    return f"acts/{act_id}/" in normalized


def collect_blocks_for_scope(film_data_dir: Path, act_id=None):
    block_files = collect_blocks(film_data_dir)
    if not act_id:
        return block_files
    return [path for path in block_files if path_matches_act(rel_path(path, film_data_dir), act_id)]


def inspect_root_script_pages(root: Path, issues, strict=False, act_id=None):
    pages_path = root / "script" / "pages.yaml"
    if not pages_path.exists():
        return 0

    if yaml is None:
        issues.append(
            issue(
                "error",
                "pyyaml_missing",
                "PyYAML is required to parse root script/pages.yaml.",
                rel_path(pages_path, root),
            )
        )
        return 0

    try:
        pages = yaml.safe_load(pages_path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.append(
            issue(
                "error",
                "yaml_parse_error",
                f"Cannot parse root script/pages.yaml: {exc}",
                rel_path(pages_path, root),
            )
        )
        return 0

    if pages is None:
        return 0
    if not isinstance(pages, list):
        issues.append(
            issue(
                "error",
                "pages_not_list",
                "root script/pages.yaml must be a list of ScriptPage objects.",
                rel_path(pages_path, root),
            )
        )
        return 0

    covered_blocks = defaultdict(list)
    block_cache = {}
    scoped_page_count = 0
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_number = page.get("page_number")
        refs = page.get("block_refs") or []
        if not isinstance(refs, list):
            issues.append(
                issue(
                    "error",
                    "block_refs_not_list",
                    f"block_refs must be a list on ScriptPage {page_number}.",
                    rel_path(pages_path, root),
                )
            )
            continue

        if act_id:
            scoped_refs = [ref for ref in refs if isinstance(ref, dict) and path_matches_act(ref.get("script_path"), act_id)]
            if not scoped_refs:
                continue
            refs = scoped_refs
        scoped_page_count += 1

        for page_ref in refs:
            if not isinstance(page_ref, dict):
                continue
            script_path = page_ref.get("script_path")
            start_id = page_ref.get("start_block_id")
            end_id = page_ref.get("end_block_id")
            page_fraction = page_ref.get("page_fraction")
            if not script_path or not start_id or not end_id:
                issues.append(
                    issue(
                        "error",
                        "invalid_page_block_ref",
                        "block_ref must include script_path, start_block_id, and end_block_id.",
                        rel_path(pages_path, root),
                    )
                )
                continue
            if isinstance(page_fraction, (int, float)) and page_fraction > 1.0:
                issues.append(
                    issue(
                        "warning",
                        "page_fraction_over_one",
                        "A single ScriptPage block_ref has page_fraction > 1.0; split the estimate across multiple ScriptPages or explain duration at scene/beat level.",
                        rel_path(pages_path, root),
                    )
                )

            block_path = root / str(script_path)
            if block_path not in block_cache:
                block_cache[block_path] = load_blocks(block_path, root, issues) if block_path.exists() else None
                if block_cache[block_path] is None:
                    issues.append(
                        issue(
                            "error",
                            "script_path_missing",
                            "ScriptPage references a missing blocks.yaml file.",
                            str(script_path),
                        )
                    )
                    continue

            blocks = block_cache[block_path]
            block_ids = [block.get("block_id") for block in blocks if isinstance(block, dict)]
            try:
                start_index = block_ids.index(start_id)
                end_index = block_ids.index(end_id)
            except ValueError:
                issues.append(
                    issue(
                        "error",
                        "page_block_range_missing",
                        f"Cannot find ScriptPage block range {start_id} -> {end_id}.",
                        str(script_path),
                    )
                )
                continue
            if start_index > end_index:
                issues.append(
                    issue(
                        "error",
                        "page_block_range_reversed",
                        f"ScriptPage block range is reversed: {start_id} -> {end_id}.",
                        str(script_path),
                    )
                )
                continue

            rel_script_path = rel_path(block_path, root)
            for block_id in block_ids[start_index : end_index + 1]:
                covered_blocks[f"{rel_script_path}#{block_id}"].append(page_number)

    duplicate_level = "error" if strict else "warning"
    for block_key, page_numbers in covered_blocks.items():
        if len(page_numbers) <= 1:
            continue
        issues.append(
            issue(
                duplicate_level,
                "duplicate_page_block_ref",
                f"Root script/pages.yaml maps block {block_key} to multiple ScriptPages {page_numbers}; split multi-page scenes into non-overlapping block ranges before production or DOCX export.",
                rel_path(pages_path, root),
            )
        )

    return scoped_page_count


def inspect_segment_script_refs(root: Path, issues, strict=False, act_id=None):
    segment_files = sorted(root.glob("acts/**/segments/*/segment.yaml"))
    if act_id:
        segment_files = [path for path in segment_files if path_matches_act(rel_path(path, root), act_id)]
    repeated_refs = defaultdict(list)
    for segment_path in segment_files:
        if yaml is None:
            return 0
        try:
            segment = yaml.safe_load(segment_path.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append(
                issue(
                    "error",
                    "yaml_parse_error",
                    f"Cannot parse segment.yaml: {exc}",
                    rel_path(segment_path, root),
                )
            )
            continue
        if not isinstance(segment, dict):
            continue
        refs = segment.get("script_refs") or []
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if not isinstance(ref, dict):
                continue
            start_id = ref.get("start_block_id")
            end_id = ref.get("end_block_id")
            if not start_id or not end_id:
                continue
            repeated_refs[f"{start_id}->{end_id}"].append(rel_path(segment_path, root))

    repeated_level = "error" if strict else "warning"
    for ref_key, paths in repeated_refs.items():
        if len(paths) <= 1:
            continue
        issues.append(
            issue(
                repeated_level,
                "duplicate_segment_script_ref",
                f"{len(paths)} VideoSegments reuse the same script range {ref_key}; each production Segment should bind to distinct playable screenplay content or a narrower unique block range.",
                paths[0],
            )
        )
    return len(segment_files)


def collect_page_blocks(root: Path, issues, act_id=None):
    pages_path = root / "script" / "pages.yaml"
    if yaml is None or not pages_path.exists():
        return []
    try:
        pages = yaml.safe_load(pages_path.read_text(encoding="utf-8")) or []
    except Exception:
        return []
    if not isinstance(pages, list):
        return []

    block_cache = {}
    page_blocks = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        scoped_refs = []
        for page_ref in page.get("block_refs") or []:
            if isinstance(page_ref, dict) and path_matches_act(page_ref.get("script_path"), act_id):
                scoped_refs.append(page_ref)
        if act_id and not scoped_refs:
            continue
        selected_blocks = []
        for page_ref in scoped_refs:
            if not isinstance(page_ref, dict):
                continue
            script_path = page_ref.get("script_path")
            start_id = page_ref.get("start_block_id")
            end_id = page_ref.get("end_block_id")
            if not script_path or not start_id or not end_id:
                continue

            block_path = root / str(script_path)
            if block_path not in block_cache:
                block_cache[block_path] = load_blocks(block_path, root, issues) if block_path.exists() else []
            blocks = block_cache[block_path]
            block_ids = [block.get("block_id") for block in blocks if isinstance(block, dict)]
            try:
                start_index = block_ids.index(start_id)
                end_index = block_ids.index(end_id)
            except ValueError:
                continue
            if start_index > end_index:
                continue
            selected_blocks.extend(blocks[start_index : end_index + 1])

        page_blocks.append(
            {
                "pageNumber": page.get("page_number"),
                "scriptPageId": page.get("script_page_id"),
                "declaredSec": page.get("estimated_duration_sec"),
                "coverageLevel": page.get("coverage_level"),
                "status": page.get("status"),
                "dialogueException": page_has_dialogue_exception(page),
                "path": rel_path(pages_path, root),
                "blocks": selected_blocks,
            }
        )
    return page_blocks


def compute_page_capacity(root: Path, issues, strict=False, act_id=None):
    page_blocks = collect_page_blocks(root, issues, act_id=act_id)
    fragment_counts = defaultdict(int)
    page_fragments = []

    for page in page_blocks:
        fragments = []
        raw_chars = 0
        block_count = 0
        for block in page["blocks"]:
            if not isinstance(block, dict):
                continue
            block_type = str(block.get("block_type", "")).strip()
            if block_type not in PAGE_CAPACITY_BLOCK_TYPES:
                continue
            block_count += 1
            text = str(block.get("text", "") or "").strip()
            raw_chars += len(text)
            for fragment in split_playable_fragments(text):
                normalized = normalize_text(fragment)
                if len(normalized) >= REPEATED_FRAGMENT_MIN_CHARS:
                    fragment_counts[normalized] += 1
                fragments.append((fragment, normalized))
        page_fragments.append((page, fragments, raw_chars, block_count))

    pages = []
    repeated_fragment_chars = 0
    total_raw_chars = 0
    total_nonrepeated_chars = 0
    under_min_pages = 0
    repeated_samples = {}

    for page, fragments, raw_chars, block_count in page_fragments:
        nonrepeated_chars = 0
        page_repeated_chars = 0
        repeated_fragment_count = 0
        for fragment, normalized in fragments:
            char_count = len(fragment)
            if len(normalized) >= REPEATED_FRAGMENT_MIN_CHARS and fragment_counts[normalized] > 1:
                page_repeated_chars += char_count
                repeated_fragment_count += 1
                repeated_samples.setdefault(normalized, fragment)
            else:
                nonrepeated_chars += char_count

        total_raw_chars += raw_chars
        total_nonrepeated_chars += nonrepeated_chars
        repeated_fragment_chars += page_repeated_chars
        if nonrepeated_chars < MIN_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE:
            under_min_pages += 1
            issues.append(
                issue(
                    "error" if strict else "warning",
                    "page_playable_capacity_underfit",
                    f"ScriptPage {page['pageNumber']} has {nonrepeated_chars} non-repeated playable characters, below the minimum {MIN_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE}. Target range is {TARGET_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE[0]}-{TARGET_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE[1]} per page.",
                    page["path"],
                )
            )

        pages.append(
            {
                "pageNumber": page["pageNumber"],
                "declaredSec": page["declaredSec"],
                "blockCount": block_count,
                "rawPlayableChars": raw_chars,
                "nonRepeatedPlayableChars": nonrepeated_chars,
                "repeatedPlayableChars": page_repeated_chars,
                "repeatedFragments": repeated_fragment_count,
                "estimatedNonRepeatedPlayableSec": round(nonrepeated_chars / MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE * 60),
            }
        )

    for normalized, sample in repeated_samples.items():
        if fragment_counts[normalized] < 3:
            continue
        issues.append(
            issue(
                "error" if strict else "warning",
                "repeated_playable_fragment",
                f"A long playable fragment is repeated {fragment_counts[normalized]} times and is excluded from non-repeated capacity estimates.",
                rel_path(root / "script" / "pages.yaml", root),
                text=sample,
            )
        )

    return {
        "pages": pages,
        "rawPlayableChars": total_raw_chars,
        "nonRepeatedPlayableChars": total_nonrepeated_chars,
        "repeatedPlayableChars": repeated_fragment_chars,
        "underMinPages": under_min_pages,
        "minPageNonRepeatedPlayableChars": min((page["nonRepeatedPlayableChars"] for page in pages), default=0),
        "targetPageNonRepeatedPlayableChars": list(TARGET_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE),
        "estimatedNonRepeatedPlayableMinutes": round(total_nonrepeated_chars / MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE, 3),
    }


def compute_dialogue_readability(root: Path, issues, strict=False, act_id=None):
    page_blocks = collect_page_blocks(root, issues, act_id=act_id)
    pages = []
    totals = {
        "pagesWithDialogue": 0,
        "pagesUnderDialogueMin": 0,
        "singleSpeakerPages": 0,
        "pagesUnderTurnMin": 0,
        "pagesMissingActionInterleave": 0,
    }

    for page in page_blocks:
        dialogue_blocks = []
        speakers = []
        issue_types = []
        dialogue_positions = []
        interleaved = True

        for index, block in enumerate(page["blocks"]):
            if not isinstance(block, dict):
                continue
            block_type = str(block.get("block_type", "")).strip()
            if block_type == "dialogue":
                dialogue_blocks.append(block)
                speakers.append(block_speaker(block))
                dialogue_positions.append(index)

        if len(dialogue_positions) >= 2:
            for left, right in zip(dialogue_positions, dialogue_positions[1:]):
                between = page["blocks"][left + 1 : right]
                has_interleave = any(
                    isinstance(block, dict) and str(block.get("block_type", "")).strip() in DIALOGUE_INTERLEAVE_BLOCK_TYPES
                    for block in between
                )
                if not has_interleave:
                    interleaved = False
                    break

        compressed_speaker_turns = []
        for speaker in speakers:
            if not compressed_speaker_turns or compressed_speaker_turns[-1] != speaker:
                compressed_speaker_turns.append(speaker)

        dialogue_count = len(dialogue_blocks)
        speaker_count = len({speaker for speaker in speakers if speaker})
        speaker_turns = len(compressed_speaker_turns)
        has_exception = page["dialogueException"]
        level = page_issue_level(page, strict)

        if dialogue_count > 0:
            totals["pagesWithDialogue"] += 1

        if dialogue_count == 1 and not has_exception:
            totals["pagesUnderDialogueMin"] += 1
            issue_types.append("page_dialogue_underfit")
            issues.append(
                issue(
                    level,
                    "page_dialogue_underfit",
                    f"ScriptPage {page['pageNumber']} has only 1 dialogue block; interactive pages should default to at least 2 dialogue blocks or record an explicit exception.",
                    page["path"],
                    dialogue_blocks[0],
                    dialogue_blocks[0].get("text", ""),
                )
            )

        if dialogue_count > 0 and speaker_count == 1 and not has_exception:
            totals["singleSpeakerPages"] += 1
            issue_types.append("single_speaker_dialogue_page")
            issues.append(
                issue(
                    level,
                    "single_speaker_dialogue_page",
                    f"ScriptPage {page['pageNumber']} has dialogue from a single speaker; record an explicit monologue/broadcast/system/interrogation/ritual/no-opponent exception or rewrite as interaction.",
                    page["path"],
                    dialogue_blocks[0],
                    dialogue_blocks[0].get("text", ""),
                )
            )

        if dialogue_count >= 2 and speaker_turns < 2 and not has_exception:
            totals["pagesUnderTurnMin"] += 1
            issue_types.append("dialogue_turn_underfit")
            issues.append(
                issue(
                    level,
                    "dialogue_turn_underfit",
                    f"ScriptPage {page['pageNumber']} has {speaker_turns} speaker turn(s); interactive dialogue pages should contain at least 2 speaker turns or record an explicit exception.",
                    page["path"],
                )
            )

        if dialogue_count >= 2 and not interleaved:
            totals["pagesMissingActionInterleave"] += 1
            issue_types.append("dialogue_action_interleave_missing")
            issues.append(
                issue(
                    level,
                    "dialogue_action_interleave_missing",
                    f"ScriptPage {page['pageNumber']} has adjacent dialogue blocks without action, reaction, silence, prop, or sound change between them.",
                    page["path"],
                )
            )

        pages.append(
            {
                "pageNumber": page["pageNumber"],
                "scriptPageId": page["scriptPageId"],
                "declaredSec": page["declaredSec"],
                "coverageLevel": page["coverageLevel"],
                "status": page["status"],
                "dialogueBlocks": dialogue_count,
                "speakerCount": speaker_count,
                "speakerTurns": speaker_turns,
                "hasActionBetweenDialogues": interleaved,
                "hasSingleSpeakerException": has_exception,
                "issueTypes": issue_types,
            }
        )

    return {
        "pages": pages,
        "totals": totals,
    }


def estimate_script_pages_duration_sec(root: Path, act_id=None):
    pages_path = root / "script" / "pages.yaml"
    if yaml is None or not pages_path.exists():
        return 0
    try:
        pages = yaml.safe_load(pages_path.read_text(encoding="utf-8")) or []
    except Exception:
        return 0
    if not isinstance(pages, list):
        return 0
    total = 0
    for page in pages:
        if isinstance(page, dict) and isinstance(page.get("estimated_duration_sec"), (int, float)):
            if act_id:
                refs = page.get("block_refs") or []
                if not any(isinstance(ref, dict) and path_matches_act(ref.get("script_path"), act_id) for ref in refs):
                    continue
            total += page["estimated_duration_sec"]
    return total


def compute_literary_score(totals, issues):
    score = 100
    deductions = []
    warning_count = sum(1 for item in issues if item["level"] == "warning")
    error_count = sum(1 for item in issues if item["level"] == "error")
    issue_type_counts = defaultdict(int)
    for item in issues:
        issue_type_counts[item["type"]] += 1

    if error_count:
        penalty = min(40, error_count * 15)
        score -= penalty
        deductions.append({"reason": "errors", "count": error_count, "points": penalty})
    if warning_count:
        penalty = min(30, warning_count * 4)
        score -= penalty
        deductions.append({"reason": "warnings", "count": warning_count, "points": penalty})

    blocks = max(1, totals.get("blocks", 0))
    dialogues = totals.get("dialogues", 0)
    actions = totals.get("actions", 0)
    if dialogues < 1 or actions < 1:
        score -= 10
        deductions.append({"reason": "missing_action_or_dialogue_balance", "points": 10})
    elif actions / blocks < 0.25 or dialogues / blocks < 0.25:
        score -= 5
        deductions.append({"reason": "weak_action_dialogue_balance", "points": 5})

    if issue_type_counts["creative_note_in_screenplay"]:
        score -= 10
        deductions.append({"reason": "creative_notes_in_screenplay", "count": issue_type_counts["creative_note_in_screenplay"], "points": 10})
    if issue_type_counts["dialogue_looks_like_summary"] or issue_type_counts["dialogue_too_expository"]:
        penalty = min(12, (issue_type_counts["dialogue_looks_like_summary"] + issue_type_counts["dialogue_too_expository"]) * 4)
        score -= penalty
        deductions.append({"reason": "summary_or_expository_dialogue", "points": penalty})
    if issue_type_counts["duplicate_page_block_ref"]:
        score -= 10
        deductions.append({"reason": "duplicate_page_refs", "count": issue_type_counts["duplicate_page_block_ref"], "points": 10})
    if issue_type_counts["page_playable_capacity_underfit"]:
        penalty = min(30, issue_type_counts["page_playable_capacity_underfit"] * 4)
        score -= penalty
        deductions.append({"reason": "page_playable_capacity_underfit", "count": issue_type_counts["page_playable_capacity_underfit"], "points": penalty})
    dialogue_readability_count = (
        issue_type_counts["page_dialogue_underfit"]
        + issue_type_counts["single_speaker_dialogue_page"]
        + issue_type_counts["dialogue_turn_underfit"]
        + issue_type_counts["dialogue_action_interleave_missing"]
    )
    if dialogue_readability_count:
        penalty = min(30, dialogue_readability_count * 4)
        score -= penalty
        deductions.append({"reason": "dialogue_readability_underfit", "count": dialogue_readability_count, "points": penalty})
    if issue_type_counts["unlocalized_screenplay_term"]:
        penalty = min(20, issue_type_counts["unlocalized_screenplay_term"] * 5)
        score -= penalty
        deductions.append({"reason": "unlocalized_screenplay_terms", "count": issue_type_counts["unlocalized_screenplay_term"], "points": penalty})
    if issue_type_counts["templated_screenplay_pattern"] or issue_type_counts["repeated_sentence_skeleton"] or issue_type_counts["synthetic_rewrite_template"]:
        template_count = (
            issue_type_counts["templated_screenplay_pattern"]
            + issue_type_counts["repeated_sentence_skeleton"]
            + issue_type_counts["synthetic_rewrite_template"]
        )
        penalty = min(35, template_count * 5)
        score -= penalty
        deductions.append({"reason": "templated_or_synthetic_rewrite", "count": template_count, "points": penalty})

    score = max(0, min(100, score))
    return {
        "score": score,
        "passingScore": LITERARY_SCORE_PASSING,
        "passed": score >= LITERARY_SCORE_PASSING and error_count == 0,
        "deductions": deductions,
    }


def build_report(film_data_dir: Path, strict=False, act_id=None):
    root = film_data_dir.resolve()
    issues = []
    block_files = collect_blocks_for_scope(root, act_id=act_id)
    totals = {
        "scopeActId": act_id or "all",
        "blockFiles": len(block_files),
        "scriptPages": 0,
        "blocks": 0,
        "screenplayChars": 0,
        "estimatedPlayableMinutes": 0,
        "nonRepeatedPlayableChars": 0,
        "estimatedNonRepeatedPlayableMinutes": 0,
        "minPageNonRepeatedPlayableChars": 0,
        "pagesUnderPlayableMin": 0,
        "pagesWithDialogue": 0,
        "pagesUnderDialogueMin": 0,
        "singleSpeakerDialoguePages": 0,
        "pagesUnderDialogueTurnMin": 0,
        "pagesMissingDialogueInterleave": 0,
        "targetEstimatedMinutes": 0,
        "segmentFiles": 0,
        "actions": 0,
        "dialogues": 0,
        "notes": 0,
        "warnings": 0,
        "errors": 0,
    }
    repeated = defaultdict(list)
    skeleton_repeated = defaultdict(list)

    if not root.exists():
        issues.append(
            issue(
                "error",
                "film_data_dir_missing",
                "film-data directory does not exist.",
                str(film_data_dir),
            )
        )

    if root.exists() and not block_files:
        issues.append(
            issue(
                "error" if strict else "warning",
                "no_screenplay_blocks",
                "No scene script/blocks.yaml files were found under film-data acts tree.",
                str(film_data_dir),
            )
        )

    if root.exists():
        totals["scriptPages"] = inspect_root_script_pages(root, issues, strict=strict, act_id=act_id)
        totals["segmentFiles"] = inspect_segment_script_refs(root, issues, strict=strict, act_id=act_id)
        page_capacity = compute_page_capacity(root, issues, strict=strict, act_id=act_id)
        totals["nonRepeatedPlayableChars"] = page_capacity["nonRepeatedPlayableChars"]
        totals["estimatedNonRepeatedPlayableMinutes"] = page_capacity["estimatedNonRepeatedPlayableMinutes"]
        totals["minPageNonRepeatedPlayableChars"] = page_capacity["minPageNonRepeatedPlayableChars"]
        totals["pagesUnderPlayableMin"] = page_capacity["underMinPages"]
        dialogue_readability = compute_dialogue_readability(root, issues, strict=strict, act_id=act_id)
        totals["pagesWithDialogue"] = dialogue_readability["totals"]["pagesWithDialogue"]
        totals["pagesUnderDialogueMin"] = dialogue_readability["totals"]["pagesUnderDialogueMin"]
        totals["singleSpeakerDialoguePages"] = dialogue_readability["totals"]["singleSpeakerPages"]
        totals["pagesUnderDialogueTurnMin"] = dialogue_readability["totals"]["pagesUnderTurnMin"]
        totals["pagesMissingDialogueInterleave"] = dialogue_readability["totals"]["pagesMissingActionInterleave"]
        target_estimated_sec = estimate_script_pages_duration_sec(root, act_id=act_id)
        totals["targetEstimatedMinutes"] = round(target_estimated_sec / 60, 3) if target_estimated_sec else 0
    else:
        page_capacity = {
            "pages": [],
            "targetPageNonRepeatedPlayableChars": list(TARGET_NONREPEATED_SCREENPLAY_CHARS_PER_PAGE),
        }
        dialogue_readability = {"pages": [], "totals": {}}

    for path in block_files:
        blocks = load_blocks(path, root, issues)
        totals["blocks"] += len(blocks)
        for block in blocks:
            if isinstance(block, dict):
                block_type = str(block.get("block_type", "")).strip()
                if block_type == "action":
                    totals["actions"] += 1
                elif block_type == "dialogue":
                    totals["dialogues"] += 1
                elif block_type == "note":
                    totals["notes"] += 1

                text = normalize_text(block.get("text", ""))
                if block_type in {"scene_heading", "action", "dialogue", "parenthetical", "transition"}:
                    totals["screenplayChars"] += len(str(block.get("text", "") or ""))
                if block_type in {"action", "dialogue"} and len(text) >= 22:
                    repeated[text].append((path, block))
                    skeleton = normalize_sentence_skeleton(block.get("text", ""))
                    if len(skeleton) >= 18:
                        skeleton_repeated[skeleton].append((path, block))

            issues.extend(inspect_block(block, path, root))

    totals["estimatedPlayableMinutes"] = round(totals["screenplayChars"] / MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE, 3)
    if totals["targetEstimatedMinutes"]:
        required_chars = int(totals["targetEstimatedMinutes"] * MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE)
        if totals["screenplayChars"] < required_chars:
            issues.append(
                issue(
                    "error" if strict else "warning",
                    "screenplay_capacity_underfit",
                    f"Screenplay text has {totals['screenplayChars']} characters, below the minimum {required_chars} characters needed to plausibly support {totals['targetEstimatedMinutes']} estimated minutes at {MIN_SCREENPLAY_CHARS_PER_ESTIMATED_MINUTE} chars/minute.",
                    rel_path(root / "script" / "pages.yaml", root),
                )
            )

    for text, occurrences in repeated.items():
        unique_paths = {item[0] for item in occurrences}
        if len(unique_paths) <= 1:
            continue
        sample_path, sample_block = occurrences[0]
        issues.append(
            issue(
                "warning",
                "repeated_screenplay_text",
                f"Same long screenplay text appears in {len(unique_paths)} scene files.",
                rel_path(sample_path, root),
                sample_block,
                text,
            )
        )

    for skeleton, occurrences in skeleton_repeated.items():
        unique_paths = {item[0] for item in occurrences}
        if len(occurrences) < 4 or len(unique_paths) < 2:
            continue
        sample_path, sample_block = occurrences[0]
        issues.append(
            issue(
                "error" if strict else "warning",
                "repeated_sentence_skeleton",
                f"Same screenplay sentence skeleton appears {len(occurrences)} times across {len(unique_paths)} scene files; rewrite as scene-specific action/dialogue instead of variable-filled template.",
                rel_path(sample_path, root),
                sample_block,
                sample_block.get("text", ""),
            )
        )

    motif_counts = defaultdict(int)
    motif_paths = defaultdict(set)
    for path in block_files:
        blocks = load_blocks(path, root, [])
        for block in blocks:
            if not isinstance(block, dict):
                continue
            if str(block.get("block_type", "")).strip() not in {"action", "dialogue"}:
                continue
            text = str(block.get("text", "") or "")
            for motif in MOTIF_TERMS:
                if motif in text:
                    motif_counts[motif] += text.count(motif)
                    motif_paths[motif].add(path)

    for motif, count in motif_counts.items():
        if count < 8 or len(motif_paths[motif]) < 4:
            continue
        sample_path = sorted(motif_paths[motif])[0]
        issues.append(
            issue(
                "warning",
                "motif_may_be_overused",
                f"Motif '{motif}' appears {count} times across {len(motif_paths[motif])} scene files; check progression instead of repetition.",
                rel_path(sample_path, root),
            )
        )

    totals["warnings"] = sum(1 for item in issues if item["level"] == "warning")
    totals["errors"] = sum(1 for item in issues if item["level"] == "error")
    literary_score = compute_literary_score(totals, issues)

    return {
        "ok": totals["errors"] == 0 and literary_score["passed"],
        "filmDataDir": str(root),
        "actId": act_id,
        "totals": totals,
        "pageCapacity": page_capacity,
        "dialogueReadability": dialogue_readability,
        "literaryScore": literary_score,
        "issues": issues,
    }


def print_human(report):
    print(f"Film data: {report['filmDataDir']}")
    if report.get("actId"):
        print(f"Act scope: {report['actId']}")
    print(f"OK: {'yes' if report['ok'] else 'no'}")
    print("metric       count")
    print("-----------  -----")
    for key in [
        "blockFiles",
        "scriptPages",
        "segmentFiles",
        "blocks",
        "screenplayChars",
        "estimatedPlayableMinutes",
        "nonRepeatedPlayableChars",
        "estimatedNonRepeatedPlayableMinutes",
        "minPageNonRepeatedPlayableChars",
        "pagesUnderPlayableMin",
        "pagesWithDialogue",
        "pagesUnderDialogueMin",
        "singleSpeakerDialoguePages",
        "pagesUnderDialogueTurnMin",
        "pagesMissingDialogueInterleave",
        "targetEstimatedMinutes",
        "actions",
        "dialogues",
        "notes",
        "warnings",
        "errors",
    ]:
        print(f"{key:<11}  {report['totals'][key]:>5}")
    literary_score = report.get("literaryScore") or {}
    if literary_score:
        print(f"literaryScore {literary_score.get('score', 0):>5}")
        print(f"passingScore  {literary_score.get('passingScore', LITERARY_SCORE_PASSING):>5}")

    if not report["issues"]:
        return

    print()
    print("Issues:")
    for item in report["issues"]:
        location = item["path"]
        if "blockId" in item:
            location = f"{location}#{item['blockId']}"
        print(f"- [{item['level']}] {item['type']} {location}: {item['message']}")
        if item.get("text"):
            print(f"  text: {item['text']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check local film screenplay block quality.")
    parser.add_argument("--film-data-dir", required=True, help="Path to local film-data directory")
    parser.add_argument("--act-id", help="Optional act scope such as act_002")
    parser.add_argument("--json", action="store_true", help="Print structured JSON")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when errors are found")
    args = parser.parse_args(argv)

    report = build_report(Path(args.film_data_dir), strict=args.strict, act_id=args.act_id)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)

    if args.strict and report["totals"]["errors"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
