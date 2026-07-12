"""Allow ``python -m llm_release_gate`` (works even when the console script
isn't on PATH, e.g. inside CI runners or user-site installs)."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
