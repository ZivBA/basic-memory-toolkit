---
name: verify-memory-relations
description: Check note for relation health - self-refs, broken links, cross-project WikiLinks
---

<purpose>
Health check skill for validating note relations.
Use after creating/editing notes or during quality audits.
</purpose>

<workflow>
  <phase name="load-rules">
    <step>Read anti-pattern rules from memory-rules project:
      - search_notes(query="Self-Referential", project="memory-rules")
      - search_notes(query="Cross-Project WikiLinks", project="memory-rules")
    </step>
  </phase>

  <phase name="read-note">
    <step>Read target note: read_note(identifier, project)</step>
    <step>Extract Relations section</step>
    <step>Extract note title for self-reference check</step>
  </phase>

  <phase name="check-self-referential">
    <step>For each relation in note:</step>
    <step>Compare WikiLink target to current note title</step>
    <step>Flag if target = current note title</step>
    <severity>CRITICAL - causes infinite loops</severity>
  </phase>

  <phase name="check-cross-project">
    <step>For each WikiLink relation:</step>
    <step>Search for target in current project</step>
    <step>If not found, check if exists in other project</step>
    <step>Flag if WikiLink points to different project</step>
    <severity>HIGH - WikiLinks don't cross projects</severity>
  </phase>

  <phase name="check-broken-links">
    <step>For each WikiLink relation:</step>
    <step>Search for target: search_notes(query="exact title", project="current")</step>
    <step>If not found and not intentional forward ref, flag as broken</step>
    <severity>MEDIUM - may indicate typo in target</severity>
  </phase>

  <phase name="check-relation-quality">
    <step>Count total relations (target: 2-3+)</step>
    <step>Check relation types used</step>
    <step>Flag overuse of generic "relates_to"</step>
    <severity>LOW - quality improvement opportunity</severity>
  </phase>

  <phase name="report">
    <step>Report findings by severity:</step>
    <format>
      CRITICAL: Self-referential relations found
      HIGH: Cross-project WikiLinks found
      MEDIUM: Broken WikiLinks found
      LOW: Quality improvements suggested
    </format>
    <step>Provide specific fix instructions for each issue</step>
  </phase>
</workflow>

<issue_types>
  <self_referential>
    <detection>WikiLink target = current note title</detection>
    <fix>Remove relation OR convert to observation</fix>
    <example>- implements [[Current Note]] → REMOVE</example>
  </self_referential>

  <cross_project_wikilink>
    <detection>WikiLink target exists in different project only</detection>
    <fix>Convert to text format: "Title" (project-name)</fix>
    <example>[[Other Project Note]] → "Other Project Note" (other-project)</example>
  </cross_project_wikilink>

  <broken_wikilink>
    <detection>WikiLink target not found in any project</detection>
    <fix>Search for correct title, fix typo, or mark as intentional forward ref</fix>
  </broken_wikilink>

  <weak_relations>
    <detection>Multiple "relates_to" instead of specific types</detection>
    <fix>Replace with: implements, requires, part_of, extends, contrasts_with</fix>
  </weak_relations>
</issue_types>

<rules_reference>
  <project>memory-rules</project>
  <self_ref>anti-patterns/Self-Referential Relations Anti-Pattern</self_ref>
  <cross_project>anti-patterns/Cross-Project WikiLinks Anti-Pattern</cross_project>
  <relation_rules>creating-notes/Relation Creation Rules</relation_rules>
</rules_reference>

<fix_commands>
  <self_referential>
    edit_note(identifier, operation="replace_section", section="## Relations", content="fixed relations")
  </self_referential>
  <cross_project>
    edit_note(identifier, operation="find_replace", find_text="[[Cross Note]]", content='"Cross Note" (other-project)')
  </cross_project>
</fix_commands>
