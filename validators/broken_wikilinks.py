"""
Broken WikiLink Validator

Detects WikiLinks [[Target]] in the Relations section where the target
note does not exist in the current project.

This is a WARNING check — broken links don't block writes but indicate
typos or missing notes.

Usage:
    python -m validators.broken_wikilinks <project> <note_title>
"""

import sys
from . import (
    ValidationResult, ValidationIssue, Severity,
    read_note_json, extract_relations, search_note_exists,
)


def check_broken_wikilinks(project: str, note_title: str) -> ValidationResult:
    """Check if a note has WikiLinks pointing to non-existent notes."""
    result = ValidationResult(passed=True, note_title=note_title, project=project)

    note = read_note_json(project, note_title)
    if not note:
        return result

    relations = extract_relations(note["content"])
    wikilink_relations = [r for r in relations if r["is_wikilink"]]

    broken_count = 0
    for rel in wikilink_relations:
        target = rel["target"]
        # Skip self-reference check (handled by self_reference validator)
        if target.lower().strip() == note_title.lower().strip():
            continue

        if not search_note_exists(project, target):
            broken_count += 1
            result.issues.append(ValidationIssue(
                severity=Severity.MEDIUM,
                check_name="broken_wikilink",
                message=(
                    f"WikiLink [[{target}]] — no matching note found in '{project}'."
                ),
                fix_suggestion=(
                    f"Search for the correct title, or create the target note, "
                    f"or convert to cross-project text format if it exists elsewhere."
                ),
            ))

    if broken_count > 0:
        result.passed = False

    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m validators.broken_wikilinks <project> <note_title>")
        sys.exit(2)

    project = sys.argv[1]
    note_title = " ".join(sys.argv[2:])
    result = check_broken_wikilinks(project, note_title)
    print(result.to_json())
    sys.exit(0 if result.passed else 1)
