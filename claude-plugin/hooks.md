# Creating Claude Code Hooks

This documents what we learned creating a `PreToolUse` hook that auto-approves safe bash commands using safecmd.

## Hook Configuration Location

Hooks are defined in `settings.json`, **not** in a separate `hooks.json` file:

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "python3 /path/to/hook.py"}
        ]
      }
    ]
  }
}
```

## Hook Input Format

The hook receives JSON on stdin. Key fields use **snake_case**:

```json
{
  "session_id": "...",
  "cwd": "/current/working/dir",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la",
    "description": "List files"
  },
  "tool_use_id": "toolu_..."
}
```

Note: It's `tool_input` (snake_case), not `toolInput` (camelCase).

## Hook Output Format

To auto-approve a tool call, output JSON with `hookSpecificOutput`:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "reason shown to user"
  }
}
```

Required fields:
- `hookEventName`: Must be `"PreToolUse"`
- `permissionDecision`: One of `"allow"`, `"deny"`, or `"ask"`
- `permissionDecisionReason`: Explanation (shown to user for allow/ask, shown to Claude for deny)

## Exit Codes

- Exit 0 with approval JSON → auto-approve
- Exit 0 without JSON → fall through to normal permission prompt
- Exit 2 → block (stderr message shown to Claude)

## Minimal Working Example

```python
#!/usr/bin/env python3
import sys,json

def main():
    try: hook_input = json.load(sys.stdin)
    except json.JSONDecodeError: sys.exit(0)

    cmd = hook_input.get("tool_input", {}).get("command", "")
    if not cmd: sys.exit(0)

    # Your validation logic here
    if is_safe(cmd):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "command validated"
        }}), flush=True)
        sys.exit(0)
    # else: fall through to normal prompt

if __name__ == "__main__": main()
```

## Gotchas We Encountered

1. **Wrong config location**: Hooks go in `settings.json`, not a separate `hooks.json`

2. **Tilde expansion**: Use full paths in settings.json (`/Users/name/...`), not `~`

3. **Snake case keys**: The input JSON uses `tool_input`, not `toolInput`

4. **Missing hookEventName**: The output JSON must include `"hookEventName": "PreToolUse"`

5. **Flush stdout**: Use `print(..., flush=True)` to ensure output is sent

6. **Import errors**: If imports fail, the hook silently fails - add error handling

## Debugging Hooks

Add logging to a file (not stdout/stderr which interfere with hook protocol):

```python
def log(msg):
    with open("/tmp/hook-debug.log", "a") as f:
        f.write(msg + "\n")
        f.flush()
```

Use `Read` tool (not `cat`) to check logs, since `cat` triggers the hook and can cause race conditions.

## Our safecmd Hook

The complete hook that auto-approves commands validated by safecmd's allowlist:

```python
#!/usr/bin/env python3
import sys,json
from safecmd import validate, DisallowedError

def main():
    try: hook_input = json.load(sys.stdin)
    except json.JSONDecodeError: sys.exit(0)

    cmd = hook_input.get("tool_input", {}).get("command", "")
    if not cmd: sys.exit(0)

    try:
        validate(cmd)
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "safecmd: validated"
        }}), flush=True)
        sys.exit(0)
    except DisallowedError: pass

if __name__ == "__main__": main()
```

## References

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
