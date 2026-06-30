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
Push-Location $root
try {
  Get-Content $prompt -Raw | claude -p --permission-mode bypassPermissions --output-format stream-json --include-partial-messages --verbose > $stdout 2> $stderr
} finally {
  Pop-Location
}
```

Notes:

- `claude -p` is the non-interactive mode.
- Use `--permission-mode bypassPermissions` only for isolated trusted test workspaces that need file writes.
- Recent Claude CLI versions require `--verbose` with `--output-format stream-json`.
- Run Claude from the test workspace directory so relative file writes stay inside the isolated workspace.
- Claude supports `.claude/skills/`, but portable `skills-under-test/` should still be present.
- To make the evidence easier to inspect, extract the final message after the run:

```powershell
python agent-skills/agent-skill-test/scripts/extract_final_message.py `
  --events-jsonl <workspace>/runner-output/stdout.txt `
  --output <workspace>/runner-output/final.md
```

## OpenCode

Native mirror: none assumed.

Recommended PowerShell command:

```powershell
$root = (Resolve-Path "<workspace>").Path
$prompt = Join-Path $root "prompt.md"
$events = Join-Path $root "runner-output/events.jsonl"
$stderr = Join-Path $root "runner-output/stderr.txt"
opencode run "Read prompt.md and complete the requested skill test in this workspace." --format json --dir $root --dangerously-skip-permissions --file $prompt > $events 2> $stderr
```

Notes:

- OpenCode supports `opencode run`, `--format json`, `--file`, and `--dir`.
- Put the message before `--file`; some OpenCode/CueLight Agent builds parse `--file` as an array and will treat following positional text as another file.
- Use `--dangerously-skip-permissions` only for isolated trusted test workspaces that need file writes.
- Do not assume OpenAI-style skill discovery. Prompt it to read `skills-under-test/<skill-name>/SKILL.md`.
- If the global `opencode` bin is unavailable, record the test as environment-blocked instead of substituting a local fork.
- Extract the final message after the run:

```powershell
python agent-skills/agent-skill-test/scripts/extract_final_message.py `
  --events-jsonl <workspace>/runner-output/events.jsonl `
  --output <workspace>/runner-output/final.md
```

## Custom Runner

Use a command template and keep these invariants:

- Set the working directory to the test workspace.
- Pass or pipe `prompt.md`.
- Capture stdout/stderr or event streams under `runner-output/`.
- Preserve `skills-under-test/` and any runner-native mirror for inspection.
