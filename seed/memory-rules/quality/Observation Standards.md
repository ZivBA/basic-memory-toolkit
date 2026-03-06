---
title: Observation Standards
type: note
permalink: quality/observation-standards
tags:
- quality
- observations
- semantic-markup
- categories
---

# Observation Standards

## Core Requirement

**Every note must have 3-5 observations** with specific categories.

Observations capture searchable, categorized insights from the note content.

## Format

```markdown
- [category] Description of the observation #optional-tag
```

## Categories Reference

| Category | Use For | Example |
|----------|---------|---------|
| `decision` | Choices made, rationale | `[decision] Use service-based folders for pipeline project` |
| `requirement` | Must-have constraints | `[requirement] All relations must be verified before creation` |
| `technique` | How something is done | `[technique] Use sed to fix ODBC config at runtime` |
| `issue` | Problems, bugs | `[issue] ODBC config doesn't expand environment variables` |
| `fact` | Objective information | `[fact] WikiLinks only work within same project` |
| `idea` | Proposals, concepts | `[idea] Consider dynamic driver discovery in Dockerfile` |
| `question` | Open items | `[question] Should archived notes retain original relations?` |
| `preference` | User/team preferences | `[preference] Use XML format for structured documentation` |
| `best-practice` | Recommended approaches | `[best-practice] Archive instead of delete` |
| `checklist` | Verification items | `[checklist] Verify relations before write_note()` |

## Quality Guidelines

### Good Observations
- **Specific** - Captures concrete insight
- **Categorized** - Uses appropriate category
- **Standalone** - Understandable without full context
- **Searchable** - Contains key terms

### Bad Observations
- Generic: `[fact] This is about testing`
- Uncategorized: `- Some observation without category`
- Redundant: Same as title or obvious from content

## Minimum Count

| Note Type | Min Observations |
|-----------|------------------|
| Standard note | 3-5 |
| Quick reference | 2-3 |
| Comprehensive | 5-7 |

## Observations

- [requirement] Every note needs 3-5 categorized observations
- [technique] Use specific categories from reference table
- [best-practice] Make observations standalone and searchable

## Relations

- part_of [[New Note Checklist]]
- part_of [[Pre-Publish Checklist]]

#quality #observations #semantic-markup #categories
