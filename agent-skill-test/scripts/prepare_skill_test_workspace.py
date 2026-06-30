#!/usr/bin/env python3
"""Prepare an isolated workspace for CLI agent skill testing."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def read_skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md not found in skill path: {skill_dir}")
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*([A-Za-z0-9-]+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else skill_dir.name


def copy_dir(source: Path, dest: Path, overwrite: bool) -> None:
    if dest.exists():
        if not overwrite:
            raise SystemExit(f"Destination already exists; pass --overwrite: {dest}")
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def copy_input(source: Path, input_root: Path, overwrite: bool) -> None:
    dest = input_root / source.name
    if dest.exists():
        if not overwrite:
            raise SystemExit(f"Input destination already exists; pass --overwrite: {dest}")
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if source.is_dir():
        shutil.copytree(source, dest)
    else:
        shutil.copy2(source, dest)


def native_dirs(workspace: Path, runner: str, native_mirror: str) -> list[Path]:
    if native_mirror == "off":
        return []
    if native_mirror != "auto":
        return [workspace / native_mirror]
    if runner == "codex":
        return [workspace / ".agents" / "skills"]
    if runner == "claude":
        return [workspace / ".claude" / "skills"]
    return []


def prompt_from_arg(value: str | None) -> str:
    if not value:
        return (
            "Use the primary skill copied under skills-under-test/ to complete this test. "
            "Read AGENTS.md first, then write requested artifacts under actual/."
        )
    path = Path(value)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return value


def write_agents_md(workspace: Path, runner: str, primary: str | None, skill_names: list[str], overwrite: bool) -> None:
    path = workspace / "AGENTS.md"
    if path.exists() and not overwrite:
        return
    primary_line = primary or (skill_names[0] if skill_names else "<primary-skill>")
    body = f"""# Agent skill test workspace

## Test Rules

- Runner: `{runner}`.
- Primary skill: `{primary_line}`.
- Read tested skills from `skills-under-test/` first.
- Runner-native skill mirrors may exist, but `skills-under-test/` is the portable source of truth.
- Keep outputs inside this workspace.
- Write task artifacts under `actual/` unless the prompt specifies a different relative path.
- Write runner evidence under `runner-output/`.
"""
    path.write_text(body, encoding="utf-8")


def write_prompt(workspace: Path, prompt_text: str, primary: str | None, skill_names: list[str], overwrite: bool) -> None:
    path = workspace / "prompt.md"
    if path.exists() and not overwrite:
        return
    primary_line = primary or (skill_names[0] if skill_names else "<primary-skill>")
    skill_lines = "\n".join(f"- `skills-under-test/{name}/SKILL.md`" for name in skill_names)
    body = f"""Use the primary skill `{primary_line}` for this isolated CLI-agent test.

Read these skill files before doing the task:

{skill_lines}

## Task

{prompt_text}
"""
    path.write_text(body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare an isolated CLI-agent skill test workspace.")
    parser.add_argument("--workspace", required=True, help="Workspace directory to create or update.")
    parser.add_argument("--runner", choices=["codex", "claude", "opencode", "custom"], default="codex")
    parser.add_argument("--skill", action="append", required=True, help="Skill directory containing SKILL.md. Repeatable.")
    parser.add_argument("--primary-skill", help="Primary skill name. Defaults to the first copied skill.")
    parser.add_argument("--input", action="append", default=[], help="Input file or directory to copy into input/. Repeatable.")
    parser.add_argument("--prompt", help="Prompt text or path to a prompt file.")
    parser.add_argument("--actual-dir", default="actual", help="Relative directory for task artifacts.")
    parser.add_argument("--native-mirror", default="auto", help="auto, off, or a workspace-relative native skill root.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing copied skills/inputs/prompt.")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "input").mkdir(exist_ok=True)
    (workspace / "runner-output").mkdir(exist_ok=True)
    (workspace / args.actual_dir).mkdir(parents=True, exist_ok=True)
    (workspace / "expected").mkdir(exist_ok=True)
    portable_root = workspace / "skills-under-test"
    portable_root.mkdir(exist_ok=True)

    skill_names: list[str] = []
    skill_sources = [Path(item).resolve() for item in args.skill]
    for source in skill_sources:
        if source.name == "SKILL.md":
            source = source.parent
        name = read_skill_name(source)
        skill_names.append(name)
        copy_dir(source, portable_root / name, args.overwrite)

    for mirror_root in native_dirs(workspace, args.runner, args.native_mirror):
        mirror_root.mkdir(parents=True, exist_ok=True)
        for source, name in zip(skill_sources, skill_names):
            if source.name == "SKILL.md":
                source = source.parent
            copy_dir(source, mirror_root / name, args.overwrite)

    for item in args.input:
        source = Path(item).resolve()
        if not source.exists():
            raise SystemExit(f"Input not found: {source}")
        copy_input(source, workspace / "input", args.overwrite)

    primary = args.primary_skill or (skill_names[0] if skill_names else None)
    write_agents_md(workspace, args.runner, primary, skill_names, args.overwrite)
    write_prompt(workspace, prompt_from_arg(args.prompt), primary, skill_names, args.overwrite)

    print(f"workspace={workspace}")
    print(f"skills={','.join(skill_names)}")
    print(f"primary={primary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
