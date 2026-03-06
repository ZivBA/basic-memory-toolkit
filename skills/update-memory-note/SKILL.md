---
name: update-memory-note
description: Update existing memory note with rule enforcement and relation verification
---

<purpose>
Atomic note update skill that enforces memory-rules when modifying notes.
Use this skill for EVERY note update to maintain quality standards.
</purpose>

<workflow>
  <phase name="pre-update">
    <step>Read rules from memory-rules project:
      - search_notes(query="Edit vs Rewrite Decision", project="memory-rules")
    </step>
    <step>Read current note to understand existing content:
      - read_note(identifier="note-title", project="target-project")
    </step>
    <step>Determine operation type: edit_note() vs write_note()</step>
  </phase>

  <phase name="operation-decision">
    <decision>
      <use_edit_note>
        <when>Adding content to end (append)</when>
        <when>Adding content to start (prepend)</when>
        <when>Replacing specific text (find_replace)</when>
        <when>Updating one section (replace_section)</when>
      </use_edit_note>
      <use_write_note>
        <when>Major restructure (50%+ content change)</when>
        <when>Fixing multiple sections</when>
        <when>Complete content overhaul</when>
      </use_write_note>
    </decision>
  </phase>

  <phase name="relation-verification" condition="if adding/modifying relations">
    <step>For EACH new relation:</step>
    <step>1. Search for target: search_notes(query="target", project="current")</step>
    <step>2. Verify target exists</step>
    <step>3. Verify target ≠ current note title (NO SELF-REFERENCE)</step>
    <step>4. Verify same project (or use text format)</step>
    <step>5. Copy exact title from search results</step>
  </phase>

  <phase name="execution">
    <if_edit_note>
      <step>Get exact identifier: search_notes() first if uncertain</step>
      <step>Execute edit_note(identifier, operation, content, project)</step>
      <operations>append, prepend, find_replace, replace_section</operations>
    </if_edit_note>
    <if_write_note>
      <step>Prepare complete content with all elements</step>
      <step>Follow create-memory-note workflow for full verification</step>
      <step>Execute write_note()</step>
    </if_write_note>
  </phase>

  <phase name="post-update-verification">
    <step>Read updated note: read_note()</step>
    <step>Verify changes applied correctly</step>
    <step>Check for self-referential relations in Relations section</step>
    <step>Confirm no cross-project WikiLinks introduced</step>
  </phase>
</workflow>

<edit_operations>
  <append>Add content to end of note</append>
  <prepend>Add content to beginning</prepend>
  <find_replace>Replace specific text (use find_text parameter)</find_replace>
  <replace_section>Replace entire section (use section parameter)</replace_section>
</edit_operations>

<rules_reference>
  <project>memory-rules</project>
  <edit_decision>updating-notes/Edit vs Rewrite Decision</edit_decision>
  <verification>updating-notes/Relation Verification After Edit</verification>
  <relations>creating-notes/Relation Creation Rules</relations>
</rules_reference>

<critical_rules>
  <rule>edit_note() requires EXACT identifier - search first if uncertain</rule>
  <rule>Verify relations after ANY edit touching Relations section</rule>
  <rule>Use create-memory-note skill if doing complete rewrite</rule>
</critical_rules>
