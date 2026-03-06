---
title: Self-Referential Relations Anti-Pattern
type: note
permalink: anti-patterns/self-referential-relations-anti-pattern
tags:
- anti-pattern
- relations
- critical
---

# Self-Referential Relations Anti-Pattern

## Rule

**NEVER** create relations where `from_entity` = `to_entity` (note referencing itself).

Creates infinite loops in knowledge graph traversal.

## Examples

❌ **WRONG**: `- implements [[Current Note Title]]`
✅ **CORRECT**: `- implements [[Different Note Title]]`

## Prevention Checklist

Before adding relation:
1. Search for target: `search_notes(query="target", project="current")`
2. Verify target exists in search results
3. **Verify target ≠ current note title**
4. Copy exact title from search results
5. Add relation: `- relation_type [[Exact Target Title]]`

## Detection

Symptom: `recent_activity()` shows `[[Note]] → type → [[Note]]`

## How to Fix

If found:
1. Use `search_notes()` to get exact identifier
2. Use `edit_note(identifier, operation="replace_section", section="## Relations")`
3. Remove self-reference OR convert to observation

**Conversion alternative** (if concept truly self-referential):
```markdown
# Instead of: - implements [[Self]]
- [technique] Implements pattern using structured approach
```

## Observations

- [requirement] ALWAYS verify target ≠ from_entity before creating relation
- [issue] Creates infinite loops in graph traversal
- [technique] Convert self-referential concepts to observations instead

## Relations

- part_of [[Relation Creation Rules]]

#anti-pattern #relations #critical
