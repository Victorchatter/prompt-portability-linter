"""Command-line interface for prompt-portability-linter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, catalog, extract, linter, outputs, score


def _exit_error(msg: str) -> int:
    print(f"error: {msg}", file=sys.stderr)
    return 2


def _lint_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-portability-linter",
        description="Local linter for vendor-locked prompt and tool features.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--prompt",
        action="append",
        required=True,
        help="Prompt file to lint. Repeatable.",
    )
    parser.add_argument(
        "--tools",
        action="append",
        help="Tool definitions file (JSON/YAML). Repeatable.",
    )
    parser.add_argument(
        "--config",
        action="append",
        help="Agent config file (JSON/YAML). Repeatable.",
    )
    parser.add_argument(
        "--rules",
        help="Path to a custom rules.yaml catalog.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--warn-only",
        action="store_true",
        help="Report blockers but exit 0.",
    )
    parser.add_argument(
        "--score",
        action="store_true",
        help="Print a 0-100 portability score and provider breakdown.",
    )
    parser.add_argument(
        "--suggest-fixes",
        action="store_true",
        help="Emit a Markdown patch report with concrete portable rewrites.",
    )
    parser.add_argument(
        "--output",
        help="Write --suggest-fixes output to a file instead of stdout.",
    )
    return parser


def _rules_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-portability-linter rules",
        description="List the known portability rules.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "sarif"],
        default="text",
        help="Output format (default: text).",
    )
    return parser


def _collect_inputs(args) -> list[tuple[Path, str]]:
    inputs = []
    for p in args.prompt:
        inputs.append((Path(p), "prompt"))
    for t in (getattr(args, "tools", None) or []):
        inputs.append((Path(t), "tools"))
    for c in (getattr(args, "config", None) or []):
        inputs.append((Path(c), "config"))
    return inputs


def _lint_command(args) -> int:
    try:
        rules = catalog.load_catalog(Path(args.rules) if args.rules else None)
    except Exception as exc:
        return _exit_error(f"Cannot load rule catalog: {exc}")

    inputs = _collect_inputs(args)
    for path, _kind in inputs:
        if not path.exists():
            return _exit_error(f"File not found: {path}")

    tokens = []
    for path, kind in inputs:
        try:
            tokens.extend(extract.extract_tokens(path, kind))
        except Exception as exc:
            return _exit_error(f"Cannot read {path}: {exc}")

    findings = linter.lint(tokens, rules)

    # Score and fix hints are orthogonal to the primary format, but they
    # control additional stdout output. The main format still prints first.
    if args.format == "json":
        print(outputs.format_json(findings))
    elif args.format == "sarif":
        print(outputs.format_sarif(findings))
    else:
        print(outputs.format_text(findings))

    if args.score:
        s, breakdown = score.compute_score(findings)
        print("")
        print(score.format_score_text(s, breakdown))

    if args.suggest_fixes:
        report = score.format_suggestions(findings)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Wrote fix hints to {args.output}")
        else:
            print("")
            print(report)

    if findings and not args.warn_only:
        return 1
    return 0


def _rules_command(args) -> int:
    try:
        rules = catalog.load_catalog()
    except Exception as exc:
        return _exit_error(f"Cannot load rule catalog: {exc}")

    if args.format == "json":
        payload = {
            "rules": [
                {
                    "id": r["id"],
                    "pattern": r["raw_pattern"],
                    "locked_to": r["locked_to"],
                    "message": r["message"],
                    "suggestion": r["suggestion"],
                    "severity": r["severity"],
                }
                for r in rules
            ]
        }
        print(json.dumps(payload, indent=2))
    else:
        for r in rules:
            print(f"{r['id']:<35} {r['locked_to']:<12} {r['message']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if argv and argv[0] == "rules":
        args = _rules_parser().parse_args(argv[1:])
        return _rules_command(args)

    args = _lint_parser().parse_args(argv)
    return _lint_command(args)
