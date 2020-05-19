import sys

from .archiver import RandomArchiver
from .finder import Finder
from . import ParseArgs
from . import Interact


def iter_urls(finder, archiver, opt):
    """Iterate given urls for saving."""
    try:
        for url in opt["urls"]:
            finder.find_and_archive(url, archiver)
            #Archive.archive(Find.extract_uri_recursive(x, opt["level"]),
            #                x, opt["retry"])
    except KeyboardInterrupt:
        print("[!]Interrupted!", file=sys.stderr)
        print("[!]Halt.", file=sys.stderr)
        exit(1)


def main():
    """Main function."""
    opt = ParseArgs.parse_args()
    archiver = RandomArchiver()
    finder = Finder()

    archiver.parse_opt(opt)
    finder.parse_opt(opt)
    
    if len(opt["urls"]) == 0:
        Interact.interactive(opt)

    elif opt["only-target"]:
        [archiver.archive(x) for x in opt["urls"]]
        exit(0)

    else:
        iter_urls(finder, archiver, opt)
        archiver.print_result()
        exit(0)


if __name__ == "__main__":
    main()