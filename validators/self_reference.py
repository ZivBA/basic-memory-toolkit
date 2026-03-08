"""
Self-Reference Validator

Detects relations where the target entity matches the current note's title.
This is a BLOCKING check — self-referential relations cause infinite loops
in graph traversal.

Usage:
    python -m validators.self_reference <project> <note_title>
"""

import sys
from . import (
    ValidationResult, ValidationIssue, Severity,
    read_note_json, extract_relations,
)


def check_self_reference(project: str, note_title: str) -> ValidationResult:
    """Check if a note has any self-referential relations."""
    result = ValidationResult(passed=True, note_title=note_title, project=project)

    note = read_note_json(project, note_title)
    if not note:
        result.issues.append(ValidationIssue(
            severity=Severity.MEDIUM,
            check_name="self_reference",
            message=f"Could not read note '{note_title}' in project '{project}'",
        ))
        return result

    relations = extract_relations(note["content"])
    title_lower = note_title.lower().strip()

    for rel in relations:
        if rel["is_wikilink"] and rel["target"].lower().strip() == title_lower:
            result.passed = False
            result.issues.append(ValidationIssue(
                severity=Severity.CRITICAL,
                check_name="self_reference",
                message=f"Self-referential relation: '{rel['type']} [[{rel['target']}]]'",
                fix_suggestion=f"Remove this relation or redirect to a different note.",
            ))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m validators.self_reference <project> <note_title>")
        sys.exit(2)

    project = sys.argv[1]
    note_title = " ".join(sys.argv[2:])
    result = check_self_reference(project, note_title)
    print(result.to_json())
    sys.exit(0 if result.passed else 1)
