---
title: Archive Protocols
type: note
permalink: organizing/archive-protocols
tags:
- organizing
- archive
- history
- preservation
---

# Archive Protocols

## Core Principle

**Archive, don't delete.** Preserve historical context for future reference.

## What to Archive

- Superseded implementations
- Outdated planning documents
- Notes consolidated into comprehensive versions
- Historical analysis no longer relevant to current state
- Incremental versions after final version created

## Archive Folder Structure

```
archive/
├── {descriptive-category}/
│   ├── Original Note 1.md
│   └── Original Note 2.md
└── {another-category}/
```

### Category Naming

Use descriptive categories, NOT dates:

✅ **Good**:
- `archive/multi-format-testing-evolution/`
- `archive/error-implementation-history/`
- `archive/phase-1-planning/`
- `archive/deprecated-patterns/`

❌ **Bad**:
- `archive/2025-11/`
- `archive/old/`
- `archive/misc/`

## Archive Workflow

1. **Identify archive candidates**
   - Superseded by newer note
   - Consolidated into comprehensive note
   - No longer relevant to active work

2. **Choose/create category folder**
   - Descriptive name reflecting content
   - Group related archived notes together

3. **Move note**
   ```
   move_note(identifier="original-note", destination_path="archive/category/")
   ```

4. **Update references**
   - Check which notes reference the archived note
   - Update to point to replacement (if applicable)

## When NOT to Archive

- Note still actively referenced
- Note contains unique information not captured elsewhere
- Uncertain if superseded (verify first)

## Retrieving Archived Content

Archived notes remain searchable:
```
search_notes(query="topic", project="project-name")
# Results include archive/ folder
```

## Observations

- [requirement] Archive instead of delete to preserve history
- [technique] Use descriptive category folders, not date-based
- [best-practice] Update references after archiving

## Relations

- part_of [[Consolidation Criteria]]
- enables [[Knowledge Graph Optimization]]

#organizing #archive #history #preservation
