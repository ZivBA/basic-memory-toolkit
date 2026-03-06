---
title: New Note Checklist
type: note
permalink: creating-notes/new-note-checklist
tags:
- creating-notes
- checklist
- quality
- workflow
---

# New Note Checklist

## Before Creating

- [ ] Search for existing notes on same topic
- [ ] Verify note doesn't duplicate existing content
- [ ] Choose appropriate project
- [ ] Choose appropriate folder within project

## Note Structure

### Required Elements

- [ ] **Title**: Specific, searchable (see [[Generic Titles Anti-Pattern]])
- [ ] **Tags**: 3-5 relevant, searchable tags
- [ ] **Observations**: 3-5 with specific categories
- [ ] **Relations**: 2-3 minimum to other notes

### Observation Categories

Use specific categories:
- `decision` - Choices made and rationale
- `requirement` - Must-have constraints
- `technique` - How something is done
- `issue` - Problems or bugs
- `fact` - Objective information
- `idea` - Proposals or concepts
- `question` - Open items to resolve
- `preference` - User/team preferences
- `best-practice` - Recommended approaches

### Relation Verification

For each relation:
- [ ] Target exists (searched and found)
- [ ] Target ≠ current note (not self-referential)
- [ ] Target in same project (or using text format)
- [ ] Using specific relation type

See [[Relation Creation Rules]] for full workflow.

## Note Length Guidelines

| Note Type | Target Length | Max Warning |
|-----------|---------------|-------------|
| Roadmap/Overview | ~100 lines | 200 lines |
| Implementation | ~150 lines | 300 lines |
| Comprehensive | ~300 lines | 500 lines |
| **Any note** | - | **1500 lines** (split!) |

If exceeding limits, consider splitting into focused modules.

## Final Verification

Before `write_note()`:
- [ ] Title is specific and unique
- [ ] All relations verified
- [ ] 3-5 observations with categories
- [ ] Appropriate folder selected
- [ ] Tags are searchable

## Observations

- [checklist] Complete all verification steps before write_note()
- [requirement] 3-5 observations, 2-3 relations minimum
- [technique] Search for duplicates before creating new notes
- [best-practice] Keep notes focused, split if exceeding 1500 lines

## Relations

- requires [[Relation Creation Rules]]
- requires [[Generic Titles Anti-Pattern]]
- part_of [[Pre-Publish Checklist]]

#creating-notes #checklist #quality #workflow
