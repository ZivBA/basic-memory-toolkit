# Basic Memory Toolkit

A comprehensive Claude Code plugin for managing [Basic Memory](https://github.com/basicmachines-co/basic-memory) knowledge bases with quality enforcement, structured workflows, automated validation, and schema-driven note types.

## Attribution

This plugin builds on the excellent work from the [Basic Memory](https://github.com/basicmachines-co/basic-memory) project by [Basic Machines](https://github.com/basicmachines-co). It cherry-picks and extends patterns from their official repositories:

- **[basic-memory](https://github.com/basicmachines-co/basic-memory)** — The core knowledge management system and MCP server that powers all note operations
- **[basic-memory-plugins](https://github.com/basicmachines-co/basic-memory-plugins)** — Official Claude Code plugin; our slash commands and skill structure draw from their patterns
- **[basic-memory-skills](https://github.com/basicmachines-co/basic-memory-skills)** — Official skill library; our skills were inspired by and extend their approach

This toolkit adds development-focused features (two-tier validation, schema types for bugs/decisions/patterns, spec-driven development workflows) on top of their foundation.

## Features

- **13 specialized skills** for note creation, editing, searching, consolidation, validation, and knowledge capture
- **8 slash commands** for quick workflows: `/remember`, `/continue`, `/organize`, `/research`, `/dev-session`, `/capture-decision`, `/validate-project`, `/doctor`
- **8 schema definitions** for development-focused note types (bug-report, design-decision, code-pattern, etc.)
- **Memory organizer agent** for autonomous multi-project knowledge management
- **6 automated hooks** for session management, validation, quality checks, and context preservation
- **Two-tier validation** — instant inline checks (PreToolUse) + thorough CLI validators (batch)
- **Polyglot setup script** (Linux/macOS/Windows) for prerequisite installation and MCP registration
- **Memory rules seed data** for bootstrapping quality standards

## Prerequisites

The plugin requires the **basic-memory** MCP server as an external prerequisite (no longer bundled — see [docs/MIGRATION.md](docs/MIGRATION.md) if upgrading from v2.x).

| Requirement | Purpose |
|---|---|
| [uv](https://docs.astral.sh/uv/) | Runs the basic-memory MCP server via `uvx` |
| `basic-memory` | The MCP server itself (auto-installed on first `uvx` invocation) |
| Claude Code CLI | Registers the MCP server with `claude mcp add` |

The setup script (Step 2 below) installs `uv` and registers the MCP server for you. See [docs/INSTALL.md](docs/INSTALL.md) for full details, manual install steps, and MCP scope configuration.

## Installation

### Step 1: Install the plugin

**Option A — From GitHub marketplace (recommended)**
```bash
claude plugin marketplace add https://github.com/ZivBA/basic-memory-toolkit.git basic-memory-toolkit
```

**Option B — Local plugin directory (development)**
```bash
claude --plugin-dir /path/to/basic-memory-toolkit
```

**Option C — Copy to project**
```bash
cp -r basic-memory-toolkit /your/project/.claude-plugin/
```

### Step 2: Install the prerequisite

If you installed from the **CLI** (Option A or B without launching Claude yet), run the setup script directly from the plugin directory before starting Claude Code:

```bash
# Linux / macOS / WSL / Git Bash
./scripts/setup-prerequisites.cmd

# Windows
scripts\setup-prerequisites.cmd
```

If you installed the plugin **from inside an active Claude Code session**, **quit Claude Code first**, then run the setup script. Do not use `/reload-plugins` — the script registers an MCP server via `claude mcp add`, which is best applied with no live session holding config state.

The script detects `uv`, installs it via the official Astral installer if missing, smoke-tests `basic-memory`, prompts for MCP registration scope, and registers the server. After it completes, start (or restart) Claude Code.

### Step 3: Verify

Inside Claude Code, run `/basic-memory-toolkit:doctor` for a full diagnostic report.

## First Run

On first install, the plugin displays a welcome message with setup steps. On version updates from v2.x, it shows a migration notice (see [docs/MIGRATION.md](docs/MIGRATION.md)). On routine version bumps it shows a brief "updated" notice. On steady-state sessions (stored version matches plugin.json) the welcome/migration messages are silent — only the standard project-selection prompt fires.

Reconciliation state is stored in `${CLAUDE_PLUGIN_DATA}/version` (typically `~/.claude/plugins/data/basic-memory-toolkit/version`). To force the welcome/migration message to fire again, delete that file and restart Claude Code. The legacy v2.x flag at `~/.claude/basic-memory-toolkit.initialized` is automatically cleaned up on first v3.0.0+ session.

### Step 1: Import Seed Rules (Recommended)

The plugin includes seed data for the `memory-rules` project, which provides quality standards that skills reference at runtime. To import:

1. Start a Claude Code session with the plugin enabled
2. Ask Claude: "Create the memory-rules project and import the seed rules from the plugin"
3. Claude will use the `create-new-memory-project` skill to set up the project and import the bundled rules from `seed/memory-rules/`

Without this step, skills will still work but won't have access to detailed quality rules.

### Step 2: Marketplace Auto-Updates (Optional)

The plugin auto-updates from GitHub when installed via marketplace. For public repos this works without authentication, but may fail silently under GitHub API rate limits (60 unauthenticated requests/hour).

For reliable auto-updates, set a GitHub personal access token in your shell config:

```bash
# Add to ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

This raises the limit to 5,000 requests/hour. The token is your standard GitHub PAT — no special scopes are needed for public repos.

| Provider | Environment Variables | Notes |
|----------|----------------------|-------|
| GitHub | `GITHUB_TOKEN` or `GH_TOKEN` | Personal access token or GitHub App token |
| GitLab | `GITLAB_TOKEN` or `GL_TOKEN` | Personal access token or project token |
| Bitbucket | `BITBUCKET_TOKEN` | App password or repository access token |

## Components

### Slash Commands (8)

| Command | Purpose |
|---------|---------|
| `/remember [title] [folder]` | Capture insights, decisions, patterns to memory |
| `/continue [topic]` | Resume previous work by loading context from memory |
| `/organize [project]` | Analyze knowledge graph health and suggest improvements |
| `/research <topic>` | Research a topic across all memory projects |
| `/dev-session [project]` | Start a development session with full memory context |
| `/capture-decision [title]` | Capture a design/architectural decision with structured template |
| `/validate-project [project]` | Run validation suite across all notes in a project |
| `/doctor` | Diagnose plugin setup, prerequisite, MCP registration, tool availability |

### Skills (13)

| Skill | Purpose |
|-------|---------|
| **create-memory-note** | Create notes with full rule enforcement and verification |
| **update-memory-note** | Update existing notes with relation verification |
| **verify-memory-relations** | Health check for self-refs, broken links, cross-project WikiLinks, informal sections |
| **create-new-memory-project** | Create and register new memory projects |
| **cross-project-search** | Search and synthesize across project boundaries |
| **consolidate-notes** | Merge duplicate/overlapping content |
| **organize-archive** | Archive outdated content with categorization |
| **optimize-graph** | Analyze and strengthen knowledge graph connections |
| **audit-quality** | Assess note quality across titles, metadata, observations, relations |
| **batch-fix-wikilinks** | Bulk repair broken, self-ref, and cross-project WikiLinks |
| **knowledge-capture** | Auto-identify and capture decisions, insights, patterns from conversations |
| **spec-driven-development** | Align implementation with specifications stored in memory |
| **validate-project** | Run full validation suite with tiered reporting |

### Schemas (8)

Development-focused Picoschema definitions for structured note types:

| Schema | Entity Type | Purpose |
|--------|-------------|---------|
| **bug-report** | `bug-report` | Track bugs with severity, reproduction, root cause |
| **fix-record** | `fix-record` | Document fixes with changes, testing, regression risk |
| **design-decision** | `design-decision` | Capture decisions with context, options, rationale |
| **architecture-constraint** | `architecture-constraint` | Document system limitations and workarounds |
| **framework-limitation** | `framework-limitation` | Track framework/library limitations |
| **session-artifact** | `session-artifact` | Structured session summaries |
| **index-note** | `index-note` | Project index with enforced relation types |
| **code-pattern** | `code-pattern` | Reusable coding patterns and conventions |

### Agent

- **memory-organizer** — Autonomous agent for multi-project memory navigation, note consolidation, knowledge graph optimization, and quality assessment. Uses canonical `mcp__basic-memory__*` tools.

### Hooks (6)

| Event | Purpose |
|-------|---------|
| **SessionStart** | Auto-detects matching memory project from CWD, prompts for project selection |
| **PreToolUse** (write_note) | Blocks self-referential relations before write (instant, 20ms) |
| **PostToolUse** (write/edit) | Warns on quality issues — missing relations, informal sections, relates_to overuse |
| **UserPromptSubmit** | Detects memory-related triggers and reminds to use appropriate skills |
| **PreCompact** | Preserves active project, open issues, pending tasks before context compression |
| **Stop** | Suggests capturing session insights with `/remember` |

### Validators

Two-tier validation architecture:

- **Tier 1 — Inline** (`validators/hook_validator.py`): Parses tool_input from hook stdin, ~20ms, zero CLI overhead. Used by PreToolUse/PostToolUse hooks.
- **Tier 2 — CLI** (`validators/run_all.py`): Uses `basic-memory` CLI for thorough checks (broken WikiLinks, cross-project detection), ~7s per note. Used by `/validate-project`.

### MCP Server

The basic-memory MCP server is an external prerequisite. Register it via the setup script (recommended) or manually:

```bash
claude mcp add basic-memory --scope user -- uvx basic-memory mcp
```

For pip-based installations of basic-memory (instead of uvx):

```bash
claude mcp add basic-memory --scope user -- basic-memory mcp
```

See [docs/INSTALL.md](docs/INSTALL.md) for full details on registration scopes (user/project/local) and the `~/.basic-memory` server config directory.

## Directory Structure

```
basic-memory-toolkit/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest (v3.0.0)
│   └── marketplace.json      # Marketplace registry
├── commands/                 # 8 slash commands
│   ├── remember.md
│   ├── continue.md
│   ├── organize.md
│   ├── research.md
│   ├── dev-session.md
│   ├── capture-decision.md
│   ├── validate-project.md
│   └── doctor.md
├── skills/                   # 13 memory management skills
│   ├── create-memory-note/
│   ├── update-memory-note/
│   ├── verify-memory-relations/
│   ├── create-new-memory-project/
│   ├── cross-project-search/
│   ├── consolidate-notes/
│   ├── organize-archive/
│   ├── optimize-graph/
│   ├── audit-quality/
│   ├── batch-fix-wikilinks/
│   ├── knowledge-capture/
│   ├── spec-driven-development/
│   └── validate-project/
├── schemas/                  # 8 Picoschema definitions
│   ├── bug-report.md
│   ├── fix-record.md
│   ├── design-decision.md
│   ├── architecture-constraint.md
│   ├── framework-limitation.md
│   ├── session-artifact.md
│   ├── index-note.md
│   └── code-pattern.md
├── agents/
│   └── memory-organizer.md   # Autonomous memory management agent
├── hooks/
│   ├── hooks.json            # 6 automated hooks
│   └── scripts/
│       └── validate-note     # Hook script wrapper
├── validators/               # Two-tier validation modules
│   ├── __init__.py           # Shared utilities
│   ├── hook_validator.py     # Tier 1: inline (20ms)
│   ├── self_reference.py     # Tier 2: CLI-based
│   ├── cross_project.py
│   ├── broken_wikilinks.py
│   ├── relation_quality.py
│   ├── section_format.py
│   └── run_all.py            # Tier 2 orchestrator
├── references/
│   └── basic-memory-guide.md # Complete Basic Memory usage guide
├── scripts/
│   ├── setup-prerequisites.cmd  # Cross-platform prerequisite installer
│   └── picoschema_to_jsonschema.py
├── docs/
│   ├── INSTALL.md            # Installation guide + MCP scopes
│   ├── MIGRATION.md          # v2.x → v3.0 migration guide
│   ├── ENHANCEMENT_PLAN.md   # Development roadmap
│   └── ARCHITECTURE.md       # Four-tier architecture
└── seed/
    └── memory-rules/         # Quality rules for import
```

## Architecture

The plugin follows a four-tier architecture:

1. **Guide** (`references/basic-memory-guide.md`) — Loaded at session start, provides operational context
2. **Rules Project** (`memory-rules`) — Authoritative quality standards, consulted before note operations
3. **Skills** — Core (atomic operations) and maintenance (workflows using core skills)
4. **Agent** (`memory-organizer`) — Autonomous multi-project operations using skills

See `docs/ARCHITECTURE.md` for detailed design documentation.

## License

MIT
