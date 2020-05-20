import sys

from .archiver import RandomArchiver, Archiver
from .finder import Finder
from . import ParseArgs
from .interactive import Interactive


def collect_archiver(opt):
    if opt["dry-run"] :
        return RandomArchiver()
    else:
        return Archiver()

def main():
    """Main function."""
    opt = ParseArgs.parse_args()

    archiver = collect_archiver(opt)
    finder = Finder()

    archiver.parse_opt(opt)
    finder.parse_opt(opt)

    if len(opt["urls"]) == 0:
        interact = Interactive(finder, archiver)
        interact.parse_opt(opt)
        interact.run()

    else:
        try:
            [finder.find_and_archive(x, archiver) for x in opt["urls"]]
            archiver.print_result()
        except KeyboardInterrupt:
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)
            exit(1)


if __name__ == "__main__":
    main()
