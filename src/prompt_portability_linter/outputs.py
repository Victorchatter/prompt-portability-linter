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


def format_sarif(findings: list[dict], *, tool_name: str = "prompt-portability-linter") -> str:
    results = []
    for finding in findings:
        line = None
        ctx = finding.get("context", "")
        if isinstance(ctx, str) and ctx.lower().startswith("line "):
            try:
                line = int(ctx.split(None, 1)[1])
            except (ValueError, IndexError):
                pass
        result = {
            "ruleId": finding["rule_id"],
            "level": "error" if finding.get("severity") == "blocker" else "warning",
            "message": {"text": f"{finding['message']} Suggestion: {finding['suggestion']}"},
            "locations": [],
        }
        physical = {"artifactLocation": {"uri": finding.get("file", "prompt")}}
        if line:
            physical["region"] = {"startLine": line}
        result["locations"].append({"physicalLocation": physical})
        results.append(result)

    payload = {
        "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": tool_name, "informationUri": "https://github.com/Victorchatter/prompt-portability-linter"}},
                "results": results,
            }
        ],
    }
    return json.dumps(payload, indent=2)
