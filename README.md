<p align="center">
  <a href="https://github.com/Victorchatter/prompt-portability-linter/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-stdlib%20only-success.svg" alt="stdlib only">
</p>

# prompt-portability-linter

**A local linter that scans prompts and agent configs for vendor-locked features.**

Multi-provider agent setups are becoming normal, but it is easy to accidentally bake Anthropic-only `cache_control` breakpoints, OpenAI-only `response_format` / `strict` mode, Gemini `responseSchema`, or Codex slash-commands into a prompt or tool definition. This linter flags those locks *before* you commit to a vendor and tells you what to change to run the same prompt elsewhere.

It is fully local, read-only, and telemetry-free.

---

## What problem this solves

You write a system prompt that works great on Claude:

```markdown
You are a helpful coding assistant.

Use cache_control breakpoints to keep the long instructions warm.
When calling tools, set response_format to json_schema and strict: true.
```

Two months later you want to run the same agent on OpenAI or Gemini. The prompt now silently fails or behaves differently because those constructs are provider-specific. There is no existing guardrail that catches this at edit time.

`prompt-portability-linter` is that guardrail.

---

## Installation

```bash
pipx install .
```

Or from source:

```bash
git clone https://github.com/Victorchatter/prompt-portability-linter.git
cd prompt-portability-linter
pip install -e .
```

No external dependencies — just Python 3.10+ and the stdlib.

---

## Quick start

Lint a single system prompt:

```bash
prompt-portability-linter --prompt system.md
```

Lint a prompt plus tool definitions and an agent config:

```bash
prompt-portability-linter \
  --prompt system.md \
  --tools tools.json \
  --config agent.json
```

Get JSON for CI:

```bash
prompt-portability-linter --prompt system.md --format json
```

List the built-in rule catalog:

```bash
prompt-portability-linter rules
```

---

## Example: make this prompt portable

**Before** — vendor-locked:

```markdown
# system.md
You are a helpful coding assistant.

Use cache_control breakpoints to keep the long instructions warm in Anthropic's prompt cache.
When you call a function, set response_format to json_schema and strict: true so OpenAI validates the arguments.
For Gemini responses, supply a responseSchema object.
In the Codex CLI, start summaries with /compact.
```

Run the linter:

```text
$ prompt-portability-linter --prompt system.md
anthropic
  system.md:3  cache_control
    Anthropic prompt cache breakpoints are not portable.
    Suggestion: Remove cache_control blocks; manage context size in application code.

openai
  system.md:5  response_format
    OpenAI structured-output response_format is not portable.
    Suggestion: Request plain text/JSON and validate the schema yourself.
  system.md:5  strict mode
    OpenAI function strict mode is not portable.
    Suggestion: Validate tool arguments in application code.

gemini
  system.md:6  responseSchema
    Gemini responseSchema is not portable.
    Suggestion: Request JSON and validate against your schema.

codex
  system.md:7  /compact
    Codex CLI slash commands are not portable.
    Suggestion: Use natural-language instructions or portable tool calls.

4 portability blockers found.
```

**After** — portable:

```markdown
# system.md
You are a helpful coding assistant.

Keep instructions concise; the caller will manage context size and caching.
Request raw JSON output when structured data is needed; the caller validates it.
Summarize progress in natural language, not with slash commands.
```

The same agent can now run on Anthropic, OpenAI, Gemini, or any other provider that accepts a plain text system prompt.

---

## Rule catalog

The default catalog lives in `src/prompt_portability_linter/data/rules.yaml` and covers:

| Rule | Provider | What it flags | Suggested alternative |
|------|----------|---------------|-----------------------|
| `anthropic-cache-control` | anthropic | `cache_control` | Manage context size in application code. |
| `anthropic-computer-use` | anthropic | `computer_use` tool type | Use a generic browser/automation tool. |
| `anthropic-bash-20250124` | anthropic | `bash_20250124` tool type | Use a generic shell execution tool. |
| `openai-response-format` | openai | `response_format` | Request plain text/JSON and validate yourself. |
| `openai-strict-functions` | openai | `strict: true` | Validate tool arguments in application code. |
| `gemini-response-schema` | gemini | `responseSchema` | Request JSON and validate against your schema. |
| `codex-slash-command` | codex | `/command` lines | Use natural-language instructions. |

You can extend the catalog by editing `rules.yaml` or passing `--rules custom-rules.yaml`.

---

## CLI reference

```text
prompt-portability-linter --help
prompt-portability-linter rules --help
```

### `prompt-portability-linter` (lint)

| Flag | Description |
|------|-------------|
| `--prompt PATH` | System prompt file. Required. Repeatable. |
| `--tools PATH` | Tool definitions file (JSON). Repeatable. |
| `--config PATH` | Agent config file (JSON). Repeatable. |
| `--rules PATH` | Custom rule catalog YAML. |
| `--format text\|json` | Output format. Default: `text`. |
| `--warn-only` | Report blockers but exit `0`. |

### `prompt-portability-linter rules`

Prints the loaded rule catalog.

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | No blockers found, or `--warn-only` was used. |
| `1` | One or more portability blockers found. |
| `2` | CLI usage error or missing file. |

---

## Development & testing

Run the built-in self-test:

```bash
python selfcheck.py
```

It creates a synthetic prompt containing one Anthropic lock, one OpenAI lock, and one portable construct, then asserts:

- Exactly two blockers are reported.
- Each finding includes a suggested alternative.
- The linter exits nonzero without `--warn-only` and zero with `--warn-only`.

---

## Project structure

```
prompt-portability-linter/
├── src/prompt_portability_linter/
│   ├── cli.py             # Command-line interface
│   ├── catalog.py         # Rule catalog loader
│   ├── yaml_min.py        # Minimal stdlib-only YAML loader
│   ├── extract.py         # Token extraction from inputs
│   ├── linter.py          # Rule matching engine
│   ├── outputs.py         # Text/JSON formatters
│   ├── data/
│   │   └── rules.yaml     # Default rule catalog
│   ├── __init__.py
│   └── __main__.py
├── selfcheck.py           # End-to-end test
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## License

MIT. See [LICENSE](LICENSE).
