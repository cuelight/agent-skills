# Example: CueLight Shortdrama Skill Smoke

This example is only for CueLight shortdrama tests. Do not load it for generic skill tests.

## Test Shape

- Runner: Codex
- Workspace: `sample-script/test-02-shortdrama`
- Primary skill: `cuelight-shortdrama`
- Supporting skill: `cuelight-drama`
- Input: `test-data/test-02.txt`
- Goal: produce first three shortdrama episode script bodies

## Important Lessons

- Copy skills to `.agents/skills/` for Codex native discovery.
- Also keep a portable copy when using the generic harness.
- Use `-c approval_policy='never'` for `codex exec` when `--ask-for-approval` is not accepted.
- Use an absolute `-o` path for final message output.
- If `-o` fails but JSONL is complete, extract the last agent message from `events.jsonl`.
- Avoid forbidden-word false positives in canonical artifacts.

## Representative Validation

```powershell
python agent-skills/agent-skill-test/scripts/validate_skill_test_workspace.py `
  --workspace sample-script/test-02-shortdrama `
  --required-skill cuelight-shortdrama `
  --required-skill cuelight-drama `
  --required-file cuelight-projects/shortdrama/test-02-shortdrama/manifest.json `
  --required-file cuelight-projects/shortdrama/test-02-shortdrama/episodes/ep-001.md `
  --required-pattern "cuelight-projects/shortdrama/test-02-shortdrama/episodes/ep-*.md::## 剧本正文" `
  --required-pattern "cuelight-projects/shortdrama/test-02-shortdrama/episodes/ep-*.md::```fountain" `
  --forbidden-path .cuelight
```
