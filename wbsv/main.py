#!/usr/bin/env python
import argparse
import http.client as httplib
import sys
import textwrap

from wbsv import __version__
from wbsv.archiver import Archiver
from wbsv.crawler import Clawler


class HttpConnectionNotFountError(Exception):
    pass


def check_connectivity(url="www.google.com", timeout=3):
    conn = httplib.HTTPConnection(url, timeout=timeout)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception as e:
        print(e, file=sys.stderr)
        return False


def check_natural(v):
    if int(v) < 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid natural number" % int(v))
    return int(v)


def check_positive(v):
    if int(v) <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid natural number" % int(v))
    return int(v)


def parse_args(test=None):
    """Parse arguments."""

    parser = argparse.ArgumentParser(
        prog='wbsv',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            CLI tool for save webpage on Wayback Machine forever.
            Save webpage and one 's all URI(s) on Wayback Machine.'''),
        epilog=textwrap.dedent('''\
            If you don't give the URL,
            interactive mode will be launched.
            (To quit interactive mode,
            type "end", "exit", "exit()",
            "break", "bye", ":q" or "finish".)'''))

    parser.add_argument('url', metavar='url', nargs='*', type=str,
                        help='Saving pages in order.')
    parser.add_argument('-r', '--retry', type=check_natural,
                        metavar='times', default=0,
                        help='Set a retry limit on failed save.(>=0')
    parser.add_argument('-t', '--only_target', action='store_true',
                        help='Save just target webpage(s).')
    parser.add_argument('-l', '--level', type=check_positive,
                        metavar='level', default=1,
                        help='Set maximum recursion depth. (>0)')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    if test:
        return parser.parse_args(test)
    else:
        return parser.parse_args()


def usual(args):
    past, now, fail = 0, 0, 0
    print('[+]Target: {}'.format(args.url))
    c = Clawler(args)
    retrieved_links = set().union(*c.run_crawl())
    len_links = len(retrieved_links)
    print('[+]{} URI(s) found.'.format(len_links))
    a = Archiver(args)
    for ind, link in enumerate(retrieved_links, 1):
        archive = a.archive(link)
        if archive:
            archived_link, cached_flag = archive
            inc = cache_or_now(ind, len_links, archived_link, cached_flag)
            past += inc[0]
            now += inc[1]
        else:
            print('[{:02d}/{}]: <FAIL> {}'.format(ind, len_links, link))
            fail += 1

    print('[+]FIN!: {}'.format(args.url))
    print('[+]ALL: {}, NOW: {}, PAST: {}, FAIL: {}'.format(
        len_links, now, past, fail))


def cache_or_now(ind, len_links, archived_link, cached_flag):
    if cached_flag:
        print('[{:02d}/{}]: <PAST> {}'.format(ind, len_links, archived_link))
        return (1, 0)
    else:
        print('[{:02d}/{}]: <NOW> {}'.format(ind, len_links, archived_link))
        return (0, 1)


def repl(args):
    finish_words = [
        'end', 'exit', 'exit()', 'break', 'bye', ':q', 'finish'
    ]
    print('[[Input a target url (ex: https://google.com)]]')
    while True:
        link = input('>>> ').rstrip()
        if link in finish_words:
            break
        else:
            args.url = [link]
            usual(args)


def main():
    if not check_connectivity():
        raise HttpConnectionNotFountError
    args = parse_args()
    if len(sys.argv) <= 1:
        repl(args)
    else:
        usual(args)


if __name__ == '__main__':
    main()
