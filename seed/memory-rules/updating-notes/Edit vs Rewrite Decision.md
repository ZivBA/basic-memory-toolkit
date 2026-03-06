---
title: Edit vs Rewrite Decision
type: note
permalink: updating-notes/edit-vs-rewrite-decision
tags:
- updating-notes
- edit
- workflow
- decision
---

# Edit vs Rewrite Decision

## Core Principle

**Prefer `edit_note()` for small changes.** Only use `write_note()` for major rewrites.

## Decision Matrix

| Change Type | Tool | Operation |
|-------------|------|-----------|
| Add content to end | `edit_note()` | `append` |
| Add content to start | `edit_note()` | `prepend` |
| Replace specific text | `edit_note()` | `find_replace` |
| Update one section | `edit_note()` | `replace_section` |
| Major restructure | `write_note()` | Full rewrite |
| Fix multiple sections | `write_note()` | Full rewrite |

## edit_note() Operations

### append
Add content to end of note:
```python
edit_note(identifier="note-title", operation="append",
          content="\n## New Section\nNew content here")
```

### prepend
Add content to beginning:
```python
edit_note(identifier="note-title", operation="prepend",
          content="## Important Notice\nContent here\n\n")
```

### find_replace
Replace specific text:
```python
edit_note(identifier="note-title", operation="find_replace",
          find_text="old text", content="new text")
```

### replace_section
Replace entire section:
```python
edit_note(identifier="note-title", operation="replace_section",
          section="## Relations", content="## Relations\n\n- new_relation [[Target]]")
```

## When to Rewrite

Use `write_note()` (full rewrite) only when:
- Restructuring entire note
- Changing 50%+ of content
- Merging content from multiple sources
- Major reorganization needed

## Important: Exact Identifiers

`edit_note()` requires **exact** identifiers:
- Search first if uncertain: `search_notes(query="title")`
- Use title, folder/title, or permalink
- No fuzzy matching

## Observations

- [technique] Use edit_note() for small, targeted changes
- [requirement] Use exact identifiers for edit_note()
- [decision] Rewrite only when changing 50%+ of content

## Relations

- requires [[Relation Verification After Edit]]
- part_of [[Pre-Publish Checklist]]

#updating-notes #edit #workflow #decision
