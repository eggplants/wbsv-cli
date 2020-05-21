import sys

from . import Archive
from . import Find
from . import ParseArgs
from . import Interact


def iter_urls(opt):
    """Iterate given urls for saving."""
    try:
        for x in opt["urls"]:
            Archive.archive(Find.extract_uri_recursive(x, opt["level"]),
                            x, opt["retry"])

    except KeyboardInterrupt:
        print("[!]Interrupted!", file=sys.stderr)
        print("[!]Halt.", file=sys.stderr)
        exit(1)


def main():
    """Main function."""
    opt = ParseArgs.parse_args()

    if len(opt["urls"]) == 0:
        Interact.interactive(opt)

    elif opt["only-target"]:
        [Archive.archive([x], x, opt["retry"]) for x in opt["urls"]]
        exit(0)

    else:
        iter_urls(opt)
        exit(0)


if __name__ == "__main__":
    main()
