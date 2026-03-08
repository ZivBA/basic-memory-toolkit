---
name: validate-project
description: Run the full validation suite across all notes in a Basic Memory project, producing a comprehensive quality report. Use when the user invokes /validate-project or wants a full project health check.
---

<purpose>
Project-wide validation skill that orchestrates all validators.
Produces a structured report of issues across all notes.
Complements /validate-project command with skill-level guidance.
</purpose>

<rules_reference>
  <project>memory-rules</project>
  <validators>${CLAUDE_PLUGIN_ROOT}/validators/</validators>
  <core_skill>verify-memory-relations (per-note checks)</core_skill>
  <core_skill>batch-fix-wikilinks (for bulk fixes)</core_skill>
  <core_skill>optimize-graph (for graph-level analysis)</core_skill>
</rules_reference>

<workflow>
  <phase name="project-selection">
    <step>Identify target project from user or /validate-project argument</step>
    <step>Confirm project exists via list_memory_projects()</step>
  </phase>

  <phase name="note-inventory">
    <step>Get all notes: search_notes(query="*", project=target)</step>
    <step>Count total notes for progress tracking</step>
    <step>Warn user if project has 50+ notes (validation will take time)</step>
  </phase>

  <phase name="tier-1-validation">
    <step>For each note, read content and run inline checks (fast, no CLI):
      - Self-referential relations (CRITICAL)
      - Missing ## Relations section (MEDIUM)
      - Insufficient relations count (MEDIUM)
      - Generic relates_to overuse (LOW)
      - Informal relation sections (MEDIUM)
      - Index notes using relates_to (MEDIUM)
    </step>
    <step>These checks parse content directly — same logic as hook_validator.py</step>
  </phase>

  <phase name="tier-2-validation">
    <step>For notes with WikiLinks, run CLI-dependent checks (slower):
      - Broken WikiLinks: search_notes() for each target
      - Cross-project WikiLinks: check if target exists only in other project
    </step>
    <step>Batch these checks efficiently — search for multiple targets per project</step>
  </phase>

  <phase name="report">
    <step>Produce structured report:</step>
    <format>
      ## Project Validation Report: [project-name]

      **Scanned**: [count] notes
      **Issues Found**: [count] (critical: X, warning: Y, suggestion: Z)

      ### Critical Issues
      | Note | Issue | Fix |
      |------|-------|-----|
      | [title] | Self-referential relation | Remove relation |

      ### Warnings
      | Note | Issue | Fix |
      |------|-------|-----|
      | [title] | Broken WikiLink [[Target]] | Search for correct title |

      ### Suggestions
      | Note | Issue | Fix |
      |------|-------|-----|
      | [title] | Only 1 relation | Add connections |

      ### Health Summary
      | Metric | Value | Target |
      |--------|-------|--------|
      | Avg relations/note | X.X | 2.0+ |
      | Notes with 0 relations | X | 0 |
      | Self-referential | X | 0 |
      | Cross-project WikiLinks | X | 0 |
      | Broken WikiLinks | X | 0 |
    </format>
  </phase>

  <phase name="remediation">
    <step>Present fix options:
      1. Fix critical issues now (recommended)
      2. Fix all issues using batch-fix-wikilinks skill
      3. Launch memory-organizer agent for comprehensive fixes
      4. Export report and fix manually
    </step>
    <step>For option 1-2, use appropriate skills with user confirmation</step>
  </phase>
</workflow>

<performance_notes>
  <tier_1>Content parsing: ~instant per note (reads note content, checks patterns)</tier_1>
  <tier_2>CLI validation: ~7s per note (subprocess overhead for basic-memory CLI)</tier_2>
  <optimization>Run Tier 1 on all notes first, then Tier 2 only on notes with WikiLinks</optimization>
  <large_projects>For 50+ notes, suggest running in background or validating subsets</large_projects>
</performance_notes>
