# Installation Guide

The basic-memory-toolkit plugin requires the **basic-memory** MCP server as an external prerequisite.
Starting in v3.0.0 the plugin no longer bundles this dependency — see [MIGRATION.md](MIGRATION.md)
if you are upgrading from v2.x.

## Prerequisites

| Requirement | Purpose | How to install |
|---|---|---|
| `uv` (Astral)        | Python package manager that runs the basic-memory MCP server. | https://docs.astral.sh/uv/getting-started/installation/ |
| `basic-memory`       | The MCP server itself. Installed/run via `uvx basic-memory`. | Auto-installed on first `uvx` invocation. |
| `claude` CLI         | Registers the MCP server with Claude Code. | https://docs.claude.com/claude-code |

## Quick start (recommended)

From the plugin root, run:

```bash
# Linux / macOS / WSL / Git Bash
./scripts/setup-prerequisites.cmd

# Windows (cmd.exe or PowerShell)
scripts\setup-prerequisites.cmd
```

The script will:
1. Detect `uv`, install it via the official Astral installer if missing.
2. Smoke-test `uvx basic-memory --version`.
3. Prompt for MCP registration scope (see below).
4. Run `claude mcp add basic-memory --scope <chosen> -- uvx basic-memory mcp`.

After setup, **restart Claude Code** so the new MCP server is loaded.

Run `/basic-memory-toolkit:doctor` from inside Claude Code to verify the installation.

## MCP registration scopes

`claude mcp add` supports three scopes. Choose based on how broadly you want the server available.

| Scope | Where it's stored | Visibility | When to use |
|---|---|---|---|
| `user` (recommended) | `~/.claude.json` | All your projects on this machine | You always want basic-memory available. **Default.** |
| `project` | `<project>/.mcp.json` (committed) | Anyone who clones the repo | Team-shared projects where everyone needs basic-memory. |
| `local` | Per-project local config (not committed) | Only you on this machine | You want it for this project but not commit the config. |

Switch scope later by removing the existing entry (`claude mcp remove basic-memory --scope <old>`) and re-registering at the new scope.

## Manual installation

If you'd rather not run the script:

```bash
# 1. Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 1. Install uv (Windows PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Smoke test
uvx basic-memory --version

# 3. Register with Claude Code (pick a scope)
claude mcp add basic-memory --scope user -- uvx basic-memory mcp
```

## The `~/.basic-memory` directory

When `basic-memory` runs for the first time, it creates `~/.basic-memory/` to store
**server configuration and project metadata** (NOT the same as MCP transport config).
This includes:

- The list of registered Basic Memory *projects* (each project is a markdown directory)
- The default project pointer
- Sync state and indexing metadata

This directory is independent of the plugin and survives plugin uninstall/reinstall.
If it exists, you have used basic-memory before; the session-start hook uses this as a
signal to provide a lighter-touch welcome message on first toolkit install.

To configure server-side options (default project, sync intervals, etc.) edit
`~/.basic-memory/config.json` directly, or use the basic-memory CLI:

```bash
uvx basic-memory project list
uvx basic-memory project add <name> <path>
```

## Verifying the installation

```bash
claude mcp list                    # should show basic-memory
uvx basic-memory --version         # should print a version
```

Inside Claude Code, run `/basic-memory-toolkit:doctor` for a full diagnostic.

## Troubleshooting

- **`uv: command not found` after install** — Open a new shell. The installer adds
  `~/.local/bin` to PATH, but only for new sessions.
- **`claude: command not found`** — Install Claude Code first: https://docs.claude.com/claude-code
- **MCP server doesn't appear after registration** — Restart Claude Code. MCP servers
  are loaded at startup.
- **Tools show as `mcp__plugin_basic-memory-toolkit_basic-memory__*` instead of
  `mcp__basic-memory__*`** — You're loading a stale bundled config. See
  [MIGRATION.md](MIGRATION.md).

For any of these, `/basic-memory-toolkit:doctor` will identify the specific issue and
recommend a fix.
