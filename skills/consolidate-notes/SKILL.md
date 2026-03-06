---
name: consolidate-notes
description: This skill should be used when reviewing a project for duplicate or overlapping notes, the user asks to "consolidate notes", "merge duplicate notes", "clean up overlapping content", or when the memory-organizer agent identifies consolidation candidates.
version: 1.0.0
---

<purpose>
Maintenance skill for consolidating duplicate or overlapping notes.
References memory-rules for criteria, uses core skills for note operations.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <criteria>organizing/Consolidation Criteria</criteria>
  <archive>organizing/Archive Protocols</archive>
  <core_skill>create-memory-note (for creating merged notes)</core_skill>
  <core_skill>verify-memory-relations (for checking results)</core_skill>
  <index>Per-project index note — update when consolidation changes entry points</index>
</rules_reference>

<workflow>
  <phase name="load-rules">
    <step>Read consolidation criteria from memory-rules:
      - search_notes(query="Consolidation Criteria", project="memory-rules")
    </step>
    <step>Read archive protocols:
      - search_notes(query="Archive Protocols", project="memory-rules")
    </step>
  </phase>

  <phase name="discovery">
    <step>Run recent_activity(timeframe="30d", project=target) for context</step>
    <step>Search for common topics/keywords to find related notes</step>
    <step>Read candidate notes to assess overlap</step>
  </phase>

  <phase name="analysis">
    <step>Apply consolidation criteria from memory-rules:</step>
    <criteria>
      <merge_if>Same topic AND same abstraction level</merge_if>
      <merge_if>70%+ content overlap</merge_if>
      <merge_if>Same audience and purpose</merge_if>
      <keep_separate_if>Different purposes (spec vs implementation)</keep_separate_if>
      <keep_separate_if>Different abstraction levels</keep_separate_if>
      <keep_separate_if>Different time contexts (planning vs retrospective)</keep_separate_if>
    </criteria>
    <step>Group consolidation candidates</step>
  </phase>

  <phase name="planning">
    <step>Create consolidation plan with specific note pairs/groups</step>
    <step>Identify which note should be primary/comprehensive version</step>
    <step>Determine archive destinations using category naming:
      - archive/implementation-history/
      - archive/migration-planning/
      - archive/phase-planning/
      - archive/consolidated-sources/
    </step>
    <step>Present plan to user for confirmation</step>
  </phase>

  <phase name="execution">
    <step>Use create-memory-note skill for merged note:</step>
    <substep>Follow full verification workflow</substep>
    <substep>Include all unique content from sources</substep>
    <substep>Verify relations (no self-refs, no cross-project WikiLinks)</substep>
    <step>Move originals to archive/{category}/ with move_note()</step>
    <step>Update relations in other notes to point to consolidated version</step>
    <step>Check if any consolidated notes were entry points in per-project index</step>
    <step>If YES: update per-project index — replace old entry-point links with consolidated note link using edit_note()</step>
  </phase>

  <phase name="verification">
    <step>Use verify-memory-relations skill on new note</step>
    <step>Confirm no quality issues introduced</step>
  </phase>

  <phase name="reporting">
    <step>Report changes made</step>
    <step>Show before/after metrics</step>
    <step>List archived notes and their destinations</step>
  </phase>
</workflow>

<archive_categories>
  <category name="implementation-history">Superseded implementations</category>
  <category name="migration-planning">Outdated planning documents</category>
  <category name="phase-planning">Incremental phase notes merged into complete</category>
  <category name="consolidated-sources">Individual notes merged into comprehensive</category>
</archive_categories>
