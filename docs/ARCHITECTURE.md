# Basic Memory Toolkit Architecture

## Four-Tier Design

The plugin is organized into four tiers, each with distinct responsibilities:

```
┌─────────────────────────────────────────────┐
│  Tier 4: Agent (memory-organizer)           │
│  Autonomous multi-project operations        │
│  Uses skills internally for all operations  │
├─────────────────────────────────────────────┤
│  Tier 3: Skills (13 skills)                 │
│  ├── Core: create/update/verify notes       │
│  └── Maintenance: consolidate/optimize/     │
│      archive/audit/batch-fix/capture        │
├─────────────────────────────────────────────┤
│  Tier 2: Rules Project (memory-rules)       │
│  Authoritative quality standards            │
│  Consulted before all note operations       │
├─────────────────────────────────────────────┤
│  Tier 1: Guide (basic-memory-guide.md)      │
│  Loaded at session start                    │
│  Provides MCP tool reference & conventions  │
└─────────────────────────────────────────────┘
```

### Tier 1: Guide

`references/basic-memory-guide.md` is loaded into the session context and provides:
- MCP tool reference (write_note, read_note, search_notes, etc.)
- Project list and when-to-use guidance
- Semantic markup format (observations, relations, WikiLinks)
- Cross-project memory:// URL format

### Tier 2: Rules Project

The `memory-rules` Basic Memory project contains authoritative quality standards:
- **anti-patterns/**: Self-referential relations, cross-project WikiLinks, generic titles
- **creating-notes/**: Relation rules, new note checklist, title standards
- **organizing/**: Consolidation criteria, archive protocols, folder patterns
- **quality/**: Observation standards, pre-publish checklist
- **updating-notes/**: Edit vs rewrite decision, relation verification

Skills consult these rules via `search_notes(project="memory-rules")` before operations.

### Tier 3: Skills

Skills are divided into core (atomic operations) and maintenance (workflows):

**Core Skills** — Used for every note operation:
- `create-memory-note`: Full rule enforcement, duplicate detection, relation verification
- `update-memory-note`: Edit vs rewrite decision, post-update verification
- `verify-memory-relations`: Self-ref, cross-project, broken link, informal section detection

**Maintenance Skills** — Compose core skills for workflows:
- `consolidate-notes`, `optimize-graph`, `organize-archive`, `audit-quality`
- `batch-fix-wikilinks`, `knowledge-capture`, `spec-driven-development`, `validate-project`

**Discovery Skills** — Cross-project navigation:
- `cross-project-search`, `create-new-memory-project`

### Tier 4: Agent

`memory-organizer` is an autonomous agent that:
- Uses skills internally (never bypasses them)
- Navigates multiple projects
- Handles bulk operations (consolidation, graph optimization, quality audits)
- Supports both direct and plugin-qualified MCP tool names

## Validation Architecture

Two-tier validation separates speed-critical from thoroughness-critical checks:

```
                    ┌──────────────────────┐
                    │   Note Write/Edit    │
                    └──────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼─────────┐   ┌──────────▼──────────┐
    │  Tier 1: Inline   │   │  Tier 2: CLI        │
    │  hook_validator.py │   │  run_all.py         │
    │  ~20ms             │   │  ~7s/note           │
    │  Parses stdin      │   │  Uses basic-memory  │
    │                    │   │  CLI commands        │
    │  Checks:           │   │                     │
    │  • Self-reference  │   │  Checks:            │
    │  • Missing rels    │   │  • Broken WikiLinks │
    │  • relates_to      │   │  • Cross-project    │
    │  • Informal sects  │   │  • All Tier 1 +     │
    │                    │   │    existence checks  │
    │  Used by:          │   │                     │
    │  PreToolUse hook   │   │  Used by:           │
    │  PostToolUse hook  │   │  /validate-project  │
    └────────────────────┘   │  Batch operations   │
                             └─────────────────────┘
```

**Why two tiers?** The `basic-memory` CLI takes ~7s per invocation due to Python interpreter startup, module loading, and database connection. Hooks need <50ms response time for acceptable UX.

## Hook Architecture

```
SessionStart ──→ Project detection, selection prompt
     │
UserPromptSubmit ──→ Memory trigger detection
     │
PreToolUse (write_note) ──→ Tier 1 blocking validation
     │                       Denies self-referential writes
     │
  [write_note executes]
     │
PostToolUse (write/edit) ──→ Tier 1 warning validation
     │                        Reports quality issues
     │
PreCompact ──→ Context preservation prompt
     │
Stop ──→ Suggest /remember for insight capture
```

## Schema System

Picoschema definitions in `schemas/` provide structured note types:

- Created as Basic Memory notes with `type: schema` and `entity: [note-type]`
- Validation modes: `warn` (default), `strict`, `off`
- Skills reference schemas when creating notes of matching types
- `schema_validate`, `schema_diff`, `schema_infer` MCP tools for management

## Command Architecture

Slash commands in `commands/` provide quick-access workflows:

- Commands are instructions FOR Claude (not user-facing docs)
- Each command delegates to appropriate skills rather than duplicating logic
- Commands handle project selection gracefully (use active or ask)
- Follow-up prompts guide users to next actions

## Cross-Project References

Basic Memory WikiLinks (`[[Target]]`) are project-scoped. For cross-project:

- **Text format**: `"Note Title" (project-name)` — in note content
- **Memory URLs**: `memory://project/folder/note` — for unambiguous references
- **WikiLinks**: Only within same project

## Directory Conventions

```
project/
├── sessions/     — Work session summaries
├── decisions/    — Architecture/design decisions
├── insights/     — Discoveries and lessons learned
├── technical/    — Implementation details
├── issues/       — Problems, bugs, troubleshooting
├── procedures/   — Step-by-step guides
├── testing/      — Test strategies and results
├── archive/      — Historical content (subcategorized)
│   ├── implementation-history/
│   ├── consolidated-sources/
│   └── deprecated-patterns/
└── [Project] Index.md  — Entry point
```
