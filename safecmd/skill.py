"""Execute bash commands safely from python using `safecmd`. 

# Execution model

`safecmd` runs shell commands through a bash parser and allowlist before anything executes. Use `bash(cmd_)` as the main entry point for shell work.

`bash` validates the whole command line, including pipelines, command substitutions, subshells, redirects, and nested commands. If validation passes, it runs the command and returns stdout plus stderr as text.

Use `bash(cmd_, as_dict=True)` when you want structured results. Successful runs return `{'success': ...}`; blocked or failed runs return `{'error': ...}` with details the agent should report.

Treat `bash` as the shell execution path. Do not use raw `subprocess`, `os.system`, shell magics, or other unmanaged shell execution when `safecmd` is available.

# Command style and workflow

Write simple, inspectable shell commands. Prefer commands that answer one question at a time: inspect, read, compare, then decide the next command.

Start with read-oriented commands such as `ls`, `tree`, `find`, `rg`, `grep`, `cat`, `head`, `tail`, `wc`, `file`, `stat`, `git status`, `git diff`, and `git log`.

Quote paths and patterns when they may contain spaces or shell metacharacters. Remember that `bash` runs through the shell, so `$`, `*`, pipes, redirects, and command substitutions have normal bash meaning.

For file edits, prefer purpose-built Python or editing tools when available. Use shell commands for locating, inspecting, comparing, and simple workspace operations.

Before running commands that may change files or repository state, make the intended change explicit and prefer checking `git status` first.

# Allowlist, permissions, and failures

`safecmd` allows commands by command prefix and validates destinations for file-writing operations. A command may be allowed in one form and blocked in another.

The allowlist checks nested commands too. Commands inside pipelines, command substitutions, subshells, `xargs`, `env`, and configured exec flags are validated before anything runs.

Destination checks apply to output redirects and configured destination arguments. If a destination is blocked, report the path and operation instead of trying another spelling.

When `bash(...)` returns or raises a safecmd error, report the blocked command and the specific reason: disallowed command, disallowed destination, or validation failure.

Do not route around the allowlist by hiding the same operation inside another command, command substitution, `xargs`, `env`, or a different shell spelling.

If a command is blocked because of an unsafe idiom, rewrite it as a simpler allowed inspection command. If the task truly needs a blocked command or destination, stop and ask the user whether it should be allowed.

If the command failed for ordinary shell reasons such as a missing file, no matches, bad quoting, or nonzero exit status, fix the command normally and retry if the next step is clear.

Use `bash(cmd_, as_dict=True)` when you need to distinguish validation errors from command output without catching exceptions.

# Common workflows

Inspect a folder:

```python
bash("tree --charset ascii -n . -L 2")
```

Search text:

```python
bash("rg -n 'pattern' .")
```

Inspect git state:

```python
bash("git status && git diff --stat")
```

Read a file section:

```python
bash("head path/to/file.py")
```

# Gotchas

`safecmd` parses bash, not Python. Quote shell strings for the shell first, then for Python if the command is inside a Python string.

Pipes and command substitutions are not shortcuts around validation. Every nested command is checked.

Output redirects and destination arguments are allowed only for approved destination roots. Prefer tool-specific editing functions for file modifications.

Globs such as `*.py` are expanded by the shell. Quote them when you want the pattern passed literally to a command like `rg` or `find`.

Allowed commands can still fail normally. A safecmd validation failure is a permission issue; a nonzero exit status is usually a command, path, or data issue.
"""
from pyskills.core import allow
from safecmd.core import bash

__all__ = ['bash']

allow(bash)
