# CueLight Agent Skills

A collection of skills for AI coding agents working on CueLight workflows.

Skills are packaged instructions and references that extend agent capabilities. This repository follows the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### cuelight-drama

Drama production workflow guidance for CueLight and AI Drama Factory.

Helps agents work through CueLight drama production via CLI-first workflows, including project inspection, text asset editing, storyboard design, video generation, and export handoff.

**Use when:**
- Building or operating CueLight drama production workflows
- Working in director-mode tasks such as visual setup, casting, storyboard design, or video generation
- Driving project progress through `@cuelight/cli`
- Continuing an existing drama project instead of restarting from scratch

## Installation

```bash
npx skills add cuelight/agent-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**

```text
Help me continue this CueLight drama project
```

```text
Generate storyboards for this episode and tell me the CLI commands
```

```text
Walk me through director mode for visual setup and video production
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `references/` - Supporting documentation loaded as needed
- `scripts/` - Helper scripts for automation when needed
