"""
Relation Quality Validator

Checks for:
- Missing Relations section (0 relations)
- Too few relations (< minimum threshold)
- Overuse of generic 'relates_to' type
- Index notes using 'relates_to' instead of 'documents'/'encompasses'

Usage:
    python -m validators.relation_quality <project> <note_title> [--min-relations 2]
"""

import sys
from . import (
    ValidationResult, ValidationIssue, Severity,
    read_note_json, extract_relations,
)

WEAK_RELATION_TYPE = "relates_to"
INDEX_PREFERRED_TYPES = {"documents", "encompasses", "covers", "contains"}


def check_relation_quality(
    project: str,
    note_title: str,
    min_relations: int = 2,
    max_relates_to: int = 1,
) -> ValidationResult:
    """Check relation count, types, and quality."""
    result = ValidationResult(passed=True, note_title=note_title, project=project)

    note = read_note_json(project, note_title)
    if not note:
        return result

    content = note["content"]
    relations = extract_relations(content)
    is_index = "index" in note_title.lower()

    # Check: no Relations section at all
    if "## Relations" not in content:
        result.issues.append(ValidationIssue(
            severity=Severity.MEDIUM,
            check_name="missing_relations_section",
            message="Note has no '## Relations' section.",
            fix_suggestion=f"Add a Relations section with at least {min_relations} relations.",
        ))
        return result

    # Check: too few relations
    if len(relations) < min_relations:
        result.issues.append(ValidationIssue(
            severity=Severity.MEDIUM,
            check_name="insufficient_relations",
            message=f"Note has {len(relations)} relations (minimum: {min_relations}).",
            fix_suggestion="Add more relations to connect this note to the knowledge graph.",
        ))

    # Check: relates_to overuse
    relates_to_count = sum(1 for r in relations if r["type"] == WEAK_RELATION_TYPE)
    if relates_to_count > max_relates_to:
        result.issues.append(ValidationIssue(
            severity=Severity.LOW,
            check_name="relates_to_overuse",
            message=f"Note has {relates_to_count} generic 'relates_to' relations (max recommended: {max_relates_to}).",
            fix_suggestion="Use specific types: implements, requires, part_of, extends, documents.",
        ))

    # Check: index notes should use documents/encompasses
    if is_index:
        weak_index_rels = [r for r in relations if r["type"] == WEAK_RELATION_TYPE]
        if weak_index_rels:
            result.issues.append(ValidationIssue(
                severity=Severity.MEDIUM,
                check_name="index_weak_relations",
                message=f"Index note uses '{WEAK_RELATION_TYPE}' for {len(weak_index_rels)} relations.",
                fix_suggestion=f"Index notes should use: {', '.join(INDEX_PREFERRED_TYPES)}.",
            ))

    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m validators.relation_quality <project> <note_title> [--min-relations N]")
        sys.exit(2)

    project = sys.argv[1]
    min_rels = 2
    args = sys.argv[2:]
    if "--min-relations" in args:
        idx = args.index("--min-relations")
        min_rels = int(args[idx + 1])
        args = args[:idx] + args[idx + 2:]

    note_title = " ".join(args)
    result = check_relation_quality(project, note_title, min_relations=min_rels)
    print(result.to_json())
    sys.exit(0 if result.passed else 1)
