# Migration Guide

## v2.x → v3.0.0 — Prerequisite Install Model (Breaking Change)

**TL;DR**: The plugin no longer bundles the basic-memory MCP server. Install it as a
prerequisite, register it with Claude Code yourself, and remove any project-level
`.mcp.json` entries that referenced the old bundled server.

### Why this changed

The bundled MCP approach had three reproducible failure modes:

1. **Config drift** — Claude Code re-syncs the plugin's `.mcp.json` on every startup,
   overwriting any user edits. Switching to a remote SSE endpoint or alternate
   transport was impossible to make stick.
2. **Hard `uv` dependency at install time** — If `uv` was missing when the plugin
   loaded, the bundled server failed silently.
3. **Duplicate registration** — Installing basic-memory standalone alongside the
   plugin produced two MCP servers with the same name (`basic-memory:*` and
   `plugin_basic-memory-toolkit_basic-memory:*`), polluting the tool namespace and
   creating confusing dual tool sets.

Treating basic-memory as an external prerequisite (the same way `uv` itself is
already treated) eliminates all three.

See the architectural decision: [decisions/Switch from bundled MCP to prerequisite
install model](memory://basic-memory-toolkit/decisions/switch-from-bundled-mcp-to-prerequisite-install-model)
in the `basic-memory-toolkit` Basic Memory project.

### Migration steps

#### 1. Install the prerequisite (if you haven't already)

Run the setup script from the plugin root, or follow [INSTALL.md](INSTALL.md).

```bash
./scripts/setup-prerequisites.cmd
```

The script is idempotent — if `uv` and `basic-memory` are already on your machine, it
will detect and skip the install steps, then prompt you for an MCP registration scope.

#### 2. Remove stale project-level `.mcp.json` entries

If you have any project-level `.mcp.json` files that reference the bundled server,
remove those entries. Look for:

- A server named `plugin_basic-memory-toolkit_basic-memory`
- Any server with `command: uvx` and args referencing `basic-memory mcp` that you did
  NOT register yourself

Example stale entry to remove:

```json
{
  "mcpServers": {
    "plugin_basic-memory-toolkit_basic-memory": {
      "command": "uvx",
      "args": ["basic-memory", "mcp"]
    }
  }
}
```

If after cleanup the file has no other servers, delete the file or leave
`{ "mcpServers": {} }`.

#### 3. Verify the migration

After restarting Claude Code, run `/basic-memory-toolkit:doctor` from inside the
Claude Code session. A healthy migrated state shows:

- `mcp__basic-memory__*` tools available (the canonical names)
- **No** `mcp__plugin_basic-memory-toolkit_basic-memory__*` tools
- `~/.claude/basic-memory-toolkit.initialized` legacy flag is gone (the session-start
  hook deletes it automatically on first v3.0.0+ session)

#### 4. Optional cleanup

The plugin v3.0.0+ session-start hook stores its reconciliation state in
`${CLAUDE_PLUGIN_DATA}/version` (typically
`~/.claude/plugins/data/basic-memory-toolkit/version`). To force the welcome /
migration message to re-fire, delete that file and restart Claude Code.

### Tool name changes

All plugin internals (the `memory-organizer` agent, validation hooks, slash commands)
now reference only the canonical `mcp__basic-memory__*` tool names. If you have your
own custom commands or hooks that referenced
`mcp__plugin_basic-memory-toolkit_basic-memory__*`, update them to canonical names.

### Rollback

If you need to roll back to v2.x, reinstall the previous plugin version. The
prerequisite installation does not need to be reverted — basic-memory itself is
unchanged, only how it's registered with Claude Code differs.
