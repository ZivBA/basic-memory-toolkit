:<<"::CMDLITERAL"
@ECHO OFF
GOTO :CMDSCRIPT
::CMDLITERAL

# ============================================================================
# Bash branch (Linux / macOS / WSL / Git Bash)
# ============================================================================
set -euo pipefail

info()  { printf '\033[1;34m[setup]\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m[setup]\033[0m %s\n' "$*" >&2; }
error() { printf '\033[1;31m[setup]\033[0m %s\n' "$*" >&2; }

ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    info "uv already installed: $(uv --version)"
    return 0
  fi
  info "uv not found — installing via official Astral installer..."
  if ! curl -LsSf https://astral.sh/uv/install.sh | sh; then
    error "uv install failed. See https://docs.astral.sh/uv/getting-started/installation/"
    return 1
  fi
  export PATH="${HOME}/.local/bin:${PATH}"
  if ! command -v uv >/dev/null 2>&1; then
    error "uv installed but not on PATH. Restart your shell and re-run this script."
    return 1
  fi
  info "uv installed: $(uv --version)"
}

smoke_test_basic_memory() {
  info "Running smoke test: uvx basic-memory --version"
  if ! uvx basic-memory --version; then
    error "basic-memory smoke test failed."
    return 1
  fi
}

prompt_scope() {
  echo "" >&2
  echo "Choose MCP registration scope:" >&2
  echo "  1) user    — available across all projects (recommended)" >&2
  echo "  2) project — committed to this project's .mcp.json (sharable with team)" >&2
  echo "  3) local   — this machine only, not shared" >&2
  echo "" >&2
  read -r -p "Scope [1]: " choice
  case "${choice:-1}" in
    1|"") echo "user" ;;
    2)    echo "project" ;;
    3)    echo "local" ;;
    *)    error "Invalid choice"; return 1 ;;
  esac
}

register_mcp() {
  local scope="$1"
  if ! command -v claude >/dev/null 2>&1; then
    error "claude CLI not found on PATH. Install Claude Code first: https://docs.claude.com/claude-code"
    return 1
  fi
  info "Registering basic-memory MCP server (scope=${scope})..."
  claude mcp add basic-memory --scope "${scope}" -- uvx basic-memory mcp
  info "Done. Verify with: claude mcp list"
}

main() {
  info "basic-memory-toolkit prerequisite setup"
  ensure_uv
  smoke_test_basic_memory
  scope="$(prompt_scope)"
  register_mcp "${scope}"
  info "Setup complete. Restart Claude Code to pick up the new MCP server."
}

main "$@"
exit $?

# The remainder of the file is the cmd.exe branch. Wrap it in a literal
# heredoc so bash never parses batch syntax (bash -n would otherwise fail).
:<<'BATCH_END'
:CMDSCRIPT
REM ============================================================================
REM Windows cmd.exe branch
REM ============================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

ECHO [setup] basic-memory-toolkit prerequisite setup

REM --- ensure uv ---
WHERE uv >NUL 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    ECHO [setup] uv not found -- installing via official Astral installer...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    IF !ERRORLEVEL! NEQ 0 (
        ECHO [setup] uv install failed. See https://docs.astral.sh/uv/getting-started/installation/ 1>&2
        EXIT /B 1
    )
    SET "PATH=%USERPROFILE%\.local\bin;%PATH%"
)

WHERE uv >NUL 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    ECHO [setup] uv installed but not on PATH. Open a new terminal and re-run this script. 1>&2
    EXIT /B 1
)

FOR /F "delims=" %%V IN ('uv --version') DO ECHO [setup] uv installed: %%V

REM --- smoke test ---
ECHO [setup] Running smoke test: uvx basic-memory --version
uvx basic-memory --version
IF %ERRORLEVEL% NEQ 0 (
    ECHO [setup] basic-memory smoke test failed. 1>&2
    EXIT /B 1
)

REM --- prompt scope ---
ECHO.
ECHO Choose MCP registration scope:
ECHO   1) user    -- available across all projects (recommended)
ECHO   2) project -- committed to this project's .mcp.json (sharable with team)
ECHO   3) local   -- this machine only, not shared
ECHO.
SET /P CHOICE="Scope [1]: "
IF "%CHOICE%"=="" SET "CHOICE=1"
IF "%CHOICE%"=="1" SET "SCOPE=user"
IF "%CHOICE%"=="2" SET "SCOPE=project"
IF "%CHOICE%"=="3" SET "SCOPE=local"
IF NOT DEFINED SCOPE (
    ECHO [setup] Invalid choice: %CHOICE% 1>&2
    EXIT /B 1
)

REM --- register MCP ---
WHERE claude >NUL 2>NUL
IF %ERRORLEVEL% NEQ 0 (
    ECHO [setup] claude CLI not found on PATH. Install Claude Code first. 1>&2
    EXIT /B 1
)

ECHO [setup] Registering basic-memory MCP server (scope=%SCOPE%)...
claude mcp add basic-memory --scope %SCOPE% -- uvx basic-memory mcp
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

ECHO [setup] Done. Verify with: claude mcp list
ECHO [setup] Setup complete. Restart Claude Code to pick up the new MCP server.

ENDLOCAL
EXIT /B 0
BATCH_END
