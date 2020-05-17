import argparse
import sys
import textwrap

from . import Archive

__version__ = 'wbsv 0.2.0'


def parse_args():
    """Parse arguments."""
    def natural_num(n):
        if not n.isdecimal():
            print("[!]Err: num {} should be positive integer.".format(n),
                  file=sys.stderr)
            exit(1)
        elif int(n) < 1:
            print("[!]Err: num {} should be more than 0.".format(n),
                  file=sys.stderr)
            exit(1)
        return int(n)
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
    parser.add_argument('-v', '--version', action='version',
                        version=__version__,
                        help='Show version and exit')
    parser.add_argument('-r', '--retry', default=3,
                        type=natural_num, metavar='cnt',
                        help='Set a retry limit on failed save.')
    parser.add_argument('-t', '--only_target', action='store_true',
                        help='Save just target webpage(s).')
    parser.add_argument('-L', '--level', default=0,
                        type=natural_num, metavar='lv',
                        help='Set maximum recursion depth.')
    args = parser.parse_args()
    urls = [i for i in args.url if Archive.is_url(i)]
    if args.url != urls:
        print("[!]invalid url format", file=sys.stderr)
        exit(1)
    param = {
        "retry": args.retry,
        "urls": urls,
        "only-target": args.only_target,
        "errout": sys.stderr,
        "out": sys.stdout,
        "level": args.level}
    return param
