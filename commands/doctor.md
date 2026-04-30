---
description: Diagnose basic-memory-toolkit setup — checks prerequisite, MCP registration, tool availability, and stale config
---

Run a comprehensive diagnostic of the basic-memory-toolkit installation and basic-memory MCP setup. Report findings with concrete remediation steps.

## Step 1 — Shell-side environment checks

Run these checks in parallel where possible. For each, capture output and note pass/fail.

**Prerequisite tooling:**
- `command -v uv` — is uv installed and on PATH?
- `uv --version` — version
- `uvx basic-memory --version` — does the basic-memory binary execute? (only if `uv` is present)

**Plugin state:**
- `cat "${CLAUDE_PLUGIN_DATA}/version" 2>/dev/null` — what version did the session-start hook last reconcile?
- `cat ~/.claude/basic-memory-toolkit.initialized 2>/dev/null` — is the legacy v2.x flag still present? (should not exist after migration)
- `ls -d ~/.basic-memory 2>/dev/null` — has basic-memory ever been initialized on this machine?

**MCP registration:**
- `claude mcp list 2>/dev/null` — list all registered MCP servers; check for `basic-memory` entries
- `cat ./.mcp.json 2>/dev/null | grep -E "basic-memory|plugin_basic-memory-toolkit"` — project-level MCP config in the current working directory; flag any `plugin_basic-memory-toolkit_basic-memory` references as stale

## Step 2 — LLM-side tool availability check

From your available tools list, count the following:
- Number of `mcp__basic-memory__*` tools (canonical, expected after v3.0.0)
- Number of `mcp__plugin_basic-memory-toolkit_basic-memory__*` tools (legacy bundled, should be zero in v3.0.0+)

Report counts to the user.

## Step 3 — Diagnose and report

Based on findings, classify the situation and report:

**Healthy state** (most/all green):
- uv installed, basic-memory smoke-tests OK
- `mcp__basic-memory__*` tools available (>0)
- No `mcp__plugin_basic-memory-toolkit_basic-memory__*` tools
- No stale plugin-prefixed entries in project `.mcp.json`
- Plugin data version matches plugin.json version

→ Report: "✅ basic-memory-toolkit setup is healthy."

**Missing prerequisite** (uv or basic-memory missing):
→ Report: "❌ Prerequisite missing. Run `scripts/setup-prerequisites.cmd` from the plugin root, then restart Claude Code. See `docs/INSTALL.md`."

**MCP not registered** (uv works but `claude mcp list` shows no basic-memory entry, no canonical tools available):
→ Report: "❌ basic-memory MCP server not registered with Claude Code. Run `scripts/setup-prerequisites.cmd` to register it (you'll be prompted for scope: user/project/local)."

**Duplicate registration** (both canonical AND plugin-prefixed tools present):
→ Report: "⚠️ Duplicate MCP registration detected. Remove the legacy `plugin_basic-memory-toolkit_basic-memory` entries from your project's `.mcp.json` (or wherever they appear). See `docs/MIGRATION.md`."

**Legacy bundled only** (plugin-prefixed tools present, canonical absent):
→ Report: "⚠️ Only the legacy bundled MCP is loaded. Plugin v3.0.0+ removed the bundled server. Run the setup script to register basic-memory canonically, then remove the plugin-prefixed entry from any `.mcp.json` files. See `docs/MIGRATION.md`."

**Stale legacy flag**:
→ Report: "ℹ️ Found `~/.claude/basic-memory-toolkit.initialized` (legacy v2.x flag). Safe to delete — `${CLAUDE_PLUGIN_DATA}/version` supersedes it."

**Plugin data version mismatch** (e.g. session-start hook didn't run):
→ Report: "ℹ️ Plugin-data version (X) does not match plugin.json version (Y). Restart Claude Code to let the session-start hook reconcile."

## Step 4 — Always end with

A concise summary table of all checks (pass/fail/warn) and the most actionable next step. If multiple issues, prioritize: missing prerequisite > MCP not registered > duplicate registration > stale config > flag cleanup.
