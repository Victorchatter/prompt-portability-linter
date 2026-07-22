# Plan: Bootstrap prompt-portability-linter v0.1.0

## Context

`PROMPT.md` describes a new local-first, stdlib-only CLI: a linter that scans system prompts, tool definitions, and agent configs for vendor-locked constructs (Anthropic `cache_control` / `computer_use` / `bash_20250124`, OpenAI `response_format` / `strict`, Gemini `responseSchema`, Codex slash-commands) and reports what to change to run the same prompt elsewhere.

Current repo is empty except for `PROMPT.md` and `.claude/settings.local.json`. We follow the same shape as the recent sibling local-first projects (`toolcall-cache`, `tokenauditor`, `mcp-openai-bridge`): MIT license, `pyproject.toml`, `selfcheck.py`, README with badges/structure, and a small `src/` package.

Hard constraints from `PROMPT.md`:
- Python 3.10+, `pipx install .`, stdlib only, read-only, no telemetry.
- Editable `rules.yaml` catalog.
- CLI: `--prompt`, optional `--tools`, optional `--config`, `--format text|json`, `--warn-only`, plus `rules` subcommand.
- Exit nonzero on blockers unless `--warn-only`.
- One `selfcheck.py` with a mixed prompt asserting exactly two locks flagged + alternatives suggested + nonzero exit.

Key tension: `rules.yaml` is required, but stdlib has no YAML parser. Ponytail resolution: ship a tiny YAML loader that handles only the controlled `rules.yaml` subset (no anchors/flow-style/quoting complexity).

## Approach

### New: `src/prompt_portability_linter/`

Package layout:

```
src/prompt_portability_linter/
├── __init__.py          # __version__ = "0.1.0"
├── __main__.py          # python -m prompt_portability_linter
├── cli.py               # argparse, dispatch, exit codes
├── yaml_min.py          # minimal YAML loader (stdlib only)
├── catalog.py           # load embedded rules.yaml + optional user rules.yaml
├── extract.py           # token extraction from text / JSON / YAML-ish files
├── linter.py            # apply rules, collect findings
├── outputs.py           # text and JSON formatters
└── data/
    └── rules.yaml       # default rule catalog
```

**`data/rules.yaml`** — initial catalog covering the required providers:
- `anthropic-cache-control`: `\bcache_control\b`
- `anthropic-computer-use`: `\bcomputer_use\b`
- `anthropic-bash-20250124`: `\bbash_20250124\b`
- `openai-response-format`: `\bresponse_format\b`
- `openai-strict-functions`: `\bstrict\s*:\s*true\b`
- `gemini-response-schema`: `\bresponseSchema\b`
- `codex-slash-command`: `^/\w+` (per line, for Codex CLI-style slash directives)

Each rule: `id`, `pattern` (regex), `locked_to`, `message`, `suggestion`, `severity` (`blocker`).

**`yaml_min.py`** — a ~80-line indentation-based loader that supports mappings, lists, comments, and scalar values (strings/bools). `# ponytail: stdlib-only replacement for PyYAML; only parses the rules.yaml subset we control.`

**`catalog.py`** — load the embedded default catalog with `importlib.resources`, then optionally merge a user-provided `rules.yaml` (or use `--rules` if added later). Validates required fields.

**`extract.py`** — produce searchable tokens per input kind:
- `--prompt` files: one token per line (line number + text). `# ponytail: regex over raw prompt text; acceptable false-positive rate for v1.`
- `--tools` / `--config` files: parse JSON, recursively walk keys/string values, emit tokens with JSON path context. `# ponytail: structural extraction avoids matching these terms inside prose comments.`
- Unknown extensions: treat as text.

**`linter.py`** — for each token, run all rule regexes (with word boundaries / anchored patterns already included in the rule). A finding records: file path, rule id, provider, line or path, matched snippet, message, suggestion.

**`outputs.py`** — `format_text(findings)` grouped by provider, sorted by file/line; `format_json(findings)` returns a stable dict. JSON output is printed via `json.dumps(..., indent=2)`.

**`cli.py`** — argparse interface:
- `prompt-portability-linter --prompt P [ --tools T ] [ --config C ] [ --format text|json ] [ --warn-only ] [ --rules R ]`
- `prompt-portability-linter rules [ --format text|json ]`
- Exit codes: `0` = clean or `--warn-only`, `1` = blocker(s) found, `2` = CLI/file error.

### New: `selfcheck.py`

End-to-end self-test:
1. Write a temp prompt containing:
   - Anthropic lock: `Use cache_control breakpoints.`
   - OpenAI lock: `Set response_format with strict:true.`
   - Portable construct: `You are a helpful assistant.`
2. Run the linter CLI via `subprocess` with `PYTHONPATH=src`.
3. Assert exit code is `1`.
4. Parse text output and assert exactly two findings, one per Anthropic and OpenAI, each with a suggestion line.
5. Run with `--warn-only` and assert exit code `0`.
6. Run with `--format json` and assert JSON contains the same two findings.
7. Run `rules` subcommand and assert the default catalog is listed.
8. Clean up temp files and print `selfcheck OK`.

### New: `pyproject.toml`, `LICENSE`, `README.md`

- `pyproject.toml`: setuptools build, name `prompt-portability-linter`, version `0.1.0`, entry point `prompt-portability-linter = "prompt_portability_linter.cli:main"`, Python `>=3.10`, no dependencies, classifiers matching siblings.
- `LICENSE`: MIT, Copyright 2026 Victor.
- `README.md`: badges, one-liner, problem statement, installation, quick start with a before/after portable-prompt example, CLI reference table, development/testing, project structure, license.

### Preserve: `PROMPT.md`

Leave the existing `PROMPT.md` in place as the project brief.

## Verification

- `python selfcheck.py` passes.
- `pipx install .` installs the `prompt-portability-linter` command (local editable install check).
- `prompt-portability-linter rules` prints the default rule catalog.
- `prompt-portability-linter --prompt README-example.md --tools example-tools.json` produces grouped output and exits `1` when locks are present.
- `--warn-only` exits `0` despite locks.

## Skipped (add when)

- Auto-rewrite / fix mode — explicitly out of scope per `PROMPT.md`.
- Model-based semantic lock detection — out of scope.
- CI GitHub Action — listed as follow-up.
- Extended behavioral soft warnings (context-window assumptions) — kept out of v1; only hard locks.
- YAML config parsing beyond the minimal subset — we only parse `rules.yaml`; user configs are treated as JSON or text.
