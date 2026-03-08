---
description: Start a development session with memory context loaded
argument-hint: [project]
---

Initialize a development session with full context from Basic Memory.

## Project Selection

1. If $ARGUMENTS names a project, use it
2. Otherwise, run list_memory_projects() and ask which project to use for this session

## Context Loading

Once project is selected, gather context in parallel where possible:

1. **Recent activity**: recent_activity(timeframe="3d", depth=2, project=selected)
2. **Project index**: search_notes(query="Index", project=selected) — read the project's index note
3. **Open issues**: search_notes(query="issue OR bug OR problem OR TODO", project=selected)
4. **Recent decisions**: search_notes(query="decision", project=selected)

## Session Brief

Present a concise development brief:

### Project: [name]
**Last active**: [date from recent activity]

### Recent Changes
- List notes modified in last 3 days with one-line summaries

### Open Items
- Active issues or bugs from notes
- Pending decisions
- TODOs found in notes

### Key Context
- Current architecture decisions in effect
- Known constraints or limitations
- Active patterns being followed

## Session Rules

Remind about active session behavior:
- All memory operations will target the selected project
- The create-memory-note skill will be used for any new notes
- The validate-note hook will check writes automatically
- Use `/remember` to capture insights during the session
- Use `/capture-decision` for architectural decisions

## Ready

End with: "Session initialized for [project]. What are we working on today?"
