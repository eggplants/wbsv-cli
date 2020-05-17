from . import Archive
from . import ParseArgs
from . import Interact


def main():
    """Main function."""
    opt = ParseArgs.parse_args()

    if len(opt["urls"]) == 0:
        Interact.interactive(opt)

    elif opt["only-target"]:
        for x in opt["urls"]:
            Archive.archive([x], x, opt["retry"])
    else:
        for x in opt["urls"]:
            Archive.archive(Archive.extract_uri_recursive(
                x, opt["level"]), x, opt["retry"])

    # if no errors occurred ...
    exit(0)


if __name__ == "__main__":
    main()
