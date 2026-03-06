---
name: create-memory-note
description: This skill should be used when creating a new note in Basic Memory, the user asks to "write a memory note", "create a note", "save this to memory", or when the memory-organizer agent needs to create notes with full rule enforcement.
version: 1.0.0
---

<purpose>
Atomic note creation skill that enforces all memory-rules before write_note().
Use this skill for EVERY new note creation to ensure quality standards.
</purpose>

<workflow>
  <phase name="pre-creation">
    <step>Read rules from memory-rules project:
      - search_notes(query="New Note Checklist", project="memory-rules")
      - search_notes(query="Relation Creation Rules", project="memory-rules")
    </step>
    <step>Search current project for duplicates:
      - search_notes(query="topic keywords", project="target-project")
    </step>
    <step>If potential duplicate found, decide: update existing or create new</step>
  </phase>

  <phase name="content-preparation">
    <step>Prepare title: Specific, searchable, follows templates</step>
    <step>Prepare observations: 3-5 with specific categories</step>
    <step>Prepare tags: 3-5 relevant, lowercase hyphenated</step>
    <step>Choose folder: Appropriate for content type</step>
  </phase>

  <phase name="relation-verification">
    <step>For EACH planned relation:</step>
    <step>1. Search for target: search_notes(query="target title", project="current")</step>
    <step>2. Verify target exists in search results</step>
    <step>3. Verify target ≠ current note title (NO SELF-REFERENCE)</step>
    <step>4. Verify target in same project (or use text format for cross-project)</step>
    <step>5. Copy exact title from search results</step>
    <step>6. Choose specific relation type (not generic relates_to)</step>
  </phase>

  <phase name="final-checklist">
    <step>Before write_note(), verify:</step>
    <step>- [ ] Title is specific and unique</step>
    <step>- [ ] 3-5 observations with categories</step>
    <step>- [ ] 2-3+ relations, all verified</step>
    <step>- [ ] No self-referential relations</step>
    <step>- [ ] No cross-project WikiLinks</step>
    <step>- [ ] Tags are relevant and searchable</step>
    <step>- [ ] Folder is appropriate</step>
  </phase>

  <phase name="creation">
    <step>Execute write_note() with prepared content</step>
    <step>Verify creation: read_note() to confirm</step>
    <step>Check resolved vs unresolved relations in response</step>
  </phase>

  <phase name="index-assessment">
    <step>After creating the note, assess: does this introduce a NEW topic area to the project?</step>
    <step>Indicators of new topic area:
      - First note in a new folder/category
      - Describes a completely new concept not covered by existing notes
      - Would be useful as an entry point for understanding the project
    </step>
    <step>If YES: read per-project index note, append new entry-point link using edit_note()</step>
    <step>If NO (most cases): no index change needed</step>
  </phase>
</workflow>

<rules_reference>
  <project>memory-rules</project>
  <anti_patterns>anti-patterns/Self-Referential Relations Anti-Pattern</anti_patterns>
  <anti_patterns>anti-patterns/Cross-Project WikiLinks Anti-Pattern</anti_patterns>
  <anti_patterns>anti-patterns/Generic Titles Anti-Pattern</anti_patterns>
  <checklist>creating-notes/New Note Checklist</checklist>
  <relations>creating-notes/Relation Creation Rules</relations>
  <titles>creating-notes/Title and Metadata Standards</titles>
  <observations>quality/Observation Standards</observations>
  <final_check>quality/Pre-Publish Checklist</final_check>
  <index>Per-project index note — update only for new topic areas</index>
</rules_reference>

<critical_rules>
  <rule>NEVER create self-referential relations (target = current note)</rule>
  <rule>ALWAYS search and verify relation targets before adding</rule>
  <rule>Use text format "Title" (project) for cross-project references</rule>
  <rule>Use specific relation types: implements, requires, part_of, extends</rule>
</critical_rules>
