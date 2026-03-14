#!/usr/bin/env python3
"""Check that the first line of the commit message follows Conventional Commits."""
import re
import sys

# Same style as OpenClaw: type(scope): description
PATTERN = re.compile(
    r"^(feat|fix|docs|style|refactor|test|build|chore|ci|revert)"
    r"(\([a-z0-9-]+\))?!?:\s+.+"
)


def main() -> int:
    if len(sys.argv) < 2:
        return 0
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            first = f.readline().strip()
    except OSError:
        return 0
    # Ignore merge commits and empty
    if first.startswith("Merge ") or not first:
        return 0
    if not PATTERN.match(first):
        print(
            "Commit message must follow Conventional Commits.\n"
            "Example: feat(bot): add new command\n"
            "See docs/COMMIT_CONVENTION.md"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
