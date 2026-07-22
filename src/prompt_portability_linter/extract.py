"""Extract searchable tokens from prompt, tools, and config files."""

from __future__ import annotations

import json
from pathlib import Path

from . import yaml_min


def _bool_str(value):
    return str(value).lower() if isinstance(value, bool) else str(value)


def _walk_struct(obj, path: str, tokens: list):
    """Recursively walk a JSON/YAML structure and emit key/value/pair tokens."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            tokens.append({"context": path, "text": key})
            child_path = f"{path}.{key}" if path else key
            if isinstance(value, (str, bool, int, float)):
                text_value = _bool_str(value)
                tokens.append({"context": child_path, "text": text_value})
                tokens.append({"context": child_path, "text": f"{key}: {text_value}"})
            _walk_struct(value, child_path, tokens)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child_path = f"{path}[{i}]"
            _walk_struct(item, child_path, tokens)


def _extract_text(file_path: Path, text: str) -> list[dict]:
    tokens = []
    for n, line in enumerate(text.splitlines(), start=1):
        tokens.append({"file": str(file_path), "context": f"line {n}", "text": line})
    return tokens


def _extract_json(file_path: Path, text: str) -> list[dict]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Cannot parse {file_path} as JSON: {exc}") from exc
    raw_tokens = []
    _walk_struct(data, "", raw_tokens)
    return [
        {"file": str(file_path), "context": t["context"], "text": t["text"]}
        for t in raw_tokens
    ]


def _extract_yaml(file_path: Path, text: str) -> list[dict]:
    try:
        data = yaml_min.load_yaml(text)
    except Exception as exc:
        raise ValueError(f"Cannot parse {file_path} as YAML: {exc}") from exc
    raw_tokens = []
    _walk_struct(data, "", raw_tokens)
    return [
        {"file": str(file_path), "context": t["context"], "text": t["text"]}
        for t in raw_tokens
    ]


def extract_tokens(file_path: Path, source_kind: str) -> list[dict]:
    """Return searchable tokens for a file.

    # ponytail: line-based regex for prompts; structural key/value/pair
    # extraction for JSON/YAML tool and config files.
    """
    text = file_path.read_text(encoding="utf-8")
    suffix = file_path.suffix.lower()
    if suffix in (".json",):
        return _extract_json(file_path, text)
    if suffix in (".yaml", ".yml"):
        return _extract_yaml(file_path, text)
    return _extract_text(file_path, text)
