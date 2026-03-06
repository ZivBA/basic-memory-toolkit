# Basic Memory Toolkit

A comprehensive Claude Code plugin for managing [Basic Memory](https://github.com/basic-memory/basic-memory) knowledge bases with quality enforcement, structured workflows, and automated checks.

## Features

- **9 specialized skills** for note creation, editing, searching, consolidation, archiving, and quality auditing
- **Memory organizer agent** for autonomous multi-project knowledge management
- **5 automated hooks** for session management, quality checks, and context preservation
- **Basic Memory MCP server** bundled via uvx for zero-config setup
- **Memory rules seed data** for bootstrapping quality standards

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Python 3.10+ (for basic-memory)
- Claude Code CLI

## Installation

### Option 1: From GitHub (recommended)
```bash
claude plugin add --marketplace https://github.com/ZivBA/basic-memory-toolkit.git basic-memory-toolkit
```

### Option 2: Plugin Directory (local development)
```bash
claude --plugin-dir /path/to/basic-memory-toolkit
```

### Option 3: Copy to Project
```bash
cp -r basic-memory-toolkit /your/project/.claude-plugin/
```

## Post-Install Setup: Memory Rules

The plugin includes seed data for the `memory-rules` project, which provides quality standards that skills reference at runtime. To import:

1. Start a Claude Code session with the plugin enabled
2. Ask Claude: "Create the memory-rules project and import the seed rules from the plugin"
3. Claude will use the `create-new-memory-project` skill to set up the project and import the bundled rules from `seed/memory-rules/`

Without this step, skills will still work but won't have access to detailed quality rules.

## Components

### Skills (9)

| Skill | Trigger Phrases |
|-------|----------------|
| **create-memory-note** | "write a memory note", "create a note", "save this to memory" |
| **update-memory-note** | "update the note", "edit the memory note" |
| **verify-memory-relations** | "check note relations", "verify links" |
| **create-new-memory-project** | "create a new memory project", "add a new project" |
| **cross-project-search** | "search all projects", "find across projects" |
| **consolidate-notes** | "consolidate notes", "merge duplicate notes" |
| **organize-archive** | "archive old notes", "clean up outdated content" |
| **optimize-graph** | "optimize knowledge graph", "find isolated notes" |
| **audit-quality** | "audit note quality", "check note standards" |

### Agent

- **memory-organizer** — Autonomous agent for multi-project memory navigation, note consolidation, knowledge graph optimization, and quality assessment.

### Hooks

| Event | Purpose |
|-------|---------|
| **SessionStart** | Auto-detects matching memory project from CWD, prompts for project selection |
| **PostToolUse** (write/edit) | Warns on self-referential relations and cross-project WikiLinks |
| **UserPromptSubmit** | Detects "remember this", "always", "never" and reminds to use create-memory-note skill |
| **PreCompact** | Preserves active project, open issues, pending tasks, and deferred items before context compression |

### MCP Server

Bundles Basic Memory MCP server configuration using `uvx` (zero-install). For manual pip installations, update `.mcp.json`:

```json
{
  "mcpServers": {
    "basic-memory": {
      "type": "stdio",
      "command": "basic-memory",
      "args": ["mcp"],
      "env": {}
    }
  }
}
```

## Directory Structure

```
basic-memory-toolkit/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest
│   └── marketplace.json      # Marketplace registry for remote install
├── .mcp.json                 # Basic Memory MCP server config
├── skills/                   # 9 memory management skills
│   ├── create-memory-note/
│   ├── update-memory-note/
│   ├── verify-memory-relations/
│   ├── create-new-memory-project/
│   ├── cross-project-search/
│   ├── consolidate-notes/
│   ├── organize-archive/
│   ├── optimize-graph/
│   └── audit-quality/
├── agents/
│   └── memory-organizer.md   # Autonomous memory management agent
├── hooks/
│   └── hooks.json            # 5 automated hooks
├── references/
│   └── basic-memory-guide.md # Complete Basic Memory usage guide
└── seed/
    └── memory-rules/         # Quality rules for import into memory-rules project
```

## License

MIT
