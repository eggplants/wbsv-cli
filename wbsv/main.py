#!/usr/bin/env python
import argparse
import http.client as httplib
import sys
import textwrap
from typing import Iterable, List, Optional, Set

from wbsv import __version__
from wbsv.archiver import Archiver
from wbsv.crawler import Crawler


class HttpConnectionNotFountError(Exception):
    pass


def check_connectivity(url: str = "www.google.com", timeout: int = 3) -> bool:
    conn = httplib.HTTPConnection(url, timeout=timeout)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        return False


def check_natural(v: str) -> int:
    if int(v) < 0:
        raise argparse.ArgumentTypeError("%s is an invalid natural number" % int(v))
    return int(v)


def check_positive(v: str) -> int:
    if int(v) <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid natural number" % int(v))
    return int(v)


def parse_args(args_list: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="wbsv",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            CLI tool for save webpage on Wayback Machine forever.
            Save webpage and one 's all URI(s) on Wayback Machine."""
        ),
        epilog=textwrap.dedent(
            """\
            If you don't give the URL,
            interactive mode will be launched.
            (To quit interactive mode,
            type "end", "exit", "exit()",
            "break", "bye", ":q" or "finish".)"""
        ),
    )

    parser.add_argument(
        "url", metavar="url", nargs="*", type=str, help="Saving pages in order."
    )
    parser.add_argument(
        "-r",
        "--retry",
        type=check_natural,
        metavar="times",
        default=0,
        help="Set a retry limit on failed save.(>=0",
    )
    parser.add_argument(
        "-t", "--only_target", action="store_true", help="Save just target webpage(s)."
    )
    parser.add_argument(
        "-l",
        "--level",
        type=check_positive,
        metavar="level",
        default=1,
        help="Set maximum recursion depth. (>0)",
    )
    parser.add_argument(
        "-O",
        "--own",
        action="store_true",
        help="Only URLs with the same domain as target",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    if args_list:
        return parser.parse_args(args_list)
    else:
        return parser.parse_args()


def wbsv(
    urls: Iterable[str], own: bool, only_target: bool, level: int, retry: int
) -> None:
    past, now, fail = 0, 0, 0
    print(f"[+]Target: {urls}")
    c = Crawler.from_args(urls=urls, own=own, only_target=only_target, level=level)
    retrieved_links_empty_set: Set[str] = set()  # required for mypy type checking
    retrieved_links: Set[str] = retrieved_links_empty_set.union(*c.run_crawl())
    len_links: int = len(retrieved_links)
    len_len_links: int = len(str(len_links))
    print(f"[+]{len_links} URI(s) found.")
    a = Archiver(retry)
    for ind, link in enumerate(retrieved_links, 1):
        print(f"[{ind:0{len_len_links}d}/{len_links}]: Wait...", end="\r")
        archive = a.archive(link)
        if archive:
            archived_link, cached_flag = archive
            cache_or_now: str = "PAST" if cached_flag else "NOW"
            print(
                f"[{ind:0{len_len_links}d}/{len_links}]: <{cache_or_now}> {archived_link}"
            )
            inc = (1, 0) if cached_flag else (0, 1)
            past += inc[0]
            now += inc[1]
        else:
            print(f"[{ind:0{len_len_links}d}/{len_links}]: <FAIL> {link}")
            fail += 1

    print(f"[+]FIN!: {urls}")
    print(f"[+]ALL: {len_links}, NOW: {now}, PAST: {past}, FAIL: {fail}")


def wbsv_from_parser_args(args: argparse.Namespace) -> None:
    wbsv(args.url, args.own, args.only_target, args.level, args.retry)


def wbsv_repl(args: argparse.Namespace) -> None:
    finish_words = ("end", "exit", "exit()", "break", "bye", ":q", "finish")
    print("[[Input a target url (ex: https://google.com)]]")
    while True:
        link = input(">>> ").rstrip()
        if link in finish_words:
            print("[+]End.")
            break
        elif link != "":
            args.url = [link]
            try:
                wbsv_from_parser_args(args)
            except Exception as e:
                print(e, file=sys.stderr)


def _main() -> None:
    if not check_connectivity():
        raise HttpConnectionNotFountError
    args = parse_args()
    if len(sys.argv) <= 1:
        wbsv_repl(args)
    else:
        wbsv_from_parser_args(args)


def main() -> None:
    try:
        _main()
    except KeyboardInterrupt:
        exit(1)


if __name__ == "__main__":
    main()
