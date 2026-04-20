---
title: Fix Record
type: schema
entity: fix-record
version: 1
schema:
  title: string, descriptive fix title
  bug_reference?: string, related bug report title or identifier
  changes_made: string, description of changes applied
  files_modified?(array): string, list of files changed
  testing_done: string, how the fix was verified
  regression_risk?(enum): [high, medium, low, none]
settings:
  validation: warn
---

# Fix Record Schema

Schema for documenting applied fixes with context for future reference.

## Usage

Create notes with `type: fix-record` to document what was changed, why, and what risks remain.

## Example Note

```markdown
---
title: Parser Async Chunking Fix
type: fix-record
---

# Parser Async Chunking Fix

- bug_reference: Parser Timeout on Large EDIFACT Messages
- changes_made: Replaced synchronous parse loop with async chunked processing
- files_modified: src/parser/edifact_parser.py, src/parser/chunk_handler.py
- testing_done: Unit tests for chunk sizes 1KB-2MB, integration test with production samples
- regression_risk: medium

## Observations

- [technique] Async chunking with 64KB default chunk size #async #performance
- [risk] Chunk boundary may split multi-byte characters #encoding
- [fact] Performance improved 3x for messages >100KB #benchmark

## Relations

- fixes [[Parser Timeout on Large EDIFACT Messages]]
- part_of [[EDIFACT PNR Processing Pipeline]]
```

## Observation Categories

Prefer: `[technique]`, `[risk]`, `[fact]`, `[decision]`
