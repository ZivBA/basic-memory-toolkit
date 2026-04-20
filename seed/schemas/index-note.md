---
title: Index Note
type: schema
entity: index-note
version: 1
schema:
  title: string, project name followed by Index
  project_name: string, the Basic Memory project this indexes
  note_count?: integer, approximate number of notes in project
  focus_areas?(array): string, main topic areas covered
settings:
  validation: warn
---

# Index Note Schema

Schema for project index notes that serve as entry points to a knowledge project.

## Critical Rule

Index notes MUST use `documents` or `encompasses` relation types — NEVER `relates_to`. Generic relation types defeat the purpose of an index.

## Title Convention

Use format: "[Project Name] Index"
Example: "EDIFACT Pipeline Index"

## Example Note

```markdown
---
title: EDIFACT Pipeline Index
type: index-note
---

# EDIFACT Pipeline Index

- project_name: edifact-pipeline
- note_count: 31
- focus_areas: EDIFACT processing, Split/Parse/Insert pipeline, error handling, multi-format testing

## Observations

- [fact] Pipeline processes EDIFACT PNR and API messages through three stages #architecture
- [requirement] All services must handle both PNR and API formats #multi-format
- [best-practice] Error wrapping preserves original message for reprocessing #error-handling

## Relations

- documents [[EDIFACT PNR Processing Pipeline]]
- documents [[Cross-Service JSON Wrapper Pattern]]
- encompasses [[Multi-Format EDIFACT Testing Environment]]
```

## Relation Rules

- Use `documents` for notes this index describes
- Use `encompasses` for broad topic areas
- NEVER use `relates_to` — it provides no semantic value for an index

## Observation Categories

Prefer: `[fact]`, `[requirement]`, `[best-practice]`
