---
description: Resume previous work by loading context from Basic Memory
argument-hint: [topic-or-project]
---

Resume a previous work session by building context from Basic Memory.

## Project Resolution

1. If $ARGUMENTS names a known Basic Memory project, use that project
2. If $ARGUMENTS is a topic, search across projects to find where that topic lives
3. If no arguments, run list_memory_projects() and ask: "Which project or topic would you like to continue working on?"

## Context Building

Once the project is identified:

1. **Recent activity**: Run recent_activity(timeframe="7d", depth=2, project=selected) to see what changed recently
2. **Topic search**: If a topic was specified, run search_notes(query=topic, project=selected) to find relevant notes
3. **Graph traversal**: For the most relevant note found, run build_context(url="memory://note-title", depth=2, project=selected) to load connected knowledge

## Context Presentation

Present the loaded context as a structured summary:

### Recent Work
- List recent notes modified (last 7 days)
- Highlight any notes that relate to the requested topic

### Key Context
- Summarize the most relevant notes found
- Include important decisions, open issues, and pending items
- Show relations to other notes (what connects to what)

### Suggested Next Steps
- Based on the loaded context, suggest what to work on next
- Mention any open issues or unresolved items found in notes
- Reference specific notes the user might want to review

## Session Setup

After presenting context:
1. Set the identified project as the active project for this session
2. Ask: "What would you like to focus on?"
