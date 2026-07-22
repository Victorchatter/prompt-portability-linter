# prompt-portability-linter — bootstrap session prompt

You are bootstrapping a new open-source project. Follow the full process: `superpowers:brainstorming` → lock design → write spec to `docs/superpowers/specs/YYYY-MM-DD-prompt-portability-linter-design.md` → commit → `superpowers:writing-plans` (approve) → implement via `superpowers:executing-plans`. Verify with `selfcheck.py` before done.

## Idea (one-liner)
A local linter that scans a system prompt (and optional tool definitions / agent config) for vendor-locked features — `cache_control` breakpoints, Anthropic `computer_use` / `bash_20250124` tool types, OpenAI `response_format`/`strict` mode, Gemini `responseSchema`, Codex-specific slash-commands — and reports portability blockers before you commit to a vendor. Tells you exactly what to change to run the same prompt on another provider.

## Why it doesn't exist
Nobody ships a linter that catches vendor lock-in in prompts *before* you're stuck. As multi-provider agent setups become normal, this is a small, useful guardrail.

## Hard constraints
- Python, `pipx install .`. Fully local/offline, no telemetry, read-only.
- Rule-based, not model-based: a curated catalog of known vendor-locked tokens/patterns per provider, each rule = `(pattern, locked_to, message, suggested_portable_alternative)`. Ship the catalog as an editable `rules.yaml` so users extend it.
- Inputs: one or more prompt files (`--prompt`), optionally a tool-definitions file (`--tools`), optionally an agent config file (`--config`). Lint all.
- Output: text or JSON report grouped by provider lock. Exit nonzero if any blocker found (configurable `--warn-only`).
- CLI: `prompt-portability-linter --prompt system.md [--tools tools.json] [--format text|json] [--warn-only]`; `prompt-portability-linter rules` lists known rules.
- Small and sharp. Ponytail: stdlib only, no unrequested abstractions, shortest working diff. `# ponytail:` comments on simplifications.
- One `selfcheck.py`: a prompt with one Anthropic lock (`cache_control`), one OpenAI lock (`response_format` strict), and one portable construct; assert the linter flags exactly the two locks, suggests alternatives, exits nonzero.
- License MIT. README with a before/after "make this prompt portable" example.

## Scope / YAGNI (v1)
Ship: rules catalog (Anthropic + OpenAI + Gemini + Codex minimum), three input kinds (prompt/tools/config), text+JSON output, exit codes, editable rules.yaml. Out: auto-rewrite (recommend against — suggest only), model-based semantic lock detection, CI action (follow-up).

## Inputs to lock during brainstorming
- Rule granularity: line-based regex vs token-based (recommend line/regex-based + structural for tool defs — keep it simple).
- Whether to also flag *behavioral* lock-in (e.g. assuming a 200k context window) — recommend a small set of soft warnings, clearly separated from hard locks.
- How to handle constructs that are portable in *meaning* but not in *spelling* (e.g. system-prompt formatting conventions) — recommend: don't lint prose, lint machine-readable tokens only.

One of 10 sibling local-first agent-tooling projects. Keep it small and ship it.