"""Minimal YAML loader for the controlled rules.yaml subset.

# ponytail: stdlib-only replacement for PyYAML; only handles mappings, lists,
# comments, and scalar values (no flow style, anchors, aliases, or multiline).
"""

from __future__ import annotations


def _to_scalar(value: str):
    """Convert a trimmed YAML scalar to a Python value."""
    value = value.strip()
    if value == "":
        return None
    lower = value.lower()
    if lower in ("true", "yes", "on"):
        return True
    if lower in ("false", "no", "off"):
        return False
    if lower in ("null", "~"):
        return None
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _tokenize(text: str):
    """Strip comments and blank lines, then return (indent, stripped_line)."""
    tokens = []
    for raw in text.splitlines():
        # # ponytail: our rules.yaml never puts # inside quoted values, so
        # stripping the first # is safe for this controlled subset.
        if "#" in raw:
            raw = raw[: raw.index("#")]
        line = raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        tokens.append((indent, line.strip()))
    return tokens


def load_yaml(text: str):
    """Parse a tiny YAML subset into dicts/lists/scalars."""
    tokens = _tokenize(text)

    def parse_block(start: int, indent: int):
        if start >= len(tokens):
            return start, None
        if tokens[start][1].startswith("- "):
            return parse_list(start, indent)
        return parse_mapping(start, indent)

    def parse_list(start: int, indent: int):
        items = []
        i = start
        while i < len(tokens):
            ind, line = tokens[i]
            if ind < indent:
                break
            if ind > indent or not line.startswith("- "):
                break
            content = line[2:].strip()
            if content == "":
                if i + 1 < len(tokens) and tokens[i + 1][0] > indent:
                    child_indent = tokens[i + 1][0]
                    i, child = parse_block(i + 1, child_indent)
                    items.append(child)
                else:
                    items.append(None)
                    i += 1
            elif ":" in content:
                i, mapping = _parse_inline_mapping(i, indent, content)
                items.append(mapping)
            else:
                items.append(_to_scalar(content))
                i += 1
        return i, items

    def _parse_inline_mapping(start: int, parent_indent: int, first_line: str):
        """Parse a mapping that appears as the first line of a list item."""
        mapping = {}
        i = start
        line = first_line
        while True:
            if ":" not in line:
                break
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest:
                mapping[key] = _to_scalar(rest)
                i += 1
            else:
                if i + 1 < len(tokens) and tokens[i + 1][0] > parent_indent:
                    child_indent = tokens[i + 1][0]
                    i, child = parse_block(i + 1, child_indent)
                    mapping[key] = child
                else:
                    mapping[key] = None
                    i += 1
            if i >= len(tokens) or tokens[i][0] <= parent_indent:
                break
            line = tokens[i][1]
        return i, mapping

    def parse_mapping(start: int, indent: int):
        mapping = {}
        i = start
        while i < len(tokens):
            ind, line = tokens[i]
            if ind < indent:
                break
            if ind > indent or ":" not in line:
                i += 1
                continue
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest:
                mapping[key] = _to_scalar(rest)
                i += 1
            else:
                if i + 1 < len(tokens) and tokens[i + 1][0] > indent:
                    child_indent = tokens[i + 1][0]
                    i, child = parse_block(i + 1, child_indent)
                    mapping[key] = child
                else:
                    mapping[key] = None
                    i += 1
        return i, mapping

    if not tokens:
        return {}
    base_indent = tokens[0][0]
    if tokens[0][1].startswith("- "):
        _, result = parse_list(0, base_indent)
    else:
        _, result = parse_mapping(0, base_indent)
    return result
