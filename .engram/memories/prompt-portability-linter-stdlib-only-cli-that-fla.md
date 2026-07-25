---
id: "0a748a81"
type: context
tags: []
created: "2026-07-25T13:27:31.659Z"
source: manual
---
prompt-portability-linter: stdlib-only CLI that flags vendor-locked prompt/tool/config features so prompts stay portable across providers. CLI entry point: prompt-portability-linter (src/prompt_portability_linter/cli.py). v0.1.0 shipped 2026-07-22, pipx-installable. # ponytail: extract.py uses line-based regex, not a structural parser; yaml_min.py is a stdlib-only PyYAML replacement handling only mappings/lists/scalars (rules.yaml never nests further).
