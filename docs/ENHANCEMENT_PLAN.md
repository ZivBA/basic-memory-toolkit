# Plugin Enhancement Plan v2

## Overview

Comprehensive roadmap for enhancing the basic-memory-toolkit plugin from v1.1.5 to v2.0.
Focus: development-specific knowledge management with validated writes, better UX, and schema-driven quality.

**Memory project**: basic-memory-toolkit (memory://basic-memory-toolkit/)
**Repository**: /home/zivben/repos/basic-memory-toolkit

---

## Phase 1: Validation Infrastructure

**Goal**: Replace prompt-based PostToolUse hooks with deterministic Python validators.
**Impact**: 85x faster validation, zero LLM cost, 100% consistency.

### 1.1 Create Validator Modules

Location: `validators/`

```
validators/
├── __init__.py              # Common utilities (parse note, extract relations)
├── self_reference.py        # BLOCKING: from_entity = to_entity
├── cross_project.py         # BLOCKING: WikiLinks across project boundaries
├── broken_wikilinks.py      # WARNING: targets that don't exist
├── relation_quality.py      # WARNING: count, types, relates_to overuse
├── section_format.py        # WARNING: informal "Related" sections
├── index_relations.py       # WARNING: index using relates_to instead of documents
└── run_all.py               # Orchestrator with blocking/warning modes
```

Each module:
- Accepts note title + project as CLI args
- Uses `basic-memory tool read-note --format json` for data
- Uses `basic-memory tool search-notes` for existence checks
- Returns exit code 0 (pass) or 1 (fail) with structured output
- Is importable as a Python module for future server use

### 1.2 Move to PreToolUse Validation

Update `hooks/hooks.json`:
- Add PreToolUse hook on `write_note` — runs blocking validators (self-ref, cross-project)
- Keep PostToolUse for warning-level checks (broken links, quality)
- Remove current prompt-based PostToolUse quality check

### 1.3 Add Stop Hook

New hook: After conversation stop, suggest capturing insights:
```
"Stop": [{
  "hooks": [{
    "type": "prompt",
    "prompt": "If significant technical decisions, insights, or patterns were discussed, suggest: 'Would you like me to capture key insights from this session using /remember?'"
  }]
}]
```

### Deliverables
- [x] `validators/__init__.py` — parse utilities
- [x] `validators/self_reference.py` — self-ref detection
- [x] `validators/cross_project.py` — cross-project WikiLink detection
- [x] `validators/broken_wikilinks.py` — broken link detection
- [x] `validators/relation_quality.py` — count + type quality
- [x] `validators/section_format.py` — informal section detection
- [x] `validators/index_relations.py` — index relation type check (merged into relation_quality.py)
- [x] `validators/run_all.py` — orchestrator
- [x] Updated `hooks/hooks.json` — PreToolUse + PostToolUse + Stop
- [ ] Tests for each validator (deferred to post-beta)

---

## Phase 2: Slash Commands

**Goal**: Add interactive commands for common workflows, adapted from official plugin for development context.

### 2.1 Commands to Add

Location: `commands/`

| Command | Purpose | Adaptation from Official |
|---------|---------|------------------------|
| `/remember [title] [folder]` | Capture insights with dev context | Add observation category selection |
| `/continue [topic]` | Resume previous work session | Add project-aware context building |
| `/organize [action] [project]` | Graph health analysis | Add relation type quality metrics |
| `/research <topic> [folder]` | Structured investigation | Add cross-project search |

### 2.2 Development-Specific Commands

| Command | Purpose |
|---------|---------|
| `/dev-session [project]` | Start a dev session with context from recent activity |
| `/capture-decision` | Structured decision capture with options/rationale template |
| `/validate-project [project]` | Run full validation across all notes in a project |

### Deliverables
- [x] `commands/remember.md`
- [x] `commands/continue.md`
- [x] `commands/organize.md`
- [x] `commands/research.md`
- [x] `commands/dev-session.md`
- [x] `commands/capture-decision.md`
- [x] `commands/validate-project.md`

---

## Phase 3: Skill Enhancements

**Goal**: Improve existing skills and add new development-focused skills.

### 3.1 Existing Skill Updates

| Skill | Enhancement |
|-------|-------------|
| create-memory-note | Add index note guidance (use documents/encompasses, not relates_to) |
| create-memory-note | Add note_type parameter usage |
| verify-memory-relations | Add informal section detection ("Related Components" etc.) |
| optimize-graph | Add batch-fix capability reference |
| cross-project-search | Use memory://project/folder/note URL format |

### 3.2 New Skills

| Skill | Purpose |
|-------|---------|
| batch-fix-wikilinks | Find/replace broken WikiLinks across a project |
| knowledge-capture | Auto-capture decisions/insights during dev conversations |
| spec-driven-development | Align implementation with specs in memory |
| validate-project | Run validators across all notes, generate report |

### Deliverables
- [x] Updated `skills/create-memory-note/SKILL.md`
- [x] Updated `skills/verify-memory-relations/SKILL.md`
- [x] Updated `skills/optimize-graph/SKILL.md`
- [x] Updated `skills/cross-project-search/SKILL.md`
- [x] `skills/batch-fix-wikilinks/SKILL.md`
- [x] `skills/knowledge-capture/SKILL.md`
- [x] `skills/spec-driven-development/SKILL.md`
- [x] `skills/validate-project/SKILL.md`

---

## Phase 4: Agent Fix & Schema System

### 4.1 Agent Tool Name Investigation

The memory-organizer agent lists tools as `mcp__basic-memory__write_note` but actual tool names may be `mcp__plugin_basic-memory-toolkit_basic-memory__write_note`.

- [x] Verify actual tool names available in agent context
- [x] Update `agents/memory-organizer.md` tool list if needed
- [x] Test agent write capability after fix

### 4.2 Schema Definitions

Location: `schemas/` (as seed content for memory-rules or target projects)

Development-focused schema types:
- [x] `bug-report` — severity, affected service, root cause, fix
- [x] `fix-record` — changes made, files modified, testing, regression risk
- [x] `design-decision` — context, options, chosen, rationale, reversibility
- [x] `architecture-constraint` — type, description, affected components, workarounds
- [x] `framework-limitation` — framework, version, limitation, impact, workaround
- [x] `session-artifact` — date, accomplishments, issues, next steps
- [x] `index-note` — project name, focus areas, documents/encompasses relations
- [x] `code-pattern` — type, language, context, when to use

### 4.3 Observation Categories

Add development-specific categories to Observation Standards:
- `constraint` — Limitations, boundaries
- `risk` — Potential problems, technical debt

---

## Phase 5: Advanced Features

### 5.1 MCP Feature Adoption
- [x] Use `note_type` parameter in all write operations
- [x] Use `search_type="semantic"` for duplicate detection
- [x] Use `metadata_filters` in quality audits
- [x] Use `memory://project/folder/note` cross-project URL format in documentation

### 5.2 Documentation
- [x] `docs/ARCHITECTURE.md` — Four-tier design explanation
- [x] Update `README.md` — Comprehensive feature list
- [x] Update `references/basic-memory-guide.md` — Cross-project URL format

---

## Version Milestones

| Version | Phases | Key Features |
|---------|--------|-------------|
| v1.2.0 | Phase 1 | Script-based validators, PreToolUse hook |
| v1.3.0 | Phase 2 | Slash commands |
| v1.4.0 | Phase 3 | Skill enhancements, new skills |
| v2.0.0 | Phase 4-5 | Schemas, agent fix, advanced MCP features |

---

## Technical Notes

### Cross-Project Memory URLs
Basic Memory supports project-qualified URLs:
```
memory://main/docs/authentication
memory://edifact-pipeline/pipeline-integration/EDIFACT PNR Processing Pipeline
```
Existing links without project name still work. Our documentation and skills should reference this format.

### Validator Design Principle
All validators are Python modules that:
1. Work standalone via CLI: `python -m validators.self_reference <project> <note_title>`
2. Are importable: `from validators.self_reference import check`
3. Return structured results (JSON on stdout, exit code for pass/fail)
4. Can be wrapped in FastAPI later with zero rewrite

### Hook Architecture After Phase 1
```
PreToolUse (write_note):
  → command hook: run_all.py --mode blocking
  → blocks write if self-ref or cross-project WikiLink detected

PostToolUse (write_note):
  → command hook: run_all.py --mode warning
  → warns about broken links, quality issues (doesn't block)

Stop:
  → prompt hook: suggest /remember for insight capture

SessionStart:
  → command hook: session-start (project selection)

PreCompact:
  → prompt hook: preserve context
```
