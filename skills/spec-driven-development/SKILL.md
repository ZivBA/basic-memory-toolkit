---
name: spec-driven-development
description: Align implementation work with specifications stored in Basic Memory. Use when implementing features that have design specs, architecture decisions, or requirements documented in memory notes, to ensure the implementation matches what was planned.
---

<purpose>
Implementation alignment skill that bridges memory specs and code.
Loads relevant specifications from Basic Memory before implementation begins,
tracks progress against spec, and captures deviations as decisions.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <core_skill>create-memory-note (for deviation records)</core_skill>
  <core_skill>knowledge-capture (for implementation insights)</core_skill>
</rules_reference>

<workflow>
  <phase name="spec-discovery">
    <step>Identify the feature or task being implemented</step>
    <step>Search for related specs in Basic Memory:
      - search_notes(query="feature keywords", project=active)
      - search_notes(query="design OR architecture OR spec", project=active)
      - search_notes(query="decision", project=active)
    </step>
    <step>Read each relevant note: read_note(identifier, project)</step>
    <step>Follow relations via build_context() for connected specs</step>
  </phase>

  <phase name="spec-summary">
    <step>Present loaded specifications to user:</step>
    <format>
      **Implementation Specs Loaded:**

      From [note-title]:
      - [key requirement or decision]
      - [constraint or limitation]

      From [note-title]:
      - [architectural pattern to follow]
      - [specific approach decided]

      **Constraints:**
      - [list hard constraints from specs]

      **Open Questions:**
      - [any ambiguities in specs]

      Does this match your understanding? Any changes before we proceed?
    </format>
  </phase>

  <phase name="implementation">
    <step>Implement according to loaded specs</step>
    <step>When deviating from spec, pause and document:
      - Why the deviation is necessary
      - What was originally specified
      - What we're doing instead
    </step>
    <step>Track implementation progress against spec requirements</step>
  </phase>

  <phase name="deviation-capture">
    <step>If implementation deviates from spec, ask user:
      "The spec says [X] but we're doing [Y] because [reason]. Should I:
      1. Update the spec note to reflect this change?
      2. Capture this as a new decision?"
    </step>
    <step>If updating spec: use edit_note() on original spec note</step>
    <step>If new decision: use /capture-decision or create-memory-note skill</step>
  </phase>

  <phase name="completion-check">
    <step>After implementation, review spec requirements:</step>
    <format>
      **Spec Compliance Check:**
      - [requirement 1]: DONE / PARTIAL / DEFERRED
      - [requirement 2]: DONE / PARTIAL / DEFERRED
      - [requirement 3]: DONE / PARTIAL / DEFERRED

      **Deviations:**
      - [list any deviations and where they're documented]

      **Not Yet Implemented:**
      - [list deferred items]
    </format>
  </phase>

  <phase name="progress-update">
    <step>Update relevant memory notes with implementation status:
      - edit_note() to mark completed items in spec notes
      - Create progress note if significant milestone reached
    </step>
    <step>Suggest using /remember to capture implementation insights</step>
  </phase>
</workflow>

<spec_types>
  <design_spec>Architecture decisions, component designs, API contracts</design_spec>
  <enhancement_plan>Phased roadmaps with deliverable checklists</enhancement_plan>
  <requirements>Feature requirements, constraints, acceptance criteria</requirements>
  <decision_record>Past decisions that constrain implementation</decision_record>
</spec_types>

<best_practices>
  <practice>Always load specs BEFORE starting implementation</practice>
  <practice>Document deviations immediately, not after the fact</practice>
  <practice>Update spec notes when implementation reveals new constraints</practice>
  <practice>Use memory as the source of truth for what was decided</practice>
  <practice>Don't silently deviate — capture the reasoning</practice>
</best_practices>
