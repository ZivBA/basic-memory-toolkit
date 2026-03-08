"""
Basic Memory Toolkit — Note Validators

Python modules for validating Basic Memory notes.
Each module works standalone via CLI and is importable for future server use.

Usage (CLI):
    python -m validators.self_reference <project> <note_title>
    python -m validators.run_all <project> <note_title> --mode blocking

Usage (Python):
    from validators.self_reference import check_self_reference
    result = check_self_reference(project="my-project", note_title="My Note")

Design:
    - Uses `basic-memory tool read-note --format json` for note data
    - Uses `basic-memory tool search-notes` for existence checks
    - Returns structured results (ValidationResult dataclass)
    - Exit code 0 = pass, 1 = fail (for hook integration)
    - Designed for future FastAPI wrapping with zero rewrite
"""

import json
import subprocess
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    CRITICAL = "critical"  # Blocks write
    HIGH = "high"          # Blocks write
    MEDIUM = "medium"      # Warning only
    LOW = "low"            # Suggestion only


@dataclass
class ValidationIssue:
    severity: Severity
    check_name: str
    message: str
    fix_suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    passed: bool
    note_title: str
    project: str
    issues: list[ValidationIssue] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps({
            "passed": self.passed,
            "note_title": self.note_title,
            "project": self.project,
            "issues": [
                {
                    "severity": i.severity.value,
                    "check": i.check_name,
                    "message": i.message,
                    "fix": i.fix_suggestion,
                }
                for i in self.issues
            ],
        }, indent=2)


def read_note_json(project: str, identifier: str) -> Optional[dict]:
    """Read a note using basic-memory CLI and return parsed JSON."""
    try:
        result = subprocess.run(
            ["basic-memory", "tool", "read-note", identifier, "--project", project],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return None
        # CLI returns JSON with {title, content, frontmatter, ...}
        parsed = json.loads(result.stdout)
        return {
            "content": parsed.get("content", ""),
            "title": parsed.get("title", identifier),
        }
    except (json.JSONDecodeError, subprocess.TimeoutExpired, FileNotFoundError):
        return None


def search_note_exists(project: str, query: str) -> bool:
    """Check if a note exists in a project using basic-memory CLI search."""
    try:
        result = subprocess.run(
            ["basic-memory", "tool", "search-notes", query, "--project", project, "--title"],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0 and query.lower() in result.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def extract_relations(content: str) -> list[dict]:
    """Extract relations from note content.

    Parses lines like:
        - relation_type [[Target Title]]
        - relation_type "Cross Project Title" (project-name)
    """
    relations = []
    in_relations = False

    for line in content.split("\n"):
        if line.strip().startswith("## Relations"):
            in_relations = True
            continue
        if in_relations and line.strip().startswith("## "):
            break
        if not in_relations:
            continue

        # WikiLink relation: - type [[Target]]
        wikilink_match = re.match(r'^-\s+(\w+)\s+\[\[(.+?)\]\]', line.strip())
        if wikilink_match:
            relations.append({
                "type": wikilink_match.group(1),
                "target": wikilink_match.group(2),
                "is_wikilink": True,
                "raw": line.strip(),
            })
            continue

        # Text cross-project relation: - type "Title" (project)
        text_match = re.match(r'^-\s+(\w+)\s+"(.+?)"\s+\((.+?)\)', line.strip())
        if text_match:
            relations.append({
                "type": text_match.group(1),
                "target": text_match.group(2),
                "project": text_match.group(3),
                "is_wikilink": False,
                "raw": line.strip(),
            })

    return relations


def extract_wikilinks_from_body(content: str) -> list[str]:
    """Extract all WikiLinks [[Target]] from entire note content."""
    return re.findall(r'\[\[(.+?)\]\]', content)
