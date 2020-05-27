import argparse
import sys
import textwrap

from . import Archive

__version__ = 'wbsv 0.2.3'


def natural_num(n):
    """Judge whether numstr is positive or not."""
    if int(n) < 1:
        print("[!]Err: num {} should be more than 0.".format(n),
              file=sys.stderr)
        exit(1)
    return n


def parse_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog='wbsv',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            CLI tool for save webpage on Wayback Machine forever.
            Save webpage and one's all URI(s) on Wayback Machine.'''),
        epilog=textwrap.dedent('''\
            additional information:
                If you don't give the URL,
                interactive mode will be launched.
                (To quit interactive mode,
                 type "end", "exit", "exit()",
                 "break", "bye", ":q" or "finish".)'''))

    parser.add_argument('url',  metavar='url', nargs='*',
                        help='Saving pages in order.')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__,
                        help='Show version and exit')
    parser.add_argument('-r', '--retry', default=3,
                        metavar='cnt', type=int,
                        help='Set a retry limit on failed save.')
    parser.add_argument('-t', '--only_target', action='store_true',
                        help='Save just target webpage(s).')
    parser.add_argument('-L', '--level', default=1,
                        metavar='lv', type=int,
                        help='Set maximum recursion depth.')
    parser.add_argument('-d', '--dry_run', action='store_true', default=False,
                        help='Running without saving (dry-run mode)')
    args = parser.parse_args()
    urls = [i for i in args.url if Archive.is_url(i)]
    if args.url != urls:
        print("[!]invalid url format", file=sys.stderr)
        exit(1)

    param = {
        "retry": natural_num(args.retry),
        "urls": urls,
        "only-target": args.only_target,
        "dry-run": args.dry_run,
        "errout": sys.stderr,
        "out": sys.stdout,
        "level": natural_num(args.level)}
    return param
