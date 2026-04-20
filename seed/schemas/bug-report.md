---
title: Bug Report
type: schema
entity: bug-report
version: 1
schema:
  title: string, descriptive bug title
  severity?(enum): [critical, high, medium, low]
  affected_service: string, service or component where bug occurs
  reproduction_steps: string, how to reproduce the bug
  root_cause?: string, identified root cause
  fix_applied?: string, description of fix if resolved
  status?(enum): [open, investigating, fixed, verified, wont-fix]
settings:
  validation: warn
---

# Bug Report Schema

Schema for tracking bugs discovered during development sessions.

## Usage

Create notes with `type: bug-report` in frontmatter to track bugs with structured fields.

## Example Note

```markdown
---
title: Parser Timeout on Large EDIFACT Messages
type: bug-report
---

# Parser Timeout on Large EDIFACT Messages

- severity: critical
- affected_service: Parser-Edifact
- reproduction_steps: Send EDIFACT message >500KB through parser
- root_cause: Synchronous parsing blocks event loop
- fix_applied: Added chunked async parsing
- status: fixed

## Observations

- [issue] Parser hangs on messages exceeding 500KB #parser #performance
- [technique] Chunked async parsing resolves timeout #async
- [fact] Average EDIFACT message is 50KB, max observed is 1.2MB #sizing

## Relations

- part_of [[EDIFACT PNR Processing Pipeline]]
- fixed_by [[Parser Async Chunking Fix]]
```

## Observation Categories

Prefer: `[issue]`, `[fact]`, `[technique]`, `[risk]`
