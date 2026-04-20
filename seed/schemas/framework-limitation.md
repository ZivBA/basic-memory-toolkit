---
title: Framework Limitation
type: schema
entity: framework-limitation
version: 1
schema:
  title: string, specific limitation title
  framework: string, framework or library name
  version: string, affected version(s)
  limitation: string, what the limitation is
  impact: string, how it affects development
  workaround?: string, known workaround
  upstream_issue?: string, link to upstream issue tracker
settings:
  validation: warn
---

# Framework Limitation Schema

Schema for known limitations in frameworks and libraries used across projects.

## Usage

Create notes with `type: framework-limitation` to document framework-specific issues that affect development.

## Example Note

```markdown
---
title: Basic Memory WikiLinks Cross-Project Limitation
type: framework-limitation
---

# Basic Memory WikiLinks Cross-Project Limitation

- framework: Basic Memory
- version: 0.19.0+
- limitation: WikiLinks [[Target]] only resolve within the same project
- impact: Cannot use WikiLinks for cross-project references in Relations section
- workaround: Use text format "Note Title" (project-name) for cross-project refs

## Observations

- [constraint] WikiLinks are project-scoped by design #basic-memory #relations
- [technique] Text format with project name in parentheses for cross-project refs #format
- [fact] memory:// URLs support cross-project: memory://project/folder/note #urls

## Relations

- constrains [[Cross-Project WikiLinks Anti-Pattern]]
- documents [[Basic Memory Toolkit Index]]
```

## Observation Categories

Prefer: `[constraint]`, `[fact]`, `[technique]`, `[risk]`
