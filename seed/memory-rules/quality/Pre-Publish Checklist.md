---
title: Pre-Publish Checklist
type: note
permalink: quality/pre-publish-checklist
tags:
- quality
- checklist
- verification
- workflow
---

# Pre-Publish Checklist

## Purpose

**Final verification before `write_note()` or `edit_note()`.** Catch issues before they enter the knowledge base.

## Quick Checklist

Run through before every note creation/update:

### Title & Metadata
- [ ] Title is specific and searchable
- [ ] Title follows template for note type
- [ ] 3-5 relevant tags included
- [ ] Correct project selected
- [ ] Appropriate folder selected

### Content
- [ ] 3-5 observations with specific categories
- [ ] No duplicate content (searched first)
- [ ] Note length reasonable (< 1500 lines)

### Relations
- [ ] 2-3 relations minimum
- [ ] Each target searched and verified to exist
- [ ] No self-referential relations (target ≠ current note)
- [ ] No cross-project WikiLinks (use text format instead)
- [ ] Specific relation types used (not generic `relates_to`)

## Common Mistakes

| Mistake | Prevention |
|---------|------------|
| Self-referential relation | Always verify target ≠ current title |
| Cross-project WikiLink | Check target is in same project |
| Generic title | Use title templates |
| Missing observations | Add 3-5 before saving |
| Broken WikiLink | Search and copy exact title |

## Verification Commands

```python
# Search for target before creating relation
search_notes(query="target title", project="current")

# Check for duplicates before creating note
search_notes(query="topic keywords", project="current")

# Verify after creation
read_note(identifier="new-note-title", project="current")
```

## If Issues Found

- **Self-referential**: Remove or convert to observation
- **Cross-project WikiLink**: Convert to text format
- **Missing observations**: Add before saving
- **Duplicate content**: Consider consolidating instead

## Observations

- [checklist] Run full checklist before every write_note()
- [requirement] Verify all relations before publishing
- [technique] Search to verify targets exist before WikiLinks

## Relations

- requires [[New Note Checklist]]
- requires [[Relation Creation Rules]]
- requires [[Observation Standards]]

#quality #checklist #verification #workflow
