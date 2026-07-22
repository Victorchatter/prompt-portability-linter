# prompt-portability-linter — design spec

**Date:** 2026-07-22  
**Version:** v0.1.0  
**Status:** implemented

## Goal

A local, stdlib-only CLI linter that scans system prompts, tool definitions, and agent configs for vendor-locked constructs and reports what must change to run the same prompt on another provider.

## Constraints

- Python 3.10+, `pipx install .`, stdlib only, read-only, no telemetry.
- Rule-based catalog; editable `rules.yaml`.
- Inputs: `--prompt`, `--tools`, `--config` (all repeatable).
- Outputs: text (grouped by provider) and JSON.
- Exit codes: `0` clean/warn-only, `1` blockers, `2` errors.
- One `selfcheck.py` with a mixed prompt asserts exactly two locks flagged + alternatives suggested + nonzero exit.

## Rule catalog

Default `rules.yaml` covers Anthropic, OpenAI, Gemini, and Codex locks:

| id | provider | pattern |
|---|---|---|
| `anthropic-cache-control` | anthropic | `\bcache_control\b` |
| `anthropic-computer-use` | anthropic | `\bcomputer_use\b` |
| `anthropic-bash-20250124` | anthropic | `\bbash_20250124\b` |
| `openai-response-format` | openai | `\bresponse_format\b` |
| `openai-strict-functions` | openai | `\bstrict["']?\s*:\s*true\b` |
| `gemini-response-schema` | gemini | `\bresponseSchema\b` |
| `codex-slash-command` | codex | `^/\w+` |

## Architecture

```
src/prompt_portability_linter/
├── cli.py           # argparse, dispatch, exit codes
├── catalog.py       # load embedded + optional user rules.yaml
├── yaml_min.py      # minimal stdlib-only YAML loader
├── extract.py       # line tokens for prompts; key/value/pair tokens for JSON/YAML
├── linter.py        # regex rule matching with (file, context, rule) deduplication
├── outputs.py       # text and JSON formatters
└── data/rules.yaml  # default catalog
```

**Extraction strategy:**
- Prompt files are scanned line-by-line with regex.
- JSON/YAML tool and config files are parsed and walked; keys, string values, and key-value pairs are emitted as searchable tokens with JSON-path context.

**YAML handling:** stdlib has no YAML parser, so a minimal loader parses only the controlled `rules.yaml` subset (mappings, lists, comments, scalars).

## CLI

```text
prompt-portability-linter --prompt P [--tools T] [--config C] \
  [--format text|json] [--warn-only] [--rules R]

prompt-portability-linter rules [--format text|json]
```

## Verification

- `python selfcheck.py` passes.
- Wheel builds and installs; entry point works.
- `prompt-portability-linter rules` lists the default catalog.
- Mixed prompt + tool definitions produce grouped output and exit `1`.

## Out of scope

- Auto-rewrite / fix mode.
- Model-based semantic lock detection.
- CI GitHub Action (follow-up).
- Behavioral soft warnings (context-window assumptions).
