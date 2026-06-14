from __future__ import annotations

import os
import sys


def main() -> int:
    print("OPENAI_API_KEY set:", bool(os.getenv("OPENAI_API_KEY")))
    try:
        import ragas
        from ragas import evaluate  # noqa: F401

        print("RAGAS import: OK")
        print("RAGAS version:", getattr(ragas, "__version__", "unknown"))
    except Exception as exc:
        print("RAGAS import: FAILED")
        print(repr(exc))
        return 1

    if not os.getenv("OPENAI_API_KEY"):
        print("")
        print("Set the API key in the SAME PowerShell window before running evaluation:")
        print('$env:OPENAI_API_KEY="paste_your_key_here"')
        return 2

    print("Setup is ready for RAGAS judge metrics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
