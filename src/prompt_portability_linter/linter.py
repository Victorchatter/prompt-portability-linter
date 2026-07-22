"""Apply the rule catalog to extracted tokens and collect findings."""

from __future__ import annotations

from typing import Iterable


def lint(tokens: Iterable[dict], rules: Iterable[dict]) -> list[dict]:
    """Return rule matches across tokens, deduplicated by (file, context, rule)."""
    seen = set()
    findings = []
    for token in tokens:
        text = token["text"]
        for rule in rules:
            if rule["pattern"].search(text):
                key = (token["file"], token["context"], rule["id"])
                if key in seen:
                    continue
                seen.add(key)
                findings.append(
                    {
                        "file": token["file"],
                        "context": token["context"],
                        "rule_id": rule["id"],
                        "locked_to": rule["locked_to"],
                        "message": rule["message"],
                        "suggestion": rule["suggestion"],
                        "severity": rule["severity"],
                        "matched": text[:120],
                    }
                )
    return findings
