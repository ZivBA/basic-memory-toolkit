"""
Cross-Project WikiLink Validator

Detects WikiLinks [[Target]] that point to notes in a different project.
WikiLinks don't work across project boundaries — use text format instead:
  "Note Title" (project-name)

This is a BLOCKING check.

Usage:
    python -m validators.cross_project <project> <note_title>
"""

import sys
from . import (
    ValidationResult, ValidationIssue, Severity,
    read_note_json, extract_relations, search_note_exists,
)


def check_cross_project(project: str, note_title: str) -> ValidationResult:
    """Check if a note has WikiLinks pointing to notes in other projects."""
    result = ValidationResult(passed=True, note_title=note_title, project=project)

    note = read_note_json(project, note_title)
    if not note:
        return result

    relations = extract_relations(note["content"])
    wikilink_relations = [r for r in relations if r["is_wikilink"]]

    for rel in wikilink_relations:
        target = rel["target"]
        # Check if target exists in current project
        if not search_note_exists(project, target):
            # Could be a forward reference OR a cross-project WikiLink
            # We flag it as a potential cross-project issue
            # The user/LLM can determine if it's intentional forward ref
            result.issues.append(ValidationIssue(
                severity=Severity.HIGH,
                check_name="cross_project_wikilink",
                message=(
                    f"WikiLink [[{target}]] not found in project '{project}'. "
                    f"If this note exists in another project, use text format instead."
                ),
                fix_suggestion=(
                    f'Convert to: {rel["type"]} "{target}" (other-project-name)'
                ),
            ))

    # Also check for cross-project WikiLinks in the body (outside Relations)
    # These are [[Target]] references embedded in prose
    import re
    body_wikilinks = re.findall(r'\[\[(.+?)\]\]', note["content"])
    relation_targets = {r["target"] for r in wikilink_relations}

    for target in body_wikilinks:
        if target in relation_targets:
            continue  # Already checked in relations
        if not search_note_exists(project, target):
            result.issues.append(ValidationIssue(
                severity=Severity.MEDIUM,
                check_name="cross_project_body_wikilink",
                message=(
                    f"Body WikiLink [[{target}]] not found in project '{project}'."
                ),
                fix_suggestion=(
                    f'If cross-project, convert to: "{target}" (other-project-name)'
                ),
            ))

    if any(i.severity in (Severity.CRITICAL, Severity.HIGH) for i in result.issues):
        result.passed = False

    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m validators.cross_project <project> <note_title>")
        sys.exit(2)

    project = sys.argv[1]
    note_title = " ".join(sys.argv[2:])
    result = check_cross_project(project, note_title)
    print(result.to_json())
    sys.exit(0 if result.passed else 1)
