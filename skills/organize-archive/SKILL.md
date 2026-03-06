---
name: organize-archive
description: This skill should be used when reviewing a project for outdated or superseded content, the user asks to "archive old notes", "organize archive", "clean up outdated content", or when the memory-organizer agent identifies content for archival.
version: 1.0.0
---

<purpose>
Maintenance skill for archiving outdated content.
References memory-rules for archive protocols and folder patterns.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <archive>organizing/Archive Protocols</archive>
  <folders>organizing/Folder Structure Patterns</folders>
  <core_skill>update-memory-note (for updating references)</core_skill>
  <index>Per-project index note — update when archiving removes entry points</index>
</rules_reference>

<workflow>
  <phase name="load-rules">
    <step>Read archive protocols from memory-rules:
      - search_notes(query="Archive Protocols", project="memory-rules")
      - search_notes(query="Folder Structure", project="memory-rules")
    </step>
  </phase>

  <phase name="discovery">
    <step>Search for keywords indicating outdated content</step>
    <step>Use recent_activity() to find notes not modified in 60+ days</step>
    <step>Review archive/ folder current state</step>
  </phase>

  <phase name="candidate_review">
    <step>Read candidate notes to assess current relevance</step>
    <step>Identify archive indicators:
      - Superseded implementations
      - Outdated planning documents
      - Notes consolidated elsewhere
      - Completed/closed items
    </step>
  </phase>

  <phase name="categorization">
    <step>Group candidates by archive category</step>
    <step>Use descriptive category names (NOT dates):
      - archive/implementation-history/
      - archive/migration-planning/
      - archive/phase-planning/
      - archive/deprecated-patterns/
      - archive/consolidated-sources/
    </step>
  </phase>

  <phase name="planning">
    <step>Create archive organization plan</step>
    <step>Map each note to archive/{category}/ destination</step>
    <step>Identify notes that reference soon-to-be-archived content</step>
    <step>Present plan to user for confirmation</step>
  </phase>

  <phase name="execution">
    <step>Move notes to appropriate archive/{category}/ folders:
      - move_note(identifier, destination_path="archive/category/", project)
    </step>
    <step>Use update-memory-note skill to update references in active notes</step>
    <step>Maintain permalinks and graph integrity</step>
    <step>Check if any archived notes were entry points in per-project index</step>
    <step>If YES: update per-project index — remove stale entry-point links using edit_note()</step>
  </phase>

  <phase name="reporting">
    <step>Report archive organization</step>
    <step>Show archive structure with counts</step>
    <step>List updated references</step>
  </phase>
</workflow>

<archive_indicators>
  <keyword>old, deprecated, superseded, legacy, outdated</keyword>
  <age>Not modified in 60+ days AND content is superseded or outdated (stable reference material should NOT be archived based on age alone)</age>
  <status>Marked as completed/archived in content</status>
  <consolidation>Merged into comprehensive note</consolidation>
  <implementation>Replaced by newer implementation</implementation>
</archive_indicators>

<archive_categories>
  <implementation_history>Superseded implementations and old code approaches</implementation_history>
  <migration_planning>Outdated planning documents for completed migrations</migration_planning>
  <phase_planning>Individual phase notes consolidated into complete implementation</phase_planning>
  <deprecated_patterns>Historical analysis or patterns no longer recommended</deprecated_patterns>
  <consolidated_sources>Original notes merged into comprehensive versions</consolidated_sources>
</archive_categories>

<preservation_principle>
  <never_delete>Archive instead of deleting</never_delete>
  <context>Preserve historical context and reasoning</context>
  <structure>Organize by meaningful categories (not dates)</structure>
  <references>Update active notes to point to current content</references>
</preservation_principle>
