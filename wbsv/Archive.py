# Built-in Module
import re
import random
import sys
import time

from requests.exceptions import TooManyRedirects

# Third-parties' Module
from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError

# local Module
# from . import Version


def is_url(url):
    """Judge whether str is url or not."""
    return re.compile(r'^(http|https)://').match(url)


def is_end(url):
    """Judge whether str is the fin cmd to quit interactive mode."""
    return re.compile(r'^(end|exit|exit\(\)|break|bye|:q|finish)$').match(url)


def show_err():
    """Print error texts without stopping process in error."""
    for err in list(sys.exc_info()):
        err_msg = "[!]%s" % str(err).strip("<>")
        print(err_msg, file=sys.stderr)


def archive(uri_dic, pageurl, RETRY):
    """Save URIs extracted from the target page."""
    print("[+]Now: %s" % pageurl)
    print("[+]%d URI(s) found." % len(uri_dic))
    # try to throw each uri to API
    count, saves, fails = 0, 0, 0
    dic_size = len(uri_dic)

    for uri in uri_dic:
        count += 1

        id_ = str(count).zfill(len(str(len(uri_dic))))

        try:
            for j in range(1, RETRY+1):
                try:
                    print("[%s/%d]: Wait...    " % (id_, dic_size), end="\r")
                    archive_uri, exist_f = capture_or_cache(uri)
                    print("[%s/%d]:" % (id_, dic_size), end=" ")
                    print("<%s>" % "NOW" if exist_f else "PAST", archive_uri)
                    saves += 1
                    break

                except WaybackRuntimeError:
                    if j != RETRY:
                        print("[%s/%d]: Retrying..." %
                              (id_, dic_size), "COUNT:%d" % j, end="\r")
                    else:
                        print("[%s/%d]:" % (id_, dic_size), "<FAIL> %s" % uri)
                        fails += 1
                finally:
                    # wait retrying
                    time.sleep(random.uniform(1, 3))
        except KeyboardInterrupt:
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)
            break

        except TooManyRedirects:
            print("[!]API says: TooManyRedirects!", file=sys.stderr)
            print("[!]Need a 1 min break...", file=sys.stderr)
            for t in range(60):
                print("%d/60s" % t, end="\r", file=sys.stderr)
                time.sleep(1)

    # after for-loop
    print("[+]FIN!: %s" % pageurl)
    print("[+]ALL:", count, "SAVE:", saves, "FAIL:", fails)
