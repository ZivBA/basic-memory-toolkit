"""
Section Format Validator

Detects informal relation sections that are NOT in the standard
'## Relations' format, making them invisible to the knowledge graph.

Common informal patterns:
  - "## Related Components"
  - "## Related Notes"
  - "## Related Work"
  - "## See Also"
  - "## Related Documentation"
  - "## References"

This is a WARNING check.

Usage:
    python -m validators.section_format <project> <note_title>
"""

import re
import sys
from . import (
    ValidationResult, ValidationIssue, Severity,
    read_note_json,
)

INFORMAL_SECTION_PATTERNS = [
    r"##\s+Related\s+Components",
    r"##\s+Related\s+Notes",
    r"##\s+Related\s+Work",
    r"##\s+See\s+Also",
    r"##\s+Related\s+Documentation",
    r"##\s+References\b",
    r"##\s+Related\s+Issues",
    r"##\s+Related\s+Projects",
]


def check_section_format(project: str, note_title: str) -> ValidationResult:
    """Check for informal relation sections outside ## Relations."""
    result = ValidationResult(passed=True, note_title=note_title, project=project)

    note = read_note_json(project, note_title)
    if not note:
        return result

    content = note["content"]
    has_formal_relations = "## Relations" in content

    for pattern in INFORMAL_SECTION_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            section_name = match.group(0).strip()
            severity = Severity.MEDIUM if not has_formal_relations else Severity.LOW

            result.issues.append(ValidationIssue(
                severity=severity,
                check_name="informal_relation_section",
                message=(
                    f"Informal section '{section_name}' found. "
                    f"References here are invisible to the knowledge graph."
                ),
                fix_suggestion=(
                    f"Convert references in '{section_name}' to proper WikiLink "
                    f"relations under a '## Relations' section."
                ),
            ))

    if any(i.severity == Severity.MEDIUM for i in result.issues):
        result.passed = False

    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m validators.section_format <project> <note_title>")
        sys.exit(2)

    project = sys.argv[1]
    note_title = " ".join(sys.argv[2:])
    result = check_section_format(project, note_title)
    print(result.to_json())
    sys.exit(0 if result.passed else 1)
