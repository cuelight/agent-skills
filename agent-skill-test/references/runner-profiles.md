# Runner Profiles

Use these profiles as starting points. Always check the local runner with `--help` when exact flags matter.

## Portable Skill Copy

Every runner test should include:

```text
skills-under-test/<skill-name>/SKILL.md
```

The prompt should explicitly tell the runner to read the primary skill from that path. Native mirrors are optional acceleration paths, not the source of truth.

## Codex

Native mirror:

```text
.agents/skills/<skill-name>/
```

Recommended PowerShell command:

```powershell
$root = (Resolve-Path "<workspace>").Path
$prompt = Join-Path $root "prompt.md"
$events = Join-Path $root "runner-output/events.jsonl"
$final = Join-Path $root "runner-output/final.md"
Get-Content $prompt -Raw | codex exec --cd $root --sandbox workspace-write -c approval_policy='never' --json -o $final - > $events
```

Notes:

- Some `codex exec` versions do not expose `--ask-for-approval`; use `-c approval_policy='never'`.
- Use an absolute `-o` path. Relative `-o` may resolve from the caller directory instead of `--cd`.
- JSONL events are usually the best evidence artifact.

## Claude Code

Native mirror:

```text
.claude/skills/<skill-name>/
```

Recommended PowerShell command:

```powershell
$root = (Resolve-Path "<workspace>").Path
$prompt = Join-Path $root "prompt.md"
$stdout = Join-Path $root "runner-output/stdout.txt"
$stderr = Join-Path $root "runner-output/stderr.txt"
Get-Content $prompt -Raw | claude -p --permission-mode dontAsk --output-format stream-json --include-partial-messages > $stdout 2> $stderr
```

Notes:

- `claude -p` is the non-interactive mode.
- Use `--permission-mode dontAsk` for unattended local tests only in trusted workspaces.
- Claude supports `.claude/skills/`, but portable `skills-under-test/` should still be present.

## OpenCode

Native mirror: none assumed.

Recommended PowerShell command:

```powershell
$root = (Resolve-Path "<workspace>").Path
$prompt = Join-Path $root "prompt.md"
$events = Join-Path $root "runner-output/events.jsonl"
$stderr = Join-Path $root "runner-output/stderr.txt"
opencode run --format json --file $prompt "Read prompt.md and complete the requested skill test in this workspace." > $events 2> $stderr
```

Notes:

- OpenCode supports `opencode run` and `--format json`.
- Do not assume OpenAI-style skill discovery. Prompt it to read `skills-under-test/<skill-name>/SKILL.md`.

## Custom Runner

Use a command template and keep these invariants:

- Set the working directory to the test workspace.
- Pass or pipe `prompt.md`.
- Capture stdout/stderr or event streams under `runner-output/`.
- Preserve `skills-under-test/` and any runner-native mirror for inspection.
