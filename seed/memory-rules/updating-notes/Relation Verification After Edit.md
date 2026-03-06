---
title: Relation Verification After Edit
type: note
permalink: updating-notes/relation-verification-after-edit
tags:
- updating-notes
- relations
- verification
- quality
---

# Relation Verification After Edit

## When to Verify

Run verification after any edit that touches relations:
- Adding new relations
- Modifying existing relations
- Using `replace_section` on Relations section
- Major content restructure

## Verification Workflow

### After Adding Relations

1. **Read the updated note**
   ```python
   read_note(identifier="note-title", project="current")
   ```

2. **Check for self-referential relations**
   - Scan Relations section
   - Ensure no `[[Current Note Title]]` references

3. **Check for cross-project WikiLinks**
   - All WikiLink targets should be in same project
   - Convert cross-project refs to text format

4. **Verify relation types**
   - Using specific types (implements, requires, part_of)
   - Not overusing generic `relates_to`

### Quick Verification Checklist

After editing relations:
- [ ] No self-references (target ≠ current note)
- [ ] No cross-project WikiLinks
- [ ] Specific relation types used
- [ ] Targets exist (or are intentional forward refs)

## Common Issues After Edit

| Issue | Detection | Fix |
|-------|-----------|-----|
| Self-referential | Target = current title | Remove or convert to observation |
| Cross-project WikiLink | Target in different project | Convert to text format |
| Broken WikiLink | Target doesn't exist | Search for correct title |
| Generic relation | Using `relates_to` | Change to specific type |

## When to Skip Verification

- Edits that don't touch Relations section
- Simple text corrections
- Appending non-relation content

## Observations

- [requirement] Verify relations after any edit touching Relations section
- [technique] Read note after edit to confirm changes
- [checklist] Check self-refs, cross-project, and relation types

## Relations

- part_of [[Edit vs Rewrite Decision]]
- extends [[Relation Creation Rules]]
- extends [[Pre-Publish Checklist]]

#updating-notes #relations #verification #quality
