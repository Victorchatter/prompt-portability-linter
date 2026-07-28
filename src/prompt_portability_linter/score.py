"""Portability score and fix-hint report generation.

# ponytail: scoring is rule-based and deterministic. Weights are documented in
README so users can predict the score and argue about the formula.
"""
from __future__ import annotations

from collections import defaultdict


# Weight table: points deducted per finding.
BLOCKER_WEIGHTS = {
    "anthropic": 10,
    "openai": 10,
    "gemini": 8,
    "codex": 8,
}
WARNING_WEIGHT = 3


def compute_score(findings: list[dict]) -> tuple[int, dict]:
    """Return (score, breakdown) for a list of findings.

    Score starts at 100 and subtracts weighted points per blocker/warning.
    Breakdown maps provider -> {"blockers": int, "warnings": int, "deduction": int}.
    """
    breakdown: dict = defaultdict(lambda: {"blockers": 0, "warnings": 0, "deduction": 0})
    total_deduction = 0
    for finding in findings:
        provider = finding.get("locked_to", "unknown")
        severity = finding.get("severity", "blocker")
        if severity == "warning":
            weight = WARNING_WEIGHT
            key = "warnings"
        else:
            weight = BLOCKER_WEIGHTS.get(provider, 8)
            key = "blockers"
        breakdown[provider][key] += 1
        breakdown[provider]["deduction"] += weight
        total_deduction += weight

    score = max(0, 100 - total_deduction)
    return score, dict(breakdown)


def format_score_text(score: int, breakdown: dict) -> str:
    lines = [f"Portability score: {score}/100"]
    if breakdown:
        lines.append("")
        lines.append("Breakdown by provider:")
        for provider in sorted(breakdown):
            info = breakdown[provider]
            lines.append(
                f"  {provider}: {info['blockers']} blocker(s), {info['warnings']} warning(s), "
                f"-{info['deduction']} points"
            )
    return "\n".join(lines)


def format_suggestions(findings: list[dict]) -> str:
    """Return a Markdown patch report: original line + portable rewrite per finding."""
    if not findings:
        return "No portability blockers found.\n"

    lines = ["# Portability Fix Hints", ""]
    for finding in findings:
        lines.append(f"## {finding['rule_id']} ({finding['locked_to']})")
        lines.append(f"- **Location:** {finding['file']}:{finding['context']}")
        lines.append(f"- **Matched:** `{finding.get('matched', '')}`")
        lines.append(f"- **Issue:** {finding['message']}")
        lines.append(f"- **Portable rewrite:** {finding['suggestion']}")
        lines.append("")
    return "\n".join(lines)
