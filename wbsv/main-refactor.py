import sys

from .archiver import RandomArchiver, Archiver
from .finder import Finder
from . import ParseArgs
from .interactive import Interactive

def main():
    """Main function."""
    opt = ParseArgs.parse_args()
    
    if opt["dry-run"] :
        archiver = RandomArchiver()
    else:
        archiver = Archiver()
    
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
        except KeyboardInterrupt:
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)
            exit(1)

        archiver.print_result()
        exit(0)


if __name__ == "__main__":
    main()