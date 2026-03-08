---
title: Design Decision
type: schema
entity: design-decision
version: 1
schema:
  title: string, specific decision title
  context: string, what prompted this decision
  options_considered?(array): string, alternatives evaluated
  chosen_option: string, the selected approach
  rationale: string, why this option was chosen
  consequences: string, what this enables and constrains
  decided_by?: string, who made the decision
  reversibility?(enum): [easy, moderate, difficult, irreversible]
settings:
  validation: warn
---

# Design Decision Schema

Schema for architectural and design choices with full rationale tracking. Based on Architecture Decision Records (ADR) pattern.

## Usage

Create notes with `type: design-decision` to capture the context, options, and rationale behind technical choices.

## Example Note

```markdown
---
title: Two-Tier Validation Architecture Decision
type: design-decision
---

# Two-Tier Validation Architecture Decision

- context: Need fast validation for PreToolUse hooks but thorough checks for batch use
- options_considered: Single CLI validator, Pure inline parsing, Two-tier architecture
- chosen_option: Two-tier — inline for hooks, CLI for batch
- rationale: CLI overhead is 7s per call (350x slower than estimated), hooks need <50ms
- consequences: Enables instant PreToolUse blocking; CLI validators reserved for /validate-project
- reversibility: easy

## Observations

- [decision] Two-tier architecture separates speed-critical from thoroughness-critical validation #architecture
- [requirement] PreToolUse hooks must complete in <50ms to avoid UX degradation #performance
- [risk] Logic duplication between tiers requires sync discipline #maintenance
- [fact] CLI overhead measured at ~7s due to Python startup + DB connection #performance

## Relations

- implements [[Basic Memory Toolkit Index]]
- informed_by [[CLI Performance Overhead Discovery]]
```

## Observation Categories

Prefer: `[decision]`, `[requirement]`, `[risk]`, `[fact]`, `[constraint]`
