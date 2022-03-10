import sys


def log_exception(e: Exception) -> None:
    print(f"{type(e).__name__}:", "%s..." % e.args[0].split('\n')[0], file=sys.stderr)
