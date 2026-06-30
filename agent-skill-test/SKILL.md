---
name: agent-skill-test
description: Build and validate isolated CLI-agent test workspaces for one or more skills. Use when testing agent skills with Codex, Claude Code, OpenCode, or another command-line agent; preparing portable skill copies; mirroring skills into runner-specific discovery directories; generating runner commands; capturing transcripts/events; extracting final messages; or validating produced files with generic required/forbidden checks.
---

# Agent Skill Test

Use this skill to test one or more skills with a CLI agent in an isolated working directory. Keep the workflow runner-neutral: the test subject is the skill behavior, not a product-specific project flow.

## Core Model

Create a self-contained workspace with:

```text
<workspace>/
  AGENTS.md or runner equivalent guidance
  prompt.md
  input/
  skills-under-test/<skill-name>/SKILL.md
  runner-output/
    events.jsonl or transcript.txt
    stdout.txt
    stderr.txt
    final.md
  actual/
  expected/
```

Always copy each tested skill to `skills-under-test/<skill-name>/`. This portable copy is the cross-runner source of truth. Add runner-native mirrors only when useful:

- Codex: `.agents/skills/<skill-name>/`
- Claude Code: `.claude/skills/<skill-name>/`
- OpenCode: no native skill directory is assumed by default
- Custom runner: use an explicit native mirror path only when the runner documentation or user provides one

## Workflow

1. **Define the test target**
   - Record runner, workspace, primary skill, supporting skills, inputs, task prompt, expected artifacts, and forbidden artifacts.
   - Keep business-specific acceptance criteria outside this skill; pass them as validation rules.

2. **Prepare the workspace**
   - Use `scripts/prepare_skill_test_workspace.py` to copy skills and inputs and generate `AGENTS.md`, `prompt.md`, `runner-output/`, `actual/`, and `expected/`.
   - Set `--primary-skill` when testing multiple skills so the prompt names the lead skill and support boundaries.
   - Prefer `--native-mirror auto` unless the runner cannot use native skill discovery or the test must be portable-only.

3. **Build the runner command**
   - Use `scripts/build_runner_command.py` for a suggested command.
   - For Codex, prefer `codex exec --cd <workspace> --sandbox workspace-write -c approval_policy='never' --json -o <absolute-final> -`.
   - For Claude Code and OpenCode, read `references/runner-profiles.md` and confirm the local `--help` output when exact flags matter.

4. **Run and capture evidence**
   - Store structured events or transcript in `runner-output/`.
   - Store the final answer in `runner-output/final.md`.
   - If a runner fails to write the final file but stdout/events are intact, use `scripts/extract_final_message.py`.

5. **Validate generically**
   - Use `scripts/validate_skill_test_workspace.py`.
   - Validate files, regex patterns, JSON parseability, skill copies, and forbidden paths/patterns.
   - Avoid writing explanatory forbidden words into the produced artifacts when a validation rule greps for those words.

## References

- Read `references/runner-profiles.md` when choosing Codex, Claude Code, OpenCode, or custom runner commands.
- Read `references/test-patterns.md` when designing smoke, regression, multi-skill, golden-output, or forbidden-artifact checks.
- Read `references/examples-cuelight-shortdrama.md` only when adapting the CueLight shortdrama sample experience.

## Guardrails

- Do not assume every runner supports OpenAI-style skill discovery.
- Do not treat `agent-skills/` as a runner discovery directory; it is usually a source directory, not a test workspace mirror.
- Do not let runner-specific convenience replace the portable `skills-under-test/` copy.
- Do not hard-code domain-specific artifact names in the generic scripts.
- Prefer absolute paths in generated commands when redirecting final messages or event logs.
