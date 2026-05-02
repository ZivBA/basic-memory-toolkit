# Schema Activation And SQLite-Based Write-Time Validation — Design Spec

**Date**: 2026-04-19
**Status**: Draft, pending implementation
**Scope**: Cycles 1+2 of a 5-cycle roadmap derived from the 2026-04-19 parallel-agent memory contamination audit
**Target branch**: `feature/schema-activation-and-sqlite-validators`

---

## 1. Problem Statement

The 2026-04-19 audit of two Basic Memory projects found 12 failure modes attributable to parallel-agent work, temporal decay of static claims, and missing mechanical enforcement. Two root causes dominate:

1. **Basic Memory's schema system is effectively inactive in this toolkit.** The plugin ships 8 schemas in `/schemas/*.md`, but they are never seeded into any memory project's `schemas/` folder. Basic Memory's schema resolver only discovers schemas within a project, so our schemas are invisible to it, to `bm schema validate`, and to any downstream tool. As a result, notes are written with `type: note` by default, no structural enforcement, and drift is unchecked.

2. **Write-time validation is limited to content-only checks.** Ghost entities (WikiLinks to nonexistent notes), cross-project references, and structural-schema conformance cannot be verified from the note content alone — they require a project-wide index lookup. The existing `validators/hook_validator.py` does not have access to one, so these checks run only in the batch `/validate-project` pass, after contamination has already landed.

This spec addresses both root causes with a single coherent implementation cycle.

---

## 2. Goals And Non-Goals

### Goals

- **G1**: Activate the schema system by seeding schemas into every project that wants them, and enforcing `type: <entity>` as a mandatory frontmatter field on new notes.
- **G2**: Extend the existing PreToolUse/PostToolUse hook layer with SQLite-backed checks that leverage basic-memory's own database as the authoritative project index.
- **G3**: Keep write-time hook latency under 100ms for the common case.
- **G4**: Preserve graceful degradation — a broken hook must never block a legitimate write.
- **G5**: Provide explicit opt-out so projects can choose "no schemas" as a persistent preference without the session-start hook nudging repeatedly.

### Non-Goals

- Bidirectional atomicity skill pattern (deferred to Cycle 3)
- Branch-aware memory folder structure (deferred to Cycle 4)
- Authoring rules R1–R12 as notes in the `memory-rules` project (deferred to Cycle 5; only `Mandatory Type Declaration` is authored in this cycle)
- Remediation of the already-contaminated `etl-packages` and `mq-backout-monitoring` projects (deferred to Cycle 5)
- Auto-migrating existing un-typed notes to have `type:` fields (separate `/migrate-notes-to-schemas` command, not in this cycle)

---

## 3. Decision Stack

| # | Decision | Chosen |
|---|---|---|
| 1 | Prevent-vs-detect boundary per check | **Locality (hard gate) + Damage-weighted (within eligible set)** |
| 2 | Cache strategy | **Direct SQLite queries against basic-memory's DB** — no separate cache |
| 3 | Schema orphaning | **Fix first**: `/install-schemas` command seeds into projects |
| 4 | `type:` field | **Mandatory on new notes**, advisory on edits of existing notes |
| 5 | Validation implementation language | **Hybrid**: bash fast path (`sqlite3`, `jq`, `ys`) + Python helpers for parameterized SQL and complex checks |
| 6 | Schema format | **Keep picoschema as source of truth**, auto-generate JSON Schema derivatives for fast validation |
| 7 | Schema validation tool | **`ys`** (Rust-based JSON Schema validator) at write time |
| 8 | JSON Schema derivative storage | **Checked in** to project under `.schemas-jsonschema/`, regenerated on source mtime change |
| 9 | Forward references to nonexistent notes | **Must be declared** explicitly in frontmatter `forward_refs: [...]` — undeclared ghost entities block |
| 10 | Per-project severity overrides | **`.memory-toolkit.conf`** YAML file at project root |
| 11 | Schema opt-out signal | **Empty `schemas/` folder** — persistent filesystem-level signal, no config file needed |

---

## 4. Component Inventory

| # | Component | Status | Responsibility |
|---|---|---|---|
| 1 | `seed/schemas/` | NEW | Canonical schema source — copied from plugin's `/schemas` at build time |
| 2 | `commands/install-schemas.md` | NEW | `/install-schemas [project]` slash command — installs/updates schemas into a project |
| 3 | `hooks/session-start` | MODIFIED | Post-project-selection: check for schemas folder state, prompt or auto-regenerate JSON Schema derivatives |
| 4 | `skills/create-memory-project` (or equivalent) | MODIFIED | On new project creation, prompt "initialize with schemas?"; empty folder created on opt-out |
| 5 | `hooks/scripts/sqlite-checks.sh` | NEW | Bash module with reusable SQLite query functions (ghost-entity, cross-project, bidirectional) |
| 6 | `hooks/scripts/sqlite-query.py` | NEW | ~30-line Python helper for parameterized SQL queries (prevents injection risk in bash) |
| 7 | `hooks/scripts/verify-bidirectional.sh` | NEW | PostToolUse script that sweeps a newly-written note's bidirectional relations for missing reverse sides |
| 8 | `hooks/scripts/bidirectional-map.conf` | NEW | Forward/reverse relation-type pairs (supersedes/superseded_by, blocks/blocked_by, etc.) |
| 9 | `hooks/scripts/validate-note` | MODIFIED | Existing bash wrapper; extended to invoke new SQLite checks and `ys` schema validation |
| 10 | `scripts/picoschema-to-jsonschema.py` | NEW | Translator: reads picoschema frontmatter, emits JSON Schema YAML. Runs at `/install-schemas` time only. |
| 11 | `validators/hook_validator.py` | MODIFIED | Extends existing blocking/warning/full modes with new reason codes; invoked as Python fallback when `ys` is missing |
| 12 | `hooks/hooks.json` | MODIFIED | Adds `PostToolUse` wiring for `write_note`/`edit_note` |
| 13 | `memory-rules/creating-notes/Mandatory Type Declaration.md` (authored in memory-rules project) | NEW | Authoritative rule: every new note must declare `type:` matching a schema |

---

## 5. Data Flow: Note Write End-To-End

### Pre-Conditions

- Agent has selected a project in session-start
- Session-start confirmed schemas are installed (`<project>/schemas/` populated, `.schemas-jsonschema/` fresh) OR project is explicitly opted out (empty `schemas/` folder)
- Agent is about to call `mcp__basic-memory__write_note`

### Flow Diagram

```
1. Agent emits write_note(project, title, content, folder, tags)
       │
       ▼
2. PreToolUse hook fires → hooks/scripts/validate-note (bash)
       - jq extracts tool_input fields: project, title, content
       - grep/sed extracts frontmatter block (---…---)
       - grep extracts `type: <entity>` line
       │
       ▼
3. Gate A — Type declaration check
       │
       ├─ Project is opted out (empty schemas/): skip type check, proceed to Gate C
       ├─ `type:` missing/unparseable: BLOCK with MISSING_TYPE
       ├─ `type: note` (free-form): skip Gate B, proceed to Gate C
       ├─ `type: <entity>` matches schema file: proceed to Gate B
       └─ `type: <entity>` with no matching schema: BLOCK with UNKNOWN_TYPE
       │
       ▼
4. Gate B — Schema validation via `ys`
       │
       ├─ Extract frontmatter YAML into temp file
       ├─ Run: ys -f <project>/.schemas-jsonschema/<entity>.yaml <frontmatter-tmp> --fail-fast --json
       ├─ Exit 0: proceed to Gate C
       └─ Exit 1: parse JSON errors, BLOCK with SCHEMA_MISMATCH
       │
       ▼
5. Gate C — SQLite structural checks
       │
       ├─ Extract WikiLink targets from content body
       ├─ Extract `forward_refs:` from frontmatter (Option 2 for ghost handling)
       ├─ For each WikiLink target not in forward_refs:
       │     Query: SELECT 1 FROM entity WHERE title=? AND project_id=?
       │     If zero rows:
       │        Secondary query: SELECT project.name FROM entity JOIN project ... WHERE entity.title=?
       │        If found in another project: WARN (CROSS_PROJECT_WIKILINK)
       │        If not found anywhere: BLOCK (GHOST_ENTITY)
       │
       ▼
6. Gate D — Deep Python checks (only if earlier gates all pass)
       │
       ├─ Bash invokes: python3 validators/hook_validator.py <mode>
       ├─ Python runs: self-reference, section format, relation quality (existing checks)
       └─ Python exits 0 (pass), 2 (block), or emits warnings
       │
       ▼
7. Hook exits 0 → write_note proceeds → basic-memory commits → SQLite updated
       │
       ▼
8. PostToolUse hook fires → hooks/scripts/verify-bidirectional.sh
       │
       ├─ For each bidirectional-typed relation in the newly-written note:
       │     Resolve target entity id via SQLite
       │     Query: SELECT 1 FROM relation WHERE from_id=<target> AND to_name=<source> AND relation_type=<reverse>
       │     If zero: emit WARN (BIDIRECTIONAL_MISSING)
       │
       ▼
9. Write flow complete
```

### Key Properties

- **Fast path is bash-only for Gates A, B, C**. Python only invoked at Gate D and only when earlier gates pass.
- **Ghost-entity detection uses live SQLite state**, not a separate cache. The DB is authoritative.
- **Cross-project WikiLinks are detected for free** — single unified DB, single query.
- **Bidirectional verification is PostToolUse** and warn-only in this cycle. Cycle 3 promotes to block via skill-enforced parallel-write pattern.
- **Error messages are structured deny JSON** per existing hook contract in `hook_validator.py`.

---

## 6. Session-Start And Install Flows

### `/install-schemas [project]` Slash Command

```
1. Resolve project path:
     sqlite3 ~/.basic-memory/memory.db "SELECT path FROM project WHERE name='<project>'"

2. Verify seed source exists at /seed/schemas/*.md in plugin install dir.
   If missing → hard error "Plugin installation is broken, reinstall or report bug."

3. For each seed schema file:
     - Read source version from frontmatter `version:` field
     - Compute source checksum
     - Compare against destination:
        * Dest missing → copy source → dest; translate picoschema → JSON Schema
        * Dest same version → skip (up-to-date)
        * Dest older → diff → prompt "overwrite? [y/n/diff-details]" → act accordingly
        * Dest NEWER than source → warn "Local schema customized. Skipping." (respects local mods)

4. Regenerate JSON Schema derivatives where source mtime > derivative mtime.

5. Write/update manifest: <project>/.schemas-jsonschema/.installed.json
     {schema_name: {version, installed_at, source_checksum}}

6. Report: "Installed N, updated M, skipped K (up-to-date), skipped L (customized)."
```

### Session-Start Hook Enhancement

After existing project-selection logic:

```
After project is confirmed:
  Check <project-path>/schemas/:
    - Does NOT exist:
        Prompt "This project has no schemas/ folder.
                [install / opt-out / skip-this-session]"
        → install: invoke /install-schemas
        → opt-out: mkdir empty schemas/ (persistent signal)
        → skip: no action, re-prompt next session
    - Exists and EMPTY: silent. Opt-out respected.
    - Exists with content, .schemas-jsonschema/ missing or stale:
        Regenerate JSON Schema derivatives silently. No prompt.
    - Exists with content, versions match seed: silent.
    - Exists with content, seed has NEWER versions:
        Prompt "Plugin schemas updated. [update / dismiss-this-session / dismiss-until-next-bump]"
```

### New Project Creation Flow

After project creation succeeds:

```
Prompt: "Initialize with schemas? [yes / no / customize]"
  → yes: invoke /install-schemas <new-project>
  → no: mkdir empty schemas/ (opt-out signal)
  → customize: show schema list → user selects subset → install only selected
```

### Data Model For Version Tracking

Per-project under `<project-path>/.schemas-jsonschema/`:

```
.installed.json
  {
    "design-decision": {"version": 1, "installed_at": "2026-04-19T14:00:00Z", "source_checksum": "sha256:..."},
    "bug-report":      {"version": 1, "installed_at": "2026-04-19T14:00:00Z", "source_checksum": "sha256:..."}
  }
<schema-name>.yaml   # one per installed schema — generated JSON Schema derivative
```

No separate registry. Self-contained per project. Plugin's seed is the authoritative source.

---

## 7. SQLite Check Module

### Module Contract

`hooks/scripts/sqlite-checks.sh` is sourced by `hooks/scripts/validate-note`. Exposes bash functions. Assumes `$BM_DB` (path to basic-memory SQLite DB), `$PROJECT_NAME`, `$PROJECT_ID` are set by the caller.

### Core Queries

**Resolve project ID** (called once per hook invocation):
```sql
SELECT id FROM project WHERE name = ? LIMIT 1;
```

**Ghost-entity check** (blocking in CRITICAL mode):
```sql
SELECT 1 FROM entity WHERE title = ? AND project_id = ? LIMIT 1;
```

**Cross-project detection** (warning, not block):
```sql
SELECT p.name FROM entity e
  JOIN project p ON e.project_id = p.id
  WHERE e.title = ? AND e.project_id != ? LIMIT 1;
```

**Bidirectional relation verification** (PostToolUse, warn-only this cycle):
```sql
-- Step 1: Resolve target's entity id
SELECT id FROM entity WHERE title = ? AND project_id = ? LIMIT 1;

-- Step 2: Check reverse relation exists on target
SELECT 1 FROM relation
  WHERE from_id = ? AND to_name = ? AND relation_type = ? LIMIT 1;
```

**Unresolved-relation sweep** (PostToolUse monitoring, reporting):
```sql
SELECT COUNT(*) FROM relation r
  JOIN entity e ON r.from_id = e.id
  WHERE e.title = ?
    AND r.project_id = ?
    AND r.to_id IS NULL;
```

### Bidirectional Relation Type Map

`hooks/scripts/bidirectional-map.conf`:
```
supersedes|superseded_by
blocks|blocked_by
part_of|contains
requires|required_by
implements|implemented_by
```

Pipe-delimited, one pair per line. `verify-bidirectional.sh` iterates.

### Escaping Strategy

User-controlled strings (titles) going into SQL require careful handling. Decision: bash control flow + Python parameterized-query helper for title-laden queries. Python startup cost (~50ms once per hook invocation) is paid for the safety guarantee.

Calling convention:
```
python3 hooks/scripts/sqlite-query.py --query ghost_entity \
  --param title="<target>" --param project_id=<id>
```

Returns JSON on stdout: `{"found": true|false, "detail": {...}}`.

---

## 8. Error Handling

### Block vs Warn Taxonomy

| Check | Mode | Severity | Reason Code |
|---|---|---|---|
| Missing `type:` field | BLOCK (PreToolUse) | CRITICAL | `MISSING_TYPE` |
| `type:` references non-existent schema | BLOCK | CRITICAL | `UNKNOWN_TYPE` |
| Schema validation failure | BLOCK | CRITICAL | `SCHEMA_MISMATCH` |
| Ghost entity (undeclared) | BLOCK | HIGH | `GHOST_ENTITY` |
| Forward reference (declared in `forward_refs:`) | WARN | LOW | `FORWARD_REF_DECLARED` |
| Cross-project WikiLink | WARN | MEDIUM | `CROSS_PROJECT_WIKILINK` |
| Self-referential relation | BLOCK (existing) | CRITICAL | `SELF_REFERENCE` |
| Unresolved outgoing relations (PostToolUse) | WARN | MEDIUM | `UNRESOLVED_RELATIONS` |
| Missing bidirectional reverse (PostToolUse) | WARN | MEDIUM | `BIDIRECTIONAL_MISSING` |
| Section format drift (existing) | WARN | LOW | `SECTION_FORMAT` |

### PreToolUse Deny JSON Format

On exit code 2, stderr emits:
```json
{
  "permissionDecision": "deny",
  "permissionDecisionReason": "<short human summary>",
  "hookSpecificOutput": {
    "reason_code": "SCHEMA_MISMATCH",
    "reason_detail": "Field 'severity' must be one of [critical, high, medium, low], got 'extreme'",
    "location": "frontmatter.severity",
    "remediation": "Fix the field value in frontmatter and retry, OR change type to 'note' for free-form."
  }
}
```

### PostToolUse Warning Format

On exit code 0, stderr may emit one or more:
```json
{
  "type": "memory_toolkit_warning",
  "check": "BIDIRECTIONAL_MISSING",
  "severity": "MEDIUM",
  "note": "<title of just-written note>",
  "detail": "Forward relation 'extends [[X]]' has no matching 'extended_by' reverse on X.",
  "remediation": "Add 'extended_by [[<source-title>]]' to X, or accept as one-way."
}
```

Claude Code surfaces these warnings to the agent. Cycle 3's skill pattern will interpret them and drive remediation.

### Graceful Degradation Ladder

| Scenario | Behavior |
|---|---|
| `ys` binary missing | Session-start warns once. Hook falls back to Python picoschema-aware validator. Never blocks solely because ys is missing. |
| SQLite DB locked (WAL contention) | Retry up to 3 times with 100ms backoff. If still locked → skip SQLite checks, emit `HOOK_DEGRADED` warning. Do NOT block the write. |
| `.schemas-jsonschema/<type>.yaml` stale vs `schemas/<type>.md` | Regenerate on-the-fly during the hook. Log staleness for next session-start cleanup. |
| Project not found in basic-memory config | Hard block with remediation "Run list_memory_projects to verify project registration." |
| Picoschema translator fails on a specific schema | That schema degrades to Python fallback for that one type. Other schemas unaffected. Error logged for next `/install-schemas` run. |

**Critical principle**: **a broken hook must never prevent legitimate writes.** Blocking is reserved for actual content violations, not infrastructure failures.

### Per-Project Severity Configuration

`<project-path>/.memory-toolkit.conf` — YAML format, for consistency with schema frontmatter and seed files:

```yaml
severity:
  ghost_entity: block          # or "warn"
  cross_project_wikilink: warn # or "block"
  bidirectional_missing: warn  # promoted to block by Cycle 3

behavior:
  forward_refs_require_declaration: true
  type_field_mandatory_on_edit: false  # allows editing legacy un-typed notes
```

Defaults ship at plugin install. Missing file → defaults apply. Opted-out projects (empty `schemas/`) skip schema-related checks but retain structural checks (ghost entities, self-references).

### Agent-Facing Remediation Message Principles

- **Actionable**: "Add X to Y" not "Relation incomplete"
- **Specific**: name the field, note, and expected value
- **Non-prescriptive where ambiguity is legitimate**: offer alternatives
- **Include escape hatches**: `type: note` fallback, `forward_refs:` declaration — never corner the agent

---

## 9. Testing Strategy

### Layer 1 — Unit Tests

| Component | Framework | What's Tested |
|---|---|---|
| `scripts/picoschema-to-jsonschema.py` | pytest | Every picoschema construct (required, optional, array, enum, nested) translates correctly |
| `hooks/scripts/sqlite-query.py` | pytest | Parameterized queries including injection-attempt inputs |
| `hooks/scripts/sqlite-checks.sh` | BATS | Each function against fixture DB |
| `validators/hook_validator.py` | pytest (existing) | Each new check in isolation — block/warn/pass paths |

Fixture location: `tests/unit/<component>/fixtures/`

### Layer 2 — Integration Tests

Simulate full hook pipeline against a fixture SQLite DB:

```
tests/integration/
├── fixtures/
│   ├── test-project.db
│   ├── schemas/
│   └── .schemas-jsonschema/
└── cases/
    ├── clean_write.json
    ├── missing_type.json
    ├── schema_enum_violation.json
    ├── ghost_entity.json
    ├── forward_ref_declared.json
    ├── cross_project.json
    ├── cycle_3_bidirectional.json
    ├── db_locked.json
    └── ys_missing.json
```

Each case asserts: exit code, stderr JSON shape, `reason_code`, `remediation` presence.

### Layer 3 — Live Smoke Test

Run in feature branch against a dedicated test project `basic-memory-toolkit-dev-test` (NOT the live `basic-memory-toolkit` project — avoid self-contamination):

1. Create test project
2. Run `/install-schemas basic-memory-toolkit-dev-test`
3. Manually write_note with: valid schema note / invalid schema note / ghost entity / forward ref / cross-project ref
4. Verify block/warn behavior matches the taxonomy in §8
5. Check PostToolUse bidirectional warnings surface in agent output
6. Measure actual hook latency — confirm <100ms end-to-end

### Layer 4 — Regression Check On Real Projects

Before wiring the PreToolUse hook in blocking mode, run `/validate-project <real-project>` against each live project (`edifact-pipeline`, `phone-refactor`, etc.) and compare against audit expectations. Ensures new SQLite checks are correct before they become write-blocking.

---

## 10. Rollout Plan

### Phase 0 — Feature Branch Only (per user directive)

- All implementation on branch `feature/schema-activation-and-sqlite-validators`
- NO push to master / publish to marketplace until all four testing layers pass
- Testing on local dev environment only

### Phase 1 — Schema Activation (Cycle 1 Deliverables)

Ship:
- `seed/schemas/`
- `/install-schemas` command
- Session-start enhancements
- `create-memory-project` skill updates
- `Mandatory Type Declaration` rule note in `memory-rules`

Behavior in Phase 1:
- Hook validator enforces `type:` on new writes in WARN mode only — does NOT block yet
- User can run `/install-schemas` manually, observe how it feels

Gate to Phase 2: at least one real project's notes pass schema validation cleanly after author adds `type:` fields.

### Phase 2 — SQLite Validators + `type:` Enforcement (Cycle 2 Deliverables)

Ship:
- `hooks/scripts/sqlite-checks.sh`, `sqlite-query.py`, `verify-bidirectional.sh`
- PreToolUse schema validation in BLOCKING mode
- PostToolUse bidirectional check in WARN mode
- Per-project `.memory-toolkit.conf` support

Gate to Phase 3: observed false-positive rate <5% across a week of real use.

### Phase 3 — Publish To Plugin Marketplace

- Bump plugin version (2.0.5 → 2.1.0 — minor: new feature)
- Update CHANGELOG
- Update README: `ys` dependency, `/install-schemas` usage, `type:` mandatory rule
- Only after Phase 2 gate is met

### Migration Path For Existing Notes

- `write_note` (new): enforce `type:` (blocks in Phase 2)
- `edit_note` (existing note with no `type:` or `type: note`): allowed, warn only
- `edit_note` (existing note with `type: <specific>`): validate per schema

`/migrate-notes-to-schemas` command (Cycle 5) walks existing notes, suggests types via content heuristics, batch-updates with user approval.

### Rollback

If Phase 2 reveals unacceptable friction:
- Hot-edit `hooks.json` to remove new PreToolUse entries → effectively disabled
- OR set `.memory-toolkit.conf` global `severity.all: warn` → everything warns, nothing blocks
- Revert commits are clean (new files + isolated modifications)

---

## 11. Known Unknowns

- **`ys` error-message quality**: untested whether ys's JSON errors are useful enough for agent remediation without post-processing. Validate during implementation.
- **SQLite WAL lock frequency**: basic-memory's sync daemon holds the DB. 3-retry backoff should cover typical contention, but needs measurement.
- **Picoschema edge cases**: 8 schemas in scope; untested constructs may surface during translator implementation.
- **`ys` installation path on different platforms**: session-start PATH check should handle macOS/Linux/WSL; Windows untested.

---

## 12. File Structure After This Cycle

```
basic-memory-toolkit/
├── hooks/
│   ├── hooks.json                          # modified: +PostToolUse wiring
│   ├── session-start                       # modified: +schemas folder check
│   └── scripts/
│       ├── validate-note                   # modified: +Gates A/B/C
│       ├── sqlite-checks.sh                # NEW
│       ├── sqlite-query.py                 # NEW
│       ├── verify-bidirectional.sh         # NEW
│       └── bidirectional-map.conf          # NEW
├── seed/
│   ├── memory-rules/                       # existing
│   └── schemas/                            # NEW: canonical schema source
├── scripts/
│   └── picoschema-to-jsonschema.py         # NEW: install-time translator
├── commands/
│   └── install-schemas.md                  # NEW: slash command
├── validators/
│   ├── hook_validator.py                   # modified: +new reason codes
│   └── ... (others unchanged)
├── docs/
│   └── superpowers/
│       └── specs/
│           └── 2026-04-19-schema-activation-and-sqlite-validators-design.md  # this file
└── tests/
    ├── unit/
    │   ├── picoschema/
    │   ├── sqlite-checks/
    │   └── hook-validator/
    └── integration/
        ├── fixtures/
        └── cases/
```

---

## 13. Dependencies

- **`ys` (Rust JSON Schema validator)**: hard requirement for fast path; Python fallback when missing
- **`sqlite3` CLI**: hard requirement; no fallback
- **`jq`**: hard requirement; no fallback (used for parsing tool_input JSON)
- **Python 3**: required for translator, sqlite-query helper, hook_validator extensions
- **`pyyaml`**: required for picoschema translator only (install-time, not hot path)
- **BATS**: testing dependency for bash-function unit tests

---

## 14. Out Of Scope / Explicitly Deferred

| Concern | Target Cycle |
|---|---|
| Bidirectional atomicity skill pattern (R6 concretization) | Cycle 3 |
| Branch-aware memory folder structure (Thought 2) | Cycle 4 |
| R1–R12 rule notes authoring (except Mandatory Type Declaration) | Cycle 5 |
| Remediation of already-contaminated projects | Cycle 5 |
| Temporal freshness checks (Rules R2, R8) | Cycle 5 |
| `/migrate-notes-to-schemas` batch migration | Cycle 5+ |

Each deferred item has its own design cycle planned.

---

## 15. Acceptance Criteria

Cycle 1+2 is complete when:

1. `/install-schemas` successfully seeds schemas into an arbitrary project, with version tracking.
2. Session-start correctly distinguishes missing / empty / populated / stale schemas folder states and prompts accordingly.
3. New project creation offers schema initialization and honors opt-out.
4. PreToolUse hook blocks writes with: missing `type:`, unknown `type:`, schema violation, undeclared ghost entity, self-reference.
5. PreToolUse hook warns on: cross-project WikiLinks, declared forward references.
6. PostToolUse hook warns on: missing bidirectional reverse relations, unresolved outgoing relations.
7. All deny JSON includes structured `reason_code`, `reason_detail`, `remediation`.
8. Hook latency measured under 100ms for clean writes on developer hardware.
9. Graceful degradation verified: `ys` removed from PATH → Python fallback works; DB locked → retries then skips without blocking.
10. Unit + integration test suites pass.
11. Smoke test on `basic-memory-toolkit-dev-test` project shows correct behavior across the taxonomy.
12. README updated with `ys` dependency and `type:` mandatory rule.
13. CHANGELOG documents the new feature.
14. Feature branch merged to master only after all of the above.
