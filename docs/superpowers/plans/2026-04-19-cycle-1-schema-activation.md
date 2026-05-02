# Cycle 1: Schema Activation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Activate the orphaned schema system by seeding schemas into memory projects, enforcing mandatory `type:` field as advisory (warn-mode), and providing an `/install-schemas` slash command with version tracking.

**Architecture:** Picoschema source files in `/schemas/*.md` are copied into the plugin's `seed/schemas/` folder at build time. A Python translator converts picoschema YAML to JSON Schema YAML derivatives used by later cycles' `ys` validator. The `/install-schemas` bash command copies schemas into target memory projects and regenerates derivatives on source change. The existing session-start hook is extended with a schema-folder state check. The existing hook validator gains a warn-mode `type:` field presence check — blocking enforcement is deferred to Cycle 2.

**Tech Stack:** Python 3 (translator, hook validator), bash (install command, session-start hook), pytest (unit tests), pyyaml (picoschema parsing), BATS-optional (bash function tests), SQLite (basic-memory DB lookups via sqlite3 CLI).

**Branch:** `feature/schema-activation-and-sqlite-validators` (already created)

**Spec reference:** `docs/superpowers/specs/2026-04-19-schema-activation-and-sqlite-validators-design.md`

**Phase rollout:** This plan delivers Cycle 1 / Phase 1 — advisory enforcement only. Phase 2 (blocking + SQLite validators) is in a separate plan written after Phase 1 gate is met.

---

## Task Group A — Seed Schemas Into Plugin Source

### Task A1: Copy plugin /schemas into seed/schemas

**Files:**
- Create: `seed/schemas/architecture-constraint.md`
- Create: `seed/schemas/bug-report.md`
- Create: `seed/schemas/code-pattern.md`
- Create: `seed/schemas/design-decision.md`
- Create: `seed/schemas/fix-record.md`
- Create: `seed/schemas/framework-limitation.md`
- Create: `seed/schemas/index-note.md`
- Create: `seed/schemas/session-artifact.md`

- [ ] **Step 1: Verify source schemas exist**

Run: `ls /home/zivben/repos/basic-memory-toolkit/schemas/`
Expected: 8 `.md` files: `architecture-constraint.md`, `bug-report.md`, `code-pattern.md`, `design-decision.md`, `fix-record.md`, `framework-limitation.md`, `index-note.md`, `session-artifact.md`

- [ ] **Step 2: Create seed/schemas directory**

Run: `mkdir -p /home/zivben/repos/basic-memory-toolkit/seed/schemas`
Expected: no error, directory created

- [ ] **Step 3: Copy each schema file**

Run:
```bash
cp /home/zivben/repos/basic-memory-toolkit/schemas/*.md /home/zivben/repos/basic-memory-toolkit/seed/schemas/
```
Expected: no output, exit 0

- [ ] **Step 4: Verify copy**

Run: `diff -r /home/zivben/repos/basic-memory-toolkit/schemas/ /home/zivben/repos/basic-memory-toolkit/seed/schemas/`
Expected: no output (directories identical)

- [ ] **Step 5: Commit**

```bash
git add seed/schemas/
git commit -m "$(cat <<'EOF'
feat(seed): add schemas seed folder with 8 canonical schemas

Copies the plugin's /schemas/*.md into seed/schemas/ so /install-schemas
can source them at install time. The /schemas folder remains the
authoritative edit location; seed/schemas is the install source.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task Group B — Picoschema To JSON Schema Translator

### Task B1: Create test fixtures directory and first simple fixture

**Files:**
- Create: `tests/unit/picoschema/__init__.py`
- Create: `tests/unit/picoschema/fixtures/__init__.py`
- Create: `tests/unit/picoschema/fixtures/simple_required/input.md`
- Create: `tests/unit/picoschema/fixtures/simple_required/expected.yaml`

- [ ] **Step 1: Create test directory structure**

Run:
```bash
mkdir -p /home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/simple_required
touch /home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/__init__.py
touch /home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/__init__.py
```

- [ ] **Step 2: Create simple-required fixture input**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/simple_required/input.md`:
```markdown
---
title: Simple Required Schema
type: schema
entity: simple-required
version: 1
schema:
  name: string, the name of the thing
  age: string, age as a string
settings:
  validation: warn
---

# Simple Required Schema

Test fixture: two required string fields, no optionals, no arrays, no enums.
```

- [ ] **Step 3: Create simple-required fixture expected output**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/simple_required/expected.yaml`:
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: simple-required
type: object
required:
  - name
  - age
properties:
  name:
    type: string
    description: the name of the thing
  age:
    type: string
    description: age as a string
additionalProperties: true
```

- [ ] **Step 4: Commit**

```bash
git add tests/unit/picoschema/
git commit -m "test(picoschema): add simple-required fixture for translator"
```

### Task B2: Write failing test for picoschema translator

**Files:**
- Create: `tests/unit/picoschema/test_translator.py`

- [ ] **Step 1: Write test file**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/test_translator.py`:
```python
"""Tests for picoschema-to-JSON-Schema translator."""
from pathlib import Path

import yaml
import pytest

# Will fail import until translator exists — that's the point
from scripts.picoschema_to_jsonschema import translate_schema_file


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> tuple[Path, dict]:
    """Return (input_path, expected_dict) for a named fixture."""
    input_path = FIXTURES_DIR / name / "input.md"
    expected_path = FIXTURES_DIR / name / "expected.yaml"
    expected = yaml.safe_load(expected_path.read_text())
    return input_path, expected


def test_simple_required():
    input_path, expected = load_fixture("simple_required")
    result = translate_schema_file(input_path)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails with import error**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py -v 2>&1 | head -20`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.picoschema_to_jsonschema'`

- [ ] **Step 3: Commit**

```bash
git add tests/unit/picoschema/test_translator.py
git commit -m "test(picoschema): add failing translator test with simple_required fixture"
```

### Task B3: Implement minimal translator — required string fields only

**Files:**
- Create: `scripts/__init__.py`
- Create: `scripts/picoschema_to_jsonschema.py`

- [ ] **Step 1: Create scripts package init**

Run: `touch /home/zivben/repos/basic-memory-toolkit/scripts/__init__.py`

- [ ] **Step 2: Write minimal translator**

Write `/home/zivben/repos/basic-memory-toolkit/scripts/picoschema_to_jsonschema.py`:
```python
"""Translate Basic Memory picoschema YAML → JSON Schema YAML.

Picoschema grammar (from inspection of /schemas/*.md):

  key: type, description            # required scalar
  key?: type, description           # optional scalar
  key?(array): type, description    # optional array of type
  key?(enum): [v1, v2, v3]          # optional enum (string type)

Output: JSON Schema draft-07 as a Python dict (caller serializes to YAML).
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml


_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _extract_frontmatter(markdown_text: str) -> dict:
    """Return parsed YAML frontmatter from a schema markdown file."""
    match = _FRONTMATTER_RE.match(markdown_text)
    if not match:
        raise ValueError("No YAML frontmatter found")
    return yaml.safe_load(match.group(1))


def _parse_value(raw_value: str) -> tuple[str, str]:
    """Split 'type, description' — return (type_token, description)."""
    if "," in raw_value:
        type_token, description = raw_value.split(",", 1)
        return type_token.strip(), description.strip()
    return raw_value.strip(), ""


def _translate_field(raw_key: str, raw_value) -> tuple[str, bool, dict]:
    """Translate one picoschema field.

    Returns (field_name, is_required, json_schema_fragment).
    """
    # Strip optional marker
    is_required = not raw_key.endswith("?") and "?(" not in raw_key
    # Normalize key — remove trailing ? and any (modifier)
    name = raw_key.rstrip("?").split("(")[0].rstrip("?")
    # The raw_key may look like "field?(array)" — extract modifier
    modifier = None
    if "(" in raw_key and ")" in raw_key:
        modifier = raw_key[raw_key.index("(") + 1 : raw_key.index(")")]
    # For initial Task B3 scope: only handle scalar string fields, no modifiers
    if modifier is not None:
        raise NotImplementedError(f"Modifier '{modifier}' not yet supported")
    type_token, description = _parse_value(raw_value)
    fragment = {"type": type_token}
    if description:
        fragment["description"] = description
    return name, is_required, fragment


def translate_schema_file(path: Path) -> dict:
    """Read a schema markdown file and return its JSON Schema dict."""
    markdown = Path(path).read_text()
    frontmatter = _extract_frontmatter(markdown)
    entity = frontmatter.get("entity")
    schema_block = frontmatter.get("schema", {})

    properties: dict = {}
    required: list[str] = []
    for raw_key, raw_value in schema_block.items():
        name, is_required, fragment = _translate_field(raw_key, raw_value)
        properties[name] = fragment
        if is_required:
            required.append(name)

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": entity,
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }
```

- [ ] **Step 3: Run test to verify it passes**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py::test_simple_required -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add scripts/__init__.py scripts/picoschema_to_jsonschema.py
git commit -m "feat(picoschema): implement minimal translator for required scalar fields"
```

### Task B4: Add optional field support

**Files:**
- Create: `tests/unit/picoschema/fixtures/with_optional/input.md`
- Create: `tests/unit/picoschema/fixtures/with_optional/expected.yaml`
- Modify: `tests/unit/picoschema/test_translator.py`

- [ ] **Step 1: Create optional-field fixture input**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_optional/input.md`:
```markdown
---
title: Optional Field Schema
type: schema
entity: with-optional
version: 1
schema:
  name: string, required name
  nickname?: string, optional nickname
settings:
  validation: warn
---

# With Optional Schema

Test fixture: one required, one optional, both scalar strings.
```

- [ ] **Step 2: Create optional-field fixture expected output**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_optional/expected.yaml`:
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: with-optional
type: object
required:
  - name
properties:
  name:
    type: string
    description: required name
  nickname:
    type: string
    description: optional nickname
additionalProperties: true
```

- [ ] **Step 3: Add test case to test_translator.py**

Append to `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/test_translator.py`:
```python


def test_with_optional():
    input_path, expected = load_fixture("with_optional")
    result = translate_schema_file(input_path)
    assert result == expected
```

- [ ] **Step 4: Run test to verify it passes (optional fields already handled)**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py -v`
Expected: both tests PASS (the initial implementation already handles `?` suffix)

- [ ] **Step 5: Commit**

```bash
git add tests/unit/picoschema/fixtures/with_optional/ tests/unit/picoschema/test_translator.py
git commit -m "test(picoschema): verify optional-field translation"
```

### Task B5: Add enum support

**Files:**
- Create: `tests/unit/picoschema/fixtures/with_enum/input.md`
- Create: `tests/unit/picoschema/fixtures/with_enum/expected.yaml`
- Modify: `scripts/picoschema_to_jsonschema.py`
- Modify: `tests/unit/picoschema/test_translator.py`

- [ ] **Step 1: Create enum fixture input**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_enum/input.md`:
```markdown
---
title: Enum Field Schema
type: schema
entity: with-enum
version: 1
schema:
  name: string, thing name
  severity?(enum): [critical, high, medium, low]
settings:
  validation: warn
---

# With Enum Schema

Test fixture: required scalar + optional enum.
```

- [ ] **Step 2: Create enum fixture expected output**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_enum/expected.yaml`:
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: with-enum
type: object
required:
  - name
properties:
  name:
    type: string
    description: thing name
  severity:
    type: string
    enum:
      - critical
      - high
      - medium
      - low
additionalProperties: true
```

- [ ] **Step 3: Add failing test case**

Append to `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/test_translator.py`:
```python


def test_with_enum():
    input_path, expected = load_fixture("with_enum")
    result = translate_schema_file(input_path)
    assert result == expected
```

- [ ] **Step 4: Run to confirm failure**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py::test_with_enum -v 2>&1 | tail -10`
Expected: FAIL — `NotImplementedError: Modifier 'enum' not yet supported`

- [ ] **Step 5: Extend translator for enum**

Replace the `_translate_field` function in `/home/zivben/repos/basic-memory-toolkit/scripts/picoschema_to_jsonschema.py` with:
```python
def _translate_field(raw_key: str, raw_value) -> tuple[str, bool, dict]:
    """Translate one picoschema field.

    Returns (field_name, is_required, json_schema_fragment).
    """
    is_required = not raw_key.endswith("?") and "?(" not in raw_key
    # Extract modifier, if present
    modifier = None
    if "(" in raw_key and ")" in raw_key:
        modifier = raw_key[raw_key.index("(") + 1 : raw_key.index(")")]
        name = raw_key[: raw_key.index("?(")] if "?(" in raw_key else raw_key[: raw_key.index("(")]
    else:
        name = raw_key.rstrip("?")

    if modifier == "enum":
        # raw_value is already a list from YAML parser
        if not isinstance(raw_value, list):
            raise ValueError(f"enum field '{name}' expects a list value, got {type(raw_value).__name__}")
        return name, is_required, {"type": "string", "enum": raw_value}

    if modifier is not None and modifier != "enum":
        raise NotImplementedError(f"Modifier '{modifier}' not yet supported")

    type_token, description = _parse_value(raw_value)
    fragment = {"type": type_token}
    if description:
        fragment["description"] = description
    return name, is_required, fragment
```

- [ ] **Step 6: Run test to verify it passes**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py -v`
Expected: 3 tests PASS

- [ ] **Step 7: Commit**

```bash
git add tests/unit/picoschema/fixtures/with_enum/ tests/unit/picoschema/test_translator.py scripts/picoschema_to_jsonschema.py
git commit -m "feat(picoschema): add enum modifier support"
```

### Task B6: Add array support

**Files:**
- Create: `tests/unit/picoschema/fixtures/with_array/input.md`
- Create: `tests/unit/picoschema/fixtures/with_array/expected.yaml`
- Modify: `scripts/picoschema_to_jsonschema.py`
- Modify: `tests/unit/picoschema/test_translator.py`

- [ ] **Step 1: Create array fixture input**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_array/input.md`:
```markdown
---
title: Array Field Schema
type: schema
entity: with-array
version: 1
schema:
  name: string, thing name
  options?(array): string, considered alternatives
settings:
  validation: warn
---

# With Array Schema

Test fixture: required scalar + optional array of strings.
```

- [ ] **Step 2: Create array fixture expected output**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/fixtures/with_array/expected.yaml`:
```yaml
$schema: http://json-schema.org/draft-07/schema#
title: with-array
type: object
required:
  - name
properties:
  name:
    type: string
    description: thing name
  options:
    type: array
    items:
      type: string
    description: considered alternatives
additionalProperties: true
```

- [ ] **Step 3: Add failing test case**

Append to `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/test_translator.py`:
```python


def test_with_array():
    input_path, expected = load_fixture("with_array")
    result = translate_schema_file(input_path)
    assert result == expected
```

- [ ] **Step 4: Run to confirm failure**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py::test_with_array -v 2>&1 | tail -10`
Expected: FAIL — `NotImplementedError: Modifier 'array' not yet supported`

- [ ] **Step 5: Extend translator for array**

In `/home/zivben/repos/basic-memory-toolkit/scripts/picoschema_to_jsonschema.py`, replace the `if modifier is not None and modifier != "enum":` branch inside `_translate_field` with:
```python
    if modifier == "array":
        type_token, description = _parse_value(raw_value)
        fragment = {
            "type": "array",
            "items": {"type": type_token},
        }
        if description:
            fragment["description"] = description
        return name, is_required, fragment

    if modifier is not None and modifier != "enum":
        raise NotImplementedError(f"Modifier '{modifier}' not yet supported")
```

- [ ] **Step 6: Run test to verify it passes**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py -v`
Expected: 4 tests PASS

- [ ] **Step 7: Commit**

```bash
git add tests/unit/picoschema/fixtures/with_array/ tests/unit/picoschema/test_translator.py scripts/picoschema_to_jsonschema.py
git commit -m "feat(picoschema): add array modifier support"
```

### Task B7: Integration test — translate all 8 real schemas without error

**Files:**
- Modify: `tests/unit/picoschema/test_translator.py`

- [ ] **Step 1: Add real-schemas test**

Append to `/home/zivben/repos/basic-memory-toolkit/tests/unit/picoschema/test_translator.py`:
```python


REAL_SCHEMAS_DIR = Path(__file__).parent.parent.parent.parent / "seed" / "schemas"


@pytest.mark.parametrize("schema_file", sorted(REAL_SCHEMAS_DIR.glob("*.md")))
def test_real_schema_translates_without_error(schema_file: Path):
    """Every shipped schema must translate to a valid JSON Schema dict."""
    result = translate_schema_file(schema_file)
    assert result["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert result["type"] == "object"
    assert "title" in result
    assert isinstance(result["required"], list)
    assert isinstance(result["properties"], dict)
```

- [ ] **Step 2: Run test**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/picoschema/test_translator.py -v`
Expected: all unit tests PASS + 8 parameterized tests PASS (one per schema). If any fails with `NotImplementedError`, note the modifier in the failure output — we'll need to add it.

- [ ] **Step 3: Fix any uncovered modifiers discovered**

If the parametrized test reveals a new modifier not yet supported:
- Add a failing fixture for it
- Extend `_translate_field` minimally
- Re-run until all 8 schemas translate cleanly

(If all 8 pass at Step 2, skip this step.)

- [ ] **Step 4: Commit**

```bash
git add tests/unit/picoschema/test_translator.py scripts/picoschema_to_jsonschema.py 2>/dev/null
git commit -m "test(picoschema): verify all 8 shipped schemas translate without error"
```

### Task B8: Add CLI wrapper for the translator

**Files:**
- Modify: `scripts/picoschema_to_jsonschema.py`

- [ ] **Step 1: Append CLI entry point**

Append to `/home/zivben/repos/basic-memory-toolkit/scripts/picoschema_to_jsonschema.py`:
```python


def main(argv: list[str]) -> int:
    """CLI: translate one or more schema files, write .yaml derivatives beside each."""
    import sys
    if len(argv) < 3:
        print(
            "Usage: picoschema_to_jsonschema.py <input-schema.md> <output-derivative.yaml>",
            file=sys.stderr,
        )
        return 2
    input_path, output_path = Path(argv[1]), Path(argv[2])
    try:
        result = translate_schema_file(input_path)
    except (ValueError, NotImplementedError) as exc:
        print(f"ERROR translating {input_path}: {exc}", file=sys.stderr)
        return 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(result, sort_keys=False))
    print(f"OK: {input_path} -> {output_path}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
```

- [ ] **Step 2: Verify CLI works against a real schema**

Run:
```bash
cd /home/zivben/repos/basic-memory-toolkit && \
python3 scripts/picoschema_to_jsonschema.py seed/schemas/bug-report.md /tmp/bug-report.yaml && \
cat /tmp/bug-report.yaml
```
Expected: prints `OK: ... -> /tmp/bug-report.yaml`, then a valid JSON Schema YAML

- [ ] **Step 3: Verify `ys` accepts the output**

Run:
```bash
cat > /tmp/test-bug.yaml <<'EOF'
title: Test Bug
severity: high
affected_service: parser
reproduction_steps: Send large message
EOF
ys -f /tmp/bug-report.yaml /tmp/test-bug.yaml
echo "exit=$?"
```
Expected: exit=0 (valid)

- [ ] **Step 4: Verify `ys` rejects invalid output**

Run:
```bash
cat > /tmp/test-bug-bad.yaml <<'EOF'
title: Test Bug
severity: extreme
affected_service: parser
reproduction_steps: Send large message
EOF
ys -f /tmp/bug-report.yaml /tmp/test-bug-bad.yaml --json
echo "exit=$?"
```
Expected: exit=1, JSON error mentioning enum violation for `severity`

- [ ] **Step 5: Commit**

```bash
git add scripts/picoschema_to_jsonschema.py
git commit -m "feat(picoschema): add CLI wrapper with ys-verified output"
```

---

## Task Group C — `/install-schemas` Slash Command

### Task C1: Create install-schemas.sh helper script

**Files:**
- Create: `commands/install-schemas-helper.sh`

- [ ] **Step 1: Write the helper script**

Write `/home/zivben/repos/basic-memory-toolkit/commands/install-schemas-helper.sh`:
```bash
#!/usr/bin/env bash
# install-schemas-helper.sh
# Installs schemas from seed/schemas/ into a target basic-memory project,
# generating JSON Schema derivatives via scripts/picoschema_to_jsonschema.py.
#
# Usage: install-schemas-helper.sh <project-name>
#
# Exit codes:
#   0 success (even if 0 changes made)
#   1 project not found in basic-memory config
#   2 seed schemas folder missing (plugin install broken)
#   3 python/pyyaml unavailable
#   4 translator failed on one or more schemas

set -euo pipefail

PROJECT_NAME="${1:-}"
if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: install-schemas-helper.sh <project-name>" >&2
    exit 1
fi

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SEED_DIR="${PLUGIN_ROOT}/seed/schemas"
TRANSLATOR="${PLUGIN_ROOT}/scripts/picoschema_to_jsonschema.py"
BM_DB="${HOME}/.basic-memory/memory.db"

if [ ! -d "$SEED_DIR" ]; then
    echo "ERROR: Seed schemas folder missing at $SEED_DIR — plugin install broken." >&2
    exit 2
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 not available on PATH." >&2
    exit 3
fi

# Resolve project path via SQLite
PROJECT_PATH=$(sqlite3 "$BM_DB" \
    "SELECT path FROM project WHERE name='${PROJECT_NAME}' LIMIT 1;")
if [ -z "$PROJECT_PATH" ]; then
    echo "ERROR: Project '$PROJECT_NAME' not registered in basic-memory." >&2
    exit 1
fi

DEST_SCHEMAS="${PROJECT_PATH}/schemas"
DEST_DERIVATIVES="${PROJECT_PATH}/.schemas-jsonschema"
MANIFEST="${DEST_DERIVATIVES}/.installed.json"

mkdir -p "$DEST_SCHEMAS" "$DEST_DERIVATIVES"

# Counters
installed=0
updated=0
uptodate=0
customized=0
failed=0

# Process each seed schema
for src in "$SEED_DIR"/*.md; do
    [ -e "$src" ] || continue
    base=$(basename "$src")
    name="${base%.md}"
    dest="${DEST_SCHEMAS}/${base}"
    derivative="${DEST_DERIVATIVES}/${name}.yaml"

    src_version=$(grep -E '^version:' "$src" | head -1 | awk '{print $2}' | tr -d '[:space:]')
    src_checksum=$(sha256sum "$src" | awk '{print $1}')

    if [ ! -f "$dest" ]; then
        # New install
        cp "$src" "$dest"
        if python3 "$TRANSLATOR" "$dest" "$derivative" >/dev/null 2>&1; then
            installed=$((installed + 1))
        else
            echo "WARN: Translator failed on $name; derivative not generated." >&2
            failed=$((failed + 1))
        fi
    else
        dest_version=$(grep -E '^version:' "$dest" | head -1 | awk '{print $2}' | tr -d '[:space:]')
        dest_checksum=$(sha256sum "$dest" | awk '{print $1}')
        if [ "$src_checksum" = "$dest_checksum" ]; then
            # mtime-based check: regenerate derivative if source newer
            if [ ! -f "$derivative" ] || [ "$dest" -nt "$derivative" ]; then
                python3 "$TRANSLATOR" "$dest" "$derivative" >/dev/null 2>&1 || true
            fi
            uptodate=$((uptodate + 1))
        elif [ "$(printf '%s\n%s\n' "$dest_version" "$src_version" | sort -n | head -1)" = "$dest_version" ] \
             && [ "$dest_version" != "$src_version" ]; then
            # Dest older than src — update
            cp "$src" "$dest"
            python3 "$TRANSLATOR" "$dest" "$derivative" >/dev/null 2>&1 || failed=$((failed + 1))
            updated=$((updated + 1))
        else
            # Dest newer or same version but different content (customized)
            customized=$((customized + 1))
        fi
    fi
done

# Write manifest
python3 - "$MANIFEST" "$DEST_SCHEMAS" <<'PY'
import json, sys, hashlib
from pathlib import Path
manifest_path, schemas_dir = Path(sys.argv[1]), Path(sys.argv[2])
entries = {}
for f in sorted(schemas_dir.glob("*.md")):
    name = f.stem
    data = f.read_text()
    version = "1"
    for line in data.splitlines():
        if line.startswith("version:"):
            version = line.split(":", 1)[1].strip()
            break
    checksum = hashlib.sha256(data.encode()).hexdigest()
    entries[name] = {"version": version, "source_checksum": f"sha256:{checksum}"}
manifest_path.write_text(json.dumps(entries, indent=2, sort_keys=True))
PY

echo "Installed: $installed  Updated: $updated  Up-to-date: $uptodate  Customized: $customized  Failed: $failed"
if [ "$failed" -gt 0 ]; then
    exit 4
fi
exit 0
```

- [ ] **Step 2: Make executable**

Run: `chmod +x /home/zivben/repos/basic-memory-toolkit/commands/install-schemas-helper.sh`

- [ ] **Step 3: Commit**

```bash
git add commands/install-schemas-helper.sh
git commit -m "feat(install-schemas): add helper bash script for schema installation"
```

### Task C2: Write integration test for install-schemas-helper

**Files:**
- Create: `tests/integration/test_install_schemas.py`

- [ ] **Step 1: Write integration test**

Write `/home/zivben/repos/basic-memory-toolkit/tests/integration/test_install_schemas.py`:
```python
"""Integration test for install-schemas-helper.sh using a throwaway project.

NOTE: This test creates a REAL basic-memory project in a temporary location and
cleans up afterward. It requires basic-memory to be installed and the plugin
seed/schemas/ to exist.
"""
import json
import shutil
import sqlite3
import subprocess
import tempfile
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).parent.parent.parent
HELPER = PLUGIN_ROOT / "commands" / "install-schemas-helper.sh"
SEED_DIR = PLUGIN_ROOT / "seed" / "schemas"
BM_DB = Path.home() / ".basic-memory" / "memory.db"


@pytest.fixture
def throwaway_project(tmp_path):
    """Register a temporary basic-memory project and tear down after test."""
    proj_name = f"test-install-schemas-{tmp_path.name}"
    proj_path = tmp_path / "proj"
    proj_path.mkdir()
    # Register via direct SQL insert to avoid MCP session dependency
    conn = sqlite3.connect(BM_DB)
    try:
        conn.execute(
            "INSERT INTO project (name, permalink, path, is_active, external_id, "
            "created_at, updated_at) VALUES (?, ?, ?, 1, ?, datetime('now'), datetime('now'))",
            (proj_name, proj_name, str(proj_path), f"ext-{proj_name}"),
        )
        conn.commit()
    finally:
        conn.close()
    yield proj_name, proj_path
    conn = sqlite3.connect(BM_DB)
    try:
        conn.execute("DELETE FROM project WHERE name=?", (proj_name,))
        conn.commit()
    finally:
        conn.close()


def test_fresh_install_copies_all_schemas(throwaway_project):
    proj_name, proj_path = throwaway_project
    result = subprocess.run(
        [str(HELPER), proj_name],
        capture_output=True,
        text=True,
        check=True,
    )
    # Verify all 8 schemas present in dest
    dest_schemas = proj_path / "schemas"
    assert dest_schemas.is_dir()
    for seed_schema in SEED_DIR.glob("*.md"):
        assert (dest_schemas / seed_schema.name).is_file(), f"missing {seed_schema.name}"
    # Verify derivatives generated
    dest_derivatives = proj_path / ".schemas-jsonschema"
    assert dest_derivatives.is_dir()
    for seed_schema in SEED_DIR.glob("*.md"):
        assert (dest_derivatives / f"{seed_schema.stem}.yaml").is_file()
    # Verify manifest written
    manifest = json.loads((dest_derivatives / ".installed.json").read_text())
    assert len(manifest) == len(list(SEED_DIR.glob("*.md")))


def test_second_install_reports_uptodate(throwaway_project):
    proj_name, proj_path = throwaway_project
    subprocess.run([str(HELPER), proj_name], check=True)
    result = subprocess.run(
        [str(HELPER), proj_name],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Up-to-date:" in result.stdout
    # Last run summary line — extract the up-to-date count
    parts = result.stdout.strip().split()
    uptodate_idx = parts.index("Up-to-date:") + 1
    assert int(parts[uptodate_idx]) == len(list(SEED_DIR.glob("*.md")))


def test_unknown_project_exits_nonzero():
    result = subprocess.run(
        [str(HELPER), "definitely-not-a-real-project-xyz"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "not registered" in result.stderr
```

- [ ] **Step 2: Run integration test**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/integration/test_install_schemas.py -v`
Expected: 3 tests PASS. If any fail, inspect the failure — possible causes: BM_DB path wrong, seed folder not populated, translator dependency missing.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_install_schemas.py
git commit -m "test(install-schemas): integration tests for fresh/uptodate/missing-project paths"
```

### Task C3: Create install-schemas.md slash command

**Files:**
- Create: `commands/install-schemas.md`

- [ ] **Step 1: Write the slash command markdown**

Write `/home/zivben/repos/basic-memory-toolkit/commands/install-schemas.md`:
```markdown
---
name: install-schemas
description: Install or update Basic Memory schemas into a project. Copies the plugin's canonical schemas from seed/schemas/ into the target project's schemas/ folder and generates JSON Schema derivatives used by the hook validator. Handles version tracking, customization preservation, and derivative regeneration on source change.
argument-hint: [project-name]
---

# Install Schemas

Install or refresh the Basic Memory schema set into a target memory project.

## Behavior

1. Resolves the target project's filesystem path via `~/.basic-memory/memory.db`.
2. For each schema in the plugin's `seed/schemas/` folder:
   - If missing in project: copies in, generates JSON Schema derivative
   - If present and same version: leaves alone (regenerates derivative only if source mtime is newer)
   - If present and older version: prompts user to update
   - If present and newer version (user-customized): skips and warns
3. Writes a manifest at `<project-path>/.schemas-jsonschema/.installed.json` with per-schema version + source checksum.
4. Reports per-category counts.

## Usage

`/install-schemas <project-name>`

If no project name provided, use the currently-selected session project.

## Invocation

Invoke the helper script:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/commands/install-schemas-helper.sh" "$1"
```

## Error Handling

- Exit 1: project not registered in basic-memory → prompt user to run `list_memory_projects()` to verify project name
- Exit 2: plugin seed folder missing → plugin install is broken
- Exit 3: Python unavailable → prompt user to install python3
- Exit 4: one or more schemas failed translation → surface stderr to user

## Cross-References

- Source schemas: `/schemas/` (plugin repo, authoritative edit location)
- Seed copies: `/seed/schemas/` (install source)
- Translator: `/scripts/picoschema_to_jsonschema.py`
- Per-project destination: `<project-path>/schemas/` + `<project-path>/.schemas-jsonschema/`
```

- [ ] **Step 2: Commit**

```bash
git add commands/install-schemas.md
git commit -m "feat(commands): add /install-schemas slash command"
```

---

## Task Group D — Session-Start Hook Enhancement

### Task D1: Write state-detection test for schema folder states

**Files:**
- Create: `tests/unit/session_start/__init__.py`
- Create: `tests/unit/session_start/test_schema_state.py`

- [ ] **Step 1: Create test directory**

Run: `mkdir -p /home/zivben/repos/basic-memory-toolkit/tests/unit/session_start && touch /home/zivben/repos/basic-memory-toolkit/tests/unit/session_start/__init__.py`

- [ ] **Step 2: Write test file**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/session_start/test_schema_state.py`:
```python
"""Test schema-folder state detection used by session-start hook.

We extract the state-detection logic into a standalone bash snippet that can
be tested with fixture directories.
"""
import subprocess
import tempfile
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).parent.parent.parent.parent
DETECTOR = PLUGIN_ROOT / "hooks" / "scripts" / "detect-schema-state.sh"


def run_detector(project_path: Path, seed_dir: Path) -> str:
    """Invoke detector, return stdout (the state keyword)."""
    result = subprocess.run(
        [str(DETECTOR), str(project_path), str(seed_dir)],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_missing_schemas_folder_returns_missing(tmp_path):
    proj = tmp_path / "proj"
    proj.mkdir()
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "x.md").write_text("---\nversion: 1\n---\n")
    assert run_detector(proj, seed) == "missing"


def test_empty_schemas_folder_returns_optout(tmp_path):
    proj = tmp_path / "proj"
    (proj / "schemas").mkdir(parents=True)
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "x.md").write_text("---\nversion: 1\n---\n")
    assert run_detector(proj, seed) == "optout"


def test_populated_schemas_up_to_date_returns_current(tmp_path):
    proj = tmp_path / "proj"
    schemas = proj / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "x.md").write_text("---\nversion: 1\n---\n")
    derivatives = proj / ".schemas-jsonschema"
    derivatives.mkdir()
    (derivatives / "x.yaml").write_text("type: object\n")
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "x.md").write_text("---\nversion: 1\n---\n")
    assert run_detector(proj, seed) == "current"


def test_stale_derivatives_returns_stale(tmp_path):
    import time
    proj = tmp_path / "proj"
    schemas = proj / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "x.md").write_text("---\nversion: 1\n---\n")
    derivatives = proj / ".schemas-jsonschema"
    derivatives.mkdir()
    old_yaml = derivatives / "x.yaml"
    old_yaml.write_text("type: object\n")
    time.sleep(0.01)
    # Touch source newer than derivative
    (schemas / "x.md").write_text("---\nversion: 1\nmodified: true\n---\n")
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "x.md").write_text("---\nversion: 1\n---\n")
    assert run_detector(proj, seed) == "stale"


def test_seed_newer_version_returns_update_available(tmp_path):
    proj = tmp_path / "proj"
    schemas = proj / "schemas"
    schemas.mkdir(parents=True)
    (schemas / "x.md").write_text("---\nversion: 1\n---\n")
    seed = tmp_path / "seed"
    seed.mkdir()
    (seed / "x.md").write_text("---\nversion: 2\n---\n")
    # Derivative exists and is current for dest version
    derivatives = proj / ".schemas-jsonschema"
    derivatives.mkdir()
    (derivatives / "x.yaml").write_text("type: object\n")
    assert run_detector(proj, seed) == "update-available"
```

- [ ] **Step 3: Run test to confirm failure (detector script doesn't exist yet)**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/session_start/test_schema_state.py -v 2>&1 | head -15`
Expected: all 5 tests FAIL — detector script not found

- [ ] **Step 4: Commit**

```bash
git add tests/unit/session_start/
git commit -m "test(session-start): add state-detection tests for schema folder"
```

### Task D2: Implement detect-schema-state.sh

**Files:**
- Create: `hooks/scripts/detect-schema-state.sh`

- [ ] **Step 1: Write detector script**

Write `/home/zivben/repos/basic-memory-toolkit/hooks/scripts/detect-schema-state.sh`:
```bash
#!/usr/bin/env bash
# detect-schema-state.sh
# Detects the state of a project's schemas folder vs. plugin seed.
#
# Usage: detect-schema-state.sh <project-path> <seed-dir>
#
# Outputs one of:
#   missing           — schemas/ directory does not exist
#   optout            — schemas/ exists and is empty
#   current           — schemas/ populated, derivatives present, versions match seed
#   stale             — derivatives older than source schemas
#   update-available  — seed has newer version than installed

set -euo pipefail

PROJECT_PATH="${1:-}"
SEED_DIR="${2:-}"

if [ -z "$PROJECT_PATH" ] || [ -z "$SEED_DIR" ]; then
    echo "Usage: detect-schema-state.sh <project-path> <seed-dir>" >&2
    exit 2
fi

SCHEMAS="${PROJECT_PATH}/schemas"
DERIVATIVES="${PROJECT_PATH}/.schemas-jsonschema"

# Missing folder
if [ ! -d "$SCHEMAS" ]; then
    echo "missing"
    exit 0
fi

# Empty folder = opt-out
if [ -z "$(ls -A "$SCHEMAS" 2>/dev/null)" ]; then
    echo "optout"
    exit 0
fi

# Check for any seed schema with newer version than installed
for src in "$SEED_DIR"/*.md; do
    [ -e "$src" ] || continue
    base=$(basename "$src")
    dest="${SCHEMAS}/${base}"
    [ -f "$dest" ] || continue
    src_ver=$(grep -E '^version:' "$src" | head -1 | awk '{print $2}' | tr -d '[:space:]')
    dest_ver=$(grep -E '^version:' "$dest" | head -1 | awk '{print $2}' | tr -d '[:space:]')
    if [ -n "$src_ver" ] && [ -n "$dest_ver" ] && [ "$src_ver" != "$dest_ver" ]; then
        # Compare numerically; if src > dest, update-available
        if [ "$(printf '%s\n%s\n' "$dest_ver" "$src_ver" | sort -n | head -1)" = "$dest_ver" ]; then
            echo "update-available"
            exit 0
        fi
    fi
done

# Check for stale derivatives (source schemas newer than .yaml files)
if [ -d "$DERIVATIVES" ]; then
    for src in "$SCHEMAS"/*.md; do
        [ -e "$src" ] || continue
        base=$(basename "$src" .md)
        derivative="${DERIVATIVES}/${base}.yaml"
        if [ -f "$derivative" ]; then
            if [ "$src" -nt "$derivative" ]; then
                echo "stale"
                exit 0
            fi
        else
            echo "stale"
            exit 0
        fi
    done
else
    echo "stale"
    exit 0
fi

echo "current"
exit 0
```

- [ ] **Step 2: Make executable**

Run: `chmod +x /home/zivben/repos/basic-memory-toolkit/hooks/scripts/detect-schema-state.sh`

- [ ] **Step 3: Run tests to verify they pass**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/session_start/test_schema_state.py -v`
Expected: all 5 tests PASS

- [ ] **Step 4: Commit**

```bash
git add hooks/scripts/detect-schema-state.sh
git commit -m "feat(session-start): add schema-folder state detector"
```

### Task D3: Integrate detector into session-start hook

**Files:**
- Modify: `hooks/session-start`

- [ ] **Step 1: Read existing session-start**

Run: `cat /home/zivben/repos/basic-memory-toolkit/hooks/session-start | tail -40`
Expected: shows the existing first-run and project-selection logic; identify the location AFTER project selection is confirmed (or the end of the script) where schema-state integration belongs.

- [ ] **Step 2: Add schema-state check block to session-start**

Append the following block at the end of `/home/zivben/repos/basic-memory-toolkit/hooks/session-start` (before any `exit 0` if present, otherwise at EOF). This block adds a guidance message to the existing output — it does NOT auto-invoke `/install-schemas`; it surfaces the state and lets Claude/user decide:

```bash

# === Schema-folder state check (added for Cycle 1) ===
# Emits a guidance note appended to the session-start message based on schema state.
# The project to check is determined at session time by Claude's selected project;
# since we can't know that in the hook before Claude picks, we emit a conditional
# "if schema state is X, ask the user to..." instruction block.
SEED_SCHEMAS="${PLUGIN_ROOT}/seed/schemas"
DETECTOR="${PLUGIN_ROOT}/hooks/scripts/detect-schema-state.sh"
if [ -d "$SEED_SCHEMAS" ] && [ -x "$DETECTOR" ]; then
    cat <<SCHEMA_NOTE

<EXTREMELY_IMPORTANT>
AFTER PROJECT SELECTION, CHECK SCHEMA STATE:

1. Resolve the selected project's filesystem path:
   sqlite3 ~/.basic-memory/memory.db "SELECT path FROM project WHERE name='<selected>'"
2. Run: bash "${DETECTOR}" "<project-path>" "${SEED_SCHEMAS}"
3. Based on the one-word output, take action:
   - "missing": prompt user "This project has no schemas/ folder.
     [install / opt-out / skip-this-session]"
     On 'install': invoke /install-schemas <project>
     On 'opt-out': mkdir empty schemas/ folder at the project path
     On 'skip-this-session': no action
   - "optout": silent. User has explicitly opted out.
   - "current": silent. All good.
   - "stale": silently regenerate derivatives by running /install-schemas <project>
     (no user prompt — this is a no-op for the user)
   - "update-available": prompt user "Plugin schemas updated for this project.
     [update / dismiss-this-session]"
     On 'update': invoke /install-schemas <project>
</EXTREMELY_IMPORTANT>
SCHEMA_NOTE
fi
```

- [ ] **Step 3: Verify the hook runs without error**

Run: `bash /home/zivben/repos/basic-memory-toolkit/hooks/session-start`
Expected: emits the existing first-run/project-selection message plus the new SCHEMA_NOTE block at the end. No errors.

- [ ] **Step 4: Commit**

```bash
git add hooks/session-start
git commit -m "feat(session-start): add schema-folder state guidance block"
```

---

## Task Group E — create-memory-project Skill Update

### Task E1: Locate and update create-memory-project skill

**Files:**
- Modify: `skills/create-new-memory-project/SKILL.md` (or equivalent — verify exact path)

- [ ] **Step 1: Locate the skill file**

Run: `find /home/zivben/repos/basic-memory-toolkit/skills -name "*.md" | xargs grep -l "create-new-memory-project\|Create.*Memory.*Project" 2>/dev/null | head`
Expected: one path. Record it as `SKILL_PATH`.

- [ ] **Step 2: Read current skill content**

Run: `cat <SKILL_PATH>`
Expected: shows current skill definition.

- [ ] **Step 3: Append schema-init prompt step**

Edit `<SKILL_PATH>`, add a new numbered step at the end of the skill's workflow (after project creation succeeds). Use this text:

```markdown

## Step N — Prompt For Schema Initialization

After the project is successfully created, prompt the user:

> "Initialize this project with schemas?
>  - **yes**: install the plugin's 8 canonical schemas
>  - **no**: create an empty schemas/ folder (persistent opt-out signal — session-start won't nudge about schemas again)
>  - **customize**: select which schemas to install"

Based on response:
- `yes` → invoke `/install-schemas <new-project>`
- `no` → `mkdir <project-path>/schemas` (empty folder = opt-out)
- `customize` → list schemas in `/seed/schemas/`, have user pick, then copy only selected files + generate derivatives

**Rationale for empty-folder opt-out:** the session-start hook detects empty schemas/ as an explicit opt-out signal, so this prevents repeated nudges on future sessions.
```

(Replace `N` with the next available step number in the existing skill.)

- [ ] **Step 4: Verify skill markdown is still valid**

Run: `head -20 <SKILL_PATH>`
Expected: frontmatter intact, body well-formed.

- [ ] **Step 5: Commit**

```bash
git add <SKILL_PATH>
git commit -m "feat(skill): create-memory-project prompts for schema initialization"
```

---

## Task Group F — Hook Validator `MISSING_TYPE` Warn-Mode Check

### Task F1: Write failing test for type-field presence check

**Files:**
- Create: `tests/unit/hook_validator/__init__.py`
- Create: `tests/unit/hook_validator/test_missing_type.py`

- [ ] **Step 1: Create test directory**

Run: `mkdir -p /home/zivben/repos/basic-memory-toolkit/tests/unit/hook_validator && touch /home/zivben/repos/basic-memory-toolkit/tests/unit/hook_validator/__init__.py`

- [ ] **Step 2: Write test file**

Write `/home/zivben/repos/basic-memory-toolkit/tests/unit/hook_validator/test_missing_type.py`:
```python
"""Test hook_validator's MISSING_TYPE warn-mode check (Cycle 1 advisory)."""
import json
import subprocess
from pathlib import Path


PLUGIN_ROOT = Path(__file__).parent.parent.parent.parent
HOOK_VALIDATOR = PLUGIN_ROOT / "validators" / "hook_validator.py"


def run_validator(tool_input: dict, mode: str = "warning") -> tuple[int, str, str]:
    """Invoke hook_validator.py with tool_input on stdin, return (code, stdout, stderr)."""
    payload = json.dumps({"tool_input": tool_input})
    result = subprocess.run(
        ["python3", str(HOOK_VALIDATOR), mode],
        input=payload,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def test_missing_type_emits_warning_not_block():
    content = """---
title: Test Note
---

# Test Note

Body content.
"""
    tool_input = {"title": "Test Note", "content": content, "project": "test"}
    code, out, err = run_validator(tool_input, mode="warning")
    # Warn mode MUST NOT block — exit 0 required
    assert code == 0
    # Stderr should mention MISSING_TYPE
    assert "MISSING_TYPE" in err or "type" in err.lower()


def test_present_type_no_warning():
    content = """---
title: Test Note
type: design-decision
---

# Test Note
"""
    tool_input = {"title": "Test Note", "content": content, "project": "test"}
    code, out, err = run_validator(tool_input, mode="warning")
    assert code == 0
    assert "MISSING_TYPE" not in err


def test_free_form_note_type_no_warning():
    content = """---
title: Test Note
type: note
---

Body.
"""
    tool_input = {"title": "Test Note", "content": content, "project": "test"}
    code, out, err = run_validator(tool_input, mode="warning")
    assert code == 0
    assert "MISSING_TYPE" not in err
```

- [ ] **Step 3: Run test to confirm current validator doesn't handle MISSING_TYPE**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/hook_validator/test_missing_type.py::test_missing_type_emits_warning_not_block -v`
Expected: FAIL — either no stderr output mentioning type, or assertion failure on the warning text.

- [ ] **Step 4: Commit**

```bash
git add tests/unit/hook_validator/
git commit -m "test(hook-validator): failing test for MISSING_TYPE warn-mode check"
```

### Task F2: Implement MISSING_TYPE warn-mode check in hook_validator.py

**Files:**
- Modify: `validators/hook_validator.py`

- [ ] **Step 1: Read current hook_validator to find integration point**

Run: `cat /home/zivben/repos/basic-memory-toolkit/validators/hook_validator.py | head -80`
Identify: the main() function and where checks are registered per mode.

- [ ] **Step 2: Add extract_type and check_missing_type functions**

Locate the section of `/home/zivben/repos/basic-memory-toolkit/validators/hook_validator.py` after existing helper functions (around `extract_relations`). Add:

```python
def extract_frontmatter_type(content: str) -> str | None:
    """Return the value of the `type:` frontmatter field, or None if absent."""
    import re
    fm_match = re.match(r"\A---\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return None
    for line in fm_match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("type:"):
            value = stripped.split(":", 1)[1].strip()
            return value or None
    return None


def check_missing_type(content: str) -> list[dict]:
    """Return warnings if `type:` field is missing from frontmatter."""
    if extract_frontmatter_type(content) is None:
        return [{
            "type": "memory_toolkit_warning",
            "check": "MISSING_TYPE",
            "severity": "MEDIUM",
            "detail": "Note is missing a `type:` field in frontmatter.",
            "remediation": (
                "Add `type: <entity>` where <entity> matches a schema in your "
                "project's schemas/ folder, OR `type: note` for free-form content. "
                "Run /install-schemas to see available types."
            ),
        }]
    return []
```

- [ ] **Step 3: Wire check_missing_type into warning mode**

Locate the main() function in `/home/zivben/repos/basic-memory-toolkit/validators/hook_validator.py`. In the warning-mode branch (where MEDIUM/LOW checks run), add:

```python
    # Warn on missing `type:` frontmatter field (Cycle 1 advisory)
    for warning in check_missing_type(content):
        print(json.dumps(warning), file=sys.stderr)
```

(Place inside the existing warning-mode dispatch, following the pattern of any existing MEDIUM/LOW emitters. If the existing dispatch structure is unclear, read the file fully to find the idiomatic spot.)

- [ ] **Step 4: Run the failing test to verify it now passes**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/unit/hook_validator/test_missing_type.py -v`
Expected: all 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add validators/hook_validator.py
git commit -m "feat(hook-validator): add MISSING_TYPE warn-mode check for Cycle 1 advisory"
```

---

## Task Group G — Mandatory Type Declaration Rule Note

### Task G1: Author rule note in memory-rules project

This step is a Basic Memory content operation, not a code change. It authors a rule note the skills will reference at runtime.

- [ ] **Step 1: Invoke create-memory-note workflow**

Use the `basic-memory-toolkit:create-memory-note` skill to create the rule with:
- Project: `memory-rules`
- Folder: `creating-notes`
- Title: `Mandatory Type Declaration`
- Tags: `rule`, `cycle-1`, `type-field`, `schema-activation`, `quality-gate`

Content:
```markdown
# Mandatory Type Declaration

## The Rule

Every new note created via `write_note` MUST declare a `type:` field in its YAML frontmatter. The value must either:

1. Match a schema present in the project's `schemas/` folder (e.g., `type: design-decision` when `schemas/design-decision.md` exists), OR
2. Be the explicit free-form value `type: note` for content that doesn't fit any schema.

A note with no `type:` field, or with a `type:` that references a schema not installed in the project, is NOT a well-formed note.

## Why This Rule Exists

The schema system is Basic Memory's structural backbone. Without a declared `type:`:
- Basic Memory's schema resolver cannot match a schema to the note
- Our validators cannot verify required fields
- Agents writing notes drift into inconsistent structure over time
- Parsing for automation (cache updates, validation, migration) becomes regex-fragile

Declaring `type:` is a quality gate — if a note's purpose is clear enough to write, it's clear enough to classify.

## Enforcement

**Cycle 1 (current)**: Advisory — hook validator emits `MISSING_TYPE` warning in warn mode but does not block.

**Cycle 2 (planned)**: Blocking — PreToolUse hook denies writes with `MISSING_TYPE` or `UNKNOWN_TYPE` reason codes.

**For existing notes** (edits via `edit_note`): not enforced retroactively; legacy notes without `type:` can still be edited. A separate `/migrate-notes-to-schemas` command will batch-retrofit existing notes.

## How To Apply

When writing a new note:

1. Choose the most-fitting schema from the project's `schemas/` folder.
2. If no schema fits and the content is inherently free-form, use `type: note`.
3. If no schema fits but one SHOULD exist for this content type, either:
   - Add the schema to `/seed/schemas/` in the plugin (authoritative edit location), then run `/install-schemas <project>`, then use the new `type:`
   - Or tell the user "this content needs a new schema — here's a proposed one"

## Examples

**Good**:
```yaml
---
title: Some Design Choice
type: design-decision
---
```

**Good (free-form opt-out)**:
```yaml
---
title: Quick Meeting Note
type: note
---
```

**Bad (missing)**:
```yaml
---
title: Some Bug
---
```

**Bad (unknown type)**:
```yaml
---
title: Some Thing
type: nonexistent-schema
---
```

## Observations

- [rule] Every new note must declare `type:` matching a schema or `type: note` #type-field #quality-gate
- [requirement] Schemas must be installed in the project via `/install-schemas` before their type values are valid #schema-activation
- [decision] Cycle 1 enforces via warn-mode hook; Cycle 2 promotes to blocking mode #rollout
- [best-practice] When no schema fits and the content is important, propose a new schema rather than defaulting to `type: note` #schema-authoring

## Relations

- part_of [[Memory Rules Index]]
- relates_to "Validation Architecture Decision" (basic-memory-toolkit)
- relates_to "Cycle 1+2 Brainstorm Decisions — Schema Activation And SQLite Validators" (basic-memory-toolkit)
```

(The create-memory-note skill will handle pre-write dedup search, relation verification, and index-assessment steps per its workflow.)

- [ ] **Step 2: Verify the note resolves in memory-rules project**

Use `read_note(project="memory-rules", identifier="Mandatory Type Declaration")` — verify the content renders and relations are resolved (or gracefully unresolved if target notes aren't in the same project).

- [ ] **Step 3: Index update if needed**

If `Memory Rules Index` exists and doesn't already reference the new rule, append a link under the "Creating Notes" section.

(Note: this task has no git commit — memory notes live in the user's `~/basic-memory-projects/` directory, not in this repo. It's a content operation.)

---

## Task Group H — Phase 1 Smoke Test

### Task H1: Run full test suite

- [ ] **Step 1: Run all unit and integration tests**

Run: `cd /home/zivben/repos/basic-memory-toolkit && python3 -m pytest tests/ -v`
Expected: all tests PASS. Any failures must be fixed before proceeding.

### Task H2: Create throwaway test project and manual smoke test

- [ ] **Step 1: Create test project via basic-memory MCP**

In a Claude Code session, ask the user or directly invoke:
`create_memory_project(project_name="basic-memory-toolkit-dev-test", project_path="/tmp/bm-toolkit-dev-test")`

- [ ] **Step 2: Run /install-schemas on it**

From the Claude Code session: `/install-schemas basic-memory-toolkit-dev-test`
Expected: "Installed: 8  Updated: 0  Up-to-date: 0  Customized: 0  Failed: 0"

- [ ] **Step 3: Verify schemas installed**

Run: `ls /tmp/bm-toolkit-dev-test/schemas/ /tmp/bm-toolkit-dev-test/.schemas-jsonschema/`
Expected: 8 `.md` files + 8 `.yaml` derivatives + `.installed.json`

- [ ] **Step 4: Write a note without type — expect MISSING_TYPE warning**

From the Claude Code session: `write_note(project="basic-memory-toolkit-dev-test", title="Smoke Test No Type", content="# Smoke Test\n\nBody.", folder="testing")`
Expected: write succeeds (warn mode); MISSING_TYPE warning surfaces in the hook output or session log.

- [ ] **Step 5: Write a note WITH type: design-decision and valid fields**

```
write_note(project="basic-memory-toolkit-dev-test",
           title="Smoke Test Valid Schema",
           folder="testing",
           content="""---
type: design-decision
---

# Smoke Test Valid Schema

- context: smoke testing Cycle 1
- chosen_option: proceed with activation
- rationale: unit and integration tests passed
- consequences: ready for Phase 2 gating
""")
```
Expected: write succeeds; no MISSING_TYPE warning.

- [ ] **Step 6: Verify session-start behavior on the test project**

Start a new Claude Code session, select `basic-memory-toolkit-dev-test` as the project. Session-start should emit the schema-state guidance block — verify it detects `current` and stays silent (or emits no prompts).

- [ ] **Step 7: Test opt-out path**

Create another test project `basic-memory-toolkit-dev-test-optout`. From session-start, choose `opt-out` on the schema prompt. Verify `<project-path>/schemas/` is created as an empty folder. Start a new session — session-start should detect `optout` and stay silent.

- [ ] **Step 8: Clean up test projects**

```
delete_project("basic-memory-toolkit-dev-test")
delete_project("basic-memory-toolkit-dev-test-optout")
rm -rf /tmp/bm-toolkit-dev-test /tmp/bm-toolkit-dev-test-optout
```

### Task H3: Update README and CHANGELOG

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md` (create if missing)

- [ ] **Step 1: Read current README**

Run: `head -30 /home/zivben/repos/basic-memory-toolkit/README.md`

- [ ] **Step 2: Add schema activation section to README**

Add a new section to README titled `## Schema System Activation (Cycle 1)` documenting:
- `/install-schemas <project>` command usage
- `type:` frontmatter field requirement (advisory in Cycle 1)
- Opt-out mechanism (empty `schemas/` folder)
- Schema customization preservation
- Version tracking via `.installed.json`

- [ ] **Step 3: Create/update CHANGELOG**

Add entry:
```markdown
## [Unreleased] — Cycle 1: Schema Activation

### Added
- `seed/schemas/` — canonical schema source copied from `/schemas/`
- `/install-schemas <project>` slash command
- `scripts/picoschema_to_jsonschema.py` — picoschema → JSON Schema translator
- `hooks/scripts/detect-schema-state.sh` — session-start state detection
- MISSING_TYPE warn-mode check in hook validator
- Mandatory Type Declaration rule in memory-rules project

### Changed
- `hooks/session-start` — emits schema-state guidance block
- `skills/create-new-memory-project` — prompts for schema initialization
- `validators/hook_validator.py` — extended with MISSING_TYPE check

### Notes
- Type declaration is advisory in Cycle 1. Cycle 2 promotes to blocking with PreToolUse enforcement.
- Schema derivatives (`.schemas-jsonschema/*.yaml`) are checked into projects for zero write-time cost.
```

- [ ] **Step 4: Commit**

```bash
git add README.md CHANGELOG.md
git commit -m "docs: document schema activation (Cycle 1) in README and CHANGELOG"
```

### Task H4: Phase 1 gate verification

- [ ] **Step 1: Verify Phase 1 acceptance criteria**

Checklist:
- [ ] `/install-schemas` works against real basic-memory projects
- [ ] Version tracking correctly reports installed/updated/uptodate/customized counts
- [ ] Session-start emits schema-state guidance without breaking existing output
- [ ] create-memory-project skill prompts for schema init
- [ ] Opt-out signal (empty schemas/ folder) persists across sessions
- [ ] MISSING_TYPE warns in hook validator without blocking
- [ ] Mandatory Type Declaration rule note is in memory-rules project
- [ ] All unit + integration tests pass
- [ ] Smoke test on throwaway project passes
- [ ] README + CHANGELOG updated

If all boxes ticked, Cycle 1 is complete. Stop here — Cycle 2 plan is a separate document, written AFTER Phase 1 gate is met (i.e., after real use in at least one live project shows schema validation working cleanly).

- [ ] **Step 2: Do NOT merge to master or publish to marketplace yet**

Per user directive: feature branch only. Cycle 2 must complete before any marketplace publish.

---

## Self-Review Checklist

Pre-execution review of this plan:

**1. Spec coverage**:
- Schema activation subsystem (spec §4 rows 1–4, 10, 13): covered by Task Groups A, B, C, D, E, G ✓
- Hook validator MISSING_TYPE (spec §4 row 11, §8 MISSING_TYPE): covered by Task Group F ✓
- Phase 1 gating (spec §10 Phase 1): covered by Task Group H ✓
- Explicitly deferred to Cycle 2: SQLite validators, bidirectional check, schema blocking mode — NOT in this plan, per decomposition decision ✓

**2. Placeholder scan**: No TBD/TODO/FIXME in any task step. Every step has either (a) exact code to write or (b) exact command to run with expected output. ✓

**3. Type consistency**:
- `translate_schema_file(path)` used consistently across Task B2, B3, B4, B5, B6, B7, B8 ✓
- `detect-schema-state.sh <project-path> <seed-dir>` signature consistent between Task D1 test and Task D2 implementation ✓
- `install-schemas-helper.sh <project-name>` signature consistent between Task C1 and Task C2 tests ✓
- `check_missing_type(content)` used consistently between Task F1 (test) and Task F2 (implementation) ✓

**4. Known gaps to flag to implementer**:
- Task E1 Step 1 — skill file path is discovered at runtime via `find`; if the skill has moved or been renamed, the implementer should update the modify target accordingly.
- Task H2 is manual — there is no automated way to test "open a new Claude Code session" from within a plan. The implementer must perform this manually.
- Task G1 is content creation in basic-memory, not a code change; no git commit is expected for this task.

---
