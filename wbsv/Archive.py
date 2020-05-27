import re
import sys
import time
import random

from requests.exceptions import ConnectionError, TooManyRedirects, HTTPError

from savepagenow import capture_or_cache
from savepagenow.api import WaybackRuntimeError


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


def wait_min():
    """Wait a minute."""
    for t in range(60):
        print("%d/60s" % t, end="\r", file=sys.stderr)
        time.sleep(1)


def retry_ntime(ret, func, c, uri):
    """Retry function given times."""
    for cnt in range(ret):
        if func:
            return True
        else:
            print("[%s/%d]: Retrying..." % (c[0], c[1]),
                  "COUNT:%d" % (cnt + 1), end="\r")
    print("[%s/%d]:" % (c[0], c[1]), "<FAIL> %s" % uri)
    return False


def add_res(func, t, f):
    """Increment t or f by func bool."""
    return [t+1, f] if func else [t, f+1]


def try_archive(id_, dic_size, uri):
    """Try to save a page on Wayback Machine."""
    try:
        print("[%s/%d]: Wait...    " % (id_, dic_size), end="\r")
        time.sleep(random.uniform(1, 3))
        archive_uri, exist_f = capture_or_cache(uri)
        print("[%s/%d]:" % (id_, dic_size), end=" ")
        print("<%s>" % "NOW" if exist_f else "PAST", archive_uri)
        return True

    except WaybackRuntimeError:
        return False


def archive(uri_dic, pageurl, RETRY):
    """Save URIs extracted from the target page."""
    print("[+]Now: %s" % pageurl)
    print("[+]%d URI(s) found." % len(uri_dic))
    # try to throw each uri to API
    count, saves, fails = 0, 0, 0
    for uri in uri_dic:
        count += 1
        # count uri_dic RETRY
        id_ = str(count).zfill(len(str(len(uri_dic))))

        try:
            saves, fails = add_res(
                retry_ntime(RETRY,
                            try_archive(id_, len(uri_dic), uri),
                            (id_, len(uri_dic)),
                            uri),
                saves, fails)

        except KeyboardInterrupt:
            print("[!]Interrupted!", file=sys.stderr)
            print("[!]Halt.", file=sys.stderr)
            break

        except (ConnectionError, TooManyRedirects, HTTPError) as e:
            print("[!]API says: " + str(type(e)), file=sys.stderr)
            print("[!]Need a 1 min break...", file=sys.stderr)
            wait_min()

    # after for-loop
    print("[+]FIN!: %s" % pageurl)
    print("[+]ALL:", count, "SAVE:", saves, "FAIL:", fails)
