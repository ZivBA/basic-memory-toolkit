---
description: Analyze knowledge graph health and suggest improvements
argument-hint: [project]
---

Analyze the knowledge graph health of a Basic Memory project and suggest improvements.

## Project Selection

1. If $ARGUMENTS names a project, use it
2. Otherwise, run list_memory_projects() and ask which project to analyze

## Analysis

Use the optimize-graph skill to perform a comprehensive analysis of the selected project.

The analysis should cover:

### Graph Density
- Count total notes and total relations
- Calculate average relations per note
- Identify isolated notes (0 relations)
- Identify weakly connected notes (1 relation)

### Relation Quality
- Count relation type distribution (implements, requires, part_of, extends, relates_to, etc.)
- Flag notes with only generic "relates_to" relations
- Flag index notes using "relates_to" instead of "documents" or "encompasses"

### Structural Issues
- Self-referential relations (note pointing to itself)
- Cross-project WikiLinks (won't resolve)
- Informal relation sections ("## Related Components", "## See Also", etc.)
- Notes missing "## Relations" section entirely

### Content Quality
- Notes with fewer than 3 observations
- Notes with generic titles
- Very large notes (>500 lines) that might need splitting

## Report Format

Present findings as:

**Project Health Score**: X/10

**Critical Issues** (fix immediately):
- List blocking problems

**Warnings** (should fix):
- List quality issues with counts

**Suggestions** (nice to have):
- List improvements

**Top 5 Actions**:
- Prioritized list of specific fixes with note names

## Follow-Up

Ask: "Would you like me to fix any of these issues? I can use the memory-organizer agent for bulk operations, or handle specific fixes directly."
