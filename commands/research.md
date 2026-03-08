---
description: Research a topic across Basic Memory projects
argument-hint: <topic> [project]
---

Perform structured research on a topic across Basic Memory projects.

## Input Parsing

1. $ARGUMENTS contains the topic and optional project restriction
2. If a project name is mentioned, restrict search to that project
3. If no project specified, search across all projects

## Research Workflow

### Phase 1: Discovery

Use the cross-project-search skill to find all notes related to the topic:

1. Run search_notes(query=topic) across relevant projects
2. For each result, note the project, title, and relevance
3. Group results by project

### Phase 2: Deep Reading

For the top 3-5 most relevant notes:
1. Run read_note() to get full content
2. Extract key observations, decisions, and relations
3. Follow important WikiLinks via build_context() for additional context

### Phase 3: Synthesis

Present findings as a structured research report:

**Topic**: [topic]
**Sources**: [count] notes across [count] projects

**Key Findings**:
- Bullet points of the most important information
- Include which note/project each finding came from

**Decisions Made**:
- Any recorded decisions related to this topic

**Open Questions**:
- Unresolved items or gaps in knowledge

**Related Topics**:
- Connected areas worth exploring further
- WikiLink references to follow

### Phase 4: Gap Analysis

Identify what's missing:
- Are there topics mentioned but not documented?
- Are there forward references (WikiLinks) that haven't been created yet?
- Would a new note help consolidate scattered information?

## Follow-Up

Ask: "Would you like me to:
1. Create a summary note capturing these findings?
2. Dive deeper into any specific finding?
3. Fill any knowledge gaps identified?"
