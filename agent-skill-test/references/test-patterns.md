# Test Patterns

## Smoke Test

Use when checking whether a skill can be loaded and complete a small representative task.

- Keep inputs small.
- Require one or two concrete output files.
- Validate final message and key file patterns.

## Regression Test

Use when a previous bug or behavior must not regress.

- Preserve the original input artifact.
- Encode the old failure as a required or forbidden validation rule.
- Capture full runner output for later comparison.

## Multi-Skill Coordination Test

Use when a primary skill depends on supporting skills.

- Mark exactly one primary skill.
- Copy every skill to `skills-under-test/`.
- Mirror all skills into the runner-native directory when available.
- Prompt the runner to read the primary skill first and supporting skills only for their bounded roles.

## Golden Output Test

Use when the result must match a known shape.

- Put expected artifacts under `expected/`.
- Validate stable structure with regex or JSON checks.
- Avoid exact full-text comparison for LLM-authored prose unless the runner is deterministic enough.

## Forbidden Artifact Test

Use when a skill must avoid side effects.

- Use `--forbidden-path` for directories or files that must not exist.
- Use `--forbidden-pattern` only for produced artifacts, not prompts or instructions.
- Avoid writing forbidden terms into generated quality notes, or the grep check will report a false failure.
