#!/usr/bin/env python3
"""Extract a final assistant message from runner output."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def text_from_json_event(event: dict[str, Any]) -> str | None:
    if event.get("type") == "item.completed":
        item = event.get("item")
        if isinstance(item, dict) and item.get("type") == "agent_message":
            text = item.get("text")
            return text if isinstance(text, str) else None
    if event.get("type") in {"result", "assistant", "message"}:
        for key in ("result", "text", "content", "message"):
            value = event.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, dict):
                nested = value.get("text") or value.get("content")
                if isinstance(nested, str):
                    return nested
    if event.get("type") == "text":
        part = event.get("part")
        if isinstance(part, dict) and part.get("type") == "text":
            text = part.get("text")
            return text if isinstance(text, str) else None
    return None


def extract_from_jsonl(path: Path) -> tuple[str, str]:
    last: str | None = None
    parsed = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        parsed += 1
        if isinstance(event, dict):
            text = text_from_json_event(event)
            if text:
                last = text
    if last:
        return last, f"extracted from {parsed} json events"
    return "", f"no final message found in {parsed} json events"


def extract_tail(path: Path, max_chars: int) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[-max_chars:], f"tail fallback: last {max_chars} characters"
    return text, "tail fallback: full file"


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract final message from JSONL or transcript output.")
    parser.add_argument("--events-jsonl", help="JSONL event file, such as Codex --json output.")
    parser.add_argument("--transcript", help="Plain transcript/stdout file.")
    parser.add_argument("--output", required=True, help="Output final message path.")
    parser.add_argument("--tail-chars", type=int, default=12000)
    args = parser.parse_args()

    if not args.events_jsonl and not args.transcript:
        raise SystemExit("Pass --events-jsonl or --transcript")

    message = ""
    note = ""
    if args.events_jsonl:
        message, note = extract_from_jsonl(Path(args.events_jsonl))
    if not message and args.transcript:
        message, note = extract_tail(Path(args.transcript), args.tail_chars)

    if not message:
        raise SystemExit(note or "No final message found")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(message, encoding="utf-8")
    print(note)
    print(f"output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
