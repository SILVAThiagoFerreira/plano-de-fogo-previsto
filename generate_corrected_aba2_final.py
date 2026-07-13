"""Legacy compatibility wrapper.

The canonical entry point is `main.py`.
"""

from main import main


if __name__ == "__main__":
    raise SystemExit(main())
