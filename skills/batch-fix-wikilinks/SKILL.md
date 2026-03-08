---
name: batch-fix-wikilinks
description: Find and fix broken, self-referential, or cross-project WikiLinks across all notes in a Basic Memory project. Use when the optimize-graph skill or /validate-project command identifies WikiLink issues at scale.
---

<purpose>
Bulk repair skill for WikiLink issues across a project.
Handles broken links, cross-project WikiLinks, and self-references in batch.
Use after /validate-project or optimize-graph identifies widespread issues.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <self_ref>anti-patterns/Self-Referential Relations Anti-Pattern</self_ref>
  <cross_project>anti-patterns/Cross-Project WikiLinks Anti-Pattern</cross_project>
  <relation_rules>creating-notes/Relation Creation Rules</relation_rules>
  <core_skill>verify-memory-relations (for detection)</core_skill>
  <core_skill>update-memory-note (for individual fixes)</core_skill>
</rules_reference>

<workflow>
  <phase name="scope">
    <step>Identify the project to fix: confirm with user</step>
    <step>Determine fix categories:
      - broken: WikiLinks to non-existent notes
      - cross-project: WikiLinks that should be text format
      - self-ref: WikiLinks pointing to the note itself
      - informal: Sections like "## See Also" that should be ## Relations
    </step>
    <step>Ask user which categories to fix (default: all)</step>
  </phase>

  <phase name="scan">
    <step>Search all notes in the project: search_notes(query="*", project=target)</step>
    <step>For each note, read content and extract:
      - All WikiLinks from ## Relations section
      - All WikiLinks from body text
      - Informal relation sections
    </step>
    <step>Build issue inventory: {note_title, issue_type, target, suggested_fix}</step>
  </phase>

  <phase name="resolution-plan">
    <step>For broken WikiLinks:
      - Search for similar titles (typo correction)
      - Search other projects (might be cross-project)
      - If no match found, mark for removal or forward-ref decision
    </step>
    <step>For cross-project WikiLinks:
      - Identify which project the target lives in
      - Prepare text-format replacement: "Title" (project-name)
    </step>
    <step>For self-references:
      - Prepare removal of the self-referential relation
      - If the content is useful, convert to an observation
    </step>
    <step>For informal sections:
      - Extract references from informal sections
      - Prepare WikiLink relations to add to ## Relations
      - Plan section removal
    </step>
    <step>Present full plan to user for confirmation before executing</step>
  </phase>

  <phase name="execution">
    <step>Process fixes in batches of 5 notes</step>
    <step>For each note, use edit_note() with appropriate operation:
      - find_replace for WikiLink text changes
      - replace_section for ## Relations rewrites
    </step>
    <step>After each batch, report progress: "Fixed X/Y notes"</step>
  </phase>

  <phase name="verification">
    <step>Re-scan fixed notes to confirm issues resolved</step>
    <step>Report: X issues fixed, Y remaining, Z new issues (if any)</step>
  </phase>
</workflow>

<fix_patterns>
  <broken_wikilink>
    <search>search_notes(query="similar title", project=current)</search>
    <if_found>edit_note: find_replace [[Wrong Title]] with [[Correct Title]]</if_found>
    <if_not_found>Ask user: remove relation, keep as forward-ref, or create target note?</if_not_found>
  </broken_wikilink>

  <cross_project>
    <detect>WikiLink target found only in different project</detect>
    <fix>edit_note: find_replace [[Target]] with "Target" (other-project)</fix>
  </cross_project>

  <self_referential>
    <detect>WikiLink target matches current note title</detect>
    <fix>edit_note: remove the self-referential relation line</fix>
  </self_referential>

  <informal_section>
    <detect>Sections named "See Also", "Related Components", "References", etc.</detect>
    <fix>Extract references, add as WikiLinks to ## Relations, remove informal section</fix>
  </informal_section>
</fix_patterns>

<safety>
  <rule>Always present plan before executing fixes</rule>
  <rule>Process in small batches to allow user to stop if needed</rule>
  <rule>Verify fixes after each batch</rule>
  <rule>Never delete relations without user confirmation</rule>
</safety>
