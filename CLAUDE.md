# safecmd

## CRITICAL: Test Safety

**NEVER use actually dangerous paths or commands in tests or examples**, even with `#| eval:false`. If a test fails or someone accidentally runs a cell, it shouldn't break the computer. Use harmless fake paths like `/nonexistent/path` instead of real system paths like `/etc/passwd` or `/usr/bin/sudo`.

---

A library for safely running bash commands by validating them against allowlists.

## Project Structure

- **nbs/**: Jupyter notebooks (source of truth for nbdev)
  - `00_bashxtract.ipynb`: Parses bash commands via shfmt AST, extracts commands/operators/redirects
  - `01_core.ipynb`: Validation logic, safe_run(), config handling, CLI
  - `index.ipynb`: Documentation homepage
- **safecmd/**: Generated Python modules (via nbdev_export)

## Key Concepts

- Uses `shfmt` to parse bash into AST (handles all bash syntax correctly)
- `extract_commands(cmd)` returns (commands, ops, redirects)
- `CmdSpec`: Prefix-matched command allowlist with optional denied flags
- `ok_dests`: Allowed destination patterns for write redirects (e.g., `./`, `/tmp`)
- All paths are resolved to absolute before matching (handles `~`, `$HOME`, `..`)
- This prevents path traversal attacks like `./..` or `./subdir/../../escape`

## Workflow

1. Edit notebooks in `nbs/`
2. Run `nbdev_export` to generate Python modules
3. Run `nbdev_test --path nbs/notebook.ipynb` to test

## Testing

Tests are inline in notebooks using `test_eq`, `test_fail` from fastcore.test.

## Config

Config file at `~/.config/safecmd/config.ini` (Linux) or equivalent XDG path.
Contains `ok_dests` (allowed write destinations) and `ok_cmds` (allowed commands).
