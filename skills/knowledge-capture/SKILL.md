---
name: knowledge-capture
description: Automatically identify and capture technical decisions, insights, patterns, and lessons learned during development conversations. Use when significant knowledge is being generated that should be preserved, or when the Stop hook suggests capturing session insights.
---

<purpose>
Proactive knowledge extraction skill for development conversations.
Identifies valuable knowledge worth preserving and creates structured notes.
Triggered by Stop hook suggestion or explicit user request.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <checklist>creating-notes/New Note Checklist</checklist>
  <observations>quality/Observation Standards</observations>
  <core_skill>create-memory-note (for note creation)</core_skill>
</rules_reference>

<workflow>
  <phase name="extraction">
    <step>Scan the current conversation for knowledge worth capturing:</step>
    <categories>
      <category name="decisions">
        Architectural choices, technology selections, design trade-offs
        Signal words: "decided", "chose", "went with", "because", "trade-off"
      </category>
      <category name="insights">
        Discoveries, "aha moments", non-obvious behaviors
        Signal words: "turns out", "discovered", "realized", "interesting"
      </category>
      <category name="patterns">
        Reusable coding patterns, configurations, workflows
        Signal words: "pattern", "approach", "technique", "workflow"
      </category>
      <category name="issues">
        Bugs found, workarounds applied, limitations hit
        Signal words: "bug", "issue", "workaround", "limitation", "error"
      </category>
      <category name="fixes">
        Solutions to problems, debugging steps that worked
        Signal words: "fixed", "solved", "root cause", "the fix was"
      </category>
    </categories>
  </phase>

  <phase name="deduplication">
    <step>For each candidate, search existing notes to avoid duplicates:
      - search_notes(query="topic keywords", project=active)
    </step>
    <step>If existing note covers same topic:
      - Suggest updating existing note instead of creating new one
      - Use edit_note(operation="append") to add new observations
    </step>
  </phase>

  <phase name="presentation">
    <step>Present candidates to user grouped by category:</step>
    <format>
      I identified these knowledge items worth capturing:

      **Decisions:**
      1. [title] — [one-line summary]

      **Insights:**
      1. [title] — [one-line summary]

      **Issues/Fixes:**
      1. [title] — [one-line summary]

      Which would you like me to save? (all / specific numbers / none)
    </format>
  </phase>

  <phase name="creation">
    <step>For each approved item, use create-memory-note skill</step>
    <step>Choose appropriate folder based on category:
      - decisions/ for architectural decisions
      - insights/ for discoveries and patterns
      - issues/ for bugs and workarounds
      - technical/ for implementation details
      - sessions/ for session summaries
    </step>
    <step>Use development-focused observation categories:
      - [decision] for choices made
      - [technique] for approaches used
      - [issue] for problems encountered
      - [fact] for technical specifics
      - [best-practice] for standards established
      - [risk] for accepted trade-offs
      - [constraint] for limitations discovered
    </step>
  </phase>

  <phase name="confirmation">
    <step>Summarize what was saved with note titles and projects</step>
    <step>Mention unresolved WikiLinks (forward references OK)</step>
  </phase>
</workflow>

<capture_templates>
  <decision>
    Title: "[Choice] Decision" (e.g., "Two-Tier Validation Architecture Decision")
    Observations: [decision], [requirement], [risk], [fact]
    Folder: decisions/
    Relations: implements/extends related components
  </decision>

  <insight>
    Title: "[Discovery] Discovery/Insight" (e.g., "CLI Performance Overhead Discovery")
    Observations: [fact], [technique], [best-practice]
    Folder: insights/
    Relations: relates_to affected components
  </insight>

  <bug_fix>
    Title: "[Component] [Issue] Fix" (e.g., "Parser Timeout on Large EDIFACT Fix")
    Observations: [issue], [fact], [technique]
    Folder: issues/
    Relations: part_of affected service, implements fix approach
  </bug_fix>

  <pattern>
    Title: "[Pattern Name] Pattern" (e.g., "Two-Tier Hook Validation Pattern")
    Observations: [technique], [best-practice], [fact]
    Folder: technical/ or insights/
    Relations: implements/extends related architecture
  </pattern>
</capture_templates>

<anti_patterns>
  <avoid>Capturing trivial configuration changes</avoid>
  <avoid>Creating notes for information already well-documented in code</avoid>
  <avoid>Duplicating existing notes — always search first</avoid>
  <avoid>Generic titles like "Session Notes" or "Discussion"</avoid>
</anti_patterns>
