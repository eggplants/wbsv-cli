import sys
from . import Archive
from . import Find


def get_input():
    try:
        return input(">>> ")
    except(EOFError, KeyboardInterrupt):
        print("\n[+]End.")
        exit(0)


def interactive(opt):
    """Interactive mode like shell."""
    print("[+]To exit, use CTRL+C or type 'end'")
    while True:
        print("[[Input a target url (ex: https://google.com)]]")
        url = get_input()

        if Archive.is_url(url) and opt["only-target"]:
            Archive.archive([url], url, opt["retry"])

        elif Archive.is_url(url):
            dic = Find.extract_uri_recursive(url, opt["level"])
            Archive.archive(dic, url, opt["retry"])

        elif Archive.is_end(url):
            print("[+]End.")
            exit(0)

        else:
            print("[!]This input is invalid.", file=sys.stderr)
