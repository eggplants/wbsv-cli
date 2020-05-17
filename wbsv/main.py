from . import Archive
from . import Find
from . import ParseArgs
from . import Interact


def main():
    """Main function."""
    opt = ParseArgs.parse_args()

    if len(opt["urls"]) == 0:
        Interact.interactive(opt)

    elif opt["only-target"]:
        [Archive.archive([x], x, opt["retry"]) for x in opt["urls"]]
        exit(0)

    else:
        for x in opt["urls"]:
            dic = Find.extract_uri_recursive(x, opt["level"])
            Archive.archive(dic, x, opt["retry"])

        exit(0)


if __name__ == "__main__":
    main()
