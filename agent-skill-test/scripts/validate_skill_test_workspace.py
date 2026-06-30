#!/usr/bin/env python3
"""Generic validation for isolated CLI-agent skill test workspaces."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


class ValidationError(Exception):
    pass


def parse_glob_regex(value: str) -> tuple[str, str]:
    if "::" not in value:
        raise ValidationError(f"Expected '<glob>::<regex>': {value}")
    glob_part, regex = value.split("::", 1)
    if not glob_part or not regex:
        raise ValidationError(f"Expected non-empty glob and regex: {value}")
    return glob_part, regex


def skill_exists(workspace: Path, name: str) -> bool:
    candidates = [
        workspace / "skills-under-test" / name / "SKILL.md",
        workspace / ".agents" / "skills" / name / "SKILL.md",
        workspace / ".claude" / "skills" / name / "SKILL.md",
    ]
    return any(path.exists() for path in candidates)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate_required_pattern(workspace: Path, spec: str) -> list[str]:
    glob_part, regex = parse_glob_regex(spec)
    paths = [path for path in workspace.glob(glob_part) if path.is_file()]
    if not paths:
        raise ValidationError(f"No files matched required pattern glob: {glob_part}")
    matched: list[str] = []
    pattern = re.compile(regex, re.MULTILINE)
    for path in paths:
        if pattern.search(read_text(path)):
            matched.append(str(path.relative_to(workspace)))
    if not matched:
        raise ValidationError(f"Required regex not found: {spec}")
    return matched


def validate_forbidden_pattern(workspace: Path, spec: str) -> list[str]:
    glob_part, regex = parse_glob_regex(spec)
    paths = [path for path in workspace.glob(glob_part) if path.is_file()]
    pattern = re.compile(regex, re.MULTILINE)
    matched: list[str] = []
    for path in paths:
        if pattern.search(read_text(path)):
            matched.append(str(path.relative_to(workspace)))
    if matched:
        raise ValidationError(f"Forbidden regex matched {len(matched)} file(s): {spec} -> {matched}")
    return matched


def validate_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ValidationError(f"Invalid JSON: {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a CLI-agent skill test workspace with generic rules.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--required-skill", action="append", default=[])
    parser.add_argument("--required-file", action="append", default=[])
    parser.add_argument("--required-pattern", action="append", default=[], help="'<glob>::<regex>', repeatable.")
    parser.add_argument("--forbidden-path", action="append", default=[])
    parser.add_argument("--forbidden-pattern", action="append", default=[], help="'<glob>::<regex>', repeatable.")
    parser.add_argument("--json-file", action="append", default=[], help="Workspace-relative JSON file to parse.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.exists():
        raise SystemExit(f"Workspace not found: {workspace}")

    checks = 0
    try:
        for name in args.required_skill:
            checks += 1
            if not skill_exists(workspace, name):
                raise ValidationError(f"Required skill not found in portable or native mirrors: {name}")

        for rel in args.required_file:
            checks += 1
            path = workspace / rel
            if not path.exists():
                raise ValidationError(f"Required file not found: {rel}")
            if path.suffix.lower() == ".json":
                validate_json(path)

        for rel in args.json_file:
            checks += 1
            path = workspace / rel
            if not path.exists():
                raise ValidationError(f"JSON file not found: {rel}")
            validate_json(path)

        for spec in args.required_pattern:
            checks += 1
            matched = validate_required_pattern(workspace, spec)
            print(f"required-pattern ok: {spec} -> {matched}")

        for rel in args.forbidden_path:
            checks += 1
            if (workspace / rel).exists():
                raise ValidationError(f"Forbidden path exists: {rel}")

        for spec in args.forbidden_pattern:
            checks += 1
            validate_forbidden_pattern(workspace, spec)

    except ValidationError as exc:
        print(f"FAIL: {exc}")
        return 1

    print(f"ok: {checks} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
