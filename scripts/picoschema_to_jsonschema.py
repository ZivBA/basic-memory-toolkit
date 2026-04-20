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
