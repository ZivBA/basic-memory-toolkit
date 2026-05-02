---
title: Session Artifact
type: schema
entity: session-artifact
version: 1
schema:
  title: string, descriptive session title with date
  session_date: string, date of the session (YYYY-MM-DD)
  accomplishments?(array): string, what was completed
  issues_encountered?(array): string, problems hit during session
  next_steps?(array): string, planned follow-up work
  associated_projects?(array): string, projects worked on
settings:
  validation: warn
---

# Session Artifact Schema

Schema for structured work session summaries that capture accomplishments, blockers, and next steps.

## Usage

Create notes with `type: session-artifact` to document development sessions with structured fields.

## Title Convention

Use format: "[Topic] Session - [Date or Milestone]"
Example: "Plugin Enhancement Session - Phase 1 Complete"

## Example Note

```markdown
---
title: Plugin Enhancement Session - Phase 1 Complete
type: session-artifact
---

# Plugin Enhancement Session - Phase 1 Complete

- session_date: 2026-03-07
- accomplishments: Implemented hook_validator.py, Created 6 CLI validators, Updated hooks.json with PreToolUse/PostToolUse
- issues_encountered: CLI overhead 350x slower than estimated, MCP config corruption during project creation
- next_steps: Phase 2 slash commands, Phase 3 skill enhancements
- associated_projects: basic-memory-toolkit

## Observations

- [fact] Phase 1 validation infrastructure complete with two-tier architecture #milestone
- [issue] MCP config corruption required filesystem workaround #mcp #bug
- [decision] Pivoted from single-tier to two-tier validation after performance discovery #architecture

## Relations

- documents [[Basic Memory Toolkit Index]]
- follows [[Validation Architecture Decision]]
```

## Observation Categories

Prefer: `[fact]`, `[issue]`, `[decision]`, `[technique]`
