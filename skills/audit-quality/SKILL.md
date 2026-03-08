---
name: audit-quality
description: Audit project for quality issues in titles, metadata, observations, relations, and semantic markup
---

<purpose>
Assessment skill for evaluating note quality across a project.
Uses verify-memory-relations for relation checks, references memory-rules for standards.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <titles>anti-patterns/Generic Titles Anti-Pattern</titles>
  <titles>creating-notes/Title and Metadata Standards</titles>
  <observations>quality/Observation Standards</observations>
  <relations>creating-notes/Relation Creation Rules</relations>
  <checklist>quality/Pre-Publish Checklist</checklist>
  <core_skill>verify-memory-relations (for relation audit)</core_skill>
  <core_skill>update-memory-note (for fixes)</core_skill>
</rules_reference>

<workflow>
  <phase name="load-rules">
    <step>Read quality standards from memory-rules:
      - search_notes(query="Observation Standards", project="memory-rules")
      - search_notes(query="Title and Metadata", project="memory-rules")
      - search_notes(query="Pre-Publish Checklist", project="memory-rules")
    </step>
  </phase>

  <phase name="discovery">
    <step>Search for generic title patterns</step>
    <step>Sample notes across project folders</step>
    <step>Run recent_activity() to check recent additions</step>
    <step>Use metadata_filters to efficiently filter by tags or note_types:
      - search_notes(query="*", note_types=["schema"], project=target)
      - search_notes(query="*", tags=["index"], project=target)
    </step>
  </phase>

  <phase name="title_audit">
    <step>Identify generic titles (Notes, Session, Discussion, etc.)</step>
    <step>Check against title templates from memory-rules</step>
    <step>Find overly long or unclear titles</step>
  </phase>

  <phase name="metadata_audit">
    <step>Verify tags are present and relevant (3-5 per note)</step>
    <step>Check entity_type accuracy</step>
    <step>Confirm folder placement matches content</step>
  </phase>

  <phase name="observation_audit">
    <step>Count observations per note (target: 3-5)</step>
    <step>Check observation categories are specific:
      - decision, requirement, technique, issue, fact
      - idea, question, preference, best-practice
    </step>
    <step>Identify notes with no observations</step>
  </phase>

  <phase name="relation_audit">
    <step>Use verify-memory-relations skill on each note</step>
    <step>Detect critical issues:
      - Self-referential relations
      - Cross-project WikiLinks
      - Broken WikiLinks
    </step>
    <step>Count relations per note (target: 2-3+)</step>
    <step>Identify isolated notes</step>
  </phase>

  <phase name="planning">
    <step>Create improvement plan prioritized by severity:
      - CRITICAL: Self-referential relations, missing required metadata
      - HIGH: Generic titles, no observations/relations
      - MEDIUM: Fewer than 2 relations, fewer than 3 observations
      - LOW: Could use more specific relation types
    </step>
    <step>Present findings and recommendations</step>
  </phase>

  <phase name="execution">
    <step>Use update-memory-note skill for fixes:</step>
    <substep>Fix critical issues first</substep>
    <substep>Improve titles from generic to specific</substep>
    <substep>Add missing observations and relations</substep>
    <substep>Correct folder placement and tags</substep>
  </phase>

  <phase name="reporting">
    <step>Report quality metrics before/after</step>
    <step>Show improvements made</step>
    <step>List remaining issues for future attention</step>
  </phase>
</workflow>

<quality_issues>
  <critical>
    <issue>Self-referential relations</issue>
    <issue>Missing required metadata (title, folder)</issue>
    <issue>Broken WikiLinks (typos in target)</issue>
  </critical>

  <high>
    <issue>Generic titles (Notes, Session, Discussion)</issue>
    <issue>No observations or relations</issue>
    <issue>Incorrect folder placement</issue>
  </high>

  <medium>
    <issue>Fewer than 2 relations (isolated)</issue>
    <issue>Fewer than 3 observations</issue>
    <issue>Generic observation categories</issue>
    <issue>Missing or irrelevant tags</issue>
  </medium>

  <low>
    <issue>Could use more specific relation types</issue>
    <issue>Long or unclear titles</issue>
    <issue>Inconsistent formatting</issue>
  </low>
</quality_issues>

<quality_standards>
  <title>Specific, descriptive, searchable, follows templates</title>
  <tags>3-5 relevant, lowercase hyphenated</tags>
  <observations>3-5 with specific categories</observations>
  <relations>2-3+ with specific types, no self-refs</relations>
</quality_standards>
