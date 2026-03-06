---
title: Title and Metadata Standards
type: note
permalink: creating-notes/title-and-metadata-standards
tags:
- creating-notes
- titles
- metadata
- tags
- standards
---

# Title and Metadata Standards

## Title Requirements

### Must Be
- **Specific** - Describes actual content
- **Searchable** - Contains key terms users would search
- **Unique** - Distinguishable from other notes in project

### Must NOT Be
- Generic ("Notes", "Discussion", "Ideas")
- Ambiguous ("Implementation", "Testing")
- Too short (single word titles)

See [[Generic Titles Anti-Pattern]] for examples.

## Title Templates

| Note Type | Template |
|-----------|----------|
| Implementation | `{Component} {Feature} Implementation` |
| Session | `Session {YYYY-MM-DD} - {Topic}` |
| Architecture | `{System/Feature} Architecture` |
| Issue | `{Component} {Problem} Issue` |
| Specification | `{Feature} Specification` |
| Procedure | `{Action} Procedure` |
| Testing | `{Component} {Test Type} Testing` |

## Tags

### Requirements
- **3-5 tags** per note
- Use lowercase, hyphenated format
- Include searchable terms

### Standard Tags by Category

**Project/Service**:
`edifact-split`, `parser-edifact`, `json-insertion`, `pipeline`

**Type**:
`implementation`, `architecture`, `testing`, `issue`, `procedure`, `session`

**Technical**:
`error-handling`, `compression`, `multi-format`, `security`

**Quality**:
`anti-pattern`, `best-practice`, `checklist`, `workflow`

## Frontmatter Structure

```yaml
---
title: Exact Note Title
type: note
tags: [tag1, tag2, tag3]
---
```

## Observations

- [requirement] Titles must be specific, searchable, and unique
- [technique] Use templates for consistent naming
- [requirement] Include 3-5 relevant tags per note
- [best-practice] Use lowercase hyphenated tag format

## Relations

- extends [[Generic Titles Anti-Pattern]]
- part_of [[New Note Checklist]]

#creating-notes #titles #metadata #tags #standards
