"""End-to-end self-test for prompt-portability-linter.

Creates a mixed prompt with one Anthropic lock, one OpenAI lock, and one
portable construct, then asserts the linter flags exactly the two locks,
includes suggestions, exits nonzero by default, and exits zero with
--warn-only.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile


def _validate_sarif(payload: dict) -> None:
    """Minimal structural validation of the SARIF payload we produce."""
    assert payload.get("version") == "2.1.0", payload.get("version")
    runs = payload.get("runs", [])
    assert runs, "missing runs"
    run = runs[0]
    assert run.get("tool", {}).get("driver", {}).get("name"), "missing tool.driver.name"
    for result in run.get("results", []):
        assert result.get("ruleId"), "missing ruleId"
        assert result.get("message", {}).get("text"), "missing message.text"
        locs = result.get("locations", [])
        assert locs and locs[0].get("physicalLocation"), "missing physicalLocation"


PROMPT = """\
You are a helpful assistant.

Use cache_control breakpoints for long prompts.

Use response_format to request JSON output.
"""


def _run(args, cwd, env):
    return subprocess.run(
        [sys.executable, "-m", "prompt_portability_linter", *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
    )


def _assert(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")
    env = os.environ.copy()
    env["PYTHONPATH"] = src_path

    prompt_path = tempfile.mktemp(suffix="_selfcheck_prompt.md")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(PROMPT)

    try:
        # Default lint run: two blockers, nonzero exit.
        result = _run(["--prompt", prompt_path], project_root, env)
        print(result.stdout)
        _assert(result.returncode == 1, f"expected exit 1, got {result.returncode}")
        _assert("cache_control" in result.stdout, "expected cache_control finding")
        _assert("response_format" in result.stdout, "expected response_format finding")
        suggestion_count = result.stdout.count("Suggestion:")
        _assert(suggestion_count >= 2, f"expected at least 2 suggestions, got {suggestion_count}")

        # --warn-only must still report but exit 0.
        result_warn = _run(["--prompt", prompt_path, "--warn-only"], project_root, env)
        _assert(result_warn.returncode == 0, "expected exit 0 with --warn-only")
        _assert("blocker" in result_warn.stdout.lower(), "expected blockers reported with --warn-only")

        # JSON format must produce the same two findings.
        result_json = _run(
            ["--prompt", prompt_path, "--format", "json"], project_root, env
        )
        _assert(result_json.returncode == 1, "expected exit 1 for JSON format")
        data = json.loads(result_json.stdout)
        _assert(data["blockers"] == 2, f"expected 2 blockers, got {data['blockers']}")
        providers = {finding["locked_to"] for finding in data["findings"]}
        _assert(
            providers == {"anthropic", "openai"},
            f"unexpected providers: {providers}",
        )

        # SARIF format must be valid and contain both findings.
        result_sarif = _run(
            ["--prompt", prompt_path, "--format", "sarif"], project_root, env
        )
        _assert(result_sarif.returncode == 1, "expected exit 1 for SARIF format")
        sarif = json.loads(result_sarif.stdout)
        _validate_sarif(sarif)
        results = sarif["runs"][0].get("results", [])
        _assert(len(results) == 2, f"expected 2 SARIF results, got {len(results)}")
        rule_ids = {r["ruleId"] for r in results}
        _assert(
            "anthropic-cache-control" in rule_ids and "openai-response-format" in rule_ids,
            f"unexpected SARIF ruleIds: {rule_ids}",
        )

        # Rules subcommand lists the default catalog.
        result_rules = _run(["rules"], project_root, env)
        _assert(result_rules.returncode == 0, "expected rules subcommand exit 0")
        _assert(
            "anthropic-cache-control" in result_rules.stdout,
            "expected default rule listed",
        )

        # --score must print a score below 100 because two blockers exist.
        result_score = _run(["--prompt", prompt_path, "--score"], project_root, env)
        _assert(result_score.returncode == 1, "expected exit 1 with --score (blockers)")
        _assert("Portability score:" in result_score.stdout, "expected score header")
        _assert("/100" in result_score.stdout, "expected score denominator")
        _assert("anthropic" in result_score.stdout.lower(), "expected anthropic in breakdown")
        _assert("openai" in result_score.stdout.lower(), "expected openai in breakdown")

        # --suggest-fixes must emit a Markdown report with concrete rewrites.
        result_fixes = _run(["--prompt", prompt_path, "--suggest-fixes"], project_root, env)
        _assert(result_fixes.returncode == 1, "expected exit 1 with --suggest-fixes")
        _assert("# Portability Fix Hints" in result_fixes.stdout, "expected Markdown heading")
        _assert("cache_control" in result_fixes.stdout, "expected cache_control fix hint")
        _assert("response_format" in result_fixes.stdout, "expected response_format fix hint")
    finally:
        try:
            os.remove(prompt_path)
        except Exception:
            pass

    print("selfcheck OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"selfcheck FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
