import sys

from . import Archive
from . import Find


def get_input(v):
    """Get a REPL input."""
    try:
        if Archive.is_url(v):
            return v

        else:
            print("[!]This input is invalid.", file=sys.stderr)
            return ''

    except(EOFError, KeyboardInterrupt):
        print("\n[+]End.")
        exit(0)


def chk_url_cond(url, opt):
    """Change a behavior according to options."""
    if Archive.is_end(url):
        print("[+]End.")
        exit(0)

    elif opt["only-target"]:
        Archive.archive([url], url, opt["retry"])

    else:
        try:
            dic = Find.extract_uri_recursive(url, opt["level"])

        except KeyboardInterrupt:
            dic = []
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)

        Archive.archive(dic, url, opt["retry"])


def interactive(opt):
    """Interactive mode like shell."""
    print("[+]To exit, use CTRL+C or type 'end'")
    while True:
        print("[[Input a target url (ex: https://google.com)]]")
        url = get_input(input(">>> "))
        if not url:
            chk_url_cond(url, opt)
