---
title: Architecture Constraint
type: schema
entity: architecture-constraint
version: 1
schema:
  title: string, specific constraint title
  constraint_type?(enum): [technical, business, regulatory, resource]
  description: string, what the constraint is
  affected_components?(array): string, components impacted
  workarounds?: string, known workarounds or mitigations
  expiration?: string, when this constraint may no longer apply
settings:
  validation: warn
---

# Architecture Constraint Schema

Schema for documenting system limitations, boundaries, and constraints that affect architectural decisions.

## Usage

Create notes with `type: architecture-constraint` to document hard limits that constrain what can be built.

## Example Note

```markdown
---
title: Basic Memory CLI Subprocess Overhead Constraint
type: architecture-constraint
---

# Basic Memory CLI Subprocess Overhead Constraint

- constraint_type: technical
- description: Each basic-memory CLI call takes ~7s due to Python interpreter startup, module loading, and DB connection
- affected_components: Hook validators, batch operations, any subprocess calling basic-memory
- workarounds: Parse tool_input from hook stdin directly (20ms), reserve CLI for batch/offline use
- expiration: If basic-memory adds a persistent server mode or socket API

## Observations

- [constraint] CLI subprocess overhead makes real-time validation impractical #performance
- [fact] Overhead breakdown: Python startup ~2s, module import ~3s, DB connect ~2s #profiling
- [technique] Stdin parsing as alternative to CLI for hook context #hooks

## Relations

- constrains [[Basic Memory Toolkit Index]]
- informed [[Two-Tier Validation Architecture Decision]]
```

## Observation Categories

Prefer: `[constraint]`, `[fact]`, `[technique]`, `[risk]`
