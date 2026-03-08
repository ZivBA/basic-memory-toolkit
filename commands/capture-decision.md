---
description: Capture a design or architectural decision with structured template
argument-hint: [decision-title]
---

Capture a technical decision using a structured decision record template.

## Input

1. If $ARGUMENTS provided, use as the decision title
2. If no arguments, review the conversation for decisions discussed and ask: "Which decision would you like to document?"

## Project Selection

1. Use the currently active Basic Memory project for this session
2. If none active, run list_memory_projects() and ask which project

## Decision Template

Gather the following information (ask the user if not clear from conversation context):

### Context
- What prompted this decision?
- What problem are we solving?

### Options Considered
- Option A: [description] — pros/cons
- Option B: [description] — pros/cons
- Option C (if applicable): [description] — pros/cons

### Decision
- Which option was chosen and why?
- What trade-offs are accepted?

### Consequences
- What does this enable?
- What constraints does this create?
- Is this reversible? At what cost?

## Note Creation

Use the create-memory-note skill with:
- **Title**: Specific, e.g., "Two-Tier Validation Architecture Decision" (not "Decision about validation")
- **Folder**: decisions/
- **Observations**:
  - [decision] The chosen approach and rationale
  - [requirement] Constraints that led to this decision
  - [risk] Accepted trade-offs or risks
  - [fact] Key technical details
- **Relations**: Connect to:
  - Notes that motivated the decision
  - Notes that implement the decision
  - Notes about related architectural choices
- **Tags**: Include "decision", the domain area, and relevant technology

## Post-Creation

After saving:
1. Confirm what was captured
2. Ask: "Should I update any related notes to reference this decision?"
