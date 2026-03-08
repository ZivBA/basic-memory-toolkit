---
name: optimize-graph
description: Analyze knowledge graph connections, identify isolated notes, detect errors, strengthen semantic relationships
---

<purpose>
Maintenance skill for improving knowledge graph connectivity.
Uses verify-memory-relations for detection, references memory-rules for fixes.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <self_ref>anti-patterns/Self-Referential Relations Anti-Pattern</self_ref>
  <cross_project>anti-patterns/Cross-Project WikiLinks Anti-Pattern</cross_project>
  <relation_rules>creating-notes/Relation Creation Rules</relation_rules>
  <core_skill>verify-memory-relations (for detection)</core_skill>
  <core_skill>update-memory-note (for fixes)</core_skill>
</rules_reference>

<workflow>
  <phase name="load-rules">
    <step>Read relation rules from memory-rules:
      - search_notes(query="Relation Creation Rules", project="memory-rules")
      - search_notes(query="Self-Referential", project="memory-rules")
    </step>
  </phase>

  <phase name="discovery">
    <step>Search broadly across project to identify all notes</step>
    <step>Use build_context() to analyze connection patterns</step>
    <step>Map current graph density metrics</step>
  </phase>

  <phase name="analysis">
    <step>Use verify-memory-relations skill on each note to detect:</step>
    <issues>
      <critical>Self-referential relations (from_entity = to_entity)</critical>
      <critical>Cross-project WikiLinks</critical>
      <high>Broken WikiLinks (unintentional)</high>
      <medium>Isolated notes (&lt; 2 relations)</medium>
      <low>Weak relation types (generic relates_to)</low>
    </issues>
  </phase>

  <phase name="relationship_discovery">
    <step>Search for semantic relationships between isolated notes</step>
    <step>Identify potential connections using specific types:
      - implements, requires, part_of, extends
      - contrasts_with, inspired_by, pairs_with
    </step>
  </phase>

  <phase name="planning">
    <step>Create improvement plan prioritized by severity</step>
    <step>Plan fixes for critical issues first</step>
    <step>Suggest strategic connections for better discoverability</step>
    <step>Present plan to user for confirmation</step>
  </phase>

  <phase name="execution">
    <step>Use update-memory-note skill for each fix:</step>
    <substep>Fix self-referential relations (remove or convert to observation)</substep>
    <substep>Convert cross-project WikiLinks to text format</substep>
    <substep>Add strategic relations to isolated notes</substep>
    <substep>Strengthen weak connections with specific relation types</substep>
    <substep>Convert informal sections ("## See Also", "## Related Components") to proper WikiLink relations</substep>
    <step>For bulk WikiLink fixes across many notes, use the batch-fix-wikilinks skill</step>
  </phase>

  <phase name="verification">
    <step>Re-run verify-memory-relations on fixed notes</step>
    <step>Confirm issues resolved</step>
  </phase>

  <phase name="reporting">
    <step>Report graph density improvements</step>
    <step>Show before/after metrics (avg relations per note)</step>
    <step>List notes still requiring attention</step>
  </phase>
</workflow>

<graph_issues>
  <issue type="self_referential" severity="critical">Relations where from_entity equals to_entity</issue>
  <issue type="cross_project_wikilink" severity="critical">WikiLinks across project boundaries</issue>
  <issue type="broken_wikilink" severity="high">WikiLinks to non-existent notes</issue>
  <issue type="isolated" severity="medium">Notes with fewer than 2 relations</issue>
  <issue type="weak_relation" severity="low">Generic relates_to instead of specific type</issue>
</graph_issues>

<relation_types>
  <strong>implements, requires, part_of, extends</strong>
  <medium>pairs_with, inspired_by, contrasts_with</medium>
  <weak>relates_to (use only when no specific type fits)</weak>
</relation_types>

<target_metrics>
  <minimum>2 relations per note</minimum>
  <good>3+ relations per note</good>
  <excellent>Dense cluster with multiple connection types</excellent>
</target_metrics>
