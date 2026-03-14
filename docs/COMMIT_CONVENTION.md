# Commit convention

Miniclaw follows [Conventional Commits](https://www.conventionalcommits.org/) (same as [OpenClaw](https://github.com/openclaw/openclaw)). This keeps history consistent and works well with changelog tools.

## Format

```
<type>[optional scope]: <description>

[optional body]
[optional footer(s)]
```

- **First line** must match: `type(scope): description`
- **Type** is required; **scope** is optional (e.g. `fix(bot):`, `docs:`).

## Types

| Type     | Use for |
|----------|---------|
| `feat`   | New feature (MINOR) |
| `fix`    | Bug fix (PATCH) |
| `docs`   | Documentation only |
| `style`  | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test`   | Adding or updating tests |
| `build`  | Build, CI, or tooling |
| `chore`  | Other (deps, config, etc.) |

## Rules

- **Description**: imperative, lowercase, no period at the end.
  - Good: `add preset overwrite prompt`
  - Bad: `Added preset overwrite prompt.`
- **Length**: about 50–72 characters for the first line.
- **Breaking changes**: add `!` after type/scope or use footer `BREAKING CHANGE: ...`.

## Examples

```
feat(skill): add /addskills chat flow
fix(presets): avoid recursion in _ensure_db
docs: add README en/ko/zh
refactor: move COMMANDS into single list
chore(deps): bump ruff to 0.8.4
```

## Check

On `git commit`, the message is checked by a pre-commit hook. If the first line does not match the convention, the commit is rejected with a pointer to this file.

Install the commit-msg hook (once per clone):

```bash
pre-commit install --hook-type commit-msg
```
