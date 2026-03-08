---
description: Run validation checks across all notes in a Basic Memory project
argument-hint: [project]
allowed-tools: Read, Grep, Glob, Bash(python3:*)
---

Run the full validation suite across all notes in a Basic Memory project.

## Project Selection

1. If $ARGUMENTS names a project, use it
2. Otherwise, run list_memory_projects() and ask which project to validate

## Validation Execution

Run the CLI validators against the project. The validators are located at `${CLAUDE_PLUGIN_ROOT}/validators/`.

### Step 1: Get Note List

List all notes in the project:
!`python3 -c "
import subprocess, json, sys
result = subprocess.run(['basic-memory', 'tool', 'search-notes', '*', '--project', '$1'], capture_output=True, text=True, timeout=30)
if result.returncode == 0:
    print(result.stdout)
else:
    print('ERROR: ' + result.stderr, file=sys.stderr)
    sys.exit(1)
"`

### Step 2: Run Validators

For each note found, run the full validation suite:
!`python3 ${CLAUDE_PLUGIN_ROOT}/validators/run_all.py $1 "<note-title>" --mode full --format json`

Collect results across all notes.

### Step 3: Aggregate Results

Note: The CLI validators (~7s per note) are thorough but slow. For large projects, consider validating a subset or running in the background.

## Report Format

Present a project-wide validation report:

**Project**: [name]
**Notes Scanned**: [count]
**Issues Found**: [count]

### Critical Issues (must fix)
- Self-referential relations: [list notes]
- Cross-project WikiLinks: [list notes]

### Warnings (should fix)
- Broken WikiLinks: [list notes with targets]
- Missing Relations section: [list notes]
- Insufficient relations (<2): [list notes]
- Generic relates_to overuse: [list notes]
- Informal sections: [list notes with section names]

### Summary by Category
| Check | Pass | Fail | Notes |
|-------|------|------|-------|
| Self-reference | X | Y | |
| Cross-project | X | Y | |
| Broken WikiLinks | X | Y | |
| Relation count | X | Y | |
| Relation quality | X | Y | |
| Section format | X | Y | |

## Follow-Up

Ask: "Would you like me to:
1. Fix critical issues automatically?
2. Address specific warnings?
3. Run the memory-organizer agent for bulk fixes?"
