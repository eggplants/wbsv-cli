import sys


def log_exception(e: Exception) -> None:
    print(e, file=sys.stderr)
