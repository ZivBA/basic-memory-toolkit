---
title: Code Pattern
type: schema
entity: code-pattern
version: 1
schema:
  title: string, descriptive pattern name
  pattern_type?(enum): [design, testing, deployment, integration, error-handling]
  language?: string, programming language if applicable
  context: string, when and why this pattern is used
  implementation: string, how the pattern works
  when_to_use: string, scenarios where this pattern applies
  when_not_to_use?: string, anti-patterns or wrong scenarios
settings:
  validation: warn
---

# Code Pattern Schema

Schema for reusable coding patterns, conventions, and architectural approaches.

## Usage

Create notes with `type: code-pattern` to document proven patterns that should be followed across projects.

## Title Convention

Use format: "[Pattern Name] Pattern"
Example: "Two-Tier Hook Validation Pattern"

## Example Note

```markdown
---
title: Contract-First Development Pattern
type: code-pattern
---

# Contract-First Development Pattern

- pattern_type: design
- language: Python
- context: Multi-service pipelines where services need to agree on data formats
- implementation: Define JSON schema contracts before implementation, validate at service boundaries
- when_to_use: When multiple services exchange data, especially in EDIFACT pipeline
- when_not_to_use: Single-service internal data structures

## Observations

- [technique] Define schemas first, implement handlers second #tdd #contracts
- [best-practice] Validate at boundaries, trust internally #validation
- [fact] Reduces integration bugs by catching format mismatches early #quality

## Relations

- extends [[Testing Philosophy - Infrastructure Over Exhaustive Coverage]]
- part_of [[Development Practices Index]]
```

## Observation Categories

Prefer: `[technique]`, `[best-practice]`, `[fact]`, `[decision]`
