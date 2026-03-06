---
name: create-new-memory-project
description: "This skill should be used when creating a new Basic Memory project, the user asks to 'create a new memory project', 'add a new project', 'set up a new project for X', or when the memory-organizer agent needs to establish a new project with proper index registration."
version: 1.0.0
---

<purpose>
Atomic skill for creating new Basic Memory projects with full index registration.
Enforces creation criteria, creates per-project index note, and registers in global PROJECT_DIRECTORY.
</purpose>

<creation_criteria>
  <create_when>
    <criterion>Work spans 10+ notes on a distinct, bounded domain</criterion>
    <criterion>The domain has its own codebase/repository</criterion>
    <criterion>Notes would create noise in existing projects' search results</criterion>
  </create_when>
  <reject_when>
    <criterion>Topic fits within an existing project's scope — add notes there instead</criterion>
    <criterion>Temporary investigation — use a folder in the relevant project</criterion>
    <criterion>Fewer than ~5 notes expected — not worth the overhead</criterion>
    <criterion>Cross-cutting concern — belongs in development-practices or infrastructure</criterion>
    <criterion>Truly cross-cutting with no domain — use main</criterion>
  </reject_when>
</creation_criteria>

<workflow>
  <phase name="validate">
    <step>Review creation vs rejection criteria against the proposed project</step>
    <step>Call list_memory_projects() to check for existing project overlap</step>
    <step>Search existing projects for related content that might already cover this domain</step>
    <step>If criteria not met, recommend alternative (existing project, folder, or main)</step>
  </phase>

  <phase name="discover-relations">
    <step>Use cross-project-search skill to identify related projects</step>
    <step>Note related projects for the per-project index (use text format, not WikiLinks)</step>
  </phase>

  <phase name="create-project">
    <step>Call create_memory_project(name="project-name")</step>
    <step>Verify creation with list_memory_projects()</step>
  </phase>

  <phase name="create-per-project-index">
    <step>Write per-project index note using the template below</step>
    <step>Use write_note(title="[Project Name] Index", folder="", tags=["index", "landing-page"], project="new-project")</step>
    <step>Include purpose, initial entry-point notes (if any exist), and related projects</step>
  </phase>

  <phase name="register-globally">
    <step>Read current PROJECT_DIRECTORY from main project:
      - read_note(identifier="project-directory", project="main")
    </step>
    <step>Add new entry following the global index entry template</step>
    <step>Use edit_note() to append the new project entry to PROJECT_DIRECTORY</step>
  </phase>

  <phase name="register-guide">
    <step>Update basic_memory_guide.md project list if accessible</step>
    <step>Add new project with purpose and when_to_use</step>
  </phase>
</workflow>

<per_project_index_template>
  <description>Minimal landing-page note, ~20-30 lines. Created in the root folder of the new project.</description>
  <format>
# [Project Name] Index

## Purpose
[1-2 sentences describing what this project covers]

## Key Notes
- [[Key Note Title 1]] — brief description
- [[Key Note Title 2]] — brief description
[3-5 entry points maximum, added as notes are created]

## Related Projects
- "Related Note Title" (other-project) — how it relates
[Text format, NOT WikiLinks — WikiLinks don't cross project boundaries]
  </format>
</per_project_index_template>

<global_index_entry_template>
  <description>Entry format for PROJECT_DIRECTORY in main project</description>
  <format>
### project-name
**Purpose:** One-line description of what this project covers
**When to use:** Brief trigger criteria for when to add notes here
  </format>
</global_index_entry_template>

<index_update_principle>
Index updates are the exception, not the rule. Only structural changes
(new topic areas, removed entry points, consolidation of key notes)
warrant an update. Most note operations do not touch the index.
</index_update_principle>

<critical_rules>
  <rule>ALWAYS validate against creation/rejection criteria before creating</rule>
  <rule>ALWAYS create per-project index note immediately after project creation</rule>
  <rule>ALWAYS register in global PROJECT_DIRECTORY in main</rule>
  <rule>Use TEXT format for cross-project references in per-project index (not WikiLinks)</rule>
  <rule>Keep per-project index minimal: purpose + 3-5 entry points + related projects</rule>
</critical_rules>

<rules_reference>
  <project>memory-rules</project>
  <new_note>creating-notes/New Note Checklist</new_note>
  <relations>creating-notes/Relation Creation Rules</relations>
  <cross_project>anti-patterns/Cross-Project WikiLinks Anti-Pattern</cross_project>
  <index>Per-project index note and global PROJECT_DIRECTORY</index>
</rules_reference>
