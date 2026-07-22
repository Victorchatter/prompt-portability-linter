"""Load and validate the rule catalog."""

from __future__ import annotations

import importlib.resources
import re
from pathlib import Path

from . import yaml_min

REQUIRED_FIELDS = {"id", "pattern", "locked_to", "message", "suggestion"}


def _load_yaml_path(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml_min.load_yaml(f.read())


def load_catalog(extra_rules_path: Path | None = None) -> list[dict]:
    """Load the embedded default catalog plus an optional user catalog."""
    data_pkg = importlib.resources.files("prompt_portability_linter") / "data"
    default_text = (data_pkg / "rules.yaml").read_text(encoding="utf-8")
    data = yaml_min.load_yaml(default_text)
    rules = data.get("rules", [])

    if extra_rules_path:
        extra = _load_yaml_path(extra_rules_path)
        rules.extend(extra.get("rules", []))

    compiled = []
    seen_ids = set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError(f"Rule catalog item is not a mapping: {rule!r}")
        missing = REQUIRED_FIELDS - set(rule.keys())
        if missing:
            rid = rule.get("id", "?")
            raise ValueError(f"Rule {rid!r} missing fields: {sorted(missing)}")
        rid = rule["id"]
        if rid in seen_ids:
            raise ValueError(f"Duplicate rule id in catalog: {rid!r}")
        seen_ids.add(rid)
        compiled.append(
            {
                "id": rid,
                "pattern": re.compile(rule["pattern"]),
                "raw_pattern": rule["pattern"],
                "locked_to": rule["locked_to"],
                "message": rule["message"],
                "suggestion": rule["suggestion"],
                "severity": rule.get("severity", "blocker"),
            }
        )
    return compiled
