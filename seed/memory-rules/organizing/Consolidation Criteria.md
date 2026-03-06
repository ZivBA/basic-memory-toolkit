---
title: Consolidation Criteria
type: note
permalink: organizing/consolidation-criteria
tags:
- organizing
- consolidation
- decision-framework
---

# Consolidation Criteria

## When to Consolidate

**MERGE** notes if ALL conditions met:

1. **Same topic** - Both notes cover same subject
2. **Same abstraction level** - Both are specs, or both are implementations
3. **70%+ content overlap** - Significant duplication
4. **Same audience** - Both for same readers

## When to Keep Separate

**DO NOT MERGE** if any condition applies:

| Condition | Example |
|-----------|---------|
| Different purposes | Specification vs Implementation |
| Different abstraction | Architecture vs Code details |
| Different audiences | Developer vs QA vs Architect |
| Different time contexts | Planning vs Completion vs Retrospective |
| Incremental versions | v1, v2, v3 (keep history in archive) |

## Decision Flowchart

```
Same topic?
├── No → Keep separate
└── Yes → Same abstraction level?
    ├── No → Keep separate
    └── Yes → 70%+ overlap?
        ├── No → Keep separate (maybe add relations)
        └── Yes → Same purpose/audience?
            ├── No → Keep separate, restructure to reduce duplication
            └── Yes → CONSOLIDATE
```

## Consolidation Workflow

1. **Identify candidates** - Search for similar titles/topics
2. **Compare content** - Read both, assess overlap percentage
3. **Decide** - Use criteria above
4. **If consolidating**:
   - Create comprehensive note with all unique content
   - Archive originals to `archive/{category}/`
   - Update relations in other notes to point to new note
5. **If keeping separate**:
   - Restructure to eliminate duplication
   - Add cross-references between notes

## Archive Location

When consolidating, move originals to:
```
archive/{descriptive-category}/
```

Examples:
- `archive/multi-format-testing-evolution/`
- `archive/error-implementation-history/`

See [[Archive Protocols]] for details.

## Observations

- [decision] Consolidate only when same topic + abstraction + 70%+ overlap
- [technique] Use archive folders to preserve history when consolidating
- [requirement] Different purposes justify separate notes despite overlap

## Relations

- requires [[Archive Protocols]]
- part_of [[Knowledge Graph Optimization]]

#organizing #consolidation #decision-framework
