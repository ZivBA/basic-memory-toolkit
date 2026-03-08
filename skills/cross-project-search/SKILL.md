---
name: cross-project-search
version: 1.0.0
description: This skill should be used when searching across multiple Basic Memory projects, the user asks to "search all projects", "find across projects", "cross-project search for X", or when synthesizing information that may span multiple project boundaries.
---

<purpose>
Discovery skill for searching across project boundaries.
References memory-rules for cross-project reference format.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <cross_project>anti-patterns/Cross-Project WikiLinks Anti-Pattern</cross_project>
  <core_skill>create-memory-note (if creating synthesis note)</core_skill>
</rules_reference>

<workflow>
  <phase name="load-rules">
    <step>Read cross-project reference rules:
      - search_notes(query="Cross-Project WikiLinks", project="memory-rules")
    </step>
  </phase>

  <phase name="scoping">
    <step>Identify topic/concept to search</step>
    <step>Determine potentially relevant projects based on topic</step>
    <step>Confirm project list with user if not specified</step>
  </phase>

  <phase name="sequential_search">
    <step>Search each project sequentially for the topic</step>
    <step>Use consistent search terms across projects</step>
    <step>Track which project yielded which results</step>
  </phase>

  <phase name="content_review">
    <step>Read matching notes from each project</step>
    <step>Extract unique insights from each</step>
    <step>Identify commonalities and differences</step>
    <step>Note any contradictions or inconsistencies</step>
  </phase>

  <phase name="synthesis">
    <step>Synthesize findings with project attribution</step>
    <step>Use TEXT FORMAT for cross-project references (NOT WikiLinks):
      - "Note Title" (project-name)
      - WikiLinks don't cross project boundaries
    </step>
    <step>Identify service-specific vs reusable patterns</step>
    <step>Determine if cross-cutting note needed in "main" project</step>
  </phase>

  <phase name="note-creation" condition="if creating synthesis note">
    <step>Use create-memory-note skill</step>
    <step>Follow full verification workflow</step>
    <step>Use text references for cross-project sources</step>
  </phase>

  <phase name="reporting">
    <step>Present comprehensive findings structured by project</step>
    <step>Highlight unique insights from each project</step>
    <step>Note contradictions or gaps</step>
    <step>Suggest next steps (create main note, update existing, etc.)</step>
  </phase>
</workflow>

<project_discovery>
  <step>Call list_memory_projects() for dynamic project list — never rely on hardcoded names</step>
  <step>Read PROJECT_DIRECTORY from main project for descriptions and when_to_use hints:
    - read_note(identifier="project-directory", project="main")
  </step>
  <step>Use project descriptions to determine which projects are relevant to the search topic</step>
  <step>When entering a project, read its per-project index note first for orientation:
    - search_notes(query="Index", project="target-project", tags=["index"])
  </step>
</project_discovery>

<cross_project_reference_format>
  <correct>"Note Title" (project-name)</correct>
  <correct_url>memory://project-name/folder/Note Title</correct_url>
  <wrong>[[Note Title]] for different project</wrong>
  <verify>Search target project first to confirm note exists</verify>
  <url_format>
    Use memory:// URLs for unambiguous cross-project references:
    - memory://main/docs/authentication
    - memory://edifact-pipeline/pipeline-integration/EDIFACT PNR Processing Pipeline
    URLs without project name still work for same-project: memory://folder/title
  </url_format>
</cross_project_reference_format>

<placement_decision>
  <keep_distributed>When implementations are truly service-specific to one project</keep_distributed>
  <elevate_to_practices>When pattern is reusable across services — check development-practices</elevate_to_practices>
  <elevate_to_infra>When pattern applies to deployment/Docker — check infrastructure</elevate_to_infra>
  <elevate_to_main>When truly universal and cross-cutting — check main</elevate_to_main>
  <consult_directory>When unsure, consult PROJECT_DIRECTORY for project scope descriptions</consult_directory>
</placement_decision>
