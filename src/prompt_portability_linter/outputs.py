"""Text and JSON formatters for linter findings."""

from __future__ import annotations

import json
from collections import defaultdict


def format_text(findings: list[dict]) -> str:
    if not findings:
        return "No portability blockers found."
    by_provider = defaultdict(list)
    for finding in findings:
        by_provider[finding["locked_to"]].append(finding)

    lines = []
    for provider in sorted(by_provider):
        lines.append(provider)
        for finding in sorted(
            by_provider[provider], key=lambda f: (f["file"], f["context"])
        ):
            lines.append(f"  {finding['file']}:{finding['context']}  {finding['rule_id']}")
            lines.append(f"    {finding['message']}")
            lines.append(f"    Suggestion: {finding['suggestion']}")
        lines.append("")

    count = len(findings)
    lines.append(
        f"{count} portability blocker{'s' if count != 1 else ''} found."
    )
    return "\n".join(lines)


def format_json(findings: list[dict]) -> str:
    payload = {
        "blockers": len(findings),
        "findings": [
            {
                "file": finding["file"],
                "context": finding["context"],
                "rule_id": finding["rule_id"],
                "locked_to": finding["locked_to"],
                "message": finding["message"],
                "suggestion": finding["suggestion"],
                "severity": finding["severity"],
            }
            for finding in findings
        ],
    }
    return json.dumps(payload, indent=2)
