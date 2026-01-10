# safecmd Claude Code Plugin

Auto-approve safe bash commands in Claude Code using safecmd's allowlist.

## Prerequisites

Install safecmd:
```bash
pip install safecmd
```

## Installation

```bash
claude /plugin install https://github.com/AnswerDotAI/safecmd/tree/main/claude-plugin
```

Or install from local path:
```bash
claude /plugin install /path/to/safecmd/claude-plugin
```

## How It Works

This plugin adds a `PreToolUse` hook for the `Bash` tool that:

1. Intercepts bash commands before execution
2. Validates them against safecmd's allowlist using AST parsing
3. Auto-approves safe commands (no permission prompt)
4. Falls through to normal permission prompt for disallowed commands

## Configuration

The allowlist is configured via safecmd's config file:
- **Linux**: `~/.config/safecmd/config.ini`
- **macOS**: `~/Library/Application Support/safecmd/config.ini`

See [safecmd documentation](https://github.com/AnswerDotAI/safecmd) for details on customizing the allowlist.
