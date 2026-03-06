---
title: Cross-Project WikiLinks Anti-Pattern
type: note
permalink: anti-patterns/cross-project-wiki-links-anti-pattern
tags:
- anti-pattern
- wikilinks
- cross-project
---

# Cross-Project WikiLinks Anti-Pattern

## Rule

**WikiLinks only work within the same project.** They do NOT cross project boundaries.

For cross-project references, use **text format** instead.

## Examples

❌ **WRONG** - WikiLink to different project:
```markdown
# In edifact-pipeline project
- relates_to [[Exception Chaining Pattern]]  # Target in development-practices
```

✅ **CORRECT** - Text reference format:
```markdown
**Cross-Project References**:
- Builds on: "Exception Chaining Pattern" (development-practices)
```

## Prevention Checklist

Before creating WikiLink:
1. Verify target is in **same project** as current note
2. If different project → Use text format `"Note Title" (project-name)`
3. If same project → Search to verify target exists, then use WikiLink

## How to Fix

If cross-project WikiLinks found:
1. Search target project to get exact title
2. Convert to text format: `"Exact Note Title" (target-project)`
3. Update note with `edit_note()`

## Quick Reference

| Situation | Format |
|-----------|--------|
| Same project | `[[Note Title]]` |
| Different project | `"Note Title" (project-name)` |

## Observations

- [requirement] WikiLinks ONLY work within same project
- [technique] Use text format "Title" (project) for cross-project references
- [issue] Cross-project WikiLinks remain unresolved indefinitely

## Relations

- part_of [[Relation Creation Rules]]

#anti-pattern #wikilinks #cross-project
