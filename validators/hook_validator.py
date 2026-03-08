"""
Hook Validator — Inline content validation for PreToolUse/PostToolUse hooks.

Parses tool_input from hook stdin JSON. No CLI calls, no subprocess overhead.
All checks work on the content string directly.

Usage (called by hooks/scripts/validate-note):
    echo '<hook_json>' | python3 hook_validator.py <mode>

Modes:
    blocking — CRITICAL checks only (PreToolUse: deny bad writes)
    warning  — MEDIUM/LOW checks only (PostToolUse: inform user)
    full     — All checks

Exit codes:
    0 = pass
    2 = blocking issue found (stderr = deny JSON for PreToolUse)
"""

import json
import re
import sys


def extract_relations(content: str) -> list[dict]:
    """Extract relations from note content."""
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
        wl = re.match(r"^-\s+(\w+)\s+\[\[(.+?)\]\]", line.strip())
        if wl:
            relations.append({
                "type": wl.group(1),
                "target": wl.group(2),
                "is_wikilink": True,
            })
        tr = re.match(r'^-\s+(\w+)\s+"(.+?)"\s+\((.+?)\)', line.strip())
        if tr:
            relations.append({
                "type": tr.group(1),
                "target": tr.group(2),
                "project": tr.group(3),
                "is_wikilink": False,
            })
    return relations


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "blocking"

    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    title = tool_input.get("title", "") or tool_input.get("identifier", "")
    content = tool_input.get("content", "")

    if not title or not content:
        sys.exit(0)

    issues = []
    relations = extract_relations(content)

    # ── BLOCKING CHECKS (PreToolUse) ──────────────────────────────────

    if mode in ("blocking", "full"):
        # Self-referential relations
        for rel in relations:
            if rel["is_wikilink"] and rel["target"].lower().strip() == title.lower().strip():
                issues.append({
                    "severity": "CRITICAL",
                    "message": (
                        f"Self-referential relation: "
                        f"'{rel['type']} [[{rel['target']}]]' points to itself"
                    ),
                    "fix": "Remove or redirect to a different note",
                })

    # ── WARNING CHECKS (PostToolUse) ──────────────────────────────────

    if mode in ("warning", "full"):
        # Missing Relations section
        if "## Relations" not in content:
            issues.append({
                "severity": "MEDIUM",
                "message": "Note has no '## Relations' section",
                "fix": "Add Relations with at least 2 relations",
            })
        elif len(relations) < 2:
            issues.append({
                "severity": "MEDIUM",
                "message": f"Note has {len(relations)} relation(s) (minimum: 2)",
                "fix": "Add more relations to connect this note",
            })

        # relates_to overuse
        relates_to_count = sum(1 for r in relations if r.get("type") == "relates_to")
        if relates_to_count > 1:
            issues.append({
                "severity": "LOW",
                "message": f"{relates_to_count} generic 'relates_to' (max: 1)",
                "fix": "Use: implements, requires, part_of, extends, documents",
            })

        # Index note with weak relation types
        if "index" in title.lower():
            weak = [r for r in relations if r.get("type") == "relates_to"]
            if weak:
                issues.append({
                    "severity": "MEDIUM",
                    "message": f"Index note uses 'relates_to' for {len(weak)} relation(s)",
                    "fix": "Use 'documents' or 'encompasses' for index relations",
                })

        # Informal relation sections
        for pattern in [
            r"##\s+Related\s+Components",
            r"##\s+Related\s+Notes",
            r"##\s+Related\s+Work",
            r"##\s+See\s+Also",
            r"##\s+Related\s+Documentation",
            r"##\s+References\b",
        ]:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                issues.append({
                    "severity": "MEDIUM",
                    "message": f"'{match.group(0).strip()}' is invisible to knowledge graph",
                    "fix": "Convert to WikiLink relations under '## Relations'",
                })

    # ── OUTPUT ────────────────────────────────────────────────────────

    blocking = [i for i in issues if i["severity"] == "CRITICAL"]
    warnings = [i for i in issues if i["severity"] != "CRITICAL"]

    if blocking:
        deny = {
            "hookSpecificOutput": {"permissionDecision": "deny"},
            "systemMessage": "BLOCKED: " + "; ".join(i["message"] for i in blocking),
        }
        print(json.dumps(deny), file=sys.stderr)
        sys.exit(2)

    if warnings and mode in ("warning", "full"):
        lines = []
        for i in warnings:
            lines.append(f"[{i['severity']}] {i['message']}")
            if i.get("fix"):
                lines.append(f"  Fix: {i['fix']}")
        print("\n".join(lines))

    sys.exit(0)


if __name__ == "__main__":
    main()
