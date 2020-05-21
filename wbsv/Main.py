import sys

from . import Archive
from . import Find
from . import ParseArgs
from . import Interact


def collect_archiver(opt):
    if opt["dry-run"]:
        return Archive.RandomArchiver()
    else:
        return Archive.Archiver()


def main():
    """Main function."""
    opt = ParseArgs.parse_args()

    archiver = collect_archiver(opt)
    finder = Find.Finder()

    archiver.parse_opt(opt)
    finder.parse_opt(opt)

    if len(opt["urls"]) == 0:
        interact = Interact.Interactive(finder, archiver)
        interact.parse_opt(opt)
        interact.run()

    else:
        try:
            for x in opt["urls"]:
                finder.find_and_archive(x, archiver)
                archiver.print_result(x)

        except KeyboardInterrupt:
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    main()
