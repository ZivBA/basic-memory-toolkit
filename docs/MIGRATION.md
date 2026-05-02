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

> **Footgun**: Claude Code reads MCP server config from `~/.claude.json`
> (and project-level `.mcp.json`), **not** from `~/.claude/settings.json`.
> If you've previously added an `mcpServers` block to
> `~/.claude/settings.json` thinking it would register an MCP server,
> that block is dead config — it does nothing. Remove it to avoid
> confusion. The canonical user-scope location is the top-level
> `mcpServers` key in `~/.claude.json`, populated by
> `claude mcp add --scope user`.

#### 3. Verify the migration

After restarting Claude Code, run `/basic-memory-toolkit:doctor` from inside the
Claude Code session. A healthy migrated state shows:

- `mcp__basic-memory__*` tools available (the canonical names)
- **No** `mcp__plugin_basic-memory-toolkit_basic-memory__*` tools
- `~/.claude/basic-memory-toolkit.initialized` legacy flag is gone (the session-start
  hook deletes it automatically on first v3.0.0+ session)

#### 3a. If you still see a phantom `plugin:basic-memory-toolkit:basic-memory` entry

Claude Code keeps **per-version snapshots** of every plugin it has ever loaded
under `~/.claude/plugins/cache/<plugin>/<plugin>/<version>/`, and its MCP
discovery walks **all** version directories, not just the active one. After
upgrading to v3, the pre-v3 cache directory will still contain the bundled
`.mcp.json` and will be discovered as a duplicate registration, showing up as
`plugin:basic-memory-toolkit:basic-memory: uvx basic-memory mcp` in
`claude mcp list` and as `mcp__plugin_basic-memory-toolkit_basic-memory__*`
tools in your tool list.

To clean:

```bash
# Identify version directories
ls ~/.claude/plugins/cache/basic-memory-toolkit/basic-memory-toolkit/
# Example output:
#   2.0.5  3.0.0

# Remove every directory that isn't the current version
rm -rf ~/.claude/plugins/cache/basic-memory-toolkit/basic-memory-toolkit/2.0.5
```

Restart Claude Code; the phantom entry will be gone. Re-run
`/basic-memory-toolkit:doctor` to confirm.

#### 4. Optional cleanup

The plugin v3.0.0+ session-start hook stores its reconciliation state in
`${CLAUDE_PLUGIN_DATA}/version` (typically
`~/.claude/plugins/data/basic-memory-toolkit/version`). To force the welcome /
migration message to re-fire, delete that file and restart Claude Code.

### Local development testing (feature branches, pre-merge validation)

If you want to test a plugin feature branch in true isolation — without the
marketplace auto-update mechanic re-syncing your local edits, and without the
per-version cache aggregation surfacing stale `.mcp.json` entries — use
`--plugin-dir` against a separately-cloned tree, and **fully deregister the
marketplace plugin first**.

`enabledPlugins["<name>@<source>"] = false` alone is not sufficient. Claude
Code will still:

- Re-clone / re-sync the marketplace tree on startup (driven by
  `~/.claude/settings.json` `extraKnownMarketplaces` and
  `~/.claude/plugins/known_marketplaces.json`).
- Copy the marketplace tree into a versioned cache directory.
- Discover `.mcp.json` from the cached tree, registering its servers regardless
  of `enabledPlugins` state.

To get a clean test bed, deregister at **all three** layers:

```bash
# 1. Remove from settings.json's extraKnownMarketplaces
jq 'del(.extraKnownMarketplaces["basic-memory-toolkit"])' \
  ~/.claude/settings.json > /tmp/s && mv /tmp/s ~/.claude/settings.json

# 2. Deregister via the CLI (cleans plugins/known_marketplaces.json)
claude plugin marketplace remove basic-memory-toolkit

# 3. Wipe the marketplace tree and any cached snapshots
rm -rf ~/.claude/plugins/marketplaces/basic-memory-toolkit
rm -rf ~/.claude/plugins/cache/basic-memory-toolkit

# 4. Clone the feature branch to a stable local path
git clone -b <feature-branch> https://github.com/<owner>/basic-memory-toolkit.git \
  ~/local-plugins/basic-memory-toolkit

# 5. Launch Claude Code with --plugin-dir pointing at the local tree
claude --plugin-dir ~/local-plugins/basic-memory-toolkit
```

For persistent local testing (e.g. across systemd-managed sessions), add
`--plugin-dir` to the command in your service definition rather than passing
it once.

`/plugin marketplace add` and `/plugin install` (or the CLI equivalents) will
re-add the marketplace registration when you're ready to switch back to the
upstream-tracked version.

### Tool name changes

All plugin internals (the `memory-organizer` agent, validation hooks, slash commands)
now reference only the canonical `mcp__basic-memory__*` tool names. If you have your
own custom commands or hooks that referenced
`mcp__plugin_basic-memory-toolkit_basic-memory__*`, update them to canonical names.

### Rollback

If you need to roll back to v2.x, reinstall the previous plugin version. The
prerequisite installation does not need to be reverted — basic-memory itself is
unchanged, only how it's registered with Claude Code differs.

**However**: if you already ran `scripts/setup-prerequisites.cmd` (or
`claude mcp add basic-memory ...` manually) against v3.0.0+, the standalone
registration you created will coexist with the rolled-back v2.x bundled
server, producing the duplicate-registration scenario v3 was designed to
fix. Tools will appear under both `mcp__basic-memory__*` and
`mcp__plugin_basic-memory-toolkit_basic-memory__*` namespaces.

To clean up before rollback:

```bash
claude mcp remove basic-memory --scope <scope-you-used>
```

Then reinstall v2.x. After rollback, `claude mcp list` should show only
`plugin_basic-memory-toolkit_basic-memory` (the bundled entry), and tools
will appear only under the plugin-prefixed namespace.
