#!/usr/bin/env python3
"""Print a suggested command for running a prepared skill test workspace."""

from __future__ import annotations

import argparse
from pathlib import Path


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def powershell_command(runner: str, workspace: Path, prompt: str, final: str, events: str, stdout: str, stderr: str) -> str:
    root = str(workspace.resolve())
    lines = [
        f"$root = (Resolve-Path {ps_quote(root)}).Path",
        f"$prompt = Join-Path $root {ps_quote(prompt)}",
    ]
    if runner == "codex":
        lines.extend(
            [
                f"$events = Join-Path $root {ps_quote(events)}",
                f"$final = Join-Path $root {ps_quote(final)}",
                "Get-Content $prompt -Raw | codex exec --cd $root --sandbox workspace-write -c approval_policy='never' --json -o $final - > $events",
            ]
        )
    elif runner == "claude":
        lines.extend(
            [
                f"$stdout = Join-Path $root {ps_quote(stdout)}",
                f"$stderr = Join-Path $root {ps_quote(stderr)}",
                "Push-Location $root",
                "try {",
                "  Get-Content $prompt -Raw | claude -p --permission-mode bypassPermissions --output-format stream-json --include-partial-messages --verbose > $stdout 2> $stderr",
                "} finally {",
                "  Pop-Location",
                "}",
            ]
        )
    elif runner == "opencode":
        lines.extend(
            [
                f"$events = Join-Path $root {ps_quote(events)}",
                f"$stderr = Join-Path $root {ps_quote(stderr)}",
                "opencode run 'Read prompt.md and complete the requested skill test in this workspace.' --format json --dir $root --dangerously-skip-permissions --file $prompt > $events 2> $stderr",
            ]
        )
    else:
        lines.extend(
            [
                f"$stdout = Join-Path $root {ps_quote(stdout)}",
                f"$stderr = Join-Path $root {ps_quote(stderr)}",
                "Get-Content $prompt -Raw | <agent-command> > $stdout 2> $stderr",
            ]
        )
    return "\n".join(lines)


def bash_command(runner: str, workspace: Path, prompt: str, final: str, events: str, stdout: str, stderr: str) -> str:
    root = str(workspace.resolve()).replace("\\", "/")
    if runner == "codex":
        return (
            f"root='{root}'\n"
            f"cat \"$root/{prompt}\" | codex exec --cd \"$root\" --sandbox workspace-write "
            f"-c approval_policy='never' --json -o \"$root/{final}\" - > \"$root/{events}\""
        )
    if runner == "claude":
        return (
            f"root='{root}'\n"
            f"(cd \"$root\" && cat \"{prompt}\" | claude -p --permission-mode bypassPermissions "
            f"--output-format stream-json --include-partial-messages --verbose > \"{stdout}\" 2> \"{stderr}\")"
        )
    if runner == "opencode":
        return (
            f"root='{root}'\n"
            f"opencode run 'Read prompt.md and complete the requested skill test in this workspace.' "
            f"--format json --dir \"$root\" --dangerously-skip-permissions --file \"$root/{prompt}\" "
            f"> \"$root/{events}\" 2> \"$root/{stderr}\""
        )
    return f"root='{root}'\ncat \"$root/{prompt}\" | <agent-command> > \"$root/{stdout}\" 2> \"$root/{stderr}\""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a suggested CLI runner command for a skill test workspace.")
    parser.add_argument("--runner", choices=["codex", "claude", "opencode", "custom"], required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--shell", choices=["powershell", "bash"], default="powershell")
    parser.add_argument("--prompt", default="prompt.md")
    parser.add_argument("--final", default="runner-output/final.md")
    parser.add_argument("--events", default="runner-output/events.jsonl")
    parser.add_argument("--stdout", default="runner-output/stdout.txt")
    parser.add_argument("--stderr", default="runner-output/stderr.txt")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if args.shell == "powershell":
        print(powershell_command(args.runner, workspace, args.prompt, args.final, args.events, args.stdout, args.stderr))
    else:
        print(bash_command(args.runner, workspace, args.prompt, args.final, args.events, args.stdout, args.stderr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
