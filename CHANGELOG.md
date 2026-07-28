# Changelog

## 0.2.0

### Added
- `--format sarif` output for CI integration.
  - SARIF includes `runs[0].results` with `ruleId`, `message.text`, and
    `locations[0].physicalLocation` mapped to the prompt file and line number.
- GitHub Actions example in README showing SARIF upload to fail a PR on blockers.
- `selfcheck.py` validates SARIF output structure.
- `--score` prints a `0-100` portability score with a per-provider breakdown.
  - Documented weights: Anthropic/OpenAI blockers -10, Gemini/Codex blockers -8,
    warnings -3.
- `--suggest-fixes` emits a Markdown patch report with matched lines and concrete
  portable rewrites; `--output PATH` writes it to a file instead of stdout.
- Richer rule suggestions in `rules.yaml`.

## 0.1.0

### Added
- Initial release: stdlib-only linter for vendor-locked prompt and tool features.
