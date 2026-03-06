---
title: Generic Titles Anti-Pattern
type: note
permalink: anti-patterns/generic-titles-anti-pattern
tags:
- anti-pattern
- titles
- searchability
---

# Generic Titles Anti-Pattern

## Rule

**Avoid generic, non-descriptive titles.** Titles must be specific and searchable.

Generic titles make notes hard to find and distinguish.

## Examples

❌ **WRONG** - Generic titles:
- "Notes 2024"
- "Discussion"
- "Session"
- "Ideas"
- "Implementation"
- "Testing"

✅ **CORRECT** - Specific titles:
- "EdifactSplit Error Handling Implementation"
- "Multi-Format EDIFACT Testing Environment"
- "Session 2025-11-23 - Edifact Pipeline Reorganization"
- "Message Reprocessability Architecture"

## Title Guidelines

Good titles should:
1. **Describe the content** - What is this note about?
2. **Be searchable** - Include key terms users would search for
3. **Be unique** - Distinguishable from other notes
4. **Include context** - Project/service/date where relevant

## Pattern Templates

| Note Type | Template | Example |
|-----------|----------|---------|
| Implementation | `{Component} {Feature} Implementation` | "Parser-Edifact Error Handling Implementation" |
| Session | `Session {Date} - {Topic}` | "Session 2025-11-23 - Pipeline Reorganization" |
| Architecture | `{System} Architecture` | "Message Reprocessability Architecture" |
| Issue | `{Component} {Problem} Issue` | "ODBC Driver Configuration Issue" |
| Specification | `{Feature} Specification` | "Error Details List Specification" |

## How to Fix

If generic titles found:
1. Read note to understand actual content
2. Identify key concepts, components, dates
3. Create specific title using templates above
4. Use `move_note()` or recreate with new title

## Observations

- [requirement] Titles must be specific and searchable
- [technique] Use templates for consistent, descriptive titles
- [issue] Generic titles make notes indistinguishable in search results

## Relations

- part_of [[Title and Metadata Standards]]

#anti-pattern #titles #searchability
