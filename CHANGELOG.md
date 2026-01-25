# Release notes

<!-- do not remove -->

## 0.1.1

### Bugs Squashed

- Fix for loop support: handle Then/Else/Do as stmt lists and add WordIter type ([#7](https://github.com/AnswerDotAI/safecmd/issues/7))


## 0.1.0

### Breaking Changes

Refactor: Replace operator blocking with destination-based redirect validation

Major changes:
- Remove `ok_ops` allowlist; all operators now permitted
- Add `ok_dests` allowlist for output redirect destinations (default: ./, /tmp)
- `extract_commands`() now returns 3-tuple: (commands, operators, redirects)
- New `collect_redirects`() extracts write redirect destinations from AST
- New `normalize_dest`()/`validate_dest`() resolve paths to absolute before matching,
preventing path traversal attacks (./.. , ./subdir/../../escape)
- Rename DisallowedOps -> DisallowedDest

CmdSpec improvements:
- Detect denied flags in combined short flags (e.g., -xvfI matches -I)
- Match long flags with =value (e.g., --to-command=cat matches --to-command)

API changes:
- `safe_run`/validate: ops param -> dests param
- `add_allowed_ops`/`rm_allowed_ops` -> `add_allowed_dests`/`rm_allowed_dests`
- `bash`/`unsafe_bash`: `rm_ops` -> `rm_dests`, `add_ops` -> `add_dests`
- Extract validate() function for reusable command validation ([#6](https://github.com/AnswerDotAI/safecmd/issues/6))


## 0.0.6

### New Features

- Add `safecmd` console script ([#5](https://github.com/AnswerDotAI/safecmd/issues/5))


## 0.0.5

### New Features

- Add `ignore_ex` to `safe_run`, and add fd redirect ops ([#4](https://github.com/AnswerDotAI/safecmd/issues/4))


## 0.0.4

### New Features

- Add tools ([#3](https://github.com/AnswerDotAI/safecmd/issues/3))


## 0.0.3

### New Features

- Add `=` op; add deny lists for rg, tar, and curl ([#2](https://github.com/AnswerDotAI/safecmd/issues/2))


## 0.0.2

### New Features

- Add builtins; new params to add/rm cmds/ops ([#1](https://github.com/AnswerDotAI/safecmd/issues/1))


## 0.0.1

- init release

