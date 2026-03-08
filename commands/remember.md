---
description: Capture an insight, decision, or pattern to Basic Memory
argument-hint: [title] [folder]
---

Capture knowledge to Basic Memory using the create-memory-note skill.

## Context Gathering

1. If $ARGUMENTS is provided, parse it:
   - First quoted string or first words = note title
   - Optional folder hint (e.g., "insights", "decisions", "technical", "issues")
2. If no arguments, review the current conversation for:
   - Technical decisions made
   - Patterns discovered
   - Problems solved
   - Insights worth preserving
   - Ask the user what they'd like to capture if unclear

## Project Selection

1. Check if a Basic Memory project is already selected for this session
2. If not, run list_memory_projects() and ask which project to use
3. Search the selected project for existing notes on this topic to avoid duplicates

## Note Creation

Use the create-memory-note skill to create the note with full rule enforcement:
- Title: Specific and searchable (never generic like "Notes" or "Session")
- Observations: 3-5 with specific categories (decision, technique, issue, fact, best-practice, requirement)
- Relations: 2-3 minimum, verified against existing notes
- Tags: 3-5 relevant, lowercase hyphenated
- Folder: Use the provided folder hint, or choose appropriate one (insights/, decisions/, technical/, issues/, sessions/)

## Development Context

When capturing from a development conversation, prefer these observation categories:
- [decision] for architectural or design choices
- [technique] for coding patterns or approaches
- [issue] for bugs, problems, or limitations discovered
- [requirement] for constraints or specifications
- [best-practice] for reusable standards

## Post-Creation

After creating the note:
1. Confirm what was saved with a brief summary
2. Mention any unresolved WikiLinks (forward references are OK)
3. Suggest related notes the user might want to update
