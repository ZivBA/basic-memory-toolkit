---
title: Relation Creation Rules
type: note
permalink: creating-notes/relation-creation-rules
tags:
- creating-notes
- relations
- verification
- quality
---

# Relation Creation Rules

## Core Principle

**Always verify before creating relations.** Never assume a target exists.

## Verification Workflow

Before adding ANY relation:

1. **Search for target**
   ```
   search_notes(query="target title", project="current-project")
   ```

2. **Verify target exists** in search results

3. **Copy exact title** from search results (don't type manually)

4. **Verify not self-referential**
   - Target title ≠ Current note title
   - See [[Self-Referential Relations Anti-Pattern]]

5. **Verify same project** (or use text format)
   - Same project → WikiLink `[[Target Title]]`
   - Different project → Text `"Target Title" (project-name)`
   - See [[Cross-Project WikiLinks Anti-Pattern]]

6. **Choose specific relation type**

## Relation Types

Use the most specific type available:

| Type | Use When |
|------|----------|
| `implements` | Note implements a specification/pattern |
| `requires` | Note depends on another note |
| `part_of` | Note is a component of larger entity |
| `extends` | Note builds upon/enhances another |
| `contrasts_with` | Note presents alternative to another |
| `inspired_by` | Note was influenced by another |
| `relates_to` | **LAST RESORT** - only when no specific type fits |

## Forward References

Forward references (to notes that don't exist yet) are **allowed** if:
- Target is planned and will be created
- Target title is specific and intentional
- Target is NOT the current note

Forward references auto-resolve when target is created.

## Minimum Relations

Each note should have **2-3 relations minimum** to maintain knowledge graph connectivity.

## Observations

- [requirement] Always search and verify before creating relations
- [technique] Copy exact title from search results
- [requirement] Use specific relation types over generic relates_to
- [best-practice] Maintain 2-3 relations minimum per note

## Relations

- extends [[Self-Referential Relations Anti-Pattern]]
- extends [[Cross-Project WikiLinks Anti-Pattern]]
- part_of [[New Note Checklist]]

#creating-notes #relations #verification #quality
