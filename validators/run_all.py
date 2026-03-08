"""
Validator Orchestrator

Runs all validators against a note and reports combined results.
Supports two modes:
  - blocking: Only runs CRITICAL/HIGH checks (for PreToolUse hooks)
  - warning:  Only runs MEDIUM/LOW checks (for PostToolUse hooks)
  - full:     Runs all checks

Usage:
    python -m validators.run_all <project> <note_title> [--mode blocking|warning|full]

Exit codes:
    0 = all checks passed
    1 = one or more checks failed
    2 = usage error
"""

import sys
import json
import argparse
from . import ValidationResult, ValidationIssue, Severity

from .self_reference import check_self_reference
from .cross_project import check_cross_project
from .broken_wikilinks import check_broken_wikilinks
from .relation_quality import check_relation_quality
from .section_format import check_section_format


# Validators grouped by severity level
BLOCKING_VALIDATORS = [
    ("self_reference", check_self_reference),
    ("cross_project", check_cross_project),
]

WARNING_VALIDATORS = [
    ("broken_wikilinks", check_broken_wikilinks),
    ("relation_quality", check_relation_quality),
    ("section_format", check_section_format),
]


def run_validators(
    project: str,
    note_title: str,
    mode: str = "full",
) -> dict:
    """Run validators based on mode and return combined results."""
    validators = []
    if mode in ("blocking", "full"):
        validators.extend(BLOCKING_VALIDATORS)
    if mode in ("warning", "full"):
        validators.extend(WARNING_VALIDATORS)

    all_issues: list[dict] = []
    has_blocking_failure = False

    for name, check_fn in validators:
        result = check_fn(project, note_title)
        for issue in result.issues:
            all_issues.append({
                "severity": issue.severity.value,
                "check": issue.check_name,
                "message": issue.message,
                "fix": issue.fix_suggestion,
            })
            if issue.severity in (Severity.CRITICAL, Severity.HIGH):
                has_blocking_failure = True

    return {
        "passed": not has_blocking_failure,
        "mode": mode,
        "note_title": note_title,
        "project": project,
        "total_issues": len(all_issues),
        "blocking_issues": sum(
            1 for i in all_issues
            if i["severity"] in ("critical", "high")
        ),
        "warning_issues": sum(
            1 for i in all_issues
            if i["severity"] in ("medium", "low")
        ),
        "issues": all_issues,
    }


def format_hook_output(results: dict) -> str:
    """Format results for hook output (human-readable warnings)."""
    if not results["issues"]:
        return ""

    lines = []
    for issue in results["issues"]:
        severity = issue["severity"].upper()
        lines.append(f"[{severity}] {issue['message']}")
        if issue.get("fix"):
            lines.append(f"  Fix: {issue['fix']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run note validators")
    parser.add_argument("project", help="Basic Memory project name")
    parser.add_argument("note_title", nargs="+", help="Note title")
    parser.add_argument(
        "--mode",
        choices=["blocking", "warning", "full"],
        default="full",
        help="Validation mode",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format",
    )

    args = parser.parse_args()
    note_title = " ".join(args.note_title)

    results = run_validators(args.project, note_title, mode=args.mode)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        output = format_hook_output(results)
        if output:
            print(output)
        elif results["passed"]:
            print("All checks passed.")

    sys.exit(0 if results["passed"] else 1)


if __name__ == "__main__":
    main()
